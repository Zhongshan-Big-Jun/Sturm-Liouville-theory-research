# L11: measure coefficients, atoms, and concentration limits

Author proposal, 2026-09-23. Independent acceptance review is pending.

## Source identity and actual reading

J. Eckhardt and G. Teschl, *Sturm-Liouville operators with measure-valued coefficients*, Journal d'Analyse Mathématique 120 (2013), 151-224, [DOI](https://doi.org/10.1007/s11854-013-0018-x). Read the primary [arXiv:1105.3755v2 PDF](https://arxiv.org/pdf/1105.3755v2), revised 2013-08-12. It has **61 PDF pages**; the landing-page comment “58 pages” is not the downloaded page count. Below, page numbers mean PDF/printed preprint pages. The [author's index](https://www.mat.univie.ac.at/~gerald/ftp/) and DOI registration confirm journal metadata. The author PDF and TeX were also captured, but their whole contents were not read or assumed byte-identical to arXiv. Springer returned HTTP 200 with a browser-challenge page, not readable article text.

Read arXiv pp.3-7,9-11,24,27-28,32-33. Original rendered pp.4,5,11,32 were inspected for the measure labels, jump formulas, hypotheses and resolvent sign/measure. Coverage is selective; the complete extension classification and Appendix C were not audited. Capture/extraction is not reading. Identities and times are in `../source-manifest.json`.

## Source contract, in compressed form

Section 3 (p.4,(3.1)) uses measures varrho, varsigma, chi and quasi-derivative f^[1]=df/dvarsigma. Hypothesis 3.7 (p.11) requires positive varrho, real chi and varsigma, full support of varsigma, no common atoms of varsigma with the other measures, a uniqueness condition in support gaps, and more than one point in supp(varrho). Theorem 3.1 (pp.5-6,(3.2)-(3.4)) gives initial-value solvability; Proposition 3.2 gives the Lagrange identity. Theorem 3.6 (pp.9-10) concerns analyticity in the spectral parameter, not moving coefficients. Proposition 7.1 and Theorem 7.6 (pp.24,27) describe regular endpoint traces and self-adjoint boundary conditions. Theorem 8.3 (p.32,(8.5)-(8.6)) supplies the separated resolvent kernel; Corollary 8.4 (p.33) gives simplicity. Page 5 encodes delta-prime interactions by atoms of varsigma, producing value jumps, and delta interactions by atoms of chi, producing quasi-derivative jumps.

## Mapping to the project and to a genuine point mass

For the existing model use `dvarrho=rho(x)dx`, `dvarsigma=dx`, `dchi=0`. Then f^[1]=f' and tau f=-f''/rho. The finite positive densities satisfy Hypothesis 3.7: varrho has full support, gap uniqueness is vacuous, and atom exclusion is immediate. Finite interval masses give regular endpoints; Dirichlet traces select a separated self-adjoint realization.

For the distinct atomic benchmark use `dvarrho=c dx+M delta_a`, c>0, M>=0, a in (0,1), while keeping varsigma=dx and chi=0. This still has full support and satisfies the same atom condition because varsigma has no atoms. Integrating the equation, with the source's left-continuous convention, gives continuous u and

`u'(a+)-u'(a-)=-lambda M u(a)`.

Its norm is `c integral u^2 dx+M u(a)^2`. The lambda-dependent jump distinguishes a **weight atom** from a potential delta interaction. It is also distinct from the original finite density interface, where both u and u' are continuous.

The source resolvent acts by integration against dvarrho. For positive density the project pencil inverse `(A-z rho)^(-1)` acts against dx; their scalar kernels agree only after making the right-hand-side conversion explicit. A reduced kernel at an eigenvalue also needs its normalized pole removed. The finite continuous kernel for the original bounded positive density model is justified in round9 V3 and in the companion derivation; it is not asserted for every possible measure-coefficient realization in L11.

## Delta-prime: interaction versus distributional derivative

The paper's delta-prime interaction is not permission to set dvarrho=delta'_a. Its extra atom lies in varsigma and changes the value matching law. By contrast, `<delta'_a,phi>=-phi'(a)` is not bounded by the uniform norm of phi, and hence is not a finite Radon measure. Taking phi_e(x)=e psi((x-a)/e) with psi'(0) nonzero proves this directly: the uniform norm tends to zero while the derivative pairing stays nonzero.

A translated point mass has distributional derivatives

`(q delta_(a(t)))dot=-q a'(t) delta'_(a(t))`,

`(q delta_(a(t)))ddot=q a'(t)^2 delta''_(a(t))-q a''(t) delta'_(a(t))`.

A moving finite density step instead has a delta first derivative and delta-prime second derivative. Neither distributional differentiation operation is a statement that the resulting derivatives are admissible positive coefficient measures in L11. Translation is not even continuous in total variation for nonzero point masses.

## Concentration: exact topology and limits

For a fixed continuous kernel K on [0,1]^2, signed measures mu_e with uniformly bounded total variation, shrinking support at a and signed mass converging to q satisfy

`double integral K(x,y) dmu_e(x)dmu_e(y) -> q^2 K(a,a)`.

This is our elementary estimate: subtract K(a,a) inside the integral, bound by its modulus of continuity times ||mu_e||_TV², then use mass convergence. Several disjoint shrinking clusters give the corresponding finite double sum when every cluster mass converges. TV bounds alone do not suffice: alternating masses 1 and 2 already destroy the one-cluster limit. The argument also handles signed mass tending to zero, without replacing it by absolute mass.

For the layer `rho_e=1+M/(2e) 1_(|x-a|<e)`, fixed M>0, the measures converge weak-* on C([0,1]) to `dx+M delta_a`, but the TV distance of the extra layer to the atom is 2M. The L-infinity densities are unbounded as e tends to zero. For a **fixed base density**, this topology controls the continuous reduced-Green quadratic form of a direction; it alone gives no convergence of a changing resolvent, its differentiated kernel, second shape derivatives, or global Hessian signs.

The companion [calibration](../derivations/calibrations.md) proves the layer-to-atom transfer limit on bounded spectral sets for this particular model, and separately derives local atomic-mass derivatives at M=0. Those extra conclusions use explicit matrix analysis. They are not attributed to an unstated weak-convergence theorem in L11. At M=0 the physical positive-measure path is one-sided; the algebraic secular function has a larger analytic extension, which does not create two-sided positive-measure admissibility.

Open applicability gaps: a common-Hilbert-space differentiable realization for arbitrary moving measures; uniform control of kernel derivatives under concentration; interface collisions and variable block values; the L10 fixed-operator bridge. No G1' or uniqueness conclusion is proposed.
