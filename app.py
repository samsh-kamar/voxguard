import pandas as pd
import streamlit as st
from src.classifier import classify_issue, suggest_department
from src.deduplication import find_duplicate_candidates
from src.priority import calculate_priority
from src.database import init_db, save_report, get_reports, update_status, get_history
from src.analytics import spike_summary
from src.location import resolve_location

st.set_page_config(page_title="VoxGuard - Jan Sahayak", page_icon="🛡️", layout="wide")

# --- COLOURFUL THEME ---
st.markdown("""
<style>
    .stApp { background: #F8F9FF; }
    div[data-testid="stMetric"] { 
        background: white !important; border-radius: 16px; padding: 20px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.06); border-left: 6px solid #6C5CE7; 
    }
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] div { color: #2D3436 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #2D3436 !important; font-weight: 800 !important; }
    .stButton>button { background: linear-gradient(90deg, #6C5CE7 0%, #00CEC9 100%); color: white !important; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:white; padding:20px 25px; border-radius:16px; box-shadow:0 8px 20px rgba(0,0,0,0.06); border-left:6px solid #6C5CE7; margin-bottom:20px;'>
    <h1 style='margin:0; color:#2D3436;'>🛡️ VoxGuard - Jan Sahayak</h1>
    <p style='margin:5px 0 0 0; color:#636E72;'>nagrik ki awaz se sarkar tak • PS-04 • Bihar Police Cyber Hackathon</p>
</div>
""", unsafe_allow_html=True)

init_db()

st.warning("Prototype notice: use only permitted/public or clearly synthetic data. Predictions and alerts require human review.")

page = st.sidebar.radio("Navigate", ["Overview", "Submit Complaint", "Incident Explorer", "Resolution Tracker", "Evaluation"])
if page == "Overview":
    reports = get_reports()
    df = pd.DataFrame(reports)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reports", len(df))
    c2.metric("Open", int((df["status"] != "Resolved").sum()) if not df.empty else 0)
    c3.metric("High priority", int((df["priority_score"] >= 70).sum()) if not df.empty else 0)
    c4.metric("Categories", int(df["issue_type"].nunique()) if not df.empty else 0)
    st.subheader("Complaint volume")
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        daily = df.dropna(subset=["created_at"]).groupby(df["created_at"].dt.date).size().rename("Reports")
        st.line_chart(daily)
        st.subheader("Latest reports")
        st.dataframe(df.sort_values("created_at", ascending=False), use_container_width=True)
        st.info(spike_summary(df))
    else:
        st.info("No reports yet. Add a sample complaint or upload a CSV to begin.")
    st.caption("Map view uses only verified coordinates from data/locations.csv. Unknown locations remain unverified.")

elif page == "Submit Complaint":
    st.subheader("Create a report")
    with st.form("report_form"):
        text = st.text_area("Complaint text", placeholder="Example: Boring Road par paani jama hai...")
        source = st.selectbox("Source", ["Manual demo entry", "Facebook sample", "X sample", "Instagram sample", "YouTube sample", "CSV import"])
        language = st.selectbox("Language", ["Hindi/Hinglish", "English", "Bhojpuri", "Maithili", "Magahi", "Unknown"])
        location_text = st.text_input("Reported locality/district (optional)", placeholder="e.g., Boring Road, Patna")
        engagement = st.number_input("Engagement count (optional)", min_value=0, max_value=1000000, value=0)
        severity = st.slider("Initial severity estimate", 1, 5, 3)
        criticality = st.slider("Criticality estimate", 1, 5, 2)
        submitted = st.form_submit_button("Analyze and save")
    if submitted:
        if not text.strip():
            st.error("Please enter complaint text.")
        else:
            issue_type = classify_issue(text)
            department = suggest_department(issue_type)
            loc = resolve_location(location_text)
            score, reasons = calculate_priority(severity, engagement, 1, criticality, 3)
            row = {
                "source": source, "text": text.strip(), "language": language,
                "location_text": location_text.strip(), "district": loc["district"],
                "latitude": loc["latitude"], "longitude": loc["longitude"],
                "location_confidence": loc["confidence"], "issue_type": issue_type,
                "department": department, "priority_score": score,
                "priority_reasons": "; ".join(reasons), "status": "New",
                "data_type": "synthetic/demo unless source is verified"
            }
            report_id = save_report(row)
            st.success(f"Saved report #{report_id}.")
            st.write({"Issue category": issue_type, "Suggested department": department,
                      "Location status": loc["confidence"], "Priority score": score,
                      "Priority reasons": reasons})
            candidates = find_duplicate_candidates(text, get_reports(exclude_id=report_id))
            if candidates:
                st.subheader("Possible duplicate reports — human review required")
                st.dataframe(pd.DataFrame(candidates), use_container_width=True)
            else:
                st.info("No text-similar report found in the current database.")

    st.divider()
    st.subheader("Import reports from CSV")
    st.caption("Expected columns: text, source (optional), location (optional), language (optional).")
    uploaded = st.file_uploader("Choose CSV", type=["csv"])
    if uploaded is not None and st.button("Import CSV"):
        try:
            incoming = pd.read_csv(uploaded).fillna("")
            if "text" not in incoming.columns:
                st.error("CSV must contain a 'text' column.")
            else:
                count = 0
                for _, r in incoming.iterrows():
                    body = str(r.get("text", "")).strip()
                    if not body:
                        continue
                    loc_text = str(r.get("location", ""))
                    loc = resolve_location(loc_text)
                    issue = classify_issue(body)
                    score, reasons = calculate_priority(3, 0, 1, 2, 3)
                    save_report({
                        "source": str(r.get("source", "CSV import")),
                        "text": body, "language": str(r.get("language", "Unknown")),
                        "location_text": loc_text, "district": loc["district"],
                        "latitude": loc["latitude"], "longitude": loc["longitude"],
                        "location_confidence": loc["confidence"], "issue_type": issue,
                        "department": suggest_department(issue), "priority_score": score,
                        "priority_reasons": "; ".join(reasons), "status": "New",
                        "data_type": str(r.get("data_type", "unverified import"))
                    })
                    count += 1
                st.success(f"Imported {count} rows.")
                st.rerun()
        except Exception as e:
            st.error(f"Could not import CSV: {e}")

elif page == "Incident Explorer":
    reports = get_reports()
    df = pd.DataFrame(reports)
    if df.empty:
        st.info("No reports yet.")
    else:
        categories = ["All"] + sorted(df["issue_type"].dropna().unique().tolist())
        selected = st.selectbox("Filter by category", categories)
        if selected != "All":
            df = df[df["issue_type"] == selected]
        statuses = st.multiselect("Status", sorted(df["status"].dropna().unique()), default=sorted(df["status"].dropna().unique()))
        df = df[df["status"].isin(statuses)]
        st.dataframe(df.sort_values("priority_score", ascending=False), use_container_width=True)
        st.subheader("Potential duplicates")
        selected_id = st.number_input("Check report ID", min_value=1, step=1, value=int(df.iloc[0]["id"]) if not df.empty else 1)
        chosen = next((r for r in reports if int(r["id"]) == int(selected_id)), None)
        if chosen:
            candidates = find_duplicate_candidates(chosen["text"], [r for r in reports if int(r["id"]) != int(selected_id)])
            if candidates:
                st.dataframe(pd.DataFrame(candidates), use_container_width=True)
            else:
                st.write("No text-similar candidates found.")

        st.subheader("Map (known coordinates only)")
        mapped = df.dropna(subset=["latitude", "longitude"])
        if not mapped.empty:
            st.map(mapped.rename(columns={"latitude":"lat", "longitude":"lon"})[["lat","lon"]])
        else:
            st.caption("No reports have verified coordinates yet.")

elif page == "Resolution Tracker":
    reports = get_reports()
    if not reports:
        st.info("No reports to track yet.")
    else:
        options = {f'#{r["id"]} • {r["issue_type"]} • {r["text"][:55]}': int(r["id"]) for r in reports}
        label = st.selectbox("Choose report", list(options.keys()))
        report_id = options[label]
        current = next(r for r in reports if int(r["id"]) == report_id)
        st.write({k: current[k] for k in ["id","issue_type","department","location_text","priority_score","status","priority_reasons"]})
        new_status = st.selectbox("Update status", ["New", "Assigned", "In Progress", "Resolved"], index=["New","Assigned","In Progress","Resolved"].index(current["status"]))
        assigned_to = st.text_input("Assigned team/department", value=current["department"] or "")
        note = st.text_input("Update note", placeholder="e.g., forwarded to field team")
        if st.button("Save status update"):
            update_status(report_id, new_status, assigned_to, note)
            st.success("Status updated and history recorded.")
            st.rerun()
        st.subheader("Status history")
        history = get_history(report_id)
        st.dataframe(pd.DataFrame(history), use_container_width=True)

elif page == "Evaluation":
    st.subheader("Simple evaluation guidance")
    st.markdown("""
    - **Classification:** label a held-out sample manually and report accuracy / macro-F1.
    - **Duplicate detection:** label pairs as same incident / different incident; report precision and recall.
    - **Location:** evaluate only locations with verified ground truth; count unknowns separately.
    - **Runtime:** record median processing time over a documented test size.
    - Do not claim model accuracy without a labelled test set. Clearly label synthetic records.
    """)
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")
