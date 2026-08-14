# Status and Literature

Run: R-20260814T070000Z-densbc-3F8A2C

## Current status
RIGOROUS_PARTIAL_RESULT. See one-line at top of file / final report.

Key deliverable: CORRECTED diagonal classification (Theorem E) and corrected
"constraints restore density" mechanism (Theorem D).  The packet's central
claim (constraints always restore density) is FALSIFIED in the coordinate/
diagonal setting; the mechanism is correct in the non-coordinate (structural,
e.g. left-definite) setting.

## Novelty audit
As of this run no published necessary-and-sufficient criterion for polynomial
density in a closed (boundary-constrained) subspace of a general Hilbert space
is known.  The classical literature addresses density in the WHOLE space:

Known (verified, with stable links and locators):
1. C. Berg, J.P.R. Christensen, "Density questions in the classical theory of
   moments", Ann. Inst. Fourier 31(3) (1981) 99-114.
   DOI 10.5802/aif.840 ; Zbl 0437.42007 ; MR 84i:44006.
   URL https://aif.centre-mersenne.org/articles/10.5802/aif.840/
   Verdict: distinguishes density in whole L^p(R,mu).  Naimark L^1
   (N-extremal/extreme point of V^mu), M.Riesz L^2 (N-extremal), determinate=>
   dense for 1<=p<=2, NOT for p>2 (Thm 7: remove an atom determinacy can be
   kept while p>2 density fails).  NO closed-subspace / boundary-constraint
   theorem. [deep-read: tmp_ai4math/densbc_lit/berg_christensen_DEEPREAD.md]

2. H. Dette, A. Zhigljavsky, "Reproducing kernel Hilbert spaces, polynomials
   and the classical moment problems", arXiv:2101.11968v5 (2021).
   URL https://arxiv.org/abs/2101.11968 ; ar5iv https://ar5iv.labs.arxiv.org/html/2101.11968
   Verdict: OPPOSITE direction -- for a DETERMINATE measure, constants and
   exact-degree polynomials do NOT lie in the RKHS H(K) (Thm 1.1, 1.2);
   const in H(K) iff spectral measure has positive mass at 0 (Cor 1.1(a)).
   NO constrained-subspace density criterion. [deep-read: .../arxiv_2101_11968_DEEPREAD.md]

3. C. Berg, M. Thill, "Rotation invariant moment problems",
   Acta Math. 167 (1991) 207-227.  Zbl 0744.44006. DOI 10.1007/BF02392450.
   URL https://zbmath.org/?q=an%3A0744.44006
   (NOTE: the packet's "Math. Ann. 1992" is INCORRECT; correct venue Acta Math. 167 (1991).)
   Verdict (from zbMATH review by D. Leviatan; full text paywalled - Project
   Euclid bot-block, sci-hub CAPTCHA, Unpaywall is_oa=false): among
   rotation-invariant determinate mu on R^d (d>1), polys not dense in L^2(mu)
   iff mu is spherical-atomic Sum alpha_n omega_{r_n}.  NO constrained-subspace
   result. [deep-read: .../berg_thill_DEEPREAD.md]

4. J.M. Rodriguez, "Approximation by polynomials and smooth functions in
   Sobolev spaces with respect to measures", J. Approx. Theory 120 (2003)
   185-216.  DOI 10.1016/S0021-9045(02)00019-9 ; Zbl 1014.41007 ; MR 1959864.
   URL https://doi.org/10.1016/S0021-9045(02)00019-9
   NOTE: the packet's lead DOI 10.1006/jath.2002.3709 is a DIFFERENT paper
   ("Weighted Sobolev Spaces on Curves", JAT 119 (2002) 41-85); the correct
   paper matching the stated topic is the one above.
   Verdict: Thm 4.1 gives an iff "P dense in W^{k,p}(Delta,mu) iff P dense in
   L^p(Delta,mu_k)" under a coercivity hypothesis, plus sufficient density
   results (C_c^infty dense etc.).  All for the WHOLE space; NO boundary-
   vanishing / constrained closed-subspace result.
   [deep-read: tmp_ai4math/densbc_lit/jat2002_shobolev_density_DEEPREAD.md]

## Reduced open core (unresolved)
- O1 general (non-diagonal) H: exact low-moment-survival criterion under
  constraints (moment representability; analogue of project O2).
- O2 general constraint-functional expansion killing free params in all beta.
- O3 fractional left-definite window (inherited).

## Citation integrity
- Every claimed external result above carries a stable URL + locator.
- Where body text was NOT read (Berg-Thill), the level is labeled and no
  content is quoted from memory.
- No fabricated citations.
