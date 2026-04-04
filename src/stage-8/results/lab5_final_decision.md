# Lab 5 Final Decision

Qdrant status: Qdrant reachable on localhost:6333

## Method summary
- prompt_only: accuracy=0.625, f1_macro=0.5238
- rag_only: accuracy=0.25, f1_macro=0.1905
- tuned_only: accuracy=1.0, f1_macro=1.0
- hybrid: accuracy=0.625, f1_macro=0.5238

## Selected method: tuned_only
Reason: highest fixed-eval accuracy in this controlled run.