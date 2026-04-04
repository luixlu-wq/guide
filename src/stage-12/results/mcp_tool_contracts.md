# MCP Tool Contracts

## tool: validate_geojson_projection
- input: `{geojson: object, expected_crs: string}`
- output: `{ok: bool, detected_crs: string, issues: list}`
- safety: reject if mandatory coordinates are missing

## tool: rank_poi_candidates
- input: `{poi_list: array, preference_profile: object}`
- output: `{ranked_poi: array, score_breakdown: object}`
- safety: redact sensitive admin identifiers before external calls