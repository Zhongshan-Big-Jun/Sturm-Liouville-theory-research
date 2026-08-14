# Run Notes: Phase 6 (evidence) and Phase 3 (literature)

Run: R-20260814T070000Z-densbc-3F8A2C

## What was done and why (trace)

1. NORMALIZED the problem (problem_contract.md): two forms (a) V = intersection of
   kernels of finitely many continuous linear functionals; (b) arbitrary closed
   subspace.  Master Hahn-Banach criterion + sparse family {p_n}.

2. DISCOVERED AND CONFIRMED that the packet's central example is wrong for
   beta > 3/2 (free params relocate M_2,M_3 -> M_4,M_5 because p_4 breaks the
   recursion).  Evidence: densbc_v1, densbc_v3 (bad_pn_ips=0, finite norm).

3. DISCOVERED the "finite-run" phenomenon at beta <= 3/2 (constraints can
   DESTROY density even in the regime where the unconstrained space is dense).
   Evidence: densbc_v4, densbc_v5.

4. FORMULATED the CORRECTED diagonal classification (Theorem E) and the
   CORRECTED constraints-restore-density mechanism (Theorem D).  These are the
   main contributions.

5. LITERATURE: 4 papers deep-read.  Berg-Christensen 1981 (whole L^p only, no
   constrained-subspace theorem), Dette-Zhigljavsky 2021 (opposite direction
   RKHS), Berg-Thill 1991 (rotation-invariant L^2(mu), no constrained result;
   note venue correction), Rodriguez 2003 (whole W^{k,p}; L^p-reduction iff; no
   boundary-subspace result).  Net: the constrained-subspace problem is open in
   the classical literature.

## Evidence script semantics

- "bad_pn_ips" = number of kept sparse p_n with |(w,p_n)| > 1e-9.
- "max|ip|" = largest |(w,p_n)| over all kept p_n.
- ||w||^2 = sum_k M_k^2 (k+1)^{-2 beta} (truncated finite sum top).
- "kept_count" = number of indices n with p_n in V.

## Honesty notes

- The diagonal classification is proven (STRICT) in candidate_proof.md and
  numerically corroborated; numerics never close an obligation by themselves.
- The finite-run detection script densbc_v4 had a bug that treated the top
  infinite run as "finite" (capped at a large hardcoded degree); densbc_v5 and
  densbc_v1 handle the infinite-vs-finite distinction correctly.  Only the
  finite-support orthogonal w phenomenon rests partly on densbc_v4, and it is
  independently confirmed by densbc_v5 (R={4,8},{3,9},{3,7}) and densbc_v1.
