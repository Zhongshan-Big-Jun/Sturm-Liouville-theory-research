# Problem contract

Run: R-20260816T200000Z-hs-operator-domain
Task packet: Q-20260816-hs-operator-domain-C0D1E2F3 (DRAFT)
Project ID: MRP-20260731-BVE-SL
Portfolio problem: O-2026-SL-DENS-BC-A1B2C3
Upstream run: R-20260816T120000Z-leftdef-density
Contract version: v1.1 (normalized and audited against the packet and the SL_hs doc)

## Objects and definitions

- Interval [-1,1]; c > 0 fixed throughout.
- Krein Laplacian `K_c f := -f'' + c f` on `L^2(-1,1)` with
  `D(K_c) = { f : f,f' in AC, f'' in L^2, f'(1) = f'(-1) = (f(1)-f(-1))/2 }`.
  `K_c` is self-adjoint, positive, 0 notin spectrum.
- Operator-domain left-definite scale (the reading used by project SL_h2/h3/hs):
  `H_op^s := D(K_c^{s/2})`, `(f,g)_s := (K_c^{s/2}f, K_c^{s/2}g)_{L^2}`, integer s >= 1.
  Even: `H_op^{2r} = D(K_c^r)`; odd: `H_op^{2r+1} = D(K_c^{r+1/2})`.
- Abstract completion: `H_abs^s :=` completion of all polynomials `Pi` under the
  pre-Hilbert structure `(f,g)_s` (well-defined on Pi by the explicit polynomial
  formulas `(f,g)_{2r}=(K_c^r f,K_c^r g)_{L^2}`, `(f,g)_{2r+1}=(K_c^r f,K_c^r g)_1`).
- Formal transport operator on Pi: `K_c^{-1} = c^{-1} sum_{j>=0} c^{-j} D^{2j}`
  (formal power series; finite sum on polynomials). `K_c^{-r}` its r-th power.
- SL_hs "complete orthogonal polynomial system" (SL_hs doc, 2026-08-05):
  - even s = 2r: `Q_n^{(2r)} := K_c^{-r} P_n` (Legendre P_n),
  - odd s = 2r+1: `Q_n^{(2r+1)} := K_c^{-r} K_n` (Krein-Sobolev K_n).
  The doc claims each is complete orthogonal in `(H^s, (·,·)_s)` for all integer s >= 1.
- Sparse family `{p_n}` (left-def run): `p_0=1, p_1=x`,
  `p_{2m}=x^{2m}-(m/(m-1))x^{2m-2}`, `p_{2m+1}=x^{2m+1}-(m/(m-1))x^{2m-1}` (m>=2).

## Hypotheses

- integer s >= 4; c > 0. Both even s = 2r (r >= 2) and odd s = 2r+1 (r >= 2).
- V = H_op^s = D(K_c^{s/2}) when asking density.

## Target conclusion (packet items 1-3, normalized)

1. Precise description of the operator domain `H_op^s = D(K_c^{s/2})`:
   (a) which polynomials lie in it (`H_op^s ∩ Pi`);
   (b) whether the SL_hs polynomials `{Q_n^{(s)}}` lie in `D(K_c^{s/2})`.
2. Compare `H_op^s` (operator-domain completion) with `H_abs^s` (abstract
   completion from the left-definite inner product on polynomials). Equal or not?
   If not, precise difference.
3. Consequence: whether `span{Q_n^{(s)}}` is dense in `H_op^s = D(K_c^{s/2})`
   under the operator-domain reading, and whether the left-definite density
   criterion extends to s >= 4.

## Quantifiers and dependency of constants

- All statements quantify over every integer s >= 4 and every c > 0.
- Constants hidden in inner-product equivalence do not appear as explicit numerical
  bounds in the strict claims; the strict claims are membership/density/difference
  statements (not quantitative bounds).

## Equivalent formulations proved equivalent (in this run)

- `Q_n^{(2r)} = K_c^{-r}P_n ∈ D(K_c^r)`  <=>  `K_c^{-m}P_n ∈ D(K_c)` for all m=1..r
  <=> (in particular) `K_c^{-1}P_n ∈ D(K_c)`.
- `Q_n^{(2r+1)} = K_c^{-r}K_n ∈ D(K_c^{r+1/2})`  <=>  `K_n ∈ D(K_c^{1/2})` and
  `K_c^{-m}K_n ∈ D(K_c)` for m=1..r <=> (K_n is a smooth polynomial, so the binding
  condition is) `K_c^{-1}K_n ∈ D(K_c)`.
- `H_op^s ↪ H_abs^s` isometric (as completion of a common dense polynomial subset)
  holds iff `Pi ∩ H_op^s` is dense in `H_op^s`, equivalently `W_r := K_c^r(Pi ∩ D(K_c^r))`
  is dense in L^2 for s = 2r (analogous for odd).

## Boundary and degenerate cases

- n = 0, 1: `Q_0^{(s)}, Q_1^{(s)}` are (scalar multiples of) 1 and x; they DO lie in
  every `H_op^s`.
- s = 1,2,3 (r <= 1): the operator-domain and abstract-completion readings coincide
  (project SL_h1/h2/h3 results); boundary conditions at a single transport level.
- s >= 4 (r >= 2): multiple transport levels; the level-1 transport condition
  `K_c^{-1}(base) ∈ D(K_c)` is the binding obstruction, and it FAILS for n >= 2.
- c > 0 fixed; c <= 0 would break positivity (out of scope).

## Permitted outcomes

- affirmative proof (membership/difference/density statements)
- negative proof (Q_n^(s) notin D(K_c^{s/2}) for n>=2; span not dense; spaces differ)
- counterexample to an auxiliary claim of the upstream run (S1d "span{1,x}" refuted)

## Completion criteria

- Item 1: exact characterization of `H_op^s ∩ Pi` (degree structure) and the
  membership decision for all `Q_n^{(s)}`, with a strict derivation for the
  n >= 2 obstruction (positive transport deficit).
- Item 2: a strict statement of equality or difference of `H_op^s` and `H_abs^s`,
  with the precise mechanism of difference.
- Item 3: a strict density statement for `span{Q_n^{(s)}}` in `H_op^s`, and whether
  the density criterion extends to s >= 4.
- All strict claims must have a derivation; finite exact-arithmetic checks are
  labeled EVIDENCE and never close a strict obligation by themselves.

## Answer space

The result must support the decision: under the OPERATOR-DOMAIN reading of H^s
(the one used in the project's concrete H^2/H^3 proofs and the SL_hs doc), do the
SL_hs `Q_n^{(s)}` form a dense/complete system in `H^s` for s >= 4, and do the
operator-domain and abstract-completion readings agree? The answer decides whether
the left-definite density criterion extends to s >= 4.

## Acceptance criteria per subproblem

- Q1a (which polys in D(K_c^{s/2})): accepted when the degree structure
  `H_op^s ∩ Pi = span{1, x} + span{degree-d polys : d >= 2 floor(s/2)+2}`
  is stated and the minimal-degree / every-degree-present claim is verified
  (c-independent, generic).
- Q1b (Q_n membership): accepted when Theorem MO (below) is proved strictly for
  both parities.
- Q2 (operator vs abstract): accepted when a strict difference statement is proved
  (Q_2^{(s)} in H_abs^s \ H_op^s).
- Q3 (density): accepted when the negative density statement is proved strictly.

## Results that do not count as completion

- Finite exact checks alone (they are EVIDENCE).
- The upstream left-def run's auxiliary claim "H^s ∩ C[x] = span{1,x} for s>=4"
  (REFUTED below) reused as a premise.
- Claiming density of `{Q_n^{(s)}}` in `H_op^s` based on completeness in `H_abs^s`
  (the spaces differ).

## Forbidden moves (per-problem discipline)

- No silent interchange of operator-domain and abstract-completion readings.
- No claim that the formal polynomial inverse equals the operator inverse without
  checking the Krein boundary conditions at every transport level.
- Numerical evidence must not close any strict obligation.
- Do not present finite-degree checks as a proof for all n.

## Tool, citation, and search constraints

- Python `C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe`,
  PYTHONUTF8=1; sympy exact arithmetic for EVIDENCE.
- Citations: Littlejohn-Wellman 2002 (left-definite theory), Fischbacher-
  Gesztesy-Hagelstein-Littlejohn arXiv:2408.01514 (abstract left-definite),
  Littlejohn-Quintero & Jones-Littlejohn-Quintero Roba (Krein-Sobolev).
- No git commit/push; manager syncs at stage close.

## Ambiguities or competing interpretations

- The packet/skill treats H^s as "either the operator domain or the abstract
  completion"; the project's concrete proofs use the OPERATOR-DOMAIN reading.
  This run resolves the relationship under that reading and reports the correction.
- The SL_hs doc's completeness claim for s >= 4 is about the abstract completion,
  NOT the operator domain; this is the central clarification.

## Contract audit

- Contract v1.1 normalized from the task packet + SL_hs doc + left-def run
  final_report/candidate_proof/audit_report (project context, not trusted facts).
- Independent adversarial audit of the candidate proof (fresh context subagent)
  checks semantic fidelity against this contract.
