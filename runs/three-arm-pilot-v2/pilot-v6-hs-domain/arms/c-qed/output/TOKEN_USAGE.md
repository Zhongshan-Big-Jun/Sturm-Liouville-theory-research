# Token Usage

**Primary Model:** `claude-fable-5`  
**Started:** 2026-08-28 09:47:18  
**Last updated:** 2026-08-28 10:11:17  

## Summary

| Metric | Value |
|--------|-------|
| Total input tokens | 167,013 |
| Total output tokens | 61,896 |
| Total tokens | 228,909 |
| Total elapsed | 1438s |
| Agent calls | 7 |

## Per-Call Breakdown

| # | Agent | Input | Output | Time | Cumul In | Cumul Out |
|---|-------|------:|-------:|-----:|---------:|----------:|
| 1 | decomposer_create | 13,054 | 23,879 | 556.1s | 13,054 | 23,879 |
| 2 | single_prover_a1_r1_p1 | 19,673 | 26,883 | 561.7s | 32,727 | 50,762 |
| 3 | proof_verify_structural | 33,061 | 7,069 | 145.2s | 65,788 | 57,831 |
| 4 | verdict_structural | 12,813 | 6 | 17.1s | 78,601 | 57,837 |
| 5 | regulator_decide_a1_r1_p1 | 33,718 | 1,117 | 45.9s | 112,319 | 58,954 |
| 6 | regulator_final_a2_r1_p1 | 31,550 | 1,923 | 64.0s | 143,869 | 60,877 |
| 7 | Proof Effort Summary | 23,144 | 1,019 | 48.3s | 167,013 | 61,896 |
