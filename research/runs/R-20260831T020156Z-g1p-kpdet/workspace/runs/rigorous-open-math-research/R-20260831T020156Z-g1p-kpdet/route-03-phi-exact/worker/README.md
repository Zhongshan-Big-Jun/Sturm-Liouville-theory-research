EVIDENCE

# Numerical discovery probe

`numeric_probe.py` is a floating-point continuation and falsification aid. It
is not part of the proof of any statement in `worker_result.md`.

Replay command:

```text
py -3.10 route-03-phi-exact/worker/numeric_probe.py
```

The 2026-08-31 replay followed the branch from `m=1.0001` through
`m=96.931034` and observed positive `Xi` and positive `G` at the printed
sample points. Newton continuation failed at `m=100`; no conclusion is drawn
from that failure. These finite floating-point observations are `EVIDENCE`
only and do not establish `G>=0`, `Xi>0`, `Phi<0`, or KP-DET.
