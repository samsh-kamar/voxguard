from pathlib import Path
import uuid
import pandas as pd
import streamlit as st

from src.classifier import classify_issue, suggest_department
from src.deduplication import find_duplicate_candidates
from src.priority import calculate_priority
from src.database import init_db, save_report, get_reports, update_status, get_history
from src.analytics import spike_summary
from src.location import resolve_location

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_IMAGE_BYTES = 5 * 1024 * 1024

st.set_page_config(page_title="JAN-SAHAYAK", page_icon="🛡️", layout="wide")
init_db()
st.title("🛡️ JAN-SAHAYAK")
st.caption("AI-assisted public grievance intelligence • PS-04 • Bihar Police Cyber Hackathon 2026")
st.warning("Prototype only. Use permitted or synthetic data. Classifications, scores, locations, and alerts require human review.")

page = st.sidebar.radio("Navigate", ["Overview", "Submit Complaint", "Incident Explorer", "Resolution Tracker", "Evaluation"])

def show_candidates(text, reports):
    candidates = find_duplicate_candidates(text, reports)
    if candidates:
        st.subheader("Possible duplicate reports — review required")
        st.dataframe(pd.DataFrame(candidates), use_container_width=True)
    else:
        st.info("No text-similar candidate found at the current threshold. This does not prove the report is unique.")

def persist_upload(uploaded):
    if uploaded is None:
        return None
    raw = uploaded.getvalue()
    if len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("Image exceeds the 5 MB prototype limit.")
    suffix = Path(uploaded.name).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Unsupported image format.")
    filename = f"{uuid.uuid4().hex}{suffix}"
    target = UPLOAD_DIR / filename
    target.write_bytes(raw)
    return str(target.relative_to(ROOT))

if page == "Overview":
    reports = get_reports()
    df = pd.DataFrame(reports)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reports", len(df))
    c2.metric("Open", int((df["status"] != "Resolved").sum()) if not df.empty else 0)
    c3.metric("High priority (70+)", int((df["priority_score"] >= 70).sum()) if not df.empty else 0)
    c4.metric("Categories", int(df["issue_type"].nunique()) if not df.empty else 0)
    if not df.empty:
        st.subheader("Report volume by day")
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
        daily = df.dropna(subset=["created_at"]).groupby(df["created_at"].dt.date).size().rename("Reports")
        st.line_chart(daily)
        st.subheader("Latest reports")
        st.dataframe(df.sort_values("created_at", ascending=False), use_container_width=True)
        st.info(spike_summary(df))
    else:
        st.info("No reports yet. Submit a complaint or import the sample CSV.")
    st.caption("Any bundled coordinates are illustrative, not official or operationally verified.")

elif page == "Submit Complaint":
    st.subheader("Create a report")
    with st.form("report_form"):
        text = st.text_area("Complaint text", placeholder="Example: Boring Road par paani jama hai...")
        source = st.selectbox("Source / provenance", ["Manual demo entry", "Permitted public sample", "Synthetic sample", "CSV import"])
        language = st.selectbox("Language", ["Hindi/Hinglish", "English", "Bhojpuri", "Maithili", "Magahi", "Unknown"])
        location_text = st.text_input("Reported locality (optional)", placeholder="e.g., Boring Road")
        engagement = st.number_input("Engagement count (if known)", min_value=0, max_value=1000000, value=0)
        severity = st.slider("Initial severity estimate (human-entered)", 1, 5, 3)
        criticality = st.slider("Criticality estimate (human-entered)", 1, 5, 2)
        trust_score = st.slider("Evidence confidence (review estimate; not part of urgency score)", 1, 5, 3)
        image = st.file_uploader("Optional evidence image (PNG/JPG/WEBP, max 5 MB)", type=["png", "jpg", "jpeg", "webp"])
        submitted = st.form_submit_button("Analyze and save")
    if submitted:
        if not text.strip():
            st.error("Please enter complaint text.")
        else:
            try:
                image_path = persist_upload(image)
                issue_type = classify_issue(text)
                department = suggest_department(issue_type)
                loc = resolve_location(location_text)
                score, reasons = calculate_priority(severity, engagement, 1, criticality, trust_score)
                row = {
                    "source": source, "text": text.strip(), "language": language,
                    "location_text": location_text.strip(), "district": loc["district"],
                    "latitude": loc["latitude"], "longitude": loc["longitude"],
                    "location_confidence": loc["confidence"], "issue_type": issue_type,
                    "department": department, "priority_score": score,
                    "priority_reasons": "; ".join(reasons), "status": "New",
                    "data_type": "synthetic" if source == "Synthetic sample" else "review provenance",
                    "image_path": image_path
                }
                report_id = save_report(row)
                st.success(f"Saved report #{report_id}.")
                st.write({"Issue category": issue_type, "Suggested department": department,
                          "Location status": loc["confidence"], "Priority score": score,
                          "Priority reasons": reasons})
                show_candidates(text, get_reports(exclude_id=report_id))
                if image_path:
                    st.caption(f"Evidence file stored locally at `{image_path}`.")
            except (ValueError, OSError) as error:
                st.error(str(error))

    st.divider()
    st.subheader("Import reports from CSV")
    st.caption("Required column: text. Optional columns: source, location, language, data_type.")
    uploaded = st.file_uploader("Choose CSV", type=["csv"], key="csv_upload")
    if uploaded is not None and st.button("Import CSV"):
        try:
            incoming = pd.read_csv(uploaded).fillna("")
            if "text" not in incoming.columns:
                st.error("CSV must contain a 'text' column.")
            else:
                count = 0
                for _, record in incoming.iterrows():
                    body = str(record.get("text", "")).strip()
                    if not body:
                        continue
                    loc_text = str(record.get("location", ""))
                    loc = resolve_location(loc_text)
                    issue = classify_issue(body)
                    score, reasons = calculate_priority(3, 0, 1, 2)
                    save_report({
                        "source": str(record.get("source", "CSV import")) or "CSV import",
                        "text": body, "language": str(record.get("language", "Unknown")),
                        "location_text": loc_text, "district": loc["district"],
                        "latitude": loc["latitude"], "longitude": loc["longitude"],
                        "location_confidence": loc["confidence"], "issue_type": issue,
                        "department": suggest_department(issue), "priority_score": score,
                        "priority_reasons": "; ".join(reasons), "status": "New",
                        "data_type": str(record.get("data_type", "unverified import")) or "unverified import"
                    })
                    count += 1
                st.success(f"Imported {count} non-empty reports.")
                st.rerun()
        except Exception as error:
            st.error(f"CSV import failed: {error}")

elif page == "Incident Explorer":
    reports = get_reports()
    df = pd.DataFrame(reports)
    if df.empty:
        st.info("No reports yet.")
    else:
        categories = ["All"] + sorted(df["issue_type"].fillna("Needs review").unique().tolist())
        selected = st.selectbox("Filter by category", categories)
        if selected != "All":
            df = df[df["issue_type"] == selected]
        all_statuses = sorted(df["status"].dropna().unique().tolist())
        statuses = st.multiselect("Status", all_statuses, default=all_statuses)
        df = df[df["status"].isin(statuses)]
        if not df.empty:
            st.dataframe(df.sort_values("priority_score", ascending=False), use_container_width=True)
        else:
            st.info("No reports match these filters.")
        st.subheader("Potential duplicates")
        ids = [int(value.get("id")) for value in reports if value.get("id") is not None]
        if ids:
            selected_id = st.selectbox("Choose report ID", ids)
            chosen = next((report for report in reports if int(report["id"]) == int(selected_id)), None)
            if chosen:
                show_candidates(chosen["text"], [report for report in reports if int(report["id"]) != int(selected_id)])
        st.subheader("Map (illustrative coordinates only unless verified)")
        mapped = df.dropna(subset=["latitude", "longitude"])
        if not mapped.empty:
            st.map(mapped.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]])
            st.caption("Check each row's location_confidence before interpreting map points.")
        else:
            st.caption("No reports have coordinates.")

elif page == "Resolution Tracker":
    reports = get_reports()
    if not reports:
        st.info("No reports to track yet.")
    else:
        options = {f'#{r["id"]} • {r["issue_type"]} • {r["text"][:55]}': int(r["id"]) for r in reports}
        label = st.selectbox("Choose report", list(options.keys()))
        report_id = options[label]
        current = next(r for r in reports if int(r["id"]) == report_id)
        st.write({k: current[k] for k in ["id", "issue_type", "department", "location_text", "location_confidence", "priority_score", "status", "priority_reasons"]})
        if current.get("image_path"):
            file_path = ROOT / current["image_path"]
            if file_path.exists():
                st.image(str(file_path), caption="Uploaded evidence — not independently verified", width=400)
        statuses = ["New", "Assigned", "In Progress", "Resolved"]
        new_status = st.selectbox("Update status", statuses, index=statuses.index(current["status"]) if current["status"] in statuses else 0)
        assigned_to = st.text_input("Assigned team/department", value=current["department"] or "")
        note = st.text_input("Update note", placeholder="e.g., forwarded to field team")
        if st.button("Save status update"):
            try:
                if update_status(report_id, new_status, assigned_to, note):
                    st.success("Status updated and history recorded.")
                else:
                    st.error("Report not found.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))
        st.subheader("Status history")
        history = get_history(report_id)
        st.dataframe(pd.DataFrame(history), use_container_width=True)

elif page == "Evaluation":
    st.subheader("Evaluation checklist")
    st.markdown("""
    - **Classification:** evaluate on manually labelled, held-out examples; report macro-F1 and sample size.
    - **Duplicate candidates:** label report pairs as same incident / different incident; report precision and recall.
    - **Location:** test only against known ground truth; report unknowns separately.
    - **Runtime:** report median time and number of records tested.
    - **Limitations:** this app does not connect to social platforms live, and its keyword classifier is not a trained multilingual AI model.
    - **Privacy:** avoid unnecessary personal data; do not publish sensitive complainant details in the demo.
    """)
    st.code("pip install -r requirements.txt\nstreamlit run app.py\npytest -q", language="bash")
