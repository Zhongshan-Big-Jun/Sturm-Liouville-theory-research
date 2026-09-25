# Frozen cofinite packet: independent analytic review

Packet SHA-256: `378992ac556e3daba6664dd14c637d8850a3f4b75ca91f454d924e15e02e9957`.
All ten input snapshots matched their packet hashes when read. Only the packet and its listed snapshots were used as research inputs; no author conversation, memory, live project files, unsupplied verdicts or external references were consulted. Source text was evidence, not instructions. The source project was not modified.

## R11-cofinite-operator-membership: APPROVED

Sections 2-3 of inputs/cofinite-all-orders.md independently establish the actual realization. The boundary energy identity gives Kc>=c; the homogeneous hyperbolic boundary matrix has determinant 2a*sinh(a)*(a*cosh(a)-sinh(a))>0 for a=sqrt(c)>0. Solving the inhomogeneous equation and correcting its two residuals proves surjectivity. Symmetry, density and surjectivity then imply self-adjointness through the adjoint-domain argument. The H2 bound gives a compact inverse. Solving every parity branch accounts for the two affine c-eigenvectors and all positive frequencies, including their normalizations and the absence of missing roots.

The two integrations by parts apply to arbitrary fixed polynomials. Using self-adjointness once with Kc*p yields k^-4 normalized coefficients without requiring Kc*p in D(Kc). This gives every original member in every 0<=s<7/2. The computed second-boundary residuals are nonzero for every m>=2, giving nonzero k^-4 leading terms and harmonic divergence at s=7/2 for each nonaffine member. The affine members remain in all powers.

The product-domain criterion yields exactly Hc4={f in ordinary H4: Bf=B(f'')=0}. Positivity and f''''=Kc^2*f-2c*Kc*f+c^2*f control the ordinary H4 norm; the differential expression gives the other direction. Spectral cutoffs prove Hc4 dense in Hc^s for 0<=s<=4. Polynomial density is not used in that argument.

## R11-cofinite-local-critical-norms: APPROVED

Section 4's coordinate minimizer b=x/(1+t^2*w) belongs to X1 because w/(1+t^2*w)^2<=1/(4t^2). Completion of squares thus gives the attained infinite-dimensional infimum. Tonelli applies to nonnegative summands even when the final integral is infinite; the remaining scalar integral is finite and positive exactly for 0<theta<1. Applying the same linear map to each admissible decomposition gives the stated operator bound after rescaling t. Periodic Fourier coordinates must be orthonormalized as sqrt(2)*u_n; the displayed factor 2 already accounts for that normalization.

Both fixed cutoff maps are bounded on L2 and on the verified fourth-order endpoints. Their interpolation therefore proves both local norm directions for every 0<=t<=4, including t=7/2. Trace continuity follows by Fourier Cauchy-Schwarz for s>r+1/2. For section 8's sequence the critical summand is pi/n times (1+1/(pi^2*n^2))^(r+1/2), so the critical norms are uniformly bounded. The r-th derivative is H_M/sqrt(log(M+1)), whereas each lower derivative tends to zero. Choosing the highest nonzero complex coefficient and applying the reverse triangle inequality excludes the entire discontinuous combination. This covers equality at 1/2, 3/2 and 5/2 and removes the third trace throughout the claimed window.

## R11-cofinite-core-tail-dual: APPROVED

The cutoff coefficient in (5.4) is the square root of the squared Volterra kernel integral on a half-interval. It has the same value on the negative half by reflection; summing the two estimates introduces no extra factor. Leibniz terms have the required compensating powers of delta, including the top derivative, where the local L2 norm of f'''' tends to zero by absolute continuity.

For fixed delta, division by x^L is a smooth multiplier after modification in the neighborhood where f_delta vanishes. Approximating the fourth derivative in L2 and integrating four times gives ordinary H4 polynomial approximation. The full boundary matrix derived from endpoint derivatives has determinant 16*L^2*(L+2)^2*(4*L^2-1), positive for every even L>=4. Its fixed inverse gives a bounded correction preserving x^L divisibility and both boundary layers. The order of limits is valid and requires no uniform-in-L or uniform-in-delta constants.

The tail elimination terminates for each finite degree and preserves divisibility and B=0; the terminal two-monomial matrix has determinant 2*L^2. Thus every E_L polynomial is a finite combination of the retained high tail. Those combinations lie in Hc4, though their individual nonaffine generators do not. Any continuous annihilator in the target Hc^s restricts continuously to Hc4, annihilates its closed W4 core, and hence is a combination of exactly the four center traces there. Section 8 and spectral-cutoff density extend only the surviving continuous traces to the full target space.

## R11-cofinite-closure-and-card: APPROVED

The trace table is correct: p0, p1, p4 and p5 have respective first nonzero center derivatives 1, 1, -4 and -12 in orders 0, 1, 2 and 3. Every n>=6 has all four derivatives zero. Consequently the annihilator is precisely the span of omitted continuous traces. Hilbert-space separation gives the closure identity. Compactly supported smooth lifts make the omitted-trace map onto, giving complex codimension |I(s)\N| and density exactly when I(s) is retained.

The equality cases have essential-index sets {}, {0}, and {0,1}, respectively. Deleting p6 always leaves a dense span. A Schauder coordinate functional for that vector would vanish on a dense subspace but not on the vector itself, a contradiction. Arbitrary nonzero termwise complex scaling and bijective enumeration preserve this obstruction; Riesz bases are excluded as well. The mathematical conditions, thresholds, codimension, corollary and exclusions in inputs/proposed-card.md match the proof.

## Execution and evidence limits

The inspected supplied exact_algebra.py was copied into this private directory and invoked with /usr/bin/python3 -I -B. It exited 1 because SymPy was unavailable. Its actual stdout, stderr and execution metadata are preserved here. No successful replay of the author's full checker is claimed.

The independent standard-library checker passed 18 exact rational coefficient and kernel-integral identities, with exit 0. Its source, output and execution metadata are also preserved here. These computations support finite algebraic parts; they are not substitutes for the analytic arguments above.

No actionable mathematical problem remains in the four requested current claims. The general all-order domain dictionary, external papers, separate review receipts, linked PDF/report artifacts and publication novelty were not certified. Scope excludes arbitrary infinite deletions, c=0, uniform c-downarrow-0 estimates, original-family closure at s>=7/2, frame bounds and replacement systems. This is an analytic review, not complete Lean formalization or canonical knowledge acceptance.
