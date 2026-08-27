---
title: Lamplighter range-translation TV reduction
tags: [mathtool, self-developed, probability, coupling, coarea, strict]
source: Pilot v5 U2 Arms A and C
status: STRICT partial theorem and reductions; constant-order joint upper bound OPEN
created: 2026-08-26
---

# Lamplighter range-translation TV reduction

## Analytic statement

For the switch-walk-switch chain on `Z_2 wr Z`, conditional on a deterministic base path with
visited interval `[L,U]`, the terminal lamps on `[L,U]` are independent fair bits and lamps outside
are zero. Thus comparison of all-zero starts at base positions 0 and 2 contracts to comparison of
the corresponding `(L,U,Z)` range triples.

The audited partial theorem is

```text
1/(2 sqrt(t)) <= TV(P_t^x,P_t^y),                      t>=1,
TV(P_t^x,P_t^y) <= (2 log(t)+15)/sqrt(t),             t>=16.
```

The improved lower constant follows from endpoint projection and the exact parity-lattice
identity

```text
TV(Law_0(W_t),Law_2(W_t))
= max_k 2^(-t) binom(t,(t+k)/2)
>= 1/(2 sqrt(t)).
```

Arm C independently derived and audited the same endpoint identity. It also proved the valid,
but weaker for the open target, upper bound `(5+3 log(t))/sqrt(t)` for every `t>=1`.

The one-sided `(L,Z)` and `(U,Z)` translated marginal TVs are each at most `12/sqrt(t)` for
`t>=1`.

## Exact joint reduction

Let `h_t(R,K,A)` count zero-start simple-walk paths with range width `R`, endpoint height above the
minimum `K`, and origin height above the minimum `A`. Then

```text
2 TV(Q_t^0,Q_t^2)
= 2^(-t) sum_(R,K,A) |h_t(R,K,A)-h_t(R,K,A+2)|.
```

If `c_(R,K)(m)` is the number of parity-lattice connected components of the superlevel set
`{A:h_t(R,K,A)>=m}`, the exact discrete coarea formula is

```text
sum_A |h_t(R,K,A)-h_t(R,K,A+2)|
= 2 sum_(m>=1) c_(R,K)(m).
```

The same count also has an exact inclusion-exclusion representation by killed interval kernels and
a mixed-difference representation by periodized binomial coefficients. These forms preserve the
cancellation lost by termwise reflection bounds.

## Scope and status

- `STRICT`: conditional lamp kernel, endpoint lower bound, logarithmic upper bound, one-sided
  `12/sqrt(t)` bounds, killed-kernel identity, periodized-binomial decomposition, and coarea
  identity.
- `STRICT route obstruction`: reflection until meeting followed by synchronization has optimal
  conditional mismatch of order `log(t)/sqrt(t)`. This blocks only that coupling class.
- `EVIDENCE`: exact integer enumeration through finite `t` supports the constant-order aggregate
  variation and the path-specific mixed marginal comparison. It is not a proof.
- `OPEN`: prove a constant `C_0` with
  `sum|h_t(R,K,A)-h_t(R,K,A+2)| <= C_0 binom(t,floor(t/2))`, or construct a different
  exact-marginal full-state coupling with mismatch `C/sqrt(t)`.

## Applicability

Use this tool for translation sensitivity of one-dimensional random-walk range functionals and
lamplighter chains whose conditional decorations are uniform on the visited interval. Do not infer
the joint bound from marginal TVs without a path-specific proof. Do not assume fiberwise
unimodality; the exact fiber at `(t,R,K)=(6,4,2)` is `[1,0,1]`.

## Strict finite counterexample to the one-turn fiber claim

The stronger claim that every parity-restricted fiber
`A -> h_t(R,K,A)` has at most one change of monotonicity is false. For
`(t,R,K)=(48,8,4)` and `A=0,2,4,6,8`, exact integer path counting gives

```text
[1000894788882,1029170933020,1017584921004,1029170933020,1000894788882].
```

The consecutive difference signs are `[+,-,+,-]`. This is a strict finite counterexample:
the recurrence propagates exact integer counts on
`(position,visited_0,visited_8)` and exhausts every length-48 nearest-neighbor path. It is not a
floating-point scan. Consequently, a proof of the open aggregate variation bound cannot use a
universal one-turn coarea shortcut.

## Verification and artifacts

- Run package: `runs/three-arm-pilot-v2/pilot-v5-codex-u2/arms/a-plugin/`.
- Primary replay: `python3 reproducibility/audit_exact.py 100` from the arm directory.
- Fresh global audit: `subagents/global_audit.md`, `PASS` for the claimed partial theorem.
- One-turn counterexample replay:
  `arms/b-blank/reproducibility/audit_false_one_turn.py` in the pilot v5 run.
- Arm C independent audit:
  `runs/three-arm-pilot-v2/pilot-v5-codex-u2/arms/c-qed/external_anonymous_audit.md`.
- Candidate proof SHA256:
  `C76537D71604F3F5402D520423BCB045B8E203B4FC967C6FB8D1EBBF8ABF043B`.
