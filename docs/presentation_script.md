# Presentation and judging script (about 8–9 minutes)

## Slide 1 — Title and mission (0:00–0:35)
“JAN-SAHAYAK is our prototype for turning scattered public grievance reports into structured, reviewable incidents. It is designed for PS-04 and prioritizes traceability and human oversight.”

## Slide 2 — Problem (0:35–1:15)
“Complaints may be repeated across posts and comments, written in mixed languages, or missing precise locations. A manual operator can struggle to compare reports and see emerging patterns.”

## Slide 3 — Existing gap and scope (1:15–1:50)
“Our MVP demonstrates the core workflow with permitted or synthetic sample data. It does not claim to scrape social platforms live; integrations require authorized access.”

## Slide 4 — Architecture (1:50–2:35)
“Inputs enter through a form or CSV. We normalize text, categorize the issue, match only curated locations, generate possible duplicate candidates, calculate an explainable priority, and store everything in SQLite.”

## Slide 5 — Classification (2:35–3:15)
“Here is a Hindi/Hinglish example. The current baseline uses transparent keyword rules. This is intentionally modest and testable; a multilingual transformer is a future extension, not a claimed feature.”

## Slide 6 — Duplicate candidates (3:15–4:00)
“TF-IDF cosine similarity surfaces reports that may describe the same incident. It does not merge or label them as fake automatically. The operator checks location, time, and evidence.”

## Slide 7 — Priority and location (4:00–4:50)
“The priority score combines severity, engagement, cluster growth, criticality, and a small trust signal. The interface exposes its components. Unknown locations stay unverified instead of being guessed.”

## Slide 8 — Lifecycle demo (4:50–6:00)
“An operator can assign a report and move it from New to Assigned, In Progress, and Resolved. Each change is stored in the history table.”

## Slide 9 — Testing and results (6:00–7:00)
“We test category rules, score range, duplicate candidate behavior, persistence, and unknown locations. We will report metrics only from a labelled test set and state its size.”

## Slide 10 — Privacy and limitations (7:00–7:45)
“We use only permitted or synthetic data in the demo, preserve provenance, avoid exposing unnecessary personal information, and keep consequential decisions under human review.”

## Slide 11 — Impact and next steps (7:45–8:30)
“The prototype demonstrates a practical foundation. Next steps are authorized connectors, stronger regional-language models, validated ward mapping, and more rigorous evidence similarity checks.”

## Live demo sequence
1. Import `data/sample_complaints.csv`.
2. Open Incident Explorer and show predicted categories.
3. Submit two similar road complaints and show duplicate candidates.
4. Show priority component reasons and unknown-location behavior.
5. Assign a report, update its status, and show the history.
6. Return to Overview and explain the small-data limitation.

Replace this script's descriptions with what actually works in your final build. Never claim a feature or metric that you have not tested.
