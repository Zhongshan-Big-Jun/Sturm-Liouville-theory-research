RIGOROUS_PARTIAL_RESULT

# Sequence-06 two-arm reconciliation

## Frozen returns

- W4 prover: `PARTIAL`, `prover_result.md`, SHA256
  `d55114570d516c69e446f2c228a76fb8827335e596df6c62e3d355a5232f9ffa`.
- W5 falsifier: `PARTIAL`, `falsifier_result.md`, SHA256
  `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9`.
- Worker restarts: 0.
- Duplicate dispatches: 0.
- Transcript replays: 0.

Both returns are candidate mathematics pending fresh independent audit. This
reconciliation records their decision deltas and does not upgrade them to
accepted strict results.

## W4 decision delta

W4 rewrites the exact mass equation as

```text
alpha A+beta B+theta H=0
```

with explicit layer coefficients and derives a candidate theorem that the
triple `(A,B,H)` is strictly mixed-sign. It also gives exact formulas for
`A`, `B`, and conditional bounds controlled by `Lalpha` and `H`. The proposed
next lemma is the sign-coherence implication `(SC)`: `G<0` would have to put
all three coefficients in one strict same-sign orthant. Proving `(SC)` would
contradict the mixed-sign balance and yield `G>=0`.

## W5 decision delta

W5 gives a candidate exact spectral-band-modal point with

```text
m=sqrt(5), c=4/5, alpha=theta=pi/4, beta=pi,
G<0, Xi<0.
```

Its exact mass residual is positive, so it is not a counterexample to the
complete problem. It rules out every route that tries to prove `G>=0` from
the spectral, band, and modal constraints alone, and it shows that `U>0` is
insufficient. W5 also proposes a restricted near-one sign theorem away from
left-switch collision. All these statements remain audit candidates.

## Combined closure decision

The two arms agree that the mass equation is load-bearing. The next earned
action is one fresh independent audit of both returns. No third solver is
authorized before that audit. The audit must check, in particular:

1. Every factor in W4 equations `(1)-(5)` and the strict mixed-sign argument.
2. Whether W4 `(SC)` is genuinely smaller than `G>=0` and is stated only as
   an open implication.
3. Exact admissibility and outward interval arithmetic for the W5 witness.
4. The W5 near-one uniformity argument, especially exclusion of endpoint
   drift and whether the cited Sturm continuity supplies all claimed limits.

`PHI-SIGN`, `G>=0`, `Xi>0`, and `KP-DET` remain open.

decision_delta: The mass-free route is eliminated and the mass constraint is localized to a candidate mixed-sign layer balance; fresh independent audit is required before any strict upgrade or new solver wave.
