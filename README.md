# JAN-SAHAYAK — Reviewed MVP starter

A local Streamlit prototype for structured complaint intake, transparent keyword categorization, TF-IDF duplicate candidates, heuristic urgency scoring, curated location lookup, a simple trend alert, optional image attachment, and status history.

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests:
```bash
pytest -q
```

Import `data/sample_complaints.csv` from the **Submit Complaint** page. All bundled rows and coordinates are synthetic/illustrative.

## Implemented in this prototype
- Manual report entry and CSV import.
- Keyword baseline for a few issue categories.
- Text similarity candidates using TF-IDF; human review required.
- Explainable urgency score from severity, engagement, cluster growth, and criticality.
- Curated locality alias matching; unknown locations stay unverified.
- Hourly complaint-volume review alert.
- SQLite report storage, status history, and optional image upload.

## Not implemented
- Live social-media APIs or scraping.
- IndicBERT or a trained multilingual classifier.
- Whisper transcription, OCR, YOLO/CLIP, image-derivative detection, or TrustGraph.
- Verified statewide ward geocoding, authentication, role-based access, or production deployment.

Do not claim those features in the presentation unless your team builds and tests them. Do not treat a similarity score as proof of duplicate identity, coordination, or fake evidence. Verify location and department suggestions before operational use.

## Team split suggestion
- Integrator: app.py, Git integration, demo.
- AI logic: classifier.py, deduplication.py, priority.py, tests.
- Data/workflow: database.py, location.py, analytics.py, sample data, evaluation.

## Evaluation
Use a labelled held-out set. Report classification macro-F1, duplicate precision/recall, location match/unknown rates, and runtime with dataset size and limitations. Do not invent metrics.
