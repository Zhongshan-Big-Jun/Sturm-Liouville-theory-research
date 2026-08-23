# Independent re-audit report (R-20260823T080000Z-b3-current-reaudit)

Audited run root: `runs/plugin-perf-eval4/R-20260823T060000Z-b3-current`
Previous audit: `R-20260823T070000Z-b3-current-audit` — REPAIRABLE_GAP (G1, G2)
Verdict: **PASS** — 0 FATAL_GAP, 0 REPAIRABLE_GAP.
Status label of audited run: `RIGOROUS_PARTIAL_RESULT` (unchanged, appropriate).

Scope: independent re-derivation and adversarially directed re-check of the
repaired STRICT claims. No subagents were spawned. All checks below were
performed directly in this session.

---

## 1. Repair verification

### G1: continuity at `sin p = 0`

Previously the candidate proof defined
`delta = sin(q)/(s sin(p))` without stating the boundary behaviour. This has
been repaired in `candidate_proof.md` Part C:

- Definitions now say `delta = sin q / (s sin p)` **read by continuity when
  `sin p = 0`; equivalently `sin(p) delta = sin q / s`**.
- The lemma statement gives the continuous form first:
  `(M_n)_{0,1} = sin(p) U_n(m) + (sin q / s) U_{n-1}(m)`.
- The proof uses the same continuous identity
  `C_{0,0} sin p + C_{0,1} cos p = 2m sin p + (sin q / s)`.

I independently re-derived the matrix algebra with SymPy for `n = 0..5`
(`(M_n)_01 - [sin p U_n + (sin q/s)U_{n-1}]` simplified to identically `0`) and
numerically for `n = 0..7`, including values exactly at and near `sin p = 0`.
The continuous secular representation is correct at the excluded points.

### G2: "Chebyshev-root monotonicity" overclaim

Previously `research_ledger.md` and `approach_registry.md` labelled the result
"Chebyshev-root monotonicity in delta". This has been repaired:

- `research_ledger.md` now says:
  "Proved fixed-delta Chebyshev root-location lemma for `0<delta<1`
  (STRICT; no monotonicity claimed)."
- `approach_registry.md` route R3 is now headed "fixed-delta Chebyshev
  root-location in `delta`" and its exact gap does not claim monotonicity.
- Remaining occurrences of "monotonicity" are either explicit OPEN gaps
  (root-ratio monotonicity in `r`) or descriptions of what would be needed for
  O2; none is presented as a proved STRICT theorem.

The root-location lemma itself is correct.

---

## 2. Independent verification of the STRICT claims

### 2.1 Lemma C1 — general alternating Chebyshev secular representation (STRICT)

With

```
A(p) = [[cos p,  sin p],
        [-sin p, cos p]],
B(q) = [[cos q,  sin q / s],
        [-s sin q, cos q]],
C(p,q) = A(p) B(q),
M_n(p,q) = C(p,q)^n A(p),
m = tr(C)/2,
delta = sin q / (s sin p)    (by continuity when sin p = 0),
```

the claim

```
(M_n)_{0,1} = sin(p) U_n(m) + (sin q / s) U_{n-1}(m)
            = sin(p) [ U_n(m) + delta U_{n-1}(m) ]
```

is correct for every `n >= 0`.

The proof chain is sound:

1. `det C = 1`, so Cayley-Hamilton gives
   `C^n = U_{n-1}(m) C - U_{n-2}(m) I`.
2. `(M_n)_{0,1} = (C^n)_{0,0} sin p + (C^n)_{0,1} cos p`.
3. Direct computation gives
   `C_{0,0} sin p + C_{0,1} cos p = 2m sin p + (sin q / s)`,
   which remains valid at `sin p = 0` in the continuous sense.
4. The Chebyshev recurrence completes the identity.

I also verified the product order: `M_n = (A B)^n A ` is exactly the transfer
matrix of `[1,R,1,...,1]` with `n` R-blocks and `n+1` 1-blocks.

No over-statement remains in the formal statement of Lemma C1.

### 2.2 Lemma D1 — fixed-delta Chebyshev root-location lemma (STRICT)

For fixed `0 < delta < 1`, the polynomial
`U_n(m) + delta U_{n-1}(m)` is the characteristic polynomial (in
`z = 2m`) of the real symmetric tridiagonal matrix with off-diagonal `1`
and bottom-right `-delta`:

```
T_n = [[ 0  1        ...  ],
       [ 1  0  1     ...  ],
       [ ...          1   ],
       [ ...        -delta ]]
```

Hence it has `n` real roots. The hyperbolic/endpoint argument in the candidate
is correct:

- for `z > 2`, `p_n(z)+delta p_{n-1}(z) > 0`;
- for `z < -2`, the expression equals
  `(-1)^n [sinh((n+1)theta) - delta sinh(n theta)]/sinh(theta)`,
  which is nonzero for `delta < 1`;
- at `z = +/-2` the expression is nonzero.

Therefore all roots lie in `(-2,2)` in `z`, i.e. `(-1,1)` in `m`. I also checked
`n = 1..6`, `delta = 1/3` with `sympy.nroots`: every polynomial has exactly `n`
real roots inside `(-2,2)` and matches the tridiagonal characteristic
polynomial. The approach-registry phrase "simple" is true by the standard
irreducible symmetric tridiagonal argument; this is not an overclaim.

The lemma is correctly called a **root-location** lemma, not a monotonicity
statement.

### 2.3 Part E — amplitude equality corollary from `E = 0` (STRICT)

Re-derived independently. On a constant block with density `rho_0`, each
eigenfunction has the form `u_k = A_k sin(k_k x + phi_k)`, with
`k_k^2 = lambda_k rho_0`. The block energy is

```
u_k'^2 + lambda_k rho_0 u_k^2 = A_k^2 k_k^2.
```

The baseline ratio energy invariant for a global maximizer gives

```
E = lambda_{n+1}(u_n'^2 + lambda_n rho_0 u_n^2)
  - lambda_n (u_{n+1}'^2 + lambda_{n+1} rho_0 u_{n+1}^2) = 0.
```

Using `k_{n+1} = k_n / c`, `c = sqrt(lambda_n / lambda_{n+1})`, this becomes

```
E = lambda_{n+1} k_n^2 (A_n^2 - A_{n+1}^2) = 0,
```

with all prefactors positive, so `A_n = A_{n+1}`. The candidate's phrase
"up to positive factors" hides no sign or normalisation error; the exact
computation is as above. This corollary is STRICT.

### 2.4 O1/O2 remain open; no numerical evidence as proof

Confirmed across `candidate_proof.md`, `problem_contract.md`,
`final_report.md`, `obligation_graph.md`, `status_and_literature.md`, and
`approach_registry.md`:

- O1 and O2 are explicitly marked OPEN.
- No theorem statement claims closure of O1 or O2.
- The O2 numerical scans are in an "EVIDENCE, not proof" section.
- The width-simplex optimization is explicitly EVIDENCE.
- The Lemma C1 numerical verification is presented as confirmation of algebra,
  not as a proof; the proof is algebraic.
- The balanced `2n`-root count and ratio extremizer structure remain baseline
  STRICT results and are not mis-stated as new.

---

## 3. Non-blocking documentation notes (not gaps)

These do not affect the validity of the registered STRICT claims, but would
improve clarity if a later edit touches the files:

1. `candidate_proof.md` Part D states that "the roots `x` of the secular
   equation satisfy ... `sin((n+1)theta) + delta(x) sin(n theta) = 0`".
   This is true for roots with `sin p != 0`; at the exceptional points
   `sin p = 0` the continuous form must be used and the phase equation is not
   meaningful in the same way. A one-line "assume `sin p != 0`" phrase would
   make the reduction airtight. The same caveat is already present in Part C
   and in the tool note, and this is a presentation item only.
2. `final_report.md`, `research_map.md`, and `tools/...` summarise the formula
   as `sin(p)[U_n(m)+delta U_{n-1}(m)]` with `delta = sin(q)/(s sin(p))`; the
   exact proof carries the continuity caveat. Adding "(read by continuity when
   `sin p = 0`)" to those summaries would be consistent.
3. `tools/general-alternating-secular-chebyshev.md` currently says
   "尚未独立审计" (not yet independently audited). After this PASS, that
   status line should be updated to reflect the completed audit.

---

## 4. Verdict

| Category | Count |
| --- | --- |
| FATAL_GAP | 0 |
| REPAIRABLE_GAP | 0 |
| PASS | yes |

The two previous gaps (G1 continuity, G2 monotonicity naming) have been
repaired. The new STRICT claims — Lemma C1 (general alternating Chebyshev
secular representation), Lemma D1 (fixed-delta Chebyshev root-location lemma,
not monotonicity), and the amplitude-equality corollary from `E=0` — are sound
and may be registered as STRICT. O1/O2 remain open and are presented honestly.
