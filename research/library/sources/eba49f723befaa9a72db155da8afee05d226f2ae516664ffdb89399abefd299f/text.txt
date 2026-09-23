# L01: abstract scales and realizations

Fischbacher, Gesztesy, Hagelstein, Littlejohn. Journal of Differential Equations 428 (2025), 422-482, DOI [10.1016/j.jde.2025.02.013](https://doi.org/10.1016/j.jde.2025.02.013). Publisher search metadata confirms the journal item. The original read was [arXiv:2408.01514v1](https://arxiv.org/abs/2408.01514v1), submitted 2024-08-02, 50 PDF pages; no later arXiv version was listed. The journal text was not acquired.

**Verified source input.** Hypothesis 2.1 assumes self-adjoint A>=I on a separable complex Hilbert space. Equations (2.2)-(2.4) define H_r(A)=D(A^{r/2}) with the power inner product. Theorem 2.4 identifies the self-adjoint realization in H_r as A restricted to D(A^{(r+2)/2}) and transports realizations unitarily across the scale. Equations (2.16)-(2.20) treat completed negative scales; Theorem 2.6 allows spectral multiplicity. General left-definite theory is credited there to earlier Littlejohn-Wellman work.

**Project map and unmatched conditions.** Take A=K_c/c: its lower bound is one, its domains equal those of K_c, and its r-norm is c^{-r/2} times the project norm. The eigenvalue c has multiplicity two, so a single simple-spectrum multiplication model is insufficient; retain both affine modes or use the direct-sum model. No unmatched condition remains for these abstract statements after rescaling. Constants need not be uniform as c decreases to zero.

**Allowed / forbidden.** Use spectral transfer, graph-norm equivalence, H_c^{r+2} as realization domain, and completion at negative orders. None proves density of the separately prescribed p_n, or identifies algebraic polynomial inverses with genuine operator inverses. Those require the current project arguments.

**Reading depth / pointers.** Targeted reading of Section 2, PDF pp.10-14, including proof of Theorem 2.4 and Theorem 2.6. Fractional Hermite examples were captured but not read. Project: `docs/SL_fractional_left_definite.tex`, Section 2; adaptation: proof 01, P3. Exact bytes and access times are in `source-manifest.json`. Status: SOURCE_READ_SCOPED; project adaptation pending independent review.
