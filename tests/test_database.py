import src.database as db

def test_report_status_history_persists(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()
    report_id = db.save_report({
        "text": "Synthetic pothole report", "status": "New",
        "issue_type": "Road / Infrastructure", "department": "PWD",
        "priority_score": 50, "priority_reasons": "test", "data_type": "synthetic"
    })
    assert db.update_status(report_id, "Assigned", "PWD", "assigned for review")
    assert db.get_reports()[0]["status"] == "Assigned"
    history = db.get_history(report_id)
    assert len(history) == 2
    assert history[-1]["new_status"] == "Assigned"

def test_invalid_status_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()
    report_id = db.save_report({"text": "sample", "status": "New"})
    try:
        db.update_status(report_id, "Closed forever", "", "")
        assert False, "Expected ValueError"
    except ValueError:
        pass
