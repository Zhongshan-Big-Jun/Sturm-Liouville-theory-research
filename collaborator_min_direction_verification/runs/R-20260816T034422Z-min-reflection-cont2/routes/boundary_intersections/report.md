FINITE_COMPUTATIONAL_RESULT

# MIN-REFL-C2-F: exact intersection map for the R17 collar complement

## Result

This deterministic Arb run maps all twelve non-`t downarrow 0` boxes that
were missing from the old inner/single-face union. It is conditional on the
noncanonical R14/R17 common-angle reduction and is not a physical theorem.

Use the exact state intervals

```text
L=[0,1/64], I=[1/64,63/64], H=[63/64,1]
```

in `(k,t,y)`. The completed conditional boxes are

| box | result | visited | retained conclusion |
|---|---|---:|---|
| `LIL` | complete | 55 | all retained leaves have `G_1,...,G_4>0` |
| `HIL` | complete | 7 | retained set empty by the stable `g` discard |
| `LHI` | complete | 13 | all retained leaves have `G_1,...,G_4>0` |
| `IHH` | complete | 1,269 | retained set empty by `rB<=1` |

The other eight boxes did not complete at the preregistered finite limit:

| box | visited | singular | atomic unresolved | residual stack | classification |
|---|---:|---:|---:|---:|---|
| `LIH` | 500,000 | 0 | 64,028 | 55 | dependency failure |
| `HIH` | 500,000 | 0 | 90,272 | 31 | dependency failure |
| `LHL` | 500,000 | 0 | 41,600 | 51 | dependency failure |
| `IHL` | 500,000 | 0 | 44,007 | 55 | dependency failure |
| `HHL` | 500,000 | 0 | 49,964 | 47 | dependency failure |
| `HHI` | 500,000 | 0 | 66,960 | 27 | dependency failure |
| `LHH` | 500,000 | 0 | 62,492 | 45 | dependency failure |
| `HHH` | 2,000,000 | 0 | 0 | 27 | bounded subdivision exhausted |

The `HHH` box received the single allowed escalation because its first
500,000-box pass had no atomic unresolved leaf. The residual stack grew
from 13 to 27, so the escalation did not exhibit convergence. Further raw
subdivision is forbidden by the computation contract.

No incomplete box produced a rigorously negative retained box. Diagnostic
positive lower endpoints from some proved leaves do not cover their sibling
leaves and are not extrapolated.

## Exact first analytic frontiers

The interval failures group into two boundary mechanisms:

1. `y upward 1` combined with `k downarrow 0` or `k upward 1`, already for
   `t` in the inner interval (`LIH`, `HIH`);
2. `t upward 1` combined with boundary `k` or `y`, including the triple
   high corner (`LHL`, `IHL`, `HHL`, `HHI`, `LHH`, `HHH`).

These are assigned to analytic edge blow-up route `MIN-REFL-C2-E`.

## Arithmetic and replay

- exact dyadic endpoints with denominator `2^34`;
- Arb precision 128 bits through python-flint 0.9.0;
- frozen alternating-sinc enclosure and conditional sign contractor;
- zero singular evaluator calls in every run;
- no random input.

Replay commands and limits are frozen in `computation_contract.md` and
`intersection_driver.py`. Exact outputs are
`intersection_results_round1.json` through
`intersection_results_round4.json`.

## Scope audit

- The four completed boxes are finite conditional certificates only.
- The eight incomplete boxes are audited computation failures, not evidence
  of a negative coefficient.
- The new C2-C small-`t` result proves only existence of an unknown analytic
  collar and does not turn these exact dyadic boxes into a global cover.
- R14/R17 are not canonical trusted premises, so even a complete cube would
  require a self-contained physical reduction package and independent audit
  before propagation.

