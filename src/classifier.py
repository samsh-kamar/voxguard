import re
import unicodedata

RULES = {
    "Road / Infrastructure": [
        "pothole", "road damage", "broken road", "sadak", "gaddha", "bridge", "pul",
        "road blockage", "traffic jam", "broken bridge"
    ],
    "Flooding / Drainage": [
        "waterlogging", "water logging", "jal jama", "water on road", "flooding",
        "drain overflow", "naali overflow", "sewer overflow", "blocked drain", "drain blockage"
    ],
    "Electricity": ["electricity", "power cut", "bijli", "light nahi", "transformer", "power outage"],
    "Water Supply": ["water supply", "drinking water", "paani supply", "paani nahi", "nal ka paani", "pipeline leakage"],
    "Sanitation": ["garbage", "kachra", "naali safai", "sewage", "toilet", "sanitation", "waste collection"],
    "Public Safety / Cyber Fraud": ["fraud", "scam", "cyber crime", "cyber fraud", "threat", "harassment", "theft", "robbery"],
}

def normalize(text: str) -> str:
    """Normalize punctuation/spacing while preserving Unicode letters."""
    text = unicodedata.normalize("NFKC", str(text or "")).lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()

def _contains_phrase(normalized_text: str, phrase: str) -> bool:
    padded_text = f" {normalized_text} "
    padded_phrase = f" {normalize(phrase)} "
    return padded_phrase in padded_text

def classify_issue(text: str) -> str:
    """Transparent keyword baseline; ambiguous ties are routed for human review."""
    normalized = normalize(text)
    if not normalized:
        return "Other / Unclassified"
    scores = {
        category: sum(1 for phrase in phrases if _contains_phrase(normalized, phrase))
        for category, phrases in RULES.items()
    }
    max_score = max(scores.values(), default=0)
    if max_score == 0:
        return "Other / Unclassified"
    winners = [category for category, score in scores.items() if score == max_score]
    if len(winners) > 1:
        return "Needs Human Review"
    return winners[0]

def suggest_department(issue_type: str) -> str:
    """A suggestion only; confirm jurisdiction and routing with an authorized operator."""
    return {
        "Road / Infrastructure": "PWD / Local Body (verify jurisdiction)",
        "Flooding / Drainage": "Municipal / Local Body (verify jurisdiction)",
        "Electricity": "SBPDCL / NBPDCL (verify by service area)",
        "Water Supply": "Local Water Supply Department (verify)",
        "Sanitation": "Municipal / Local Body (verify jurisdiction)",
        "Public Safety / Cyber Fraud": "Police / Cyber Cell (human review)",
    }.get(issue_type, "Needs human routing")
