import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "locations.csv"

def resolve_location(location_text):
    """Resolve only exact curated aliases; do not guess unknown wards."""
    query = (location_text or "").strip().lower()
    if not query:
        return {"district": "", "latitude": None, "longitude": None, "confidence": "Location unverified"}
    try:
        with open(DATA, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                aliases = [a.strip().lower() for a in row.get("aliases", "").split(";") if a.strip()]
                aliases.append(row["locality"].strip().lower())
                if query in aliases:
                    return {
                        "district": row["district"],
                        "latitude": float(row["latitude"]) if row["latitude"] else None,
                        "longitude": float(row["longitude"]) if row["longitude"] else None,
                        "confidence": "Curated sample match — verify before use"
                    }
    except (FileNotFoundError, KeyError, ValueError):
        pass
    return {"district": "", "latitude": None, "longitude": None, "confidence": "Location unverified"}
