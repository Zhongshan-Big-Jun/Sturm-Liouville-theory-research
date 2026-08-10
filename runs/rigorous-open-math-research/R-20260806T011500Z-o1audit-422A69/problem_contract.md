# Problem contract (audit)

## Role of this document

This run is a READ-ONLY, independent audit of the draft reduction theorem O1
in run R-20260805T000000Z-gapn1-a1b2c3 (file O1_reduction_draft.md), with
obligations O1a-O1f taken from obligation_graph.md of the same run.  The task
packet Q-20260806-o1-audit-422A69 is treated as project context, NOT as a
verified theorem contract.  The exact problem statement is normalized below and
audited against the draft and against the primary sources.

## Objects and definitions

Let R > 1.  Dirichlet vibrating string on [0,1]:

    -y''(x) = lambda rho(x) y(x),  y(0) = y(1) = 0,
    rho measurable, 1 <= rho(x) <= R a.e.  (box class K)

Let 0 < lambda_1(rho) < lambda_2(rho) be the first two eigenvalues
(simple; the k-th eigenfunction has exactly k-1 interior zeros), normalized by
integral rho u_k^2 dx = 1.  Define

    D(rho) := lambda_2(rho) - lambda_1(rho),
    f(x)   := lambda_1 u_1(x)^2 - lambda_2 u_2(x)^2.

Barrier family B = { rho = R on (a,b), 1 elsewhere : 0 <= a <= b <= 1 }.
Well family    W = { rho = 1 on (a,b), R elsewhere : 0 <= a <= b <= 1 }.

## Theorem under audit (O1, as stated in the draft)

(i)  sup_{rho in K} D(rho)  =  max_{0<=a<=b<=1} D(rho = R on (a,b), 1 elsewhere),
(ii) inf_{rho in K} D(rho)  =  min_{0<=a<=b<=1} D(rho = 1 on (a,b), R elsewhere),
and both extrema over the two-parameter families are attained.

## Audit obligations (from the draft-run obligation graph, O1 node)

- O1a: lambda_k continuous in L^1 on {1<=rho<=R}.  Draft gives Lemma 1.
- O1b: FH derivative wrt moving a jump point is (c_{j+1}-c_j) f(x_j).  Draft Lemma 3.
- O1c: f has at most 2 zeros and {f>0} is a single interval (Wronskian).  Draft Lemma 2.
- O1d: Compactness of the N-jump family and existence of rho^N.  Draft Lemma 4.
- O1e: M_N -> S(R).  Draft Lemmas 4-5.
- O1f: Bang-bang at a global extremizer.  Draft SUP/INF parts.

## Verdict scale (per packet)

PROVED / PARTIAL / FAILED / OPEN, with exact reasons; every cited theorem
rechecked against its original source and exact version.

## Boundary and degenerate cases to be checked

- a = 0 or b = 1 (2-block configs), a = b and rho constant (1 or R).
- Constant densities; rho taking interior values in (1,R) on intervals.
- Measure-zero changes of rho.
- R -> 1+ and unbounded number of jumps (class K is not a bounded-jump class).
- Moving-jump families: one-sided derivatives at a jump point.

## Permitted outcomes

- PROVED verdicts per obligation with exact reasons;
- FAILED/PARTIAL verdicts with the smallest failing claim and repair (report only,
  do not repair the draft);
- overall audit verdict from the skill taxonomy.

## Completion criteria for this audit run

1. O1a-O1f each receive a verdict with a line-level justification.
2. Every premise cited by the draft (AEH arXiv:2407.02459v2 Lemma 2.1, Lemma 2.2,
   min-max continuity of self-adjoint compact operators) is quoted exactly from the
   local primary source papers/fundamental_gap.txt and checked.
3. The relevance (or non-relevance) of Keller 1976, Mahar-Willner 1976,
   Cheng-Kung-Law-Lian 2010 to the O1 premises is recorded.
4. Numeric checks are run as evidence only and are labeled as such.
5. All standard artifacts are written under the run root.

## Results that do not count as completion

- Merely restating the draft without a verdict.
- Declaring the theorem PROVED without auditing each obligation.
- Repairing the draft (the packet forbids it; gaps are reported precisely).

## Ambiguities and competing interpretations

- The draft does not specify the Hilbert space for the operator T_rho in Lemma 1;
  this matters for O1a (see audit).
- The sign convention in Lemma 3 ("up to the sign of eps") is ambiguous and is
  resolved against the numerical verification in the draft run itself (R-003:
  dD/du = -2(R-1) f_sym) and against direct computation in this run.

## Contract audit

Normalized by the auditor from the task packet, the draft O1_reduction_draft.md,
and the draft-run obligation_graph.md, problem_contract.md, and
research_ledger.md.  No quantifier, class, or definition was changed relative to
the draft theorem statement.
