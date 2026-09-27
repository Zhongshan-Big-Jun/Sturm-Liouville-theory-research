# Helly selection and conditional attainment

Author candidate for R13-11. The coordinator owns card versioning, source bindings and independent release. This text replaces the unconditional attainment claim; it does not withdraw measurable-box existence.

## Selection, topology and admissibility

Let \(I=[a,b]\) be a fixed finite interval. For real-valued representatives \(f_m\in BV(I)\), require uniform constants

\[
 \sup_m\|f_m\|_{\infty}\le M<\infty,
 \qquad \sup_m\operatorname{TV}_I(f_m)\le V<\infty.
\]

Here the first norm is the pointwise supremum of the chosen representatives. There is a subsequence converging at every point to a BV representative \(f\), with the same two bounds. It also converges in \(L^p(I)\) for every \(1\le p<\infty\). A family monotone in a fixed direction needs only the uniform value bound, since its total variation is at most \(2M\). Individual BV membership without a common variation bound is insufficient. Uniform convergence and \(L^\infty\) convergence are not asserted.

For completeness, write \(v_m(x)=\operatorname{TV}_{[a,x]}(f_m)\). Both

\[
 g_m^{\pm}(x)=\tfrac12\{v_m(x)\pm(f_m(x)-f_m(a))\}
\]

are nondecreasing and uniformly bounded, and \(f_m=f_m(a)+g_m^+-g_m^-\). First select a convergent subsequence of the bounded numbers \(f_m(a)\). A diagonal subsequence on a countable dense set then gives limits of both monotone parts at every continuity point of their monotone limiting functions. Their discontinuity sets are countable; a further diagonal extraction there and at the endpoints gives pointwise convergence everywhere. Each finite partition variation passes to the limit, so \(\operatorname{TV}(f)\le V\). Dominated convergence gives the stated \(L^p\) convergence. For BV equivalence classes, the intrinsic conclusion is a.e. and \(L^p\) convergence after choosing representatives.

Fix the topology before claiming attainment. For example, take a nonempty admissible class \(\mathcal A\) satisfying the above uniform bounds and sequentially closed in \(L^1(I)\), and a real-valued objective \(J:\mathcal A\to\mathbb R\). Then:

- If \(J(f)\le\liminf_m J(f_m)\) whenever \(f_m\to f\) in \(L^1\), a minimizing sequence has an admissible limit attaining the infimum.
- If \(J(f)\ge\limsup_m J(f_m)\), a maximizing sequence similarly attains the supremum.
- Sequential continuity gives both conclusions.

Indeed, extract a convergent subsequence from the optimizing sequence, use closedness to place its limit in \(\mathcal A\), and apply the correctly directed inequality. Finite-valued lower semicontinuity also rules out infimum \(-\infty\) by the same argument; upper semicontinuity rules out supremum \(+\infty\). The same principle applies to pointwise representatives if admissibility and semicontinuity are verified for that convergence instead. Continuity of every approximant does not imply continuity of a Helly limit. Endpoint values and endpoint traces must not be treated as the same condition, or as automatically closed conditions in \(L^1\). The limiting function need not be a step function.

## Spectral objective and the full measurable box

For the fixed Dirichlet problem \(-u''=\lambda\rho u\) on \(I\), assume \(0<a_0\le\rho\le b_0<\infty\). On \(H_0^1(I)\) with energy inner product, define the positive compact operator

\[
 (T_\rho u,v)_{H_0^1}=\int_I\rho u\overline v,
 \qquad \|u\|_{H_0^1}=\|u'\|_2.
\]

The estimate \(\|u\|_\infty\le |I|^{1/2}\|u'\|_2\) gives

\[
 \|T_{\rho_m}-T_\rho\|\le |I|\,\|\rho_m-\rho\|_1.
\]

Compactness follows from the compact embedding of the energy unit ball into \(C(I)\). The decreasing positive eigenvalues of \(T_\rho\) are \(1/\lambda_j(\rho)\). The min-max estimate for compact self-adjoint operators therefore proves continuity of every fixed \(\lambda_j\) under this \(L^1\) convergence. Fixed-index gaps and ratios are continuous too. This checks the objective hypothesis; the admissible-class hypothesis remains separate. Other SL operators or coefficient topologies need their own continuity proof.

The full measurable box \(K_R=\{\rho\in L^\infty(0,1):1\le\rho\le R\ \text{a.e.}\}\) has no uniform TV restriction and uses weak-star compactness instead. Every bounded sequence in \(L^\infty(0,1)\) has a weak-star convergent subsequence with limit in \(L^\infty(0,1)\), because \(L^1(0,1)\) is separable; testing against nonnegative functions preserves the box. Weak-star convergence is uniform on the compact \(L^1\) closure of \(\{u\overline v:\|u'\|_2,\|v'\|_2\le1\}\), by a finite-net argument and the uniform \(L^\infty\) bound. Thus \(T_{\rho_m}\to T_\rho\) in operator norm also along these weak-star sequences. The same eigenvalue argument gives both extrema of fixed gaps or ratios on \(K_R\). The existing project proof uses weak-star compactness and spectral continuity explicitly; it does not require the false unconditional Helly statement.

## Preserved nonattainment counterexample

Fix \(R>1\) and keep exactly the supplied class

\[
 \mathcal C_R=\{\rho\in C[0,1]:\rho\text{ nondecreasing},\ 1\le\rho\le R,
       \ \rho(0)=1,\ \rho(1)=R\}.
\]

For every \(\rho\in\mathcal C_R\), continuity at zero gives a nonempty internal interval where \(\rho<R\). The first Dirichlet eigenfunction is strictly positive in the interior: an absolute-value Rayleigh minimizer is nonnegative, and an interior zero would force zero Cauchy data and the zero solution. Hence

\[
 \lambda_1(\rho)=\frac{\int_0^1|u'|^2}{\int_0^1\rho u^2}
 >\frac{\int_0^1|u'|^2}{R\int_0^1u^2}\ge\frac{\pi^2}{R}.
\]

For integers \(k\ge1\), set \(\rho_k(x)=1+(R-1)\min(kx,1)\). Each \(\rho_k\) is admissible, with variation \(R-1\). Using \(\sin(\pi x)\) in the Rayleigh quotient gives

\[
 \frac{\pi^2}{R}<\lambda_1(\rho_k)
 \le\frac{\pi^2/2}{R/2-\delta_k},\qquad
 \delta_k=(R-1)\int_0^{1/k}(1-kx)\sin^2(\pi x)\,dx.
\]

Since \(\sin^2(\pi x)\le\pi^2x^2\),

\[
 0\le\delta_k\le(R-1)\pi^2\int_0^{1/k}(1-kx)x^2\,dx
 =\frac{(R-1)\pi^2}{12k^3}\longrightarrow0.
\]

Thus \(\inf_{\mathcal C_R}\lambda_1=\pi^2/R\), and no member attains it. The pointwise limit has value 1 at zero and \(R\) everywhere else, so it leaves \(C[0,1]\). In \(L^1\) its class is the constant \(R\); there is no continuous representative satisfying the original endpoint data. The failure is admissible-class closedness, despite uniform boundedness, uniform TV and spectral continuity. Constant \(R\) is admissible in \(K_R\) and attains the bound there, so this example does not refute measurable-box existence.

## Source and reuse boundary

- Supplied input: `/mnt/c/Users/HuangZY/Downloads/sl_audit_round13/analytic_notes.md`, section 11, and `REPORT.md`, R13-11. The counterexample, strict inequality and \(1/(12k^3)\) bound were checked algebraically above by this author; this is not an independent review receipt.
- Actual project source: `docs/SL_gap_nge2_finite_reduction_proof.tex`, `lem:wscompact`, `lem:wscont`, `cor:attain` (source lines 322-425 at author read time). These establish the distinct measurable-box route.
- [[bang-bang]] and [[keller-variational]] need an existence premise verified for their actual class and topology; Helly selection alone supplies neither attainment nor the switching structure.
- The old precise attribution to "Keller 1976 Section 2" is not used here: its original content was not accessed in this task. No replacement literature theorem number is asserted. The derivation and the actual project source suffice for this correction.
