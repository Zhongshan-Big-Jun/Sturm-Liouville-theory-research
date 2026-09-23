# L04: boundary quotient and finite rank

Fleeman, Frymark, Liaw. Journal of Approximation Theory 239 (2019), 1-28, DOI [10.1016/j.jat.2018.10.005](https://doi.org/10.1016/j.jat.2018.10.005). Publisher search metadata and arXiv journal metadata agree. Read [arXiv:1706.01539v1](https://arxiv.org/abs/1706.01539v1), submitted 2017-06-05, 28 pages. Publisher direct access returned HTTP403; the 2019 body was not compared with v1.

**Verified usable statement.** Proposition 2.14: for maximal-domain vectors, a full-rank matrix of their boundary-form pairings implies linear independence modulo the minimal domain. The converse is not asserted. Theorem 3.2 adds a self-adjoint target with complete orthogonal eigenfunctions and an appropriate quotient basis containing selected eigenfunctions. GKN realization requires the correct deficiency count and isotropy, not rank alone.

**Project map.** For the regular expression c-D^2, maximal/minimal domains are H^2 and H^2_0, with deficiency (2,2); its fourth-order expression has deficiency (4,4). Proof 04 derives these counts and checks the Krein boundary subspace. The project's four-trace residual matrix of determinant 15360 is a right-inverse construction, not the paper's skew pairing matrix. The actual eigenfunctions are affine, cosine and sine modes; p_n are not substitutes.

**Unmatched/version issue.** The captured v1 p.15 prints deficiency (1,1) for its full-interval minimal Legendre setup; the both-limit-circle model has (2,2). This was visually confirmed and contrasted with L06 p.6. Whether the published revision corrects the examples remains unverified. No v1 Legendre dimension/example result is imported.

**Allowed / forbidden.** Reuse the general quotient-independence argument with separately verified dimensions and boundary form. It gives no unconditional sparse-family or constrained-subspace density criterion.

**Reading depth.** Targeted pp.4-20, especially Proposition 2.14 and proof, GKN hypotheses, Theorem 3.2 and proof, and Section 4's examples/limitations. This is not a whole-paper audit. Project: `tools/spectral-domain-checks.md`; proof 04; `scripts/exact_checks.py`. Status: GENERAL_INPUT_READ; SINGULAR_EXAMPLES_NOT_ADOPTED.
