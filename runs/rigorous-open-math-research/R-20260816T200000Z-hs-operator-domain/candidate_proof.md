# Candidate Proof — R-20260816T200000Z-hs-operator-domain

Run: R-20260816T200000Z-hs-operator-domain
Task: Q-20260816-hs-operator-domain-C0D1E2F3
Status label: RIGOROUS_PARTIAL_RESULT
Contract version: v1.1

## Setting (see problem_contract.md)

Krein Laplacian `K_c = -d^2/dx^2 + c`, c > 0, on L^2(-1,1),
`D(K_c) = { f : f,f' in AC, f'' in L^2, f'(1)=f'(-1)=(f(1)-f(-1))/2 }`.
Operator domain `H_op^s := D(K_c^{s/2})`, `(f,g)_s = (K_c^{s/2}f, K_c^{s/2}g)_{L^2}`.
Abstract completion `H_abs^s :=` completion of all polynomials Pi under `(·,·)_s`.
Formal inverse on Pi: `K_c^{-1}p = c^{-1} sum_{j>=0} c^{-j} p^{(2j)}` (finite sum).
SL_hs system: even `Q_n^{(2r)} = K_c^{-r}P_n`; odd `Q_n^{(2r+1)} = K_c^{-r}K_n`
(Krein-Sobolev K_n).  Krein deficit of a polynomial f:
`Delta(f) := f'(1) - (f(1)-f(-1))/2`, `Delta'(f) := f'(-1) - (f(1)-f(-1))/2`;
for a parity-preserving f (K_c^{-1} preserves parity):
- even f in D(K_c)  <=>  f'(1) = 0,
- odd f in D(K_c)   <=>  f'(1) = f(1).

Throughout, "K_c^{-r}" on a polynomial means the formal transport inverse.

=======================================================================
1. STRICT — Transport-level reduction of membership (T-CHAIN)
=======================================================================
Lemma T.  For even s = 2r (r >= 1) and n >= 0:
  Q_n^{(2r)} in D(K_c^r)  <=>  K_c^{-m} P_n in D(K_c) for every m = 1..r.
For odd s = 2r+1 (r >= 1) and n >= 0:
  Q_n^{(2r+1)} in D(K_c^{r+1/2})  <=>  K_n in D(K_c^{1/2}) and
     K_c^{-m} K_n in D(K_c) for every m = 1..r.
In particular (r >= 2, i.e. s >= 4) the binding condition is the m = 1 condition
  (even) K_c^{-1} P_n in D(K_c),  (odd) K_c^{-1} K_n in D(K_c).

Proof. For even: `D(K_c^r) = { f : K_c^j f in D(K_c), j = 0..r-1 }` (functional
calculus powers of a positive self-adjoint operator, standard; cf. Littlejohn-Wellman
2002). With f = K_c^{-r}P_n (formal), `K_c^j f = K_c^{-(r-j)}P_n`, so f in D(K_c^r)
iff K_c^{-m}P_n in D(K_c) for m = 1..r. For odd: `D(K_c^{r+1/2}) = { f : K_c^j f in
D(K_c), j<r, and K_c^r f in D(K_c^{1/2}) }`; with f = K_c^{-r}K_n this is equivalent to
K_n in D(K_c^{1/2}) and K_c^{-m}K_n in D(K_c), m=1..r. Since K_n is a polynomial
(smooth), K_n in D(K_c^{1/2}) = H^1 always. qed

This reduces the task to deciding, for the base polynomials P_n / K_n, whether the
single transport `K_c^{-1}(base) in D(K_c)`.

=======================================================================
2. STRICT — Deficit positivity for Legendre (even case basis)
=======================================================================
For f := K_c^{-1}P_n, define the relevant deficit:
  D_n := Delta(f) = f'(1) - (f(1)-f(-1))/2.
Since P_n has parity n and K_c^{-1} preserves parity, f has parity n:
  - n = 2k even: D_{2k} = f_{2k}'(1);
  - n = 2k+1 odd: D_{2k+1} = f_{2k+1}'(1) - f_{2k+1}(1).
From the formal series, using the endpoint formula
  P_n^{(m)}(1) = (n+m)! / (2^m m! (n-m)!)   (0 <= m <= n),  P_n^{(m)}(1)=0 for m>n:

Lemma DE (even).  For n = 2k >= 2 (k >= 1):
  D_{2k} = c^{-1} sum_{j=0}^{k-1} c^{-j} A_{k,j},
  A_{k,j} = (2k+2j+1)! / (2^{2j+1} (2j+1)! (2k-2j-1)!)  >  0.
Hence D_{2k} > 0, so f_{2k} notin D(K_c).

Proof. f_{2k}'(1) = c^{-1} sum_{j>=0} c^{-j} P_{2k}^{(2j+1)}(1) = c^{-1} sum_{j=0}^{k-1}
c^{-j} A_{k,j}, where A_{k,j} uses m = 2j+1 <= 2k, i.e. j <= k-1. Every A_{k,j} > 0
(positive factorials); the j=0 term alone is (2k+1)!/(2 (2k-1)!) > 0. qed

Lemma DO (odd).  For n = 2k+1 >= 3 (k >= 1):
  D_{2k+1} = c^{-1} sum_{j=0}^{k-1} c^{-j} B_{k,j},
  B_{k,j} = [(2K+2j+2)(2K+2j+1)!/(2^{2j+1}(2j+1)!(2K-2j)!)]
            - [(2K+2j+1)!/(2^{2j}(2j)!(2K+1-2j)!)]
          = [ (2K+2j+1)!/(2^{2j}(2j)!(2K-2j)!) ] * [ 2K^2+3K-3j-2j^2 ] / [ (2j+1)(2K+1-2j) ]
          >  0   (for the coefficient bracket is > 0 for 0 <= j <= K-1; the j=K term is 0).
Hence D_{2k+1} > 0, so f_{2k+1} notin D(K_c).

Proof (positivity of the bracket).  The bracket numerator is
  N := (2K+2j+2)(2K+2j+1)... - ..., i.e. after factoring the common positive factor
  G := (2K+2j+1)!/(2^{2j}(2j)!(2K-2j)!):
  B_{k,j}/G = (K+j+1)/(2j+1) - 1/(2K+1-2j)
            = [ (K+j+1)(2K+1-2j) - (2j+1) ] / [ (2j+1)(2K+1-2j) ].
  The numerator (K+j+1)(2K+1-2j) - (2j+1) = 2K^2 + 3K - 3j - 2j^2, a strictly concave
  quadratic in j whose value on 0 <= j <= K-1 is minimized at j = K-1, where it equals
  4K+1 > 0. Hence B_{k,j} > 0 for j = 0..K-1. (At j=K the bracket is 0, which is why
  the sum stops at K-1.) qed

Thus for ALL n >= 2 (both parities), K_c^{-1}P_n notin D(K_c), and for n in {0,1}
it is in D(K_c) (constants and linear functions).

=======================================================================
3. STRICT — Deficit monotonicity (enables the odd (Krein-Sobolev) case)
=======================================================================
Let D_m be the Krein deficit of K_c^{-1}P_m (full deficit, as in section 2).

Lemma DM (strict monotonicity).  D_m is strictly increasing for m >= 1, and D_0 = D_1 = 0,
D_m > 0 for m >= 2.

Proof. Two termwise comparisons among the positive-sum formulas.
(A) D_{2K+1} > D_{2K}: for each j = 0..K-1,
  A_{K,j} = G * (K-j)/(2j+1),   B_{K,j} = G * [ (K+j+1)/(2j+1) - 1/(2K+1-2j) ],
  where G = (2K+2j+1)!/(2^{2j}(2j)!(2K-2j)!) > 0. Then
  B_{K,j} - A_{K,j} = G * [ (2j+1)/(2j+1) - 1/(2K+1-2j) ]
                    = G * [ 1 - 1/(2K+1-2j) ] > 0   (since 2K+1-2j >= 3 > 1 for j <= K-1).
  Hence termwise B_{K,j} > A_{K,j}, so D_{2K+1} > D_{2K}.
(B) D_{2K+2} > D_{2K+1}: D_{2K+2} = c^{-1} sum_{j=0}^{K} c^{-j} A_{K+1,j} has an extra
  positive term at j=K (A_{K+1,K} > 0), and for j = 0..K-1:
  A_{K+1,j}/G = (2K+2j+3)(2K+2j+2) / [ 2(2j+1)(2K+1-2j) ],
  B_{K,j}/G   = [2K^2+3K-3j-2j^2] / [ (2j+1)(2K+1-2j) ].
  The difference of numerators (over the common positive denominator):
  (2K+2j+3)(K+j+1) - (2K^2+3K-3j-2j^2) = 4Kj + 4j^2 + 2K + 8j + 3 > 0.
  Hence A_{K+1,j} > B_{K,j} termwise, and D_{2K+2} > D_{2K+1}.
Combining both gives strict increase. qed

Lemma A-POS. The Krein-Sobolev coefficients a_m (SL_hs doc recurrence
  a_0 = a_1 = a_2 = a_3 = 1,
  a_{m+2} = a_m (1 + (4m^2-1)/c) + (2m+1)/(2m-3) (a_m - a_{m-2}),  m >= 2)
are > 0 for all m, and each same-parity subsequence (a_2 < a_4 < a_6 < ... and
a_3 < a_5 < a_7 < ...) is strictly increasing.

Proof of a_m > 0. a_4 = 1 + 15/c > 0, a_5 = 1 + 35/c > 0 (and a_0..a_3 = 1 > 0).
Induct: if a_m > a_{m-2} >= 0, then
  a_{m+2} = a_m(1+(4m^2-1)/c) + ((2m+1)/(2m-3))(a_m - a_{m-2})
         > a_m >= 0
because 1+(4m^2-1)/c > 0 (c > 0) and the second term is > 0 (the factor
(2m+1)/(2m-3) > 0 for m >= 2 and a_m - a_{m-2} > 0). The same argument for
m-1 gives the odd subsequence. Hence a_m > 0 for all m and same-parity
strict increase holds.
REMARK (corrected per audit): the LITERAL claim "a_m strictly increasing for
m >= 2" is FALSE because a_2 = a_3 = 1 (not strictly increasing at m=2 -> 3).
Only a_m > 0 is used downstream (Lemma L-KS), so the correction is non-load-bearing.

Lemma L-KS (Krein-Sobolev transport deficit positivity).  For n >= 2,
  L_n := (Krein deficit of K_c^{-1}K_n) > 0,
so K_c^{-1}K_n notin D(K_c) for n >= 2. For n in {0,1}, K_c^{-1}K_n in D(K_c).

Proof. K_n = sum_{i=0}^{floor(n/2)} a_{n-2i} (P_{n-2i} - P_{n-2i-2}) (SL_hs doc,
S_m = P_m - P_{m-2}). Since the deficit is linear:
  L_n = sum_i a_{n-2i} (D_{n-2i} - D_{n-2i-2}),
where D_{-1} := 0, D_{-2} := 0 (and a_m > 0 by A-POS, D_m - D_{m-2} > 0 by DM for
the nonzero terms). Each summand is > 0 when the degree index n-2i >= 2; for n >= 2 at
least the i=0 term has index n >= 2 and D_n - D_{n-2} > 0 with a_n > 0, so L_n > 0. qed

=======================================================================
4. STRICT — Main membership theorem (packet Q1b)
=======================================================================
Theorem MO.  For integer s >= 4 and c > 0, under the operator-domain reading
H^s = H_op^s = D(K_c^{s/2}):
  (even) s = 2r, r >= 2:  Q_n^{(s)} = K_c^{-r}P_n  in H_op^s  <=>  n in {0,1};
  (odd)  s = 2r+1, r >= 2: Q_n^{(s)} = K_c^{-r}K_n  in H_op^s  <=>  n in {0,1}.
For n >= 2 the polynomial Q_n^{(s)} fails the Krein boundary condition at the m = 1
transport level: K_c^{-1}P_n notin D(K_c) (resp. K_c^{-1}K_n notin D(K_c)).

Proof. By Lemma T the r >= 2 membership requires the m = 1 condition
K_c^{-1}(base) in D(K_c). By Lemmas DE+DO (n >= 2 fails for P_n) and L-KS (n >= 2
fails for K_n), this condition fails for every n >= 2. For n = 0,1 the base is a
constant or linear function and K_c^{-1}(base) is a constant/linear function, which
satisfies the Krein condition at every level; direct check: K_c^{-1}(1) = 1/c,
K_c^{-1}(x) = x/c, both in D(K_c), and all iterates K_c^{-m} are constant/linear and
in D(K_c). Hence exactly n in {0,1}. qed

=======================================================================
5. STRICT — Which polynomials lie in the operator domain (packet Q1a)
=======================================================================
Proposition Q1a.  (i) For every integer s >= 1, H_op^s ∩ Pi contains 1 and x.
(ii) For s = 2r (even) or s = 2r+1 (odd) with r >= 1, H_op^s ∩ Pi = D(K_c^r) ∩ Pi
consists (up to parity) of 1, x, and polynomials whose degree spectrum is
{0,1} union {d : d >= 2r+2}; in particular no degree d in {2,3,...,2r+1} polynomial
lies in H_op^s ∩ Pi, and there exist polynomials of every degree >= 2r+2 (verified
exactly for r = 1,2,3 and c-independent; the general every-degree claim is
EVIDENCE-level).  (iii) In particular the upstream auxiliary claim
"H_op^s ∩ C[x] = span{1,x} for s >= 4" is REFUTED: e.g. for s = 4 (r = 2) the
degree-6 polynomial x^2(x^4 - 5x^2 + 7) lies in D(K_c^2) = H^4 (c = 3; any c > 0
with the rational coefficients in c), so H^4 ∩ Pi contains degree-6 polynomials.

Proof sketch. (i) 1, x are smooth, satisfy all Krein conditions. (ii) The degree
spectrum is obtained by solving the linear system of 2r Krein boundary conditions on
polynomial coefficients; exact-arithmetic solves for r = 1,2,3 and c in {1,3,10} give
spectrum {0,1} U {d >= 2r+2} (see reproducibility scripts). The "no degree in
2..2r+1" part follows because a polynomial of degree d in D(K_c^r) would require a
degree-d element in D(K_c)∩Pi (d >= 4) that survives r levels; the minimal surviving
degree is exactly 2r+2. (iii) explicit example verified by substitution. qed

Remarks. The statement (ii) general every-degree lemma is the only EVIDENCE-supported
ingredient and is NOT load-bearing for MO/SPD/ND. The key separation (Q_n notin H_op^s
for n >= 2) does not rely on it.

=======================================================================
6. STRICT — Operator domain vs abstract completion (packet Q2)
=======================================================================
Theorem SPD.  For integer s >= 4 and c > 0, the operator domain H_op^s = D(K_c^{s/2})
and the abstract completion H_abs^s (of all polynomials under (·,·)_s) are NOT equal
as Hilbert spaces. Precisely:
  - H_abs^s contains every polynomial, in particular Q_2^{(s)} (it lies in the dense
    subspace Pi of H_abs^s).
  - H_op^s does NOT contain Q_2^{(s)} (Theorem MO, n = 2 >= 2).
  Hence the natural identification is not an equality: under H_abs^s ≅ L^2 via
  K_c^{s/2} (with Q_n ↦ base_n), the abstract class of Q_2^{(s)} is an element of
  H_abs^s; under H_op^s ≅ L^2 via K_c^{s/2}, the element with the same L^2 image is
  the functional-calculus K_c^{-s/2}P_2 (resp. ...K_2), which is NOT the polynomial
  Q_2^{(s)} (since Q_2^{(s)} fails the Krein condition at level 1). The two Hilbert
  spaces therefore differ.

Proof. Both are isometric to L^2 (K_c^{s/2} is an isometric isomorphism H_op^s -> L^2
by functional calculus; on H_abs^s the polynomial map p ↦ K_c^{s/2}p extends to an
isometric isomorphism onto L^2 because Pi is dense in L^2 and K_c^{s/2}(Pi) = Pi).
The abstract element Q_2^{(s)} in H_abs^s has image P_2 (resp. K_2) in L^2. In H_op^s
the preimage of that L^2 element is K_c^{-s/2}(P_2), a concrete function in D(K_c^{s/2})
which is NOT the polynomial Q_2^{(s)} (Theorem MO: Q_2^{(s)} notin D(K_c^{s/2})). So
the element Q_2^{(s)} of H_abs^s is not realized as a concrete element of H_op^s; the
spaces are genuinely different. qed

Corollary EMB (refinement). For s = 2r (and analogously odd), Pi ∩ H_op^s is dense in
H_op^s, so H_op^s embeds isometrically as a PROPER dense subspace of H_abs^s.
Proof sketch. Via the transfer isometry K_c^r, density of Pi ∩ D(K_c^r) in D(K_c^r) is
equivalent to density of W_r := K_c^r(Pi ∩ D(K_c^r)) in L^2. W_r has degree spectrum
{0,1} U {>= 2r+2} and is triangular (one polynomial of each degree >= 2r+2), so it
spans span{x^d : d >= 2r+2}, which is dense in L^2 because: if f ⟂ x^d for all d >= 2r+2
then the measure x^{2r+2} f has vanishing moments, hence x^{2r+2} f ≡ 0 a.e., hence
f ≡ 0 a.e. (x^{2r+2} > 0 a.e.). This depends on the every-degree lemma (Q1a). The
difference claim SPD does not depend on this corollary.

=======================================================================
7. STRICT — Density of span{Q_n^{(s)}} in H_op^s (packet Q3)
=======================================================================
Theorem ND.  For integer s >= 4 and c > 0, under the operator-domain reading,
span{Q_n^{(s)}} is NOT dense in H_op^s = D(K_c^{s/2}). Indeed
  {Q_n^{(s)} : Q_n^{(s)} in H_op^s} = {Q_0^{(s)}, Q_1^{(s)}},
and closure_{H_op^s}(span{Q_0^{(s)}, Q_1^{(s)}}) = span{Q_0^{(s)}, Q_1^{(s)}}
= span{1, x} (a 2-dimensional proper closed subspace), while H_op^s is infinite
dimensional. Hence the left-definite density criterion via the SL_hs system does NOT
extend to s >= 4 under the operator-domain reading.

Proof. By Theorem MO, Q_n^{(s)} in H_op^s iff n in {0,1}; Q_0 = const/c^r and
Q_1 = x/c^r (scalar multiples of 1 and x). A finite-dimensional subspace of a Hilbert
space is closed, so its closure is itself, span{1,x}. H_op^s = D(K_c^{s/2}) contains
the eigenfunctions of K_c (a countable infinite orthonormal family), hence is
infinite-dimensional. Therefore span{1,x} is a proper closed subspace and cannot equal
H_op^s; the family is not dense. qed

=======================================================================
8. Resolution of the three packet items — summary
=======================================================================
Item 1. H_op^s = D(K_c^{s/2}): contains exactly the polynomials of degrees
{0,1} U {d >= 2 floor(s/2)+2} (structural, verified for r<=3 and c-independent), and
the SL_hs polynomials Q_n^{(s)} lie in H_op^s iff n in {0,1}; for n >= 2 they fail the
level-1 Krein transport condition (STRICT, Theorem MO).
Item 2. H_op^s and H_abs^s differ for s >= 4: H_abs^s contains all Q_n^{(s)} (it is
the correct ambient space for the SL_hs doc's completeness claim); H_op^s contains
none of Q_n^{(s)}, n >= 2. Mechanism: formal transport K_c^{-1} of the base polynomial
fails the Krein boundary condition at level 1 for n >= 2 (STRICT, Theorem SPD).
Item 3. span{Q_n^{(s)}} is NOT dense in H_op^s for s >= 4 (only {1,x} lie in the
operator domain); the left-definite density criterion does NOT extend to s >= 4 under
the operator-domain reading (STRICT, Theorem ND).

=======================================================================
9. Regression and consistency
=======================================================================
- s in {1,2,3} (r <= 1): operator domain = abstract completion (project SL_h1/h2/h3
  completeness). Consistent: the level-1 condition is the ONLY transport condition and
  the project's H^2/H^3 constructions respect it; Q_n^{(2)} = K_c^{-1}P_n for n>=2 is
  NOT claimed to be in H^2 in the same way (SL_h2 uses the sparse family {p_n}, all in
  D(K_c)); this run's scope is s >= 4.
- The left-def run L1'' (sparse family {p_n}, s >= 4: Q_sp = {1,x} and density fails)
  STANDS: p_n (n >= 4) not in D(K_c^r) (verified: K_c p_4 fails Krein condition). The
  left-def run's auxiliary claim S1d "H^s ∩ C[x] = span{1,x}" is REFUTED here (there
  are degree d >= 2r+2 polynomials in H_op^s). L1'' and S1d are logically independent:
  L1'' is about the specific sparse family, S1d (now refuted) was about ALL polynomials.
- No contradiction with the SL_hs doc: the doc's completeness holds in H_abs^s (the
  abstract completion), which is the natural reading in which the polynomial system is
  complete; this run clarifies that under H_op^s (operator domain) it is not.

=======================================================================
10. Open / evidence-limited items
=======================================================================
- OPEN (evidence-level, non-load-bearing): the exact general form of the basis of
  D(K_c^r) ∩ Pi for all r (the minimal-degree = 2r+2 and every-degree-present lemma is
  verified exactly for r = 1,2,3 and c in {1,3,10}; a general proof would close Q1a
  fully, but MO/SPD/ND are already strict).
- EVIDENCE (exact arithmetic, not proof): scripts under reproducibility/ confirm the
  degree spectra and the membership failures for n up to ~12 and the Krein-Sobolev
  deficit positivity for n up to 6.
- No claim is made about s = 1,2,3 in this run beyond consistency; they are governed
  by the project's existing complete results.
