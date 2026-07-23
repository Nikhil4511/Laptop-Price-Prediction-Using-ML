"""
Maps laptop brands to Unsplash-hosted representative images
and emoji fallbacks (used when network is unavailable).
"""

BRAND_EMOJI = {
    "Apple":   "🍎",
    "Dell":    "🖥️",
    "Lenovo":  "⬛",
    "HP":      "🖨️",
    "Asus":    "🔷",
    "Acer":    "🔴",
    "MSI":     "🟢",
    "Toshiba": "🔵",
    "Samsung": "📱",
    "Razer":   "🐍",
    "Huawei":  "📡",
    "Xiaomi":  "🟠",
    "LG":      "🔲",
    "Google":  "🌈",
    "Microsoft": "🪟",
}

# Free-to-use representative stock images (Unsplash, no auth needed)
BRAND_IMAGES = {
    "Apple":    "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&auto=format&fit=crop",
    "Dell":     "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&auto=format&fit=crop",
    "Lenovo":   "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&auto=format&fit=crop",
    "HP":       "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&auto=format&fit=crop",
    "Asus":     "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&auto=format&fit=crop",
    "Acer":     "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&auto=format&fit=crop",
    "MSI":      "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&auto=format&fit=crop",
    "Razer":    "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&auto=format&fit=crop",
}

TYPE_EMOJI = {
    "Notebook":   "💼",
    "Gaming":     "🎮",
    "Ultrabook":  "✨",
    "2 in 1 Convertible": "🔄",
    "Workstation": "🖥️",
    "Netbook":    "📟",
}


def get_brand_image_url(brand: str) -> str | None:
    return BRAND_IMAGES.get(brand)


def get_brand_emoji(brand: str) -> str:
    return BRAND_EMOJI.get(brand, "💻")


def get_type_emoji(type_name: str) -> str:
    return TYPE_EMOJI.get(type_name, "💻")
