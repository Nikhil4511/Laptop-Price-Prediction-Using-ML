"""
SHAP-based explainability helpers.

Falls back gracefully when shap is not installed
by computing a simple feature-importance proxy instead.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

try:
    import shap
    _SHAP_AVAILABLE = True
except ImportError:
    _SHAP_AVAILABLE = False


# ── Human-readable feature names ──────────────────────────────────────
FEAT_LABELS = {
    "Company":    "Brand",
    "TypeName":   "Laptop Type",
    "Ram":        "RAM",
    "Weight":     "Weight",
    "Touchscreen":"Touchscreen",
    "Ips":        "IPS Display",
    "ppi":        "Screen PPI (sharpness)",
    "Cpu brand":  "CPU Brand",
    "HDD":        "HDD Storage",
    "SSD":        "SSD Storage",
    "Gpu brand":  "GPU Brand",
    "os":         "Operating System",
}


def _friendly(name: str) -> str:
    return FEAT_LABELS.get(name, name)


def explain_prediction(pipe, query_df: pd.DataFrame, base_price_log: float) -> list[dict]:
    """
    Returns a list of dicts:
        [{"feature": "RAM", "value": 16, "shap": 0.18, "delta_inr": 14000}, ...]
    Sorted by |shap| descending.
    """
    results = []

    if _SHAP_AVAILABLE:
        try:
            # Most sklearn pipelines: transform → final estimator
            preprocessor = pipe[:-1]  # everything except final step
            model        = pipe[-1]

            X_transformed = preprocessor.transform(query_df)
            explainer     = shap.TreeExplainer(model)
            shap_vals     = explainer.shap_values(X_transformed)

            if hasattr(X_transformed, "toarray"):
                X_arr = X_transformed.toarray()
            else:
                X_arr = np.array(X_transformed)

            # Map transformed feature indices back to original names
            # (works for ColumnTransformer with get_feature_names_out)
            try:
                feat_names = preprocessor.get_feature_names_out()
            except Exception:
                feat_names = [f"feat_{i}" for i in range(X_arr.shape[1])]

            shap_array = shap_vals[0] if shap_vals.ndim > 1 else shap_vals

            # Group by original column (OneHot creates many sub-features)
            agg: dict[str, float] = {}
            for fname, sv in zip(feat_names, shap_array):
                # Strip transformer prefix like "onehotencoder__Company_Apple"
                parts = fname.split("__")
                raw   = parts[-1] if len(parts) > 1 else fname
                # Strip category suffix "Company_Apple" → "Company"
                col   = raw.split("_")[0] if "_" in raw else raw
                agg[col] = agg.get(col, 0.0) + float(sv)

            for col, sv in agg.items():
                raw_val = query_df[col].iloc[0] if col in query_df.columns else "—"
                delta   = int(np.exp(base_price_log + sv) - np.exp(base_price_log))
                results.append({
                    "feature":   _friendly(col),
                    "raw_value": raw_val,
                    "shap":      sv,
                    "delta_inr": delta,
                })

        except Exception:
            # Fall through to proxy
            results = _proxy_explain(pipe, query_df, base_price_log)
    else:
        results = _proxy_explain(pipe, query_df, base_price_log)

    results.sort(key=lambda x: abs(x["shap"]), reverse=True)
    return results[:8]  # top 8 most influential


def _proxy_explain(pipe, query_df: pd.DataFrame, base_price_log: float) -> list[dict]:
    """
    When SHAP is unavailable: perturb each feature by its mean and
    measure the change in prediction as a proxy importance.
    """
    results = []
    base_pred = pipe.predict(query_df)[0]

    for col in query_df.columns:
        perturbed = query_df.copy()
        orig_val  = query_df[col].iloc[0]

        # Nudge numeric; flip categorical
        if isinstance(orig_val, (int, float, np.integer, np.floating)):
            perturbed[col] = orig_val * 1.5
        else:
            perturbed[col] = orig_val  # can't perturb meaningfully without data dist

        try:
            new_pred = pipe.predict(perturbed)[0]
        except Exception:
            new_pred = base_pred

        sv    = float(new_pred - base_pred)
        delta = int(np.exp(base_pred + sv) - np.exp(base_pred))
        results.append({
            "feature":   _friendly(col),
            "raw_value": orig_val,
            "shap":      sv,
            "delta_inr": delta,
        })

    return results


def render_shap_html(explanations: list[dict]) -> str:
    """Returns HTML for the SHAP waterfall card."""
    max_abs = max(abs(e["shap"]) for e in explanations) or 1.0
    rows = ""
    for e in explanations:
        sv       = e["shap"]
        feat     = e["feature"]
        raw_val  = e["raw_value"]
        delta    = e["delta_inr"]
        bar_pct  = int(abs(sv) / max_abs * 220)          # px width, cap at 220
        positive = sv > 0

        direction = "▲ raises" if positive else "▼ lowers"
        bar_class = "shap-bar-pos" if positive else "shap-bar-neg"
        val_class = "shap-val-pos" if positive else "shap-val-neg"
        sign      = "+" if positive else ""
        delta_str = f"{sign}₹{abs(delta):,}" if delta else "—"

        rows += f"""
        <div class="shap-row">
            <div class="shap-feat"><strong>{feat}</strong>
                <span style="opacity:0.55;font-size:0.78rem;margin-left:4px">({raw_val})</span>
            </div>
            <div style="width:{bar_pct}px;flex-shrink:0">
                <div class="{bar_class}" style="width:{bar_pct}px"></div>
            </div>
            <div class="{val_class}">{delta_str}</div>
        </div>
        """

    return f"""
    <div class="glass-card">
        <div class="section-header">🧠 Why this price? — SHAP Explanation</div>
        <p style="color:var(--muted,#9090b0);font-size:0.85rem;margin-bottom:1rem">
            Each bar shows how much a spec <em>raised</em> or <em>lowered</em>
            the predicted price relative to an average laptop.
        </p>
        {rows}
    </div>
    """









# def explain_prediction(pipe, query_df: pd.DataFrame, base_price_log: float) -> list[dict]:
    
#     if not _SHAP_AVAILABLE:
#         return _proxy_explain(pipe, query_df, base_price_log)

#     try:
#         # Pipeline ke steps alag karo
#         preprocessor = pipe[:-1]
#         model        = pipe.steps[-1][1]

#         # Transform karo
#         X_transformed = preprocessor.transform(query_df)

#         # SHAP explainer banao
#         explainer = shap.TreeExplainer(model)
#         shap_vals = explainer.shap_values(X_transformed)

#         # ✅ Shape fix — har case handle karo
#         if isinstance(shap_vals, list):
#             shap_array = np.array(shap_vals[0]).flatten()
#         elif hasattr(shap_vals, 'ndim'):
#             if shap_vals.ndim == 3:
#                 shap_array = shap_vals[0][0]
#             elif shap_vals.ndim == 2:
#                 shap_array = shap_vals[0]
#             else:
#                 shap_array = shap_vals
#         else:
#             shap_array = np.array(shap_vals).flatten()

#         # Feature names lo
#         try:
#             feat_names = preprocessor.get_feature_names_out()
#         except Exception:
#             n = len(shap_array)
#             feat_names = [f"feat_{i}" for i in range(n)]

#         # ✅ Length match karo — zaroor
#         min_len = min(len(feat_names), len(shap_array))
#         feat_names = feat_names[:min_len]
#         shap_array = shap_array[:min_len]

#         # Group karo original columns mein
#         agg: dict[str, float] = {}
#         for fname, sv in zip(feat_names, shap_array):
#             parts = fname.split("__")
#             raw   = parts[-1] if len(parts) > 1 else fname
#             col   = raw.split("_")[0] if "_" in raw else raw
#             agg[col] = agg.get(col, 0.0) + float(sv)

#         results = []
#         for col, sv in agg.items():
#             raw_val = query_df[col].iloc[0] if col in query_df.columns else "—"
#             delta   = int(np.exp(base_price_log + sv) - np.exp(base_price_log))
#             results.append({
#                 "feature":   _friendly(col),
#                 "raw_value": raw_val,
#                 "shap":      sv,
#                 "delta_inr": delta,
#             })

#         results.sort(key=lambda x: abs(x["shap"]), reverse=True)
#         return results[:8]

#     except Exception as e:
#         # SHAP fail hua toh proxy use karo
#         return _proxy_explain(pipe, query_df, base_price_log)
