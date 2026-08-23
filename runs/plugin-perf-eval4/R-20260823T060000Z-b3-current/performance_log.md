# Performance log

Run root: `F:\LaTeX\BVE research\runs\plugin-perf-eval4\R-20260823T060000Z-b3-current`

## Protocol

v1.5.0 lightweight reuse protocol:
- Compact pre-scan, no per-route REUSE/MISS tags.
- Minimum artifact set.
- No nested subagents.

## Phases

| Phase | Work | Outcome |
| --- | --- | --- |
| Pre-scan | Read baseline candidate/final reports, docs, research_map, tools, LEMMA_INDEX | ~1.6k lines context reused |
| Contract | problem_contract.md | written |
| Literature | Web/local quick search | no direct fixed-n theorem |
| Route | Chebyshev secular representation | STRICT new tool |
| Route | O2 elliptic phase | exact gap |
| Route | O1/O2 numerical evidence | EVIDENCE |
| Artifacts | 10+ files written | done |

## Rough cost indicators

- Tool calls (bash/web/write): approximately 35–45, mostly local reads and one
  web search.
- Background jobs: none long-running completed (one attempted scan timed out
  after 60s; not part of final artifacts).
- No nested subagents.

## Comparison to round-2 B3

- Round-2 baseline: two STRICT results (structure + root count), O1/O2 open.
- This run: one additional STRICT partial tool (general alternating Chebyshev
  secular representation) plus a STRICT corollary; O1/O2 still open.

## Reproducibility notes

- Environment: WSL, Python 3.14, numpy 2.5.2, mpmath 1.3.0, sympy 1.14.0,
  scipy 1.18.1.
- Scripts: `probe_general_alternating_chebyshev.py` in run root (EVIDENCE);
  exploratory `/tmp` scripts not committed.
