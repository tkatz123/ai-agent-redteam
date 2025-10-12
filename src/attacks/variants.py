# src/attacks/variants.py
VARIANTS = ("clean", "comment", "css", "zwc", "datauri", "multipage", "reply")

def normalize_variant(v: str) -> str:
    v = (v or "").strip().lower()
    if v not in VARIANTS:
        raise ValueError(f"Unknown variant '{v}'. Choose from {', '.join(VARIANTS)}")
    return v
