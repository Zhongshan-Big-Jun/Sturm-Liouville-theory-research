# R13-03 / R13-04 author handoff

Status: AUTHOR_SLICE_COMPLETE, source frozen. Author selfchecks passed;
independent review and integrated all57 acceptance remain with the coordinator.

Only repository change: `misc/rigid1d.py` (61 additions, 34 deletions).
No commit, AGENTS, document, card, canonical, historical script, generator,
exporter, table or ledger edit was made by this author.

Frozen source SHA256:

```
3a34bdd9d839c542d004933fabbd15aca4908cef04cf54f076fe4a1b74f80be2
```

`rigid1d.frozen.py` preserves the exact edited bytes. `rigid1d.patch` is the
source-only diff against HEAD `4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`.
`HANDOFF.json` binds the artifacts and executed commands.

## Changes and mathematical envelope

- `_sc_u(w)` now encloses the entire offset range. For 0<=w<=1,
  cos(t)>=1-t^2/2>=1/2 implies increasing sin and decreasing cos on [0,w].
  Hence the ranges are [-sin(w),sin(w)] and [cos(w),1]. For w>1 use [-1,1].
- Point Taylor bounds use degrees 2N for sine and 2N-1 for cosine, including
  their final zero coefficients. Bounded derivatives give remainders
  |c|^(2N+1)/(2N+1)! and |c|^(2N)/(2N)! for every real center c.
  Addition identities and exact interval arithmetic then enclose the full
  input interval. Final intersection with [-1,1] is sound.
- Atan encloses its two endpoints and uses monotonicity. Oddness, the
  reciprocal identity for v>1, exact pi/4 at v=1, and the pi/4 reduction
  for 1/2<v<1 guarantee termination and useful accuracy near 1.
- I/D/D2 powers, nonnegative I sqrt, strictly positive D/D2 sqrt,
  atan-series arguments and term counts now use explicit exceptions.
  Machin's sanity guard also survives -O. Dual atan uses interval squaring
  so its denominator remains >=1 across zero.

Full finite-series, Machin, monotonicity, derivative and domain arguments:
`analytic_justification.md`. No increase in production series length,
random-sampling proof, or Lean certification is used.

## Completed selfchecks

Python 3.14.4; ordinary and optimized modes each completed 22 tests, exit 0.
The test assertions use unittest and remain active with -O.

| Mode | Test runtime | Raw log |
| --- | ---: | --- |
| normal | 23.698 s | `test_rigid1d.normal.log` |
| -O | 23.669 s | `test_rigid1d.optimized.log` |

Coverage includes exact rational false-positive witnesses, 34 translated
critical-point checks, 540 structured trig probes, atan crossing 0 and +/-1,
positive/negative centers, powers and sqrt guards, derivative identities,
and known-negative sign-helper cases. Finite probes accompany the proof.

Actual E1 parameter coverage: 11 primary gamma points plus 13/10, all 64
distinct cells of the loaded 12 derivative obligations, tau and both
derivatives, and selected exact `comps2` margins. Point widths passed
sin/cos < 10^-20 and tau < 10^-12; no thresholds were lowered.

Both logs bind `rigid1d.py` to the frozen hash above. They also record the
then-current generator hash
`db92fc5dbeaa0f2ec5f399320210d7d4246c08b7e146d86d8602ba1429bdb829`
and parameter-source hash
`65bab32c155fae9402b35a10d1c482c220cbf85648ae133e9a219cdd39c3a940`.
Only named definition AST and literal parameter data were loaded before
the coordinator's final freeze request; the full generator was never invoked.
No new generator read or execution was started after that request.

Original defects were separately reproduced in both modes from the saved
actual pre-edit source. See `reproduce_before.normal.log` and
`reproduce_before.optimized.log`. The two interrupted/failed harness attempts
are preserved with explanations in `attempt1-unbounded-reference` and
`attempt2-concurrent-e1-layout`; neither is counted as a passing run.

## Boundaries

Wide/large trigonometric arguments can yield only [-1,1]. Negative or
noninteger powers, a negative I sqrt input, a D/D2 sqrt value interval
touching zero, and zero-containing divisors are unsupported and rejected.
Arctan itself supports every finite real interval. Fraction semantics and
the original valid call signatures are preserved.

Unrelated subdivision-helper APIs were not redesigned; their existing valid
input and differentiability contracts are listed in the analytic note.
There is no claim to have run all57, independently reviewed the repair,
executed Lean, or certified the full theorem/certificate/export chain.
The coordinator can now run the real new generator against the frozen source.
