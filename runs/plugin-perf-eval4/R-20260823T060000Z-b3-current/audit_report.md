# Audit report

## Verdict

**Not independently audited in this run.**

This document is an explicit audit note rather than an independent adversarial
audit. The new STRICT claims are:

1. General alternating Chebyshev secular representation (Lemma C1).
2. Fixed-delta Chebyshev roots in `(-1,1)` for `0<delta<1` (Lemma D1).
3. Amplitude equality corollary from `E=0`.

## Status of each new STRICT claim

| Claim | Internal status | Independent audit |
| --- | --- | --- |
| Lemma C1 | Symbolically/numerically checked; proof documented | NOT AUDITED |
| Lemma D1 | Proof documented; mathematically standard | NOT AUDITED |
| Amplitude corollary | Follows from baseline E=0; no independent audit | NOT AUDITED |

## Cross-checks performed (EVIDENCE only)

- Lemma C1 checked numerically for `s=2`, `r in {1,1.5,2,2.5,3}`, `n=0..5`,
  maximum discrepancy vs direct matrix power ~1e-14.
- Lemma D1 checked by `sympy.nroots` for `n=2..4`, `delta in {0.2,0.5,1.0,1.5,2.0}`;
  roots simple/real; for `delta<1` all in `(-1,1)` (in `m`), matching the proof.
- O2 maxima scanned numerically; EVIDENCE only.

## Known residual risks

- Lemma C1 uses `sin p` in the denominator of `delta`; at points where `sin p=0`
  the representation must be read by continuity. The roots of interest for the
  central pair have `sin p != 0`; this should be stated carefully in a final proof.
- The amplitude corollary assumes a constant-density block and a global
  maximizer; it does not say amplitudes are equal across different blocks.
