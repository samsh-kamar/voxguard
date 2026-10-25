# JAN-SAHAYAK architecture and implementation boundary

1. **Input:** manual reports, CSV, permitted sample records, optional image uploads.
2. **Normalize:** trim text, retain source/language/time and mark data provenance.
3. **Analyze:** transparent keyword categorization and a suggested department; human confirmation required.
4. **Location:** exact curated alias lookup. Bundled coordinates are illustrative, not authoritative.
5. **Duplicate candidates:** TF-IDF text similarity surfaces candidates; it does not prove common incident identity. Location/time gates and visual hashes are future work.
6. **Prioritize:** 0–100 heuristic based on severity, engagement, cluster growth, and criticality. Evidence confidence is shown separately.
7. **Alert:** hourly-volume comparison creates a review signal, not proof of coordinated activity.
8. **Resolve:** report queue, available-coordinate map, status history, assignment, and resolution.
9. **Governance:** minimize personal data, use permitted sources, preserve provenance, and keep consequential decisions with a human operator.

## Future extensions (not part of this MVP)
- Authorized social-platform API ingestion.
- Speech-to-text, OCR, image embeddings, IndicBERT or another trained multilingual model.
- Verified ward-level geocoding.
- Image derivative checks / perceptual hashes.
- Graph analysis for coordination hypotheses.
- Authentication, role-based access, and production audit controls.
