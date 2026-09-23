# Finite synthesis maps: exact TSVD error and noise bounds

Status: AUTHOR_PROOF, pending the coordinator's fresh independent review. No frame hypothesis and no infinite-dimensional conclusion are hidden in Theorem T1. The derivation below also allows linearly dependent columns.

## T1. Contract and threshold

Let H be a complex Hilbert space, with inner products linear in the first argument. Let T:C^N -> H be any linear map, Tz=sum z_j phi_j. Thus (T*f)_j=<f,phi_j> and G=T*T has entries G_ij=<phi_j,phi_i>. Choose an orthonormal eigenbasis v_j of G with eigenvalues lambda_j>=0. For lambda_j>0 put u_j=Tv_j/sqrt(lambda_j). These u_j are orthonormal. For epsilon>0 define

$$
G_\epsilon^\dagger=\sum_{\lambda_j>\epsilon}\lambda_j^{-1}v_jv_j^*,\qquad
P_\epsilon=T G_\epsilon^\dagger T^*.
$$

The cutoff is on Gram eigenvalues: equality is discarded. Then, for every f in H,

$$
P_\epsilon f=\sum_{\lambda_j>\epsilon}\langle f,u_j\rangle u_j,
\qquad
\boxed{\|f-P_\epsilon f\|\le
\inf_{z\in\mathbb C^N}\{\|f-Tz\|+\sqrt\epsilon\|z\|_2\}.}\tag{T1}
$$

The corresponding coefficient vector z_epsilon=G_epsilon^dagger T*f obeys

$$
\|z_\epsilon\|_2\le
\inf_z\{\epsilon^{-1/2}\|f-Tz\|+\|z\|_2\}.\tag{T2}
$$

Proof. The displayed formula for P_epsilon follows by applying T and T* in the eigenbasis; zero eigenvalues contribute nothing. Hence P_epsilon is an orthogonal projection. For every z,

$$
f-P_\epsilon f=(I-P_\epsilon)(f-Tz)+(I-P_\epsilon)Tz.
$$

The first term has norm at most ||f-Tz||. Orthogonality gives

$$
\|(I-P_\epsilon)Tz\|^2
=\sum_{0<\lambda_j\le\epsilon}\lambda_j|\langle z,v_j\rangle|^2
\le\epsilon\|z\|_2^2.
$$

The triangle inequality and then the infimum prove (T1). For (T2), decompose

$$
z_\epsilon=G_\epsilon^\dagger T^*(f-Tz)+G_\epsilon^\dagger Gz.
$$

The first operator has norm at most epsilon^(-1/2); its retained singular values are lambda_j^(-1/2). The second is an orthogonal coordinate projection, of norm at most one. This proves (T2), including the case of an empty retained spectrum.

The exact squared error is also useful:

$$
\|f-P_\epsilon f\|^2
=\|(I-P_{\operatorname{ran}T})f\|^2
 +\sum_{0<\lambda_j\le\epsilon}|\langle f,u_j\rangle|^2.\tag{T3}
$$

## Noise and the two different SVD conventions

If available moments are y=T*f+e, form f_epsilon=T G_epsilon^dagger y. Then

$$
\boxed{\|f-f_\epsilon\|\le
\inf_z\{\|f-Tz\|+\sqrt\epsilon\|z\|_2\}
+\epsilon^{-1/2}\|e\|_2.}\tag{T4}
$$

Indeed ||T G_epsilon^dagger|| is the maximum of lambda_j^(-1/2) over retained j (zero if none). The coefficient perturbation has bound epsilon^(-1)||e||_2. If the perturbation is instead to f itself in H, P_epsilon is a contraction, so ||P_epsilon(f+eta)-P_epsilon f||<=||eta||. These are different data models. Gram/quadrature errors require a separate perturbation analysis; (T4) holds with the exact G.

Write sigma_j=sqrt(lambda_j) for singular values of the synthesis map T. A cutoff sigma_j>tau has epsilon=tau^2; its approximation penalty is tau||z|| and its moment-noise penalty is ||e||/tau. Applying the same numerical threshold to G and T produces different retained subspaces. A relative Gram cutoff lambda_j>rho||G|| has penalty sqrt(rho)||T||||z||. If T=0, all reconstructions are zero and the assertions are interpreted directly, without dividing by ||G||.

For example, T=diag(1,1/10) and epsilon=1/20: a Gram cutoff discards the second direction (lambda_2=1/100), whereas a synthesis cutoff at the same number retains it (sigma_2=1/10). At epsilon=1/100 the second Gram direction is still discarded under the strict convention above.

## Exact relation to L09

Adcock--Huybrechs, arXiv:1612.04464v4, PDF p.10, (2.13)-(2.14), defines finite synthesis and Gram matrices. PDF p.19, (5.1)-(5.4), uses **sigma_n for singular values of the Gram matrix**, which there equal its eigenvalues. Equation (5.2) retains sigma_n>epsilon. Theorem 5.3, PDF p.20, (5.5), is the sqrt(epsilon) inequality. Its proof uses finite orthogonal projections; the surrounding article assumes an infinite linearly independent frame. The separate limiting estimate (5.6) uses its lower frame bound A. Theorem 5.5, PDF p.22, bounds sensitivity to moment data. Our T1-T4 expose precisely which finite steps survive without those infinite-frame assumptions.

Primary source: [arXiv v4](https://arxiv.org/pdf/1612.04464v4); journal identity: SIAM Review 61(3) (2019), 443-473, [DOI](https://doi.org/10.1137/17M1114697). We read the stated arXiv version, not an authenticated publisher full text.

## Conditional transfer to the actual Krein spaces

Fix real c>0 and s in {2,4}. Define

$$
K_cf=-f''+cf,\quad
\mathcal Bf=(f'(1)-\Delta f/2,\ f'(-1)-\Delta f/2),\quad
\Delta f=f(1)-f(-1).
$$

Use H_c^2=D(K_c)={f in ordinary H^2: Bf=0}, norm ||K_cf||_2, or H_c^4=D(K_c^2)={f in ordinary H^4: Bf=B(f'')=0}, norm ||K_c^2 f||_2. These domains and positive self-adjointness are read in current project sources, not inferred from formal differential expressions. See source-manifest.json for their frozen identities.

For any **finite set already in this domain**, let T_N z=sum z_j phi_j and

$$
G_{ij}=\langle K_c^{s/2}\phi_j,K_c^{s/2}\phi_i\rangle_2,
\qquad y_i=\langle K_c^{s/2}f,K_c^{s/2}\phi_i\rangle_2.
$$

T1-T4 apply verbatim in the indicated norm. This transfer is conditional on f and every column belonging to H_c^s and on exact moment/Gram data. At s=2 the original p_n meet membership. At s=4 every nonaffine named original p_n fails membership; one must first form and check a compatible combination, or use the construction in note 03. The expression (c-D^2)^2 alone cannot discharge this requirement.

For a general complete system, convergence with a fixed cutoff does not follow from completeness. One needs a bound on useful coefficient norms or a proved uniform Riesz/frame bound. Note 03 supplies explicit bounds for its particular replacement systems at fixed c, independently of the number of columns. No all-c or all-s claim is made.
