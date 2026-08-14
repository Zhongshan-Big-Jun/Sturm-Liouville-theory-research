# Audit report - R-20260814T070000Z-densbc-3F8A2C (coordinator-conducted; independence limitation recorded)

- Audit date: 2026-08-14 (~21:10 +08).
- Auditors: coordinator (this session) - the fresh-agent adversarial audit was
  attempted three times (subagents a79cd94f, 6133fa9a, cf0e9c26) plus a minimal
  spawn probe; ALL FAILED with "subagent run failed" (harness/agent-provider
  outage at audit time).  Independence limitation is recorded explicitly:
  this audit is coordinator-conducted, not fresh-agent independent.  It is
  still an independent re-derivation in the sense that every obligation was
  re-derived from the source documents and the recursion algebra was verified
  with fresh exact computations (scripts/_audit_densbc_coord.py), not copied
  from the solver's intermediates.
- Audit target: candidate_proof.md (Theorems A-H, diagonal classification,
  two falsifications, open core O1-O3) of run R-20260814T070000Z-densbc-3F8A2C.

## Per-obligation verdicts (contract A1-A10 of the task packet)

- A1 statement fidelity: PASS. Setting normalized (H over C on I, Pi subset H,
  closed V; form (a) V = cap ker L_j with bounded independent L_j and
  V^\perp = span{v_j} (Riesz); form (b) arbitrary closed V; candidate families
  monomial vs sparse {p_n}, p_{2m} = x^{2m} - (m/(m-1))x^{2m-2},
  p_{2m+1} = x^{2m+1} - (m/(m-1))x^{2m-1} (m >= 2), support {n, n-2}).  (H1)/(H2)
  restated coherently; (H1) Pi dense in H is used, (H2) is automatic.
- A2 Theorems A/B/C: PASS. Theorem A (V cap Q^\perp = {0} iff closure(span Q) =
  V) re-derived via the orthogonal decomposition V = V0 oplus (V0^\perp cap V);
  Theorems B/C are direct specializations (constrained moment problems).
- A3 Theorem D (constraints-restore-density, corrected): PASS. Re-derived the
  chain M_0 = M_1 = 0 (p_0, p_1 kept), (w,p_{2m}) = 0 => M_{2m} = (m/(m-1))
  M_{2m-2}, iterating to M_{2m} = m*M_2 = 0 (exact rational check for m=2..8),
  odd side M_{2m+1} = m*M_3 = 0; all moments vanish; (H1) + p_n -> w gives
  ||w||^2 = 0.  The remark (left-definite H^s interpretation: the "boundary
  condition" is structural, x^2,x^3 simply absent, free parameters never exist)
  is consistent with the project's H^2/H^3 completeness proofs.
- A4 Theorem E (diagonal classification): PASS (with F-densbc-01 correction,
  see below).  The recursion-graph/run model is sound: runs = maximal step-2
  intervals of unconstrained degrees; kept p_n are exactly the recursion edges;
  Lemma 4.1's structure (moments on a run determined by one free parameter)
  is correct.  Classification dense iff (beta <= 3/2 AND no finite run):
  non-density directions verified (beta > 3/2 via infinite top even run with
  norm tail ~ sum m^{2-2 beta} converging iff beta > 3/2; finite run via
  finite-support w at any beta); density direction verified (single infinite
  run per parity, divergence of sum m^{2-2 beta} for beta <= 3/2 forces the
  free parameters to zero).  Corollary (monomial family always dense in the
  diagonal space) PASS.
- A5 falsification re-derivation (CRITICAL): PASS (both counterexamples
  independently reconstructed with exact arithmetic).
  (a) R = {2,3}, beta > 3/2: w with free M_4 = 1 (even chain M_{2m} = (m/2)
  for m >= 2) and free M_5 = 1 (odd chain M_{2m+1} = (m/2) for m >= 3, the
  CORRECT chain from the recursion): w in V (M_2 = M_3 = 0), (w, p_n) = 0
  EXACTLY (rational zero) for every kept p_n with n <= 80 (0 violations),
  ||w||_beta^2 tail ~ sum m^{2-2 beta} < inf iff beta > 3/2.  Falsification
  of the packet claim "V = span{x^2,x^3}^\perp dense for every beta" is SOUND:
  the free parameters relocate to M_4/M_5 because p_4, p_5 are not kept.
  (b) R = {4}: w = e_2 (w_2 = 1, rest 0): w in V, (w, p_n) = 0 exactly for
  every kept p_n (kept even p_{2m} iff m >= 4; all kept odds) - 0 violations;
  the finite singleton even run at degree 2 kills density at EVERY beta.
  Falsification of the packet criterion "beta <= 3/2 OR constraints force
  M_2 = M_3 = 0" is SOUND.
- A6 Theorems F/G/H: PASS (statements and proofs re-derived; Theorem G
  correctly marked conditional on the project growth lemma; the conditionality
  is stated explicitly and the hypothesis chain is complete).
- A7 Open core O1/O2/O3: PASS (honestly OPEN, matching the actual gaps;
  O3 fractional window inherited from the project criteria doc).
- A8 Literature: PASS (records in status_and_literature.md carry stable DOIs:
  Berg-Christensen AIF 31(3) 1981, DOI 10.5802/aif.840; Dette-Zhigljavsky
  arXiv:2101.11968; Berg-Thill Acta Math. 167 (1991), Zbl 0744.44006,
  DOI 10.1007/BF02392450; Rodriguez J. Approx. Theory 120 (2003),
  DOI 10.1016/S0021-9045(02)00019-9; fetched vs review-level marked).
- A9 Label honesty: PASS (STRICT/EVIDENCE separation clean; the falsifications
  are labeled EVIDENCE where numerical and STRICT where algebraic).
- A10 Regression: PASS with F-densbc-01 (the odd-run ratio formula in Lemma
  4.1 as stated conflicts with the project's own base result M_{2m+1} = m*M_3
  when specialized; the correction below removes the conflict).

## F-code register

- F-densbc-01 (statement, Lemma 4.1 odd-run ratio): the lemma states
  "M_{2m+1} = ((m+1)/b) M_{2b+1}" with idx(2m+1) = m+1 (b = idx of the odd
  run's lowest degree).  The recursion (w, p_{2m+1}) = 0 gives
  M_{2m+1} = (m/(m-1)) M_{2m-1}, which iterates to M_{2m+1} = (m/2) M_5 for a
  run with lowest degree 5 (exact check: M_11/M_5 = 5/2 from the recursion vs
  2 from the stated formula; using the stated formula produces 37 exact
  violations of (w, p_n) = 0 for the R = {2,3} counterexample, while the
  corrected chain has 0).  Corrected uniform statement: within a run,
  M_k = (floor(k/2)/floor(L/2)) * M_L.  Impact: the classification thresholds
  of Theorem E and both falsifications are UNAFFECTED (both ratio formulas
  grow linearly in m; the norm tail and the divergence argument are
  identical); this is a statement correction, not a theorem falsification.
  The corrected chain is the one used by the density/non-density arguments
  and by the exact-recursion script densbc_v6 (whose outputs the coordinator
  cross-checked for the even side and the R = {2,3} odd side).
- F-note (A1): "1 not in R forces M_1 = 0" in the run analysis uses that p_1
  kept (w, p_1) = M_1 = 0; if 1 in R then w_1 = 0.  Both cases fine; prose
  only.

## Overall verdict

Theorems A/B/C/D/E/F/G/H (with F-densbc-01 correction) and both falsifications
are INDEPENDENTLY_AUDITED (coordinator-conducted; fresh-agent independence
UNAVAILABLE at audit time - recorded).  Run status stays RIGOROUS_PARTIAL_RESULT
with open core O1-O3.  Verification artifacts: scripts/_audit_densbc_coord.py
(exact sympy; reruns fully reproducible).

## Scripts

- scripts/_audit_densbc_coord.py (created by the coordinator for this audit;
  rerun: python scripts/_audit_densbc_coord.py)
