# JAN-SAHAYAK — PS-04 MVP starter

An explainable, local Python/Streamlit prototype for public grievance intake, basic categorization, text-similarity duplicate candidates, priority scoring, curated locality matching, and status tracking.

## Important limitations
- This is a hackathon prototype, not an operational police system.
- Social platform connectors are **not** implemented. Use manual entries, CSVs, or data collected with permission.
- Classifier uses keyword rules, not IndicBERT.
- Duplicate detection identifies candidates using TF-IDF similarity; it does not prove reports describe the same incident.
- Location lookup only matches entries in `data/locations.csv`. Sample coordinates are illustrative and must be verified before presenting as authoritative.
- No automatic fake-news determination. Human review is required.
- Sample rows are synthetic.

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Test
```bash
pytest -q
```

## Import sample data
In the app, open **Submit Complaint → Import reports from CSV** and upload `data/sample_complaints.csv`.

## Suggested team ownership
- Member 1 / integrator: `app.py`, `README.md`, integration, demo.
- Member 2 / AI logic: `src/classifier.py`, `src/deduplication.py`, `src/priority.py`, related tests.
- Member 3 / data and dashboard: `src/database.py`, `src/location.py`, `src/analytics.py`, sample dataset, evaluation.

## Metrics to report
Measure results on a manually labelled holdout set. Do not invent accuracy or claim real-time integration without a working connector. Report classification macro-F1, duplicate precision/recall, verified-location match rate, and runtime along with sample sizes.
