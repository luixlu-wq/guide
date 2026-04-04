# GIS Boundary Retrieval Failure Report

- Project context: `MapToGo`
- Failure scenario: user GPS point lies on subdivision boundary and wrong 5A spot is returned.
- Compared causes: coordinate projection mismatch (NAD83/WGS84) vs retrieval Top-K limit.
- Root cause verdict: projection mismatch dominates observed failure pattern.
- Resolution: normalize coordinate system before retrieval and keep Top-K unchanged.


## ICV Audit Trail

Identify:
- failure metric: retrieval_hit_rate
- threshold: < 0.80 on boundary cases
- failing case: ontario_boundary_001

Compare:
- option A: projection_fix_nad83_to_wgs84
- option B: increase_top_k_5_to_12

Verify:
- measured delta: boundary retrieval_hit: 0 -> 1 with projection fix
- decision: promote
