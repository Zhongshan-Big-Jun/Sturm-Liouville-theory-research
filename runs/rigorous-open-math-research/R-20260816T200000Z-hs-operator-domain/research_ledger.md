# Research Ledger — R-20260816T200000Z-hs-operator-domain

Run objective: resolve the operator-domain vs abstract-completion reading of the
Krein left-definite spaces H^s for s >= 4, and decide membership of the SL_hs
orthogonal system {Q_n^{(s)}} in D(K_c^{s/2}); consequences for density criterion.

## Chronology

### 2026-08-16 — Normalization and contract
- Read task packet Q-20260816-hs-operator-domain-C0D1E2F3.
- Read left-def run final_report / candidate_proof / audit_report
  (R-20260816T120000Z-leftdef-density) and SL_hs doc (docs/SL_hs_orthogonal_systems_proof.tex).
- Contract v1.1 written; two readings (operator domain vs abstract completion) isolated.

### 2026-08-16 — Exact boundary computations (EVIDENCE)
- Script reproducibility/boundary_facts.py (exact sympy):
  - `K_c^{-1}P_n ∈ D(K_c)` ONLY for n in {0,1}; all n >= 2 fail.
    (even n: Krein deficit f'(1) > 0; odd n: f'(1) - f(1) > 0.)
  - `K_c^{-2}P_n ∈ D(K_c^2)` ONLY for n in {0,1} (r=2, s>=4).
  - `K_c^{-3}P_n ∈ D(K_c^3)` ONLY for n in {0,1} (r=3).
  - `D(K_c^r) ∩ {monomials} = span{1,x}` for r = 1,2 (monomial-level check).
- Script reproducibility/krein_sobolev_membership.py (fixed Krein-Sobolev):
  - `K_c^{-1}K_n ∈ D(K_c)` ONLY for n in {0,1} (odd-case binding condition).

### 2026-08-16 — KEY structural correction to upstream
- Script reproducibility/domain_poly_span.py + degree_structure.py + genericity_check.py:
  - For r=1 (s=2): D(K_c) ∩ Pi has degrees {0,1} U {d >= 4}.
  - For r=2 (s=4): D(K_c^2) ∩ Pi has degrees {0,1} U {d >= 6}.
  - For r=3 (s=6): D(K_c^3) ∩ Pi has degrees {0,1} U {d >= 8}.
  - c-independent (checked c in {1,3,10}) => generic structure.
  - REFUTES the left-def run S1d auxiliary claim "H^s ∩ C[x] = span{1,x} for s>=4":
    explicit degree-6 polynomial x^2(x^4-5x^2+7) lies in D(K_c^2)=H^4 (c=3).
  - The left-def run L1'' (sparse family {p_n} not dense for s>=4) STANDS:
    p_n (n>=4) not in D(K_c^r), so Q_sp = {1,x} for the sparse family.

### 2026-08-16 — Strict positivity proofs (STRICT)
- Even case: D_{2k}'(1) formula strictly positive (sum of positive Legendre
  derivative terms); D_{2K+1} - D_{2K} > 0 via termwise A,B comparison; proved.
- Odd case: D_m strictly increasing (D_{2K+1}>D_{2K}, D_{2K+2}>D_{2K+1} proved
  termwise), D_m>0 for m>=2, a_m>0 and increasing (recurrence) => L(K_n)>0 for n>=2.
- => Theorem MO: for s >= 4, Q_n^{(s)} notin H_op^s = D(K_c^{s/2}) for all n >= 2
  (both parities).

### 2026-08-16 — Space comparison and density (STRICT)
- Theorem SPD: H_op^s and H_abs^s differ (Q_2^(s) in H_abs^s \ H_op^s).
- Theorem ND: span{Q_n^{(s)}} not dense in H_op^s for s >= 4 (only Q_0,Q_1 in H_op^s;
  span = span{1,x} is a proper closed 2-dim subspace).
- W_r density: W_r (degree spectrum {0,1} U {>=2r+2}) is dense in L^2 (triangular +
  moment-orthogonality argument) => Pi ∩ H_op^s dense in H_op^s => H_op^s embeds
  isometrically (as a proper dense subspace) in H_abs^s. [This is a refinement; the
  difference claim does not depend on it.]

### 2026-08-16 — Literature / novelty sweep
- Web: left-definite theory (LW 2002; FGH L arXiv:2408.01514), Krein-Sobolev papers;
  no external source settles the specific operator-domain vs abstract-completion
  membership question for s>=4 => POTENTIALLY_NEW (consistent with project flag).

### 2026-08-16 — Independent adversarial audit (fresh subagent 88de280c)
- Verdict: REPAIRABLE_GAP. Critical_errors: []. Gaps:
  1. Q1a(ii) degree-spectrum "every degree >= 2r+2 present" / "no degree in 2..2r+1"
     is EVIDENCE-only (finite r<=3, c in {1,3,10}) and its proof sketch asserts the
     minimal-degree claim without a derivation; non-load-bearing (MO/SPD/ND independent).
  2. A-POS literal "a_m strictly increasing for m>=2" is FALSE (a_2=a_3=1); only
     a_m > 0 is used by L-KS and is correctly proved.
- Verified correct by audit: parity Krein conditions; Lemma T direction; DE/DO/DM/L-KS
  algebra; MO, SPD, ND logic; boundary cases; and the three mandated ground-truth
  dual-wire checks (D_4 = 5(2c+21)/c² by two independent means; Q_4^(2) failing the
  Krein condition; x²(x⁴-5x²+7) in D(K_3²)).
- Repair applied: A-POS statement corrected (a_m>0 + same-parity monotonicity; notes
  the false literal). Q1a already labeled EVIDENCE/OPEN for the every-degree lemma in
  candidate_proof.md §5 and §10; kept non-load-bearing.
- Lean scaffold SL/HsOperatorDomain_Scaffold.lean builds (lake build, 8567 jobs);
  all proof bodies are `sorry` (scaffold, not verified).

## Decisions
- Use the OPERATOR-DOMAIN reading H^s = D(K_c^{s/2}) as the primary answer space,
  matching the project's concrete proofs; report the abstract-completion reading as
  the one in which the SL_hs doc's completeness holds.
- Record the upstream S1d correction honestly; it does not invalidate the left-def
  run's L1'' (sparse-family negative finding).

## Phase 12 — Fresh-context convergence check (2026-08-16)
Reconciled from files only: problem_contract (v1.1), obligation_graph (MO/SPD/ND
PROVED, Q1a PARTIAL/EVIDENCE), approach_registry (R1 main PROVED, R2 SPD PROVED/EMB
PARTIAL, R3 REFUTED-correction), candidate_proof (strict MO/DE/DO/DM/A-POS/L-KS/
SPD/ND + Q1a split), audit_report (REPAIRABLE_GAP, gaps recorded/repaired), ledger,
evidence log, Lean scaffold (builds). CONVERGED: load-bearing obligations closed;
one non-load-bearing EVIDENCE lemma (Q1a every-degree) open; no divergence, no
re-opened blocked route. Result status: RIGOROUS_PARTIAL_RESULT.
