# Obligation Graph — R-20260816T120000Z-leftdef-density

Root theorem RT: For H^s[-1,1] (s integer >= 1, c > 0) and closed constrained
  V ⊆ H^s, give an exact/structured account of closure(span{p_n in V}) = V,
  handling the structural absence of x^2,x^3, deciding finite-data O1', the
  first obstruction, and recovering V = H^s.
Evidence/status: PARTIAL (several STRICT subtheorems; O1'LD open).

## Nodes

N0  S1: for s >= 2, H^s ∩ C[x] = span{p_n : n in D}, only monomials 1,x in H^s.
    Status: PROVED (STRICT; documented + exact-arithmetic verified for s=2,
    higher s by embedding H^s ⊂ H^2).  Depends on: SL_h2 Lemma 1 (BC),
    exact arithmetic (EVIDENCE support).
N1  span{p_n} dense in H^s for all integer s >= 0.  Status: PROVED (project
    DERIVED, SL_denseness_criteria Theorem 8; audited).  Depends on: N0,
    jump recursion, growth lemma, transfer.
N2  L1: V = H^s => Q_sp = {p_n}, density holds.  Status: PROVED.  Depends N1.
N3  L2: P_V(W_s) dense in V (structural projection density).  Status: PROVED.  Depends N1.
N4  L3: transfer descent to H^{s'}, s' in {0,1}.  Status: PROVED.  Depends:
    K_c : H^t -> H^{t-2} isometry (denseness Lemma 6, audited).
N5  L4: all p_n in V => V = H^s.  Status: PROVED.  Depends N1.
N6  L5: V = ker(Delta) in H^2 => density fails, q = p_5-2p_7 in V ∩ Q_sp^perp.
    Status: PROVED (STRICT).  Depends: DensBC Theorem A, parity-orthogonality,
    BC computation for odd p_n, Sobolev boundedness of Delta.
N7  L6/O1'LD: finite-data status; general proper V open.  Status: PARTIAL
    (decided V=H^s + L5 instance; general open).  Depends N2,N3,N6,DensBC O1 Thm5.

## Inferences
- RT depends on N0,N2,N3,N4,N5,N6,N7.
- N2 <- N1; N3 <- N1; N4 <- denseness Lemma 6; N5 <- N1; N6 <- DensBC Theorem A;
  N7 <- N2,N3,N6,DensBC O1 Theorem 5.

## Evidence / status legend
PROVED = STRICT (proof given in candidate_proof.md or audited upstream).
OPEN = O1'LD (the realization/membership step for general proper V).
EVIDENCE = exact-arithmetic scripts (never close an obligation).

## Open edge
RT main edge (general proper V decision) is OPEN, reduced to O1'LD.  The
smallest still-open obligation is: realize a free jump-base moment sequence by a
nonzero element of the descended constraint K_c^r V in H^{s'} (s' in {0,1}).
