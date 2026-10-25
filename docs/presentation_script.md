# Presentation script (about 8–9 minutes)

## 0:00–0:40 — Problem and mission
“JAN-SAHAYAK is a prototype that organizes scattered public grievance reports into structured, reviewable incident records.”

## 0:40–1:25 — Scope and architecture
“Data enters through manual entry or CSV. This demo does not claim live social-platform ingestion. The pipeline classifies issues, looks up curated locations, surfaces possible duplicates, estimates priority, and stores status history.”

## 1:25–2:30 — Classification and location
“The current classifier is a transparent keyword baseline, not a trained language model. If a location is not in the curated sample list, the system marks it unverified instead of guessing.”

## 2:30–3:45 — Duplicate candidates
“TF-IDF similarity surfaces text-similar reports for human review. It does not establish that two reports refer to the same incident or prove fake evidence.”

## 3:45–4:45 — Priority score
“The score combines severity, engagement, cluster growth, and criticality. It is an explainable prototype heuristic, not a validated operational risk model.”

## 4:45–6:00 — Resolution workflow
“An operator can assign a report, update its status, attach a note, and review the status history. An optional image can be stored with the report, but the application does not verify the image's authenticity.”

## 6:00–7:00 — Evaluation
“We tested core rules, candidate matching, score validation, location uncertainty, and status persistence. We will show only metrics measured on a labelled dataset.”

## 7:00–8:00 — Privacy and limitations
“The demo uses synthetic or permitted data, keeps uncertain outputs visible, and leaves important decisions to a human reviewer. Live APIs, advanced vision, speech-to-text, and production access controls remain future work unless implemented separately.”

## 8:00–8:45 — Impact and next steps
“Our next steps are validated local data, stronger multilingual evaluation, authorized integrations, and a more rigorous duplicate and evidence workflow.”

Replace any statement that does not match the final tested build. Never claim a feature or metric that has not been verified.
