# Arm C invalid run 1 stage report

This launch is `INFRA_INVALID` and excluded from the three-arm score because the supposedly
offline child made 44 nested web calls during QED Stage 0.

| Metric | Value |
|---|---:|
| Observed telemetry span | 801 s |
| Model responses | 47 |
| Tool calls | 46 |
| Nested web calls | 44 |
| Input tokens | 5244795 |
| Cached input tokens | 4911872 |
| Uncached input tokens | 332923 |
| Output tokens | 12492 |
| Reasoning output tokens | 7837 |
| API-equivalent normalized estimate | USD 3.5462808 |
| Primary five-hour use | 48 to 68 percent |
| Secondary use | 47 to 50 percent |
| Proof artifact | none |

The process was manually interrupted upon detection. The exact wrapper wall time is unknown
because QED stdout was buffered and Ctrl-C ended the wrapper before it wrote a completion record.
The first and last scored token records are 801 seconds apart.

See `PROTOCOL_VIOLATION.md` for root cause, hashes, and the replacement condition.
