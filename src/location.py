import csv
import re
import unicodedata
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "locations.csv"

def _clean(value):
    value = unicodedata.normalize("NFKC", str(value or "")).lower()
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()

def resolve_location(location_text):
    """Match a curated alias; never infer a ward from incomplete text."""
    query = _clean(location_text)
    unknown = {
        "district": "", "latitude": None, "longitude": None,
        "confidence": "Location unverified"
    }
    if not query:
        return unknown
    try:
        with open(DATA, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                aliases = [row.get("locality", "")]
                aliases.extend(row.get("aliases", "").split(";"))
                cleaned_aliases = {_clean(alias) for alias in aliases if _clean(alias)}
                if query in cleaned_aliases:
                    try:
                        lat = float(row["latitude"]) if row.get("latitude") else None
                        lon = float(row["longitude"]) if row.get("longitude") else None
                    except (TypeError, ValueError):
                        return unknown
                    if lat is not None and not -90 <= lat <= 90:
                        return unknown
                    if lon is not None and not -180 <= lon <= 180:
                        return unknown
                    status = row.get("coordinate_status", "unverified").strip().lower()
                    confidence = "Verified source match" if status == "verified" else "Illustrative coordinate — verify before operational use"
                    return {"district": row.get("district", ""), "latitude": lat, "longitude": lon, "confidence": confidence}
    except (OSError, KeyError, csv.Error):
        return unknown
    return unknown
