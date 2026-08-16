# Obligation graph — R-20260816T200000Z-hs-operator-domain

Root theorem (bundles packet items 1-3): for integer s >= 4, c > 0, under the
operator-domain reading H^s = D(K_c^{s/2}), the SL_hs system {Q_n^{(s)}} does NOT
lie in H^s for n >= 2 and is NOT dense; H_op^s and H_abs^s differ; the left-definite
density criterion does not extend to s >= 4 via the Q_n^{(s)} system.

## Nodes

ID: MO (Membership Obstruction, packet Q1b)
Statement: for s = 2r (r>=2): Q_n^{(2r)} = K_c^{-r}P_n in D(K_c^r) iff n in {0,1};
for s = 2r+1 (r>=2): Q_n^{(2r+1)} = K_c^{-r}K_n in D(K_c^{r+1/2}) iff n in {0,1}.
Quantifiers: every n >= 0, every c > 0, every r >= 2.
Depends on: L-DEF (deficit positivity: D_n > 0 for n>=2 for even; L(K_n)>0 for n>=2
for odd); L-DEC (deficit strictly increasing); A-POS (Krein-Sobolev a_m > 0);
T-CHAIN (transport-level reduction of membership).
Evidence/status: PROVED (strict) with exact EVIDENCE.
Proof or citation: candidate_proof.md Theorems MO-even / MO-odd.
Known edge cases: n=0,1 in; n>=2 out; c>0 essential.
Verifier notes: independent audit pending.

ID: L-DEF (deficit positivity, even)
Statement: for even n = 2k >= 2, f_{2k} = K_c^{-1}P_{2k} has f_{2k}'(1) > 0 (so notin D(K_c)).
Status: PROVED (sum of positive Legendre-derivative endpoint terms).
Depends on: known formula P_n^{(m)}(1).

ID: L-KS-DEF (deficit positivity, odd)
Statement: for n >= 2, L(K_n) := (Krein deficit of K_c^{-1}K_n) > 0.
Status: PROVED via L-DEC (D_m increasing) + A-POS (a_m>0): L(K_n)=sum_i a_{n-2i}(D_{n-2i}-D_{n-2i-2})>0.
Depends on: L-DEC, A-POS, KS-dec structure (K_n = sum a S).

ID: L-DEC (deficit strictly increasing)
Statement: D_m (Krein deficit of K_c^{-1}P_m) strictly increasing for m >= 1; D_m>0 for m>=2.
Status: PROVED (termwise comparisons D_{2K+1}>D_{2K} and D_{2K+2}>D_{2K+1} via explicit
A/B/CF formulas).
Depends on: P_n^{(m)}(1) formula.

ID: A-POS (Krein-Sobolev coefficients positive)
Statement: a_m > 0 for all m; each same-parity subsequence strictly increasing.
(Note: the literal "a_m strictly increasing for m>=2" is FALSE since a_2=a_3=1;
 only a_m > 0 is used by L-KS.)
Status: PROVED (a_m > 0 by induction; same-parity monotonicity; monotonicity
claim corrected per independent audit).
Depends on: recurrence positivity.

ID: T-CHAIN (transport-level reduction)
Statement: Q_n^{(2r)} in D(K_c^r) iff K_c^{-m}P_n in D(K_c) for m=1..r (in particular m=1);
Q_n^{(2r+1)} in D(K_c^{r+1/2}) iff K_c^{-m}K_n in D(K_c) for m=1..r (in particular m=1).
Status: PROVED (definition of D(K_c^r)/D(K_c^{r+1/2}) via functional calculus; polynomials smooth).

ID: Q1a (which polys in H_op^s)
Statement: H_op^s ∩ Pi = span{1,x} + span{degree-d polynomials : d in {2 floor(s/2)+2, ...}}.
For even s=2r and odd s=2r+1: H_op^s ∩ Pi = D(K_c^r) ∩ Pi has degrees {0,1} U {d >= 2r+2}.
Status: PARTIAL (structure established exactly for r=1,2,3 and c-independent; general
every-degree-present lemma is EVIDENCE-supported, minimal degree = 2r+2 proved for r<=3;
the membership-iff for n>=2 (MO) is PROVED).

ID: SPD (spaces differ, packet Q2)
Statement: H_op^s != H_abs^s for s >= 4; precisely, Q_2^{(s)} in H_abs^s (polynomial,
dense subspace) but Q_2^{(s)} notin H_op^s (MO); the identification H^s ≅ L^2 via
K_c^{s/2} maps the abstract class of Q_2^{(s)} and the operator-domain element
K_c^{-s/2}P_2 differently.
Status: PROVED (from MO).
Depends on: MO; definition of H_abs^s.

ID: EMB (embedding refinement)
Statement: Pi ∩ H_op^s is dense in H_op^s, hence H_op^s embeds isometrically as a
PROPER dense subspace of H_abs^s (for s>=4). Equiv W_r dense in L^2.
Status: PARTIAL-proved (W_r degree spectrum {0,1} U {>=2r+2} triangular => contains
span{x^k:k>=2r+2} dense in L^2 by moment orthogonality; relies on every-degree-present
lemma, EVIDENCE for r<=3). The difference claim SPD does NOT depend on this.
Depends on: Q1a (every-degree-present).

ID: ND (non-density, packet Q3)
Statement: span{Q_n^{(s)}} not dense in H_op^s = D(K_c^{s/2}) for s >= 4; indeed
{Q_n^{(s)} : Q_n in H_op^s} = {Q_0,Q_1}, closure = span{1,x} (2-dim) != H_op^s.
Status: PROVED (from MO + H_op^s infinite-dimensional).
Depends on: MO.

## Root completeness
Root is complete when MO, SPD, ND are proved (strict) and Q1a is characterized with
a clear strict/evidence split. All nodes above are either PROVED or EVIDENCE-supported
structural claims; the only EVIDENCE-only sub-claim is the "every degree >= 2r+2
present" lemma inside Q1a/EMB, which does not carry any load-bearing strict conclusion
(MO/SPD/ND are independent of it).
