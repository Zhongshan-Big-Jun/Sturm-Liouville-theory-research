# Token Usage

**Primary Model:** `claude-fable-5`  
**Started:** 2026-08-26 23:31:32  
**Last updated:** 2026-08-26 23:35:42  

## Summary

| Metric | Value |
|--------|-------|
| Total input tokens | 217,608 |
| Total output tokens | 4,395 |
| Total tokens | 222,003 |
| Total elapsed | 250s |
| Agent calls | 6 |

## Per-Call Breakdown

| # | Agent | Input | Output | Time | Cumul In | Cumul Out |
|---|-------|------:|-------:|-----:|---------:|----------:|
| 1 | decomposer_create | 61,367 | 1,345 | 58.5s | 61,367 | 1,345 |
| 2 | single_prover_a1_r1_p1 | 62,737 | 1,241 | 46.1s | 124,104 | 2,586 |
| 3 | proof_verify_structural | 74,258 | 1,401 | 59.4s | 198,362 | 3,987 |
| 4 | verdict_structural | 19,246 | 408 | 26.6s | 217,608 | 4,395 |
| 5 | regulator_decide_a1_r1_p1 | 0 | 0 | 43.8s | 217,608 | 4,395 |
| 6 | regulator_final_a2_r1_p1 | 0 | 0 | 15.4s | 217,608 | 4,395 |
