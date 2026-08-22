# Performance log

Run: R-20260823T000000Z-o1p-baseline
Variant: BASELINE (plugin/process as-is, no additional reuse protocol)
Duration: long single run, no artificial early stop
Cost tier reached: 2 (Tier 0/1 cheap probes, then Tier 2 proof writing)

## Tool/action log (abbreviated)

| # | Action | Tool class | Artifact/outcome |
| --- | --- | --- | --- |
| 1 | Read problem + required context | bash | Identified gap |
| 2 | Load skill + phase refs | bash | Process compliance |
| 3 | Construct banded-shift family route | reasoning | Route A |
| 4 | Write contract | write | problem_contract.md |
| 5 | Symbolic/numeric scripts | write + bash | banded_shift_verify.py, audit_banded_shift.py |
| 6 | Fix two script bugs | edit + bash | Correct odd recursion, numpy coeff order |
| 7 | Web search (3 queries) | web_search | degraded, no exact external source |
| 8 | Write candidate proof | write | candidate_proof.md |
| 9 | Write status/approaches/ledger/obligations/escalation | write | artifacts |
| 10 | Internal adversarial audit | reasoning | audit_report.md UNCERTAIN (non-independent) |
| 11 | Lean scaffold + formalization progress | write/bash | scaffold + register |
| 12 | Lean Tier-0 compile attempt | bash | timed out after 120s (Mathlib warm-up needed) |

## Counts / estimates

- Artifacts created in run root: >= 13 standard files plus reproducibility/2 scripts and lean-scaffold/1 file.
- External search calls: 1 tool call with 3 queries.
- Parallel subagents: 0 (explicitly prohibited).
- No git commit made; repo remains dirty with pre-existing changes.

## Observations

- The baseline process successfully found a new STRICT subclass extension without
  any mandatory reuse-gate protocol, because route construction came from
  reading the prior closed m=1 result and asking the natural "what is the
  bandwidth m version" question.
- The most useful prior work was `R-20260816T220000Z-densbc-o1p2`; the new
  theorem is largely a bandwidth generalization of its H_lambda machinery.
