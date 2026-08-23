# Independent adversarial audit report

Run: R-20260823T070000Z-b3-current-audit
Audited run root: `runs/plugin-perf-eval4/R-20260823T060000Z-b3-current`
Status label: `RIGOROUS_PARTIAL_RESULT` (audit)
Verdict: **REPAIRABLE_GAP** — 0 FATAL_GAP, 2 REPAIRABLE_GAP.

Scope: independent re-derivation of the four claimed statements, plus
verification of the honesty of the O2 reduction and the absence of
proof-by-numerics. No subagents were spawned. All algebraic/numerical checks
below were performed in this session.

---

## 1. Statement fidelity and notation

The run correctly targets the normalized B3 contract:

- `-y'' = lambda rho y` on `(0,1)`, Dirichlet `y(0)=y(1)=0`,
  `1 <= rho <= R` a.e.;
- `Lambda_n(rho) = lambda_{n+1}(rho)/lambda_n(rho)`, `n >= 1`, `R > 1`;
- O1 is the finite reduced family `[1,R,1,...,1]` with exactly `2n`
  positive-width blocks;
- O2 is the one-parameter equal-within-type family (all 1-blocks width `a`,
  all R-blocks width `b`, `r = a/b`).

The notation in Part B of `candidate_proof.md` is consistent:
`p = r x`, `q = s x`, `s = sqrt(R)`, `x = omega b`. The transfer matrices
are the natural normalized matrices acting on the vector `(u, u'/omega)`;
this normalization is legitimate and determinant-1. The only notation
weakness is that this coordinate convention is not stated explicitly in the
candidate, making the off-diagonal `1/s` and `s` look dimensionally unusual.
This is a presentation point, not a mathematical gap.

No silent change of `n`, `R`, boundary conditions, or density class was found.
O1 and O2 remain explicitly open, and no earlier STRICT result was downgraded.

---

## 2. Claim 1: general alternating Chebyshev secular representation

### 2.1 Independent derivation

With

```
A(p) = [[cos p,  sin p],
        [-sin p, cos p]],
B(q) = [[cos q,  sin q / s],
        [-s sin q, cos q]],
C = A(p) B(q),   M_n = C^n A(p),
```

and `m = tr(C)/2`, `delta = sin q / (s sin p)`, the Cayley-Hamilton step is
correct:

```
C^n = U_{n-1}(m) C - U_{n-2}(m) I,
(M_n)_{01} = (C^n)_{00} sin p + (C^n)_{01} cos p.
```

A direct computation gives

```
C_{00} sin p + C_{01} cos p
  = 2 m sin p + (sin q / s)
  = (2m + delta) sin p     (for sin p != 0).
```

Therefore

```
(M_n)_{01} = sin p [U_n(m) + delta U_{n-1}(m)].
```

This algebra is correct. I re-verified it symbolically with SymPy for
`n = 0..5` (the simplified difference is identically `0`) and numerically for
many `s`, `r`, `n`, `x`, including near and exactly at `sin p = 0` using the
continuous extension `sin(p) delta = sin(q)/s`. The maximum numerical error
was about `1.2e-12`, consistent with double precision.

### 2.2 REPAIRABLE_GAP G1: `sin p = 0` in the formula

As stated in `candidate_proof.md` Part C (Definitions and Proof), the formula

```
delta = sin(q) / (s sin(p))
```

is not defined when `sin p = 0`. The identity itself is still meaningful by
continuity, because the expression `sin(p) U_n(m) + sin(q)/s U_{n-1}(m)` is
well defined at those points and equals `(M_n)_{01}`. Symbolic/numeric checks
confirm this. But the STRICT statement "for every ... with `delta = ...`"
is literally false/incomplete at `p in pi Z` unless the reader is told that
`delta` is understood via continuity.

**Suggested repair:** add one sentence to Part C (and to the tool note if it is
not already there):

> If `sin p = 0`, read `delta` by continuity; equivalently, the identity
> should be written as
> `(M_n)_{01} = sin(p) U_n(m) + (sin(q)/s) U_{n-1}(m)`,
> which is well defined for all `p`.

The `tools/general-alternating-secular-chebyshev.md` already contains this
boundary caveat; the candidate proof does not. The mathematical content of
Lemma C1 is nevertheless sound.

---

## 3. Claim 2: amplitude-equality corollary from `E=0`

Re-derived. On a constant block with density `rho_0`, write

```
u_k = A_k sin(k_k x + phi_k),
k_n = sqrt(lambda_n rho_0),
k_{n+1} = sqrt(lambda_{n+1} rho_0) = k_n / c,
c = sqrt(lambda_n / lambda_{n+1}).
```

The ratio energy invariant

```
E = lambda_{n+1}(u_n'^2 + lambda_n rho_0 u_n^2)
  - lambda_n (u_{n+1}'^2 + lambda_{n+1} rho_0 u_{n+1}^2) = 0
```

becomes exactly

```
E = lambda_{n+1} k_n^2 (A_n^2 - A_{n+1}^2) = 0.
```

Since all factors are positive, `A_n = A_{n+1}`. The proof in Part E is a
little loose with the phrase "up to positive factors", but the algebra is
exact. This corollary follows from the baseline STRICT `E=0` result and is
itself STRICT. No gap found.

---

## 4. Claim 3: O2 elliptic-zone reduction

### 4.1 The reduction is honest

For a point with `|m(x)| < 1`, write `m = cos theta`, `theta in (0,pi)`.
The fixed-delta identity

```
U_n(m) + delta U_{n-1}(m) = 0
  <=>  sin((n+1)theta) + delta sin(n theta) = 0
```

is correct. In the actual equal-within-type family, `delta = delta(x)`, so
the secular roots in the elliptic zone satisfy an x-dependent equation. This
does **not** close O2, and the candidate explicitly says so. The exact gap is
correctly identified as the x-dependence of `delta`.

### 4.2 REPAIRABLE_GAP G2: internal "monotonicity" overclaim

The actual Lemma D1 (candidate Part D) proves only that, for fixed
`0 < delta < 1`, the `n` roots of `U_n(m) + delta U_{n-1}(m)` are real,
simple, and lie in `(-1,1)`. It does **not** prove monotonicity of the roots
in `delta`. However:

- `research_ledger.md` says: "Proved Chebyshev-root monotonicity in delta
  for `0<delta<1` (STRICT)."
- `approach_registry.md` labels route R3 "Chebyshev root monotonicity in
  delta", although the stated content is only the root-location lemma.

This is an overstatement of the run's strict output. The final report does
not repeat the monotonicity claim, so this is an internal consistency/wording
issue, not an attempted closure of O2.

**Suggested repair:** rename route R3 and the ledger sentence to "Chebyshev
root-location lemma for fixed delta" or, if monotonicity is intended, provide
a proof of it. The root-location lemma itself is correct and STRICT.

### 4.3 Minor presentation precision in Part D

The sentence "the roots `x` of the secular equation satisfy ..." should
include the caveat `sin(p) != 0` (or the continuity reading of `delta`), since
the bracket form is used after dividing by `sin p`. This is the same caveat
as G1 and is not an independent mathematical flaw.

---

## 5. Claim 4: O1/O2 open; no downgrade

Confirmed:

- Ratio extremizer structure (bang-bang `[1,R,1,...,1]`, exactly `2n`
  switches) is still marked STRICT (baseline).
- Balanced `2n`-root count / O3 is still marked STRICT (baseline).
- O1 and O2 are explicitly OPEN in `problem_contract.md`, `final_report.md`,
  `obligation_graph.md`, and `candidate_proof.md`.
- The final report does not claim closure of O1 or O2.

No previous STRICT result was downgraded.

---

## 6. Numerical evidence handling

The probe script and the "Numerical evidence (EVIDENCE, not proof)" section
are correctly labelled. No numerical computation is presented as a proof.
The candidate explicitly distinguishes STRICT proof from EVIDENCE. This
meets the project convention.

---

## 7. Error/gap summary

| # | Location | Severity | Description | Suggested repair |
|---|---|---|---|---|
| G1 | `runs/plugin-perf-eval4/R-20260823T060000Z-b3-current/candidate_proof.md`, Part C definitions/proof (`delta = sin(q)/(s sin(p))`) | REPAIRABLE | Formula is undefined at `sin p = 0`; identity holds by continuity but is not stated as such | Add the continuous form `sin(p) U_n(m) + (sin(q)/s) U_{n-1}(m)` or explicitly say `delta` is read continuously at `sin p = 0`; tool note already has this caveat |
| G2 | `runs/plugin-perf-eval4/R-20260823T060000Z-b3-current/research_ledger.md`, `approach_registry.md` R3 | REPAIRABLE | "Chebyshev-root monotonicity in delta" is claimed, but only the root-location lemma `0<delta<1 => n roots in (-1,1)` is proved | Rename to root-location lemma, or prove monotonicity if claimed |
| — | `candidate_proof.md` Part C | Presentation | Transfer-matrix normalization `(u,u'/omega)` is not stated | Add one sentence defining the coordinate vector |

FATAL_GAP count: **0**.
REPAIRABLE_GAP count: **2**.

---

## 8. Registration decision

The new mathematical content is sound:

- Lemma C1 (general alternating Chebyshev secular representation) may be
  registered as STRICT **after** the one-line continuous-extension repair at
  `sin p = 0`.
- Lemma D1 (fixed `delta` root-location in `(-1,1)` for `0<delta<1`) may be
  registered as STRICT, but only under the name "root-location lemma";
  the run's "monotonicity" wording must be corrected.
- The amplitude-equality corollary is STRICT with no repair needed.
- O1/O2 remain open; the O2 elliptic reduction is honest and does not claim
  closure.
