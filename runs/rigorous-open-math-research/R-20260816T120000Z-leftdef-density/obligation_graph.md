# Obligation Graph — R-20260816T120000Z-leftdef-density

Root theorem RT: For H^s[-1,1] (s integer >= 1, c > 0, operator-domain
H^s = D(K_c^{s/2})) and closed constrained V ⊆ H^s, give an exact/structured
account of closure(span{p_n in V}) = V, handling the structural absence of x^k
(k>=2) and of the sparse family for s>=4; decide finite-data O1'; give the first
obstruction; recover the full-space result with correct scope.
Evidence/status: PARTIAL (STRICT structural theorems for s in {1,2,3}; decisive
negative finding for s>=4; O1'LD open).

## Nodes

N0  S1a-S1d structural facts.
    N0a (S1a/S1b/S1c): s in {1,2,3}: all p_n in H^s; (s=2,3) H^s ∩ C[x] = span{p_n}.
        Status: PROVED (docs + exact-verified).
    N0b (S1d): s >= 4: sparse p_n (n>=4) NOT in H^s; H^s ∩ C[x] = span{1,x}.
        Status: PROVED (exact witness p_4 notin H^4; STRICT deduction).
N1  span{p_n} dense in H^s (for s in {1,2,3}).
    Status: PROVED (L1': s=1 first-moment; s=2 SL_h2 L^2-descent; s=3 SL_h3
    H^1-moments; all moments well-defined).  NOTE: denseness_criteria Theorem 8
    step (i) is NOT used (unsound for s>=2, uses undefined H^s-moments).
N2  L1': V = H^s (s in {1,2,3}) => Q_sp = {p_n}, density holds.  Status: PROVED.  Depends N1.
N2' L1'': V = H^s (s >= 4) => Q_sp = {1,x}, closure(span Q_sp) = span{1,x} != H^s.
    Status: PROVED (STRICT negative).  Depends N0b.
N3  L2: P_V(W_s) dense in V (s in {1,2,3}).  Status: PROVED.  Depends N1.
N4  L3: transfer descent to H^{s'}, s' in {0,1}.  Status: PROVED.  Depends denseness Lemma 6.
N5  L4: all p_n in V (s in {1,2,3}) => V = H^s.  Status: PROVED.  Depends N1.
N6  L5: V = ker(Delta) in H^2 => density fails, q = p_5-2p_7 in V ∩ Q_sp^perp.
    Status: PROVED (airtight per independent audit).  Depends: DensBC Theorem A,
    parity-orthogonality, BC, Sobolev boundedness.
N7  L6/O1'LD: finite-data status; general proper V open.  Status: PARTIAL
    (decided V=H^s [L1'/L1''] + L5; general open).  Depends N2,N2',N3,N6,DensBC O1 Thm5.
N8  NEW open: membership of SL_hs system {Q_n^{(s)}} (s>=4) in D(K_c^{s/2});
    operator-domain vs abstract-completion reading.  Status: OPEN (flagged).

## Inferences
- RT depends on N0,N2,N2',N3,N4,N5,N6,N7,N8.
- N2 <- N1; N2' <- N0b; N3 <- N1; N4 <- denseness Lemma 6; N5 <- N1;
  N6 <- DensBC Theorem A; N7 <- N2,N2',N3,N6,DensBC O1 Theorem 5.

## Evidence / status legend
PROVED = STRICT (proof in candidate_proof.md or audited upstream).
OPEN = O1'LD / N8.
EVIDENCE = exact-arithmetic scripts (never close an obligation).

## Open edge
RT main edge (general proper V decision) is OPEN, reduced to O1'LD: realize a
free jump-base moment sequence by a nonzero element of the descended constraint
K_c^r V in H^{s'} (s' in {0,1}).  Also N8 (s>=4 operator-domain vs completion).

## Audit-status note
- Independent audit (023d145f): REPAIRABLE_GAP (original L1 s>=2 unsound; L3
  remark; L6(3)).
- Re-verification (ed2a5348): FATAL on the first L1 s>=4 repair (S1 equality false
  for s>=4; p_n notin H^s; Q_n^(s) notin span{p_n}); points 2,3 correct.
- Final correction: scope to s in {1,2,3} (L1') + negative L1'' (s>=4); exact
  re-derivation of all corrected points in this run.  N1/N2 re-PROVED (scoped);
  N2'/N0b newly PROVED (decision).  A further fresh verification of the FINAL
  corrected artifact is recommended before canonical promotion.
