import re

RULES = {
    "Road / Infrastructure": ["pothole", "road", "sadak", "gaddha", "bridge", "pul", "blockage", "traffic", "jal jama", "waterlogging", "road damage"],
    "Electricity": ["electricity", "power cut", "bijli", "light nahi", "transformer", "power outage"],
    "Water Supply": ["water supply", "paani", "nal", "drinking water", "pipeline", "leakage"],
    "Sanitation": ["garbage", "kachra", "drain", "naali", "sewage", "toilet", "sanitation"],
    "Public Safety / Cyber Fraud": ["fraud", "scam", "cyber", "threat", "harassment", "theft", "robbery", "police"],
}

def normalize(text: str) -> str:
    text = (text or "").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text)).strip()

def classify_issue(text: str) -> str:
    normalized = normalize(text)
    scores = {category: sum(1 for term in terms if term in normalized) for category, terms in RULES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "Other / Unclassified"

def suggest_department(issue_type: str) -> str:
    return {
        "Road / Infrastructure": "PWD / Local Body (verify)",
        "Electricity": "SBPDCL / NBPDCL (verify by area)",
        "Water Supply": "Local Water Supply Department (verify)",
        "Sanitation": "Municipal / Local Body (verify)",
        "Public Safety / Cyber Fraud": "Police / Cyber Cell (human review)",
    }.get(issue_type, "Needs human routing")
