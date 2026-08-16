# Obligation Graph

Run: R-20260816T000000Z-densbc-o1
Task: Q-20260816-densbc-o1-A1B2C3D4

## Dependency structure (leaf -> root)

N0 (Hilbert facts): (H1) Pi dense in H, (H2) moments, continuity of P_V,
   Riesz representers <w,v_j> = L_j(w).  [assumed standard; STRICT]

N1 (Master, upstream Theorem A, audited): closure(span Q_sp) = V <=> V cap Q_sp^\perp = {0}.
   status: PROVED (upstream, audited).

N2 (Theorem 1 projection density) = N0.
   Statement: P_V(Pi) dense in V; span{P_V(p_n)} dense in V.
   status: PROVED (STRICT, this run).
   Proof: continuous image of dense set.  EVIDENCE corroboration: o1_projection_density.py.

N3 (Theorem 2 obstruction system) = N0 + N1.
   V cap Q_sp^\perp = { w in V : <w,p_n>=0 for all n in N } with p_n expanded in M_k.
   status: PROVED (STRICT).

N4 (Theorem 3 run lemma + first obstruction) = N0 + N3 + corrected Lemma 4.1 ratio.
   Run decomposition of (R); free run-bases; first obstruction degree D*.
   status: PROVED (STRICT), using F-densbc-01 corrected ratio.

N5 (Theorem 4 diagonal reduction) = N4 + upstream Theorem E.
   Criterion reduces to Theorem E (beta <= 3/2 AND no finite run) for coordinate L_j.
   status: PROVED (STRICT).

N6 (Theorem 5 finite-rank structure) = N3 + N4.
   Answer is structured, not purely finite-rank in general; finite-rank under
   (all v_j polynomials) + (finite-rank realization).
   status: PROVED (STRICT structural claim); the realizability core is O1' (OPEN).

N7 (Lemma 6.1 empty kept set) = N3.
   N empty => Q_sp = empty => density fails unless V = {0}.
   status: PROVED (STRICT).  Heuristic 6.2 (generic N empty) is EVIDENCE/HEURISTIC,
   NOT STRICT (audit correction).  EVIDENCE corroboration in both scripts.

## Open obligations

- O1' (reduced core): decide free run-base realization (moment representability +
  membership in V) for general H.  OPEN (honest; not closed).
- O2 / O3 (inherited upstream): still open; not addressed as solved.

## Refuted / blocked routes (this run)

- Route "force a purely finite-rank closed form valid for all non-diagonal H":
  BLOCKED by Theorem 5 (requires moment data).  Precise gap: the realization step
  is a moment problem.
- Route "numeric verification closes O1": REFUTED (EVIDENCE never closes an
  obligation; numerical scripts are EVIDENCE only).

## Verification status

- Theorems 1-5 and Lemma 6.1 are STRICT statements; Heuristic 6.2 is EVIDENCE; the independent
  adversarial audit (audit_report.md) checks them.  Numerical scripts are EVIDENCE.
