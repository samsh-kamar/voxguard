from src.classifier import classify_issue, suggest_department

def test_road_classification():
    assert classify_issue("Boring Road par bada gaddha hai") == "Road / Infrastructure"

def test_electricity_classification():
    assert classify_issue("Power cut since morning, bijli nahi") == "Electricity"

def test_unknown_classification():
    assert classify_issue("hello world") == "Other / Unclassified"

def test_department_mapping():
    assert "PWD" in suggest_department("Road / Infrastructure")
