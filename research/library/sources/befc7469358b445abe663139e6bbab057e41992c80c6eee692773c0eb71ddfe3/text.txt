# L05: symmetry and normalized restriction

Fischbacher, Stanfill. Journal of Differential Equations 427 (2025), 560-600, DOI [10.1016/j.jde.2025.01.088](https://doi.org/10.1016/j.jde.2025.01.088). Publisher metadata identifies the journal article. Read [arXiv:2410.04647v2](https://arxiv.org/abs/2410.04647v2), revised 2025-02-11, 36 pages. Direct publisher access returned HTTP403; the journal body's identity with v2 was not established.

**Verified source input.** Hypotheses 2.1/4.1 require positive measurable p,r, local integrability of 1/p,q,r with real q, finite endpoints, limit-circle nonoscillatory endpoints, and midpoint-symmetric coefficients. Proposition 4.2 and Theorems 4.3/4.4/4.7 concern reflection-invariant self-adjoint domains. The parity reductions have Dirichlet/Neumann midpoint conditions; equations (4.11)-(4.12) include sqrt(2) normalization. Nonnegative-extension assertions add positivity hypotheses on the minimal operator.

**Project map.** Here p=r=1, q=c, I=(-1,1). Regular endpoints satisfy the required endpoint class. The ordinary coupled boundary matrix is [[1,2],[0,1]], and direct calculation verifies domain reflection invariance. Proof 01 establishes both domain inclusions and U K_c U^{-1}=A_NN,c direct-sum A_DR,c, then transfers all Borel functional calculus with its domains. No angle parameters in generalized boundary coordinates need be guessed.

**Unmatched assumptions / terminology.** K_c is K_0+cI with K_0 the original Krein realization. It is not automatically the Krein extension of the newly shifted minimal differential operator; that different extension would have different zero-energy solutions. Our derivation uses the actual fixed boundary conditions.

**Allowed / forbidden.** Reuse the symmetry principle and normalized parity map. Symmetric coefficients alone do not make every chosen domain reflection invariant. The decomposition alone proves neither fractional Sobolev descriptions nor deletion closure.

**Reading depth.** Hypothesis 2.1 p.4; Section 4, pp.20-26, including Theorem 4.4's domain reduction proof. Two-interval theorems and nonnegative-extension ordering were seen for context but are not proof inputs. Project: actual `SL_fractional_left_definite.tex`, Section 2.2; proof 01. Status: SOURCE_READ_SCOPED; adaptation pending independent review.
