# Independently derived local contracts

Assume positive fixed block densities, ordered interior interfaces, simple differentiable real Dirichlet eigenpairs of -u'' = lambda rho u, and integral rho u_k^2 = 1. Differentiate the weak eigenproblem and test against u: the u-derivative terms cancel by self-adjointness, leaving lambda' = -lambda integral rho' u^2. A rightward interface displacement replaces right density by left density, so rho' = -s_i delta_xi, with s_i = rho_right-rho_left. Hence partial_i lambda_k = lambda_k s_i u_k(x_i)^2, and for f_i=lambda_n u_n(x_i)^2-lambda_h u_h(x_i)^2, h=n+1, g_i=partial_i D=-s_i f_i. The jump and eigenvalue signs are thus fixed without using an author's test count.

For free widths w=(w_1,...,w_m), w_last=1-sum(w), interfaces x=Lw where L is the lower triangular ones matrix. J_x=J_w L^{-1}; H_x=L^{-T} H_w L^{-1}. For (a,b), x=(a,a+b), g_(a,b)=(g_1+g_2,g_2). With SUP jumps (R-1,-(R-1)), this is ((R-1)(f_2-f_1),(R-1)f_2); INF reverses both jumps.

A mirrored variation x=x0+Bq has g_q=B^T g_x and H_q=B^T H_x B. For n=1, B=(1,-1)^T, so the derivative is -(R-1)(f_left+f_right) for SUP and +(R-1)(f_left+f_right) for INF. Only reflection symmetry permits replacing the sum by 2 f_left. Independent interface derivatives are not doubled. For INF paired eigenvalue derivatives, both interface contributions are negative: -lambda_k(R-1)(u_k(left)^2+u_k(right)^2).

Let F=f/lambda_h, with J_ij=partial F_i/partial x_j a TOTAL derivative including sampling-point motion, and S=diag(s) constant. Differentiating g=-lambda_h S F gives H=-S[lambda_h J+F (grad lambda_h)^T]. The outer product orientation is F by grad(lambda_h), not its transpose. It is zero at F=0; elsewhere omission is invalid. At stationarity H=-lambda_h S J, and the transposed expression -lambda_h J^T S agrees under Hessian symmetry. ndarray multiplication S*J deletes offdiagonals; matrix multiplication S@J preserves them.

A column-state transfer matrix satisfies state_next=P_block state_previous, so cumulative M_new=P_block M_old. The legacy M_old P_block product is a reversed-order propagation. Its normalization also inconsistently combines wrong block starts with a forward solution formula. The fixed backend uses forward propagation and the closed integrals of A cos(wt)+B sin(wt). Numerical local validation is still required.

These derivations are conditional local interface contracts, not a proof of analytic shape regularity, infinite spectral tails, global extrema or branch continuation.
