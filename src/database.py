import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parents[1] / "jan_sahayak.db"

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, text TEXT NOT NULL, language TEXT, location_text TEXT,
            district TEXT, latitude REAL, longitude REAL, location_confidence TEXT,
            issue_type TEXT, department TEXT, priority_score INTEGER,
            priority_reasons TEXT, status TEXT DEFAULT 'New', data_type TEXT,
            created_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL, old_status TEXT, new_status TEXT,
            assigned_to TEXT, note TEXT, changed_at TEXT NOT NULL
        )""")

def save_report(row):
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    keys = ["source","text","language","location_text","district","latitude","longitude",
            "location_confidence","issue_type","department","priority_score","priority_reasons","status","data_type"]
    values = [row.get(k) for k in keys]
    with connect() as con:
        cur = con.execute(
            f"INSERT INTO reports ({','.join(keys)},created_at) VALUES ({','.join(['?']*(len(keys)+1))})",
            values + [created]
        )
        report_id = cur.lastrowid
        con.execute("INSERT INTO status_history (report_id, old_status, new_status, assigned_to, note, changed_at) VALUES (?,?,?,?,?,?)",
                    (report_id, None, row.get("status","New"), row.get("department",""), "Report created", created))
    return report_id

def get_reports(exclude_id=None):
    with connect() as con:
        if exclude_id is None:
            rows = con.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
        else:
            rows = con.execute("SELECT * FROM reports WHERE id != ? ORDER BY id DESC", (exclude_id,)).fetchall()
        return [dict(r) for r in rows]

def update_status(report_id, new_status, assigned_to, note):
    changed = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as con:
        row = con.execute("SELECT status FROM reports WHERE id=?", (report_id,)).fetchone()
        if row is None:
            return False
        old = row["status"]
        con.execute("UPDATE reports SET status=?, department=? WHERE id=?", (new_status, assigned_to, report_id))
        con.execute("INSERT INTO status_history (report_id,old_status,new_status,assigned_to,note,changed_at) VALUES (?,?,?,?,?,?)",
                    (report_id, old, new_status, assigned_to, note, changed))
    return True

def get_history(report_id):
    with connect() as con:
        rows = con.execute("SELECT old_status,new_status,assigned_to,note,changed_at FROM status_history WHERE report_id=? ORDER BY id", (report_id,)).fetchall()
        return [dict(r) for r in rows]
