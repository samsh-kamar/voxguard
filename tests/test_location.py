from src.location import resolve_location

def test_known_alias_matches_as_illustrative():
    result = resolve_location("Boring Road")
    assert result["district"] == "Patna"
    assert result["latitude"] is not None
    assert "Illustrative" in result["confidence"]

def test_unknown_location_is_not_guessed():
    result = resolve_location("unknown street")
    assert result["confidence"] == "Location unverified"
    assert result["latitude"] is None
