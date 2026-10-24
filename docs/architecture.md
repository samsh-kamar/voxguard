# JAN-SAHAYAK architecture and scope

1. **Input:** CSV/manual reports, permitted sample posts, optional uploaded media metadata.
2. **Normalize:** clean text, retain source and timestamp, mark data provenance.
3. **Analyze:** keyword-based issue category, suggested department, curated locality match.
4. **Cluster:** TF-IDF cosine similarity suggests duplicate candidates; later add timestamp/location gates and image hashes.
5. **Prioritize:** transparent 0–100 heuristic; show component reasons.
6. **Alert:** compare hourly report counts with a baseline; alert is a review signal only.
7. **Resolve:** queue, map for curated coordinates, status history, human assignment and resolution.
8. **Govern:** data minimization, permitted collection, access control, audit trail, no unsupported claims.

## Future extensions (not in current MVP)
- Authorized social-platform API ingestion.
- Speech-to-text, OCR, image embeddings, IndicBERT or other multilingual model.
- Ward-level geocoding based on a verified source.
- Image derivative checks / perceptual hashes.
- Graph analysis for coordination hypotheses.
