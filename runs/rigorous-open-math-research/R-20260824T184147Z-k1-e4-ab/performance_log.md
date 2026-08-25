# Performance Log - K(1) strict anchor benchmark

Both arms used `gpt-5.6-sol`, `xhigh`, and `priority`, with a 7200 second cap.
The runs started within approximately five seconds of one another.

| Metric | Blueprint v2.3 | Bare Codex |
|---|---:|---:|
| Wall time | 905.708 s | 486.004 s |
| Solver sessions | 7 | 1 |
| Input tokens | 7,037,733 | 415,186 |
| Cached input tokens | 6,621,696 | 350,464 |
| Uncached input tokens | 416,037 | 64,722 |
| Output tokens | 108,062 | 26,899 |
| Total input plus output | 7,145,795 | 442,085 |

Blueprint/Bare ratios: wall time `1.8636`, total tokens `16.1638`.
Reasoning output is included in output tokens and is not added again.

Excluded from solver accounting: public problem scouting, aborted runs before
the cap was changed from 45 minutes to two hours, environment diagnostics, and
the post-run blinded review.
