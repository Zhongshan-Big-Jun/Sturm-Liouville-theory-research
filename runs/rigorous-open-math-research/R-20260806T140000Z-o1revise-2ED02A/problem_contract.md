# Problem contract - O1 reduction theorem revision (R-20260806T140000Z-o1revise-2ED02A)

Run type: repair + re-audit (single-agent reviser-verifier loop per the upstream
skill, phases 0-12).  All files use ASCII punctuation only.

## Authoritative problem source (provenance chain)

- Task packet: agenda/task-packets/Q-20260806-o1-revise-2ED02A.md
  sha256 4A2452D9DC53F4FCE77A541EBA0B85054A354B07893F642271ABF00638479225.
- Repair target: R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md
  sha256 C647297430348618A5120A3EAE5FAD09003B25EAFB9C8A8CCD9F449D1B397341.
- Audit verdicts: R-20260806T011500Z-o1audit-422A69/audit_report.md
  sha256 E6D1688963184DCBB87EC71EF8DB3B095A322D8B10D229CF8547ADB198B162CA.
- Repair list R1-R4: R-20260806T011500Z-o1audit-422A69/candidate_proof.md
  sha256 7DF07F84810788BC2AF5E5F718AB019AB731B26F19B98CD35008CEB0B53B4C06.
- Obligation graph (draft run): R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md
  sha256 62998C6E8066AAC9E6676FD0B78288830439E964330F7B84E404A604E7ADC7B2.
- Draft problem contract: R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md
  sha256 0FCD9F94293C7847342F4BDD7BE2B8B2F517D32F6E7D41536AB7409AECDBF779.

The packet is project context, NOT a verified theorem contract.  The exact
mathematical statement is re-normalized and re-audited below.

## Objects and definitions

Let R > 1 be fixed.  Let K = { rho in L^inf(0,1) : 1 <= rho <= R a.e. }.
Dirichlet string on (0,1):

    -y''(x) = lambda rho(x) y(x),   y(0) = y(1) = 0.

Eigenvalues 0 < lambda_1(rho) < lambda_2(rho) < ... (simple for every rho in K,
Sturm-Liouville with separated boundary conditions).  Eigenfunctions u_k chosen
L^2(rho)-normalized:  int_0^1 rho u_k^2 dx = 1.  Define

    D(rho) := lambda_2(rho) - lambda_1(rho).

Two-parameter families (closed parameter domain [0,1]^2):

    Barrier:  rho^{bar}_{a,b}(x) = R on (a,b), 1 elsewhere,  0 <= a <= b <= 1.
    Well:     rho^{well}_{a,b}(x) = 1 on (a,b), R elsewhere,  0 <= a <= b <= 1.

## Hypotheses

- R > 1 (degenerate R = 1 case is trivial: K = {1}, D = 3 pi^2, all families
  coincide; excluded from the theorem statement and handled separately).
- rho measurable (equivalently L^1) with pointwise bounds 1 <= rho <= R a.e.
- Dirichlet boundary conditions at both endpoints.
- D = lambda_2 - lambda_1 (fundamental gap), NOT any ratio.

## Target conclusion (Theorem O1, normalized)

(i)  sup_{rho in K} D(rho) = max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),  attained.
(ii) inf_{rho in K} D(rho) = min_{0<=a<=b<=1} D(rho^{well}_{a,b}),  attained.

Equivalently: every global maximizer is a.e. a barrier config and every global
minimizer is a.e. a well config (single-interval sign structure).

## Quantifiers and dependency of constants

- R is a parameter; the proof must hold for every fixed R > 1.  Constants such
  as the Hilbert-Schmidt bound C(R) = R/4 and the eigenvalue bounds
  lambda_k(rho) in [k^2 pi^2 / R, k^2 pi^2] may depend on R and k, not on rho.
- "a.e." statements are w.r.t. Lebesgue measure on (0,1); changes of rho on
  null sets do not change the operator or D.

## Equivalent formulations that are actually proved equivalent

- (i) is equivalent to: sup_K D = sup_{K_2} D where K_2 = piecewise constant
  rho in K with at most 2 jumps, because the supremum over K_2 is attained and
  the maximizer is bang-bang with single-interval positive set.
- (ii) is the mirror statement for the well family.

## Boundary and degenerate cases

- a = b: empty barrier / empty well -> rho = 1 (constant), D = 3 pi^2.
- (a,b) = (0,1): full barrier / full well -> rho = R, D = 3 pi^2 / R.
- a = 0 or b = 1: 2-block configs are members of the closed families.
- Effective jumps of an extremizer must be interior (jumps at 0 or 1 have zero
  measure effect and are absorbed into the adjacent interval).
- R -> 1+ is excluded (R > 1); the statement is continuous in R at R = 1.

## Permitted outcomes

- affirmative proof: revised candidate_proof.md with all obligations O1a-O1f
  closed and every premise verified against a primary source;
- self-audit report audit_report.md returning per-obligation verdicts and an
  explicit list of any residual gaps;
- negative proof / counterexample to any O1x claim, with certificate, if found.

## Completion criteria

1. The revised proof applies repairs R1 (S_rho operator presentation),
   R2 (moving-jump sign), R3 (u_2 sign convention), R4 (moving-jump FH by
   approximation) exactly as listed, with each repair's correctness rechecked
   (not copied blindly).
2. Every obligation O1a-O1f has a closed proof in the revised text and a
   self-audit verdict.
3. The theorem statement (i)-(ii) is NOT silently upgraded or weakened.
4. Numeric checks (scripts under reproducibility/) are recorded as evidence
   only, with a proof bridge for any computational claim used at proof level.
5. The final status label and gap list follow the upstream skill output
   protocol; an honest statement that a reviser cannot self-certify closure is
   included (independent re-audit remains the manager's step).

## Results that do not count as completion

- Merely restating the audit verdicts or the repair list.
- A revised proof that still contains O1a/O1b in unrepaired form.
- Proof for a different constraint class (L^p balls, fixed mass, MDE) without
  a rigorous transfer.
- Numerical evidence alone for any obligation.

## Tool, citation, and search constraints

- Premises to recheck against exact sources: AEH arXiv:2407.02459v2 Lemmas
  2.1, 2.2 (papers/fundamental_gap.txt); min-max/Weyl eigenvalue inequality
  for self-adjoint compact operators (standard, state precisely); Keller 1976
  and Mahar-Willner 1976 (context only, verify the class difference).
- Computation is evidence only; every proof-level computational claim needs a
  proof bridge or certificate.
- Chinese final reporting; ASCII punctuation in all files; clickable citation
  links in the final report.
- No use of private chain-of-thought; all claims externally checkable.

## Ambiguities or competing interpretations

- Operator identity: the draft and the audit write S_rho = rho^(1/2) T_rho
  rho^(1/2).  With T_rho = T_0 M_rho (T_0 = Dirichlet Green operator), the
  symmetric operator with kernel sqrt(rho(x)) G(x,t) sqrt(rho(t)) is
  S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} = M_{sqrt(rho)} T_rho M_{rho^{-1/2}},
  which is SIMILAR to T_rho (conjugation by M_{sqrt(rho)}), so spectra coincide.
  The expression rho^(1/2) T_rho rho^(1/2) is NOT symmetric in general; the
  intended operator is the kernel form.  This run uses the kernel form and
  records the correction.
- Moving-jump derivative: "rightward" and "leftward" are defined by the
  displacement of the jump point.  Signed parametrization (jump at x_j + eps)
  is used for the exact statement; the one-sided distance formulation is given
  as an equivalent corollary.  The audit's parenthetical about the two-sided
  derivative is recorded as imprecise (the two-sided derivative of
  eps |-> D(jump at x_j + eps) exists for every x_j and equals -(c_+ - c_-)f(x_j));
  what is true is that rightward/leftward DISTANCE derivatives differ in sign
  unless f(x_j) = 0.  Stationarity consequence f_N(x_j) = 0 is unchanged.
- The class K contains step functions with arbitrarily many jumps; the
  bounded-jump classes K_N are used only as an approximation ladder.

## Contract audit

Performed by the reviser (this run) against the packet, the draft, and the
audit run.  Fidelity checks:
- Statement (i)-(ii) above reproduces the draft theorem verbatim in content
  and the audit's audited statement; no quantifier or class change.
- The repair obligations R1-R4 are exactly the audit's gap list G1-G4.
- Boundary cases required by the packet (a=0, b=1, a=b, constants) are
  explicitly listed.
- A disproof route is preserved (counterexample search against each claim),
  although the independent re-derivation in this run confirms the statement.
- Unknown fields (model, exact version of draft) are recorded in
  repro_manifest.md; no invented provenance.
