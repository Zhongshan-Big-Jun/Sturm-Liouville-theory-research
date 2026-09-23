# Primary-source reading and adaptation boundary

This is an author reading record, not an independent audit. Raw papers and extracted texts remain private. Exact bytes, retrieval outcomes, pages actually read, original-page inspection and local source identities are recorded in source-manifest.json. Only the following bounded inputs are imported; no paper is described as read cover to cover.

| ID | Obtained primary text and version | Actually used locators | Allowed role |
|---|---|---|---|
| L07 | Erdelyi--Johnson, author-hosted bill.pdf, 26 pages, undated author version linked as item [64] on Erdelyi's publication list | PDF p.3, Theorem 1.3 and norm/lower-density definitions; p.4, Theorem 2.2; pp.10-11, Theorems 3.1-3.3 and 3.6; pp.14-15, p>=1 sufficiency argument; p.20, final proof paragraph of 3.6 | Exact monomial comparison theorem; not a theorem for the project difference family |
| L08 | Shen, author-hosted LegendreG.pdf, 16 pages, journal header SIAM J. Sci. Comput. 15(6) (1994), 1489-1505 | PDF pp.3-4 / printed 1491-1492, (2.1)-(2.8), Lemma 2.1; pp.7-8 / 1495-1496, (3.1)-(3.7), Lemma 3.1; pp.11-12 / 1499-1500, §4.1; p.12/13 transition / 1500-1501, coefficient/quadrature limitations | Finite Legendre recombinations and their exact sparsity; actual Krein extension separately proved |
| L09 | Adcock--Huybrechs, arXiv:1612.04464v4, revision 2018-11-05, 32 pages; journal publication SIAM Review 61(3) (2019), 443-473 | PDF p.10, (2.11)-(2.14); pp.18-20, §5.2, (5.1)-(5.6), Theorem 5.3 and proof; pp.20-21, first coefficient-bound proof of 5.4; p.22, Theorem 5.5 and proof | Finite TSVD inequality with the correct Gram threshold; global frame consequences remain separately conditional |

Author versions are not asserted byte-identical to the publisher editions. In particular, author-PDF pagination for L07 and L09 is not journal pagination. DOI landing pages fetched directly were blocked/challenge bodies; those bodies are retained with their actual status. Browser-indexed primary metadata was accessible, but no publisher subscription full text was obtained. The legal full texts used are the author's own institutional pages and arXiv.

## L07: hypotheses preserved

The exact formula is (D5) in note 04. It is unweighted Lebesgue Lp(A), for finite positive p; A must have positive lower density at zero, defined by liminf_(y->0+) m(A intersect [0,y])/y>0. The exponents are distinct, real and strictly above -1/p; no monotonicity or tending-to-infinity assumption is imposed. The convergent-sum branch provides analytic representatives on the slit disk up to the essential upper endpoint of A. The original PDF has **sum < infinity** for that branch. A browser extraction of the publisher abstract displayed the opposite comparison and malformed r_A; it is not used for this mathematical claim. This is an extraction discrepancy, not a verified publisher erratum.

For A=[0,1] the geometry assumption is automatic. At p=2 the source theorem applies to the deduplicated exponent sets (D6), all above -1/2. The power-weight conjugation in (D3)-(D4) is our explicit isometry, not an undocumented weighted variant of L07. Arbitrary complex exponents, Sobolev norms and project row-coefficient constraints are outside the theorem used. Only the bounded theorem statements and selected proof portions above were read; the quasi-Banach proof chain was not audited in full.

## L08: what is sparse, and what is assumed

For homogeneous Dirichlet second-order problems, Lemma 2.1 uses (P_k-P_(k+2))/sqrt(4k+6). Its derivative Gram is the identity; its mass entries have offsets 0,±2. For clamped fourth-order problems, Lemma 3.1 uses

$$
d_k\left(P_k-\frac{2(2k+5)}{2k+7}P_{k+2}+\frac{2k+3}{2k+7}P_{k+4}\right),
\qquad d_k=[2(2k+3)^2(2k+5)]^{-1/2}.
$$

Its second-derivative Gram is the identity; mass and first-derivative offsets are 0,±2,±4 and 0,±2 respectively. The approximation hypotheses printed with (2.3) are alpha>=0, Sobolev regularity s>=1; (3.3) uses alpha,beta>0, s>=2 and clamped membership. These source estimates concern the stated local-boundary PDEs. They are not Riesz bounds for the project norm.

The adaptation in note 03 uses the clamped core plus explicit lifts. Source §4.1 instead discusses separated Robin data and a three-term ansatz. Its endpoint coefficient system must be nonsingular before uniqueness is invoked. Also, its printed (4.1) omits a generic Robin boundary term: integrating alpha u-u''=f gives alpha(u,v)+(u',v')-[u' conjugate(v)]_-1^1=(f,v). Thus a Robin or coupled Krein form must be rederived. For the Krein domain this boundary contribution is -Delta u conjugate(Delta v)/2. The source's Neumann special case has zero boundary term. The positive, constant-c operator and graph norm in our construction are checked directly. No exponential convergence is deduced merely from the word 'smooth'.

## L09: cutoff identity and finite/global separation

The article's sigma_n in §5.2 denotes singular values of G_N, not of T_N. Since its Gram matrix is positive definite, those values are its eigenvalues. Equation (5.2) retains sigma_n>epsilon and sets equality to zero. Hence ||T_Nv_n||=sqrt(sigma_n), explaining the sqrt(epsilon) penalty. Theorem 5.3 and its finite proof were checked against the original page; (5.6) additionally invokes an infinite frame lower bound A. Note 02 gives a self-contained finite theorem for arbitrary finite synthesis maps, allowing zero eigenvalues, and separates synthesis cutoffs, Gram cutoffs and moment-data noise. It does not transfer the article's global frame premise to the project's original sparse family.

Primary links: [L07 author](https://people.tamu.edu/~terdelyi/papers-online/bill.pdf), [author publication list](https://people.tamu.edu/~terdelyi/papers-online/list.html), [L07 publisher identity](https://doi.org/10.1007/BF02788108); [L08 author](https://www.math.purdue.edu/~shen7/pub/LegendreG.pdf), [L08 publisher identity](https://doi.org/10.1137/0915089); [L09 arXiv v4](https://arxiv.org/abs/1612.04464v4), [L09 publisher identity](https://doi.org/10.1137/17M1114697).

## Current project inputs actually consulted

The root AGENTS and both supplied attachments were read. Mathematical source reading concentrated on docs/SL_cofinite_left_definite.tex (operator isomorphism/norm, exact family and q rows, central traces, cutoff and cofinite proof), docs/SL_fractional_left_definite.tex (genuine square domain, four-trace polynomial core, full-family window/member threshold), docs/SL_h2_completeness_proof.tex (§§1-2.3), and the moment/cofinite tool cards. These were frozen privately before authoring. The old memory entry with only s<=3 established is superseded by the current source's 0<=s<7/2 theorem. No old evidence, canonical records or project programs were changed or executed.
