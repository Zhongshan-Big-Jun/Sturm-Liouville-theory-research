# Candidate Proof: O1' on stable banded-shift Hilbert spaces H_shift(m,lambda)

Run: R-20260823T000000Z-o1p-baseline
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT
This-run status: RIGOROUS_PARTIAL_RESULT
  (A new STRICT finite-rank decision criterion for the stable banded-shift
   family H_shift(m,lambda) with finite polynomial representers.  This widens
   the closed H_lambda family to bandwidth m >= 1 and gives a concrete
   bandwidth-2 non-dense example.  General O1' remains open.)

All statements below are STRICT unless explicitly labeled HEURISTIC/EVIDENCE.
No numerical evidence is used as a proof.

============================================================================
0. Setting and notation
============================================================================
Let m >= 1 and lambda = (lambda_1,...,lambda_m) in R^m.  Let e_0,e_1,...
be the standard orthonormal basis of the real Hilbert space l^2(N_0).
Define the monomials

    x^k = e_k + sum_{s=1}^m lambda_s e_{k+s},   k >= 0.

Let H = H_shift(m,lambda) be l^2(N_0) with this monomial set; the Hilbert
inner product is the standard l^2 inner product.

Standing stability assumption (S):
    L(z) = 1 + sum_{s=1}^m lambda_s z^s   has no zeros in the closed unit
    disk |z| <= 1.

Define the moment map J: l^2(N_0) -> l^2(N_0) by

    (Jw)_k = M_k(w) = <w, x^k>_H = w_k + sum_{s=1}^m lambda_s w_{k+s}.

For a finite-degree polynomial representer

    v = sum_{i=0}^d c_i x^i,   c_i in R,

we write a_k = <v,x^k>_H = sum_{i=0}^d c_i <x^i,x^k>_H.

Lemma 0.1 (H_shift is admissible).  Under (S), Pi = span{x^k : k >= 0} is
dense in H, the moments M_k(w) are well defined, and J is a bounded linear
isomorphism of l^2(N_0).  Consequently a sequence M = (M_k) is the moment
sequence of some w in H iff M in l^2.

Proof.  Since x^k = e_k + finite lower/upper shifts, the linear operator
A: l^2 -> l^2, A e_k = x^k, is bounded and A^* = J.  The closure of
Pi = range A equals (ker A^*)^{\perp} = (ker J)^{\perp}.  We show J is
invertible.  Let 1/L(z) = sum_{j>=0} c_j z^j; because L has no zeros in the
closed unit disk, 1/L is analytic in an open disk containing it, hence
|c_j| <= C r^j for some C and r<1.  Define C: l^2 -> l^2 by
(Cw)_k = sum_{j>=0} c_j w_{k+j}.  This is bounded.  The convolution identity
L(z)(1/L(z))=1 gives, for every k>=0,

    (C J w)_k = sum_{j>=0} c_j ( w_{k+j} + sum_{s=1}^m lambda_s w_{k+j+s} )
              = sum_{t>=0} ( c_t + sum_{s=1}^m lambda_s c_{t-s} ) w_{k+t}
              = w_k,

where c_t = 0 for t<0.  The same identity gives J C = I on the cyclic
basis, hence J is invertible with bounded inverse C.  Thus ker J = {0} and
Pi is dense; also M_k(w) = (Jw)_k is continuous in w.  qed

============================================================================
1. Kept set for finite polynomial representers
============================================================================
For j=1..r let v_j = sum_{i=0}^{d_j} c_i^{(j)} x^i, with d_j < infinity.
Let D = max_j d_j.  The Gram matrix is

    G_{i,k} = <x^i, x^k>_H.

Because x^i has support concentrated in {i,...,i+m}, G is banded:
G_{i,k} = 0 whenever |i-k| > m.

Theorem 1.1 (cofinite kept set).  For every n > D + m + 2, p_n in V; that is,
n in N.  In particular only finitely many n fail to be kept, and on each
parity the tail above D+m+2 is one infinite run.

Proof.  For n >= 4 the sparse element p_n has support {n, n-2}.  For
i <= D and n > D+m+2 we have n > D+m and n-2 > D+m, hence
G_{i,n} = G_{i,n-2} = 0 for every i <= D.  Therefore

    <v_j,p_n>_H = sum_{i=0}^{d_j} c_i^{(j)} ( G_{i,n}
                    - R_n G_{i,n-2} ) = 0,

where R_n = floor(n/2)/(floor(n/2)-1) is the sparse-family ratio.  The
finitely many n <= D+m+2 are checked separately.  qed

Thus the run graph has only finitely many finite components and at most one
infinite run on each parity.  Let B be the finite? careful: B may be finite?
Because N cofinite, the free bases outside the tail? Actually on each parity
there is exactly one infinite run above the tail, and its free base is a finite
degree (the least vertex of that run). Thus B may be finite too? Wait there is
an infinite run per parity with a finite base; plus finite runs below. So B is
finite (all free bases are finite degrees). Yes because every run that extends
to infinity has finite least vertex below or at threshold; every finite run is
below tail. So B is finite. Good (unlike general H). Thus B_fin is finite and
B_inf finite? B includes infinite-run bases too (which are finite degrees). We
will define B_fin = free bases whose run is finite; B_inf = free bases whose
run is infinite (also finite cardinality at most 2). The finite-rank theorem
restricts to B_fin.

Definition (run weights).  For b in B, let R_b be the run.  Define
rho_b(b)=1 and, for b>=2, rho_b(k) = floor(k/2)/floor(b/2) for k in R_b;
for b in {0,1}, R_b={b} and rho_b(b)=1.  Let m_b be the moment vector
supported on R_b with values rho_b(k).

============================================================================
2. The exact obstruction criterion
============================================================================
Theorem 2.1 (main theorem).  Let r >= 0, let v_1,...,v_r be finite-degree
polynomial representers, and let V = { w in H : <w,v_j>_H = 0 for all j }.
Define the r x |B_fin| matrix T by

    T_{j,b} = sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b},   b in B_fin.

Then

    closure(span Q_sp) = V
        <=>
    ker(T|_{B_fin}) = {0}.

Equivalently, density fails iff there is a nonzero vector
t = (t_b)_{b in B_fin} with T t = 0; such a t produces a nonzero
w in V cap Q_sp^perp.

Proof.  By the upstream master criterion (Theorem A), density holds iff
V cap Q_sp^perp = {0}.  We identify this space.

Let w in V cap Q_sp^perp.  For every n in N, <w,p_n>_H = 0.  Expanding p_n
in monomials, the kept sparse recursions imply the run lemma (same algebra as
R-20260816T000000Z Theorem 3, which is pure linearity of moments):

    M_k(w) = sum_{b in B} t_b rho_b(k) 1_{k in R_b},   t_b = M_b(w).

Because w in H, M(w) = Jw is in l^2 (Lemma 0.1).  For an infinite run R_b,
the vector m_b grows linearly along that parity (rho_b(b+2a) ~ a); hence
m_b notin l^2.  Since the infinite runs are at most one on each parity and
their supports are disjoint, the sum representation forces t_b = 0 for every
b in B_inf.  Thus the nonzero part of the obstruction is supported on B_fin.

Membership in V is

    0 = <w,v_j>_H = sum_{i=0}^{d_j} c_i^{(j)} M_i(w)
      = sum_{b in B_fin} t_b ( sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b} )
      = (T|_{B_fin} t)_j.

Hence every obstruction gives a vector t in ker(T|_{B_fin}).

Conversely, let t in ker(T|_{B_fin}).  Define a moment sequence
M = sum_{b in B_fin} t_b m_b.  This is finitely supported: all finite runs
are finite and lie below the infinite tails.  Hence M in l^2.  By Lemma 0.1
there exists a unique w in H with Jw = M, i.e. M_k(w) = M_k for all k.
The same recursive algebra gives <w,p_n>_H = 0 for every n in N: for kept
edges inside finite runs the ratios rho_b satisfy the sparse recursion; for
kept elements in the infinite tails both endpoints have M=0 because M is
finitely supported below the tails; and n=0,1 are handled by the free-base
pinning.  Also

    <w,v_j>_H = sum_i c_i^{(j)} M_i(w) = (T|_{B_fin} t)_j = 0,

so w in V.  Thus w in V cap Q_sp^perp.

The correspondence w <-> t is injective: if two parameter vectors give the
same w, their difference has all moments zero; by density of Pi (H1) the
difference is zero, and then each t_b, being a single moment M_b(w), is
determined.  Therefore V cap Q_sp^perp is isomorphic to ker(T|_{B_fin}), and
the criterion follows.  qed

Remark 2.2 (finite linear algebra).  In the treated family O1' is decidable:
compute N for finitely many n <= D+m+2, build the finite run graph and B_fin,
form the finite matrix T, and test whether its kernel is zero.

============================================================================
2b. Abstract band-invertible structure theorem
============================================================================
The proof of Theorem 2.1 did not use the Toeplitz form of J: it used only
that J is a bounded invertible moment map and that the Gram matrix is banded.
This suggests the following cleaner structure theorem.

Theorem 2.3 (abstract band-invertible structure theorem).  Let H be a real
Hilbert space with orthonormal basis (e_k)_{k>=0} and monomials
x^k = A e_k, where A: l^2 -> H is a bounded invertible operator.  Suppose the
Gram matrix G_{i,k} = <x^i, x^k>_H is banded with bandwidth m:
G_{i,k} = 0 whenever |i-k| > m.  For finite-degree polynomial representers
v_j = sum_i c_i^{(j)} x^i, define N, the run graph, B_fin, and T exactly as
above.  Then

    closure(span Q_sp) = V
        <=>
    ker(T|_{B_fin}) = {0}.

Proof.  Let J = A^*, so (Jw)_k = <w, x^k>_H and J is bounded invertible.
Therefore Pi = range A is dense in H (ker A^* = {0}), and a moment sequence
M is realizable by some w in H iff M in l^2.

Bandedness of G gives, for v_j of degree d_j, a^{(j)}_n = <v_j,x^n>_H = 0
when n > d_j + m; hence N is cofinite with the same threshold computation
(Theorem 1.1), and B_fin is finite.

Now repeat the proof of Theorem 2.1 verbatim:
- For w in V cap Q_sp^perp, the run lemma gives
  M(w) = sum_{b in B} t_b m_b.
- Since M(w) = Jw in l^2, every t_b for an infinite run must vanish; the
  infinite runs are disjoint and at most one per parity.
- Membership in V gives T|_{B_fin} t = 0.
- Conversely, t in ker(T|_{B_fin}) gives a finitely supported M in l^2, and
  w = J^{-1} M is in H with the required moments and orthogonality.
- The correspondence is injective by density of Pi.

Thus the abstract theorem holds.  qed

Remark 2.4.  The stable banded-shift family H_shift(m,lambda) is one concrete
instance of Theorem 2.3: take A = I + sum_{s=1}^m lambda_s S^s, where S is the
forward shift.  Then A is bounded and, under (S), has a bounded inverse whose
adjoint is J; the Gram matrix is banded with bandwidth m.  This shows exactly
where the H_beta/H_lambda criteria extend: the moment map must be a bounded
invertible "realizability oracle" onto l^2, not merely banded.

============================================================================
3. Regression and relationship to prior closures
============================================================================
Theorem 3.1 (m=1 regression).  For m=1, H_shift(1,lambda) is exactly the
H_lambda space of R-20260816T220000Z, and Theorem 2.1 is exactly the criterion
Theorem 2 of that run: density <=> ker(T|_{B_fin}) = {0}.

Proof.  The definitions coincide: x^k = e_k + lambda e_{k+1}, the moment map
J = I + lambda B is the same, and finite-degree polynomial representers are the
same class.  The criterion statement is identical.  qed

Theorem 3.2 (lambda=0 regression).  For lambda = 0, H_shift(m,0) is the
diagonal H_0 = l^2 with monomials x^k = e_k.  For finite polynomial
representers, Theorem 2.1 reduces to the H_beta, beta=0, finite polynomial
criterion of R-20260816T210000Z: density <=> ker(T|_{B_adm}) = {0}, where
B_adm = B_fin because every finite run is admissible in H_0.

Proof.  For lambda=0, J=I, so every finite-support moment sequence is
realizable; infinite runs are inadmissible exactly as in the H_beta analysis
when beta=0 (the moment vectors are not l^2).  Thus the criterion is the
finite-run restriction.  qed

============================================================================
4. Concrete bandwidth-2 example: v_1 = x^4 is never dense
============================================================================
Let m = 2, lambda = (lambda_1, lambda_2) satisfying (S), and let

    v_1 = x^4,   V = ker <w,v_1> = { w : M_4(w) = 0 }.

Theorem 4.1.  For every lambda satisfying (S), closure(span Q_sp) != V.

Proof.  For the Gram matrix in this family,

    a_2 = <v_1,x^2>_H = G_{4,2} = lambda_2,
    a_4 = <v_1,x^4>_H = G_{4,4} = 1 + lambda_1^2 + lambda_2^2,
    a_n = 0 for n > 6.

Hence

    <v_1,p_4>_H = a_4 - 2 a_2
                = 1 + lambda_1^2 + lambda_2^2 - 2 lambda_2
                = lambda_1^2 + (lambda_2 - 1)^2.

Under (S), L(z) = 1 + lambda_1 z + lambda_2 z^2 has no zeros in |z| <= 1.
If lambda_1 = 0 and lambda_2 = 1, then L(z) = 1 + z^2 has zeros at z = +-i on
the unit circle, contradicting (S).  Therefore the displayed expression is
strictly positive, so 4 not in N.

Now consider the moment sequence M = delta_2, i.e. M_2 = 1 and M_k = 0 for
all k != 2.  It is finitely supported, hence in l^2; by Lemma 0.1 there is a
nonzero w in H with M_k(w) = M_k for all k.

- Since M_4(w) = 0, w in V.
- Since 0 and 1 are in N (a_0=a_1=0), M_0(w)=M_1(w)=0, so w is orthogonal
  to p_0 and p_1.
- For every kept n >= 4: p_n has support {n,n-2}.  If n = 4, then 4 is not
  in N, so no requirement.  For every n >= 5 with n in N, neither n nor
  n-2 equals 2; hence M_n(w) = M_{n-2}(w) = 0, so <w,p_n>=0.  Thus
  <w,p_n>=0 for all kept n.

Therefore w in V cap Q_sp^perp and w != 0.  By Theorem A, Q_sp is not dense
in V.  qed

Remark 4.2.  This is a genuinely non-diagonal bandwidth-2 obstruction.  For
lambda_2 != 0 the Gram matrix has nonzero second-off-diagonal entries; for
lambda_2 = 0, lambda_1 != 0 it has nonzero first-off-diagonal entries.  In
either case H is not a coordinate-diagonal H_beta space.

============================================================================
5. What remains open
============================================================================
The new theorem closes O1' on the stable banded-shift family with finite
polynomial representers, for every bandwidth m >= 1.  It does not close O1' for:

- general non-diagonal H where the moment map is not a bounded invertible
  Toeplitz/banded shift (e.g. weighted L^2, non-cyclic moment problems);
- banded Gram matrices without a bounded invertible moment map and without
  the explicit l^2 realizability characterization;
- infinite-degree or non-polynomial representers;
- the full O1' moment-problem core: for arbitrary H, deciding free-base
  realizability + membership is still open.

General O1' remains RIGOROUS_PARTIAL_RESULT.
