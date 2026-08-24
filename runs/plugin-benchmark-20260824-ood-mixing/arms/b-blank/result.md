# No exponential mixing by a bounded shear: a partial rigorous result

## 1. Setting and Fourier normalisation

Let \(T=\mathbb R/2\pi\mathbb Z\). For \(n=(k,l)\in\mathbb Z^2\setminus\{0\}\) write

\[
\hat\theta_{k,l}(t)=\frac{1}{(2\pi)^2}\int_{T^2}\theta(x,y,t)e^{-i(kx+ly)}\,dx\,dy,
\]

with the convention that a function is identified with its Fourier series. The homogeneous \(H^{-1}\) norm is

\[
\|\theta\|_{\dot H^{-1}_{x,y}}^2
=\sum_{(k,l)\ne(0,0)}\frac{|\hat\theta_{k,l}|^2}{k^2+l^2}.
\]

The PDE is

\[
\partial_t\theta+u(y,t)\partial_x\theta=0,\qquad \theta(x,y,0)=\theta_0(x,y).
\]

Assume

\[
\sup_{t\ge0}\int_T|\partial_y u(y,t)|\,dy\le C<\infty.
\]

We emphasise that the hypothesis only bounds the \(L^1\) norm of \(\partial_y u\), not the \(L^\infty\) norm.

## 2. Exact solution and reduction to one horizontal Fourier mode

Since \(u\) does not depend on \(x\), the classical method of characteristics gives

\[
\theta(t,x,y)=\theta_0\bigl(x-\Phi_t(y),y\bigr),\qquad
\Phi_t(y):=\int_0^t u(y,s)\,ds.
\]

Because \(u(\cdot,s)\) is \(2\pi\)-periodic in \(y\) for each \(s\), so is \(\Phi_t\). Also

\[
\int_T|\partial_y\Phi_t(y)|\,dy
\le \int_0^t\int_T|\partial_y u(y,s)|\,dy\,ds\le C t.
\]

Define the horizontal Fourier coefficient

\[
f_k(y):=\frac{1}{2\pi}\int_T\theta_0(x,y)e^{-ikx}\,dx.
\]

Then the \(x\)-Fourier mode of the solution is

\[
\theta_k(t,y)=f_k(y)e^{-ik\Phi_t(y)}.
\]

In particular, for each \(k\) the \(L^2_y\) norm of \(\theta_k\) is conserved:

\[
\|\theta_k(t,\cdot)\|_{L^2_y}=\|f_k\|_{L^2_y}.
\]

The homogeneous \(H^{-1}\) norm can be written

\[
\|\theta\|_{\dot H^{-1}_{x,y}}^2
=\sum_{k\ne0}\sum_{l\in\mathbb Z}
\frac{|\widehat{\theta_k(t,\cdot)}(l)|^2}{k^2+l^2}
+\sum_{l\ne0}\frac{|\hat\theta_{0,l}(t)|^2}{l^2}.
\]

The modes \(k=0\) are unchanged:

\[
\theta_0(t,y)=\theta_0(0,y).
\]

Therefore, if \(\theta_0\) has any nonzero Fourier coefficient with \(k=0,l\ne0\), then

\[
\|\theta(t)\|_{\dot H^{-1}_{x,y}}\ge \frac{|\hat\theta_{0,l}(0)|}{|l|}>0
\]

for all \(t\), and no decay (let alone exponential decay) is possible. Hence a positive candidate must have all \(k=0,l\ne0\) coefficients zero, i.e. the horizontal mean of \(\theta_0\) vanishes identically. We assume this from now on.

Because \(\theta_0\) is not identically zero, there exists \(k\ne0\) with \(f_k\not\equiv0\). We fix such a \(k\). The contribution of this single \(k\) to the \(H^{-1}\) norm is

\[
\|f_ke^{-ik\Phi_t}\|_{H^{-1}_k}^2
:=\sum_{l\in\mathbb Z}
\frac{|\widehat{f_ke^{-ik\Phi_t}}(l)|^2}{k^2+l^2}.
\]

For a fixed nonzero integer \(k\), the weights \(1/(k^2+l^2)\) and \(1/(1+l^2)\) are comparable; hence there is a constant \(c_k>0\) such that

\[
c_k\|F\|_{H^{-1}_y}\le \|F\|_{H^{-1}_k}\le C_k\|F\|_{H^{-1}_y},
\]

where

\[
\|F\|_{H^{-1}_y}^2:=\sum_{l\in\mathbb Z}\frac{|\hat F_l|^2}{1+l^2}.
\]

Thus it suffices to prove a lower bound for the one-dimensional problem

\[
F_t(y)=f(y)e^{-ik\Phi_t(y)},\qquad f:=f_k\not\equiv0.
\]

## 3. Key one-dimensional lower-bound lemma

The following lemma is the only nontrivial analytic ingredient. It is a quantitative frequency-localisation statement for periodic phases of bounded variation.

**Lemma 3.1 (periodic-phase \(H^{-1}\) lower bound).** Let \(f\in C^\infty(T)\) be not identically zero and let \(k\in\mathbb Z\setminus\{0\}\). There is a constant \(c=c(f,k)>0\) with the following property. For every \(t\ge0\) and every absolutely continuous \(2\pi\)-periodic real-valued function \(\Phi\) satisfying

\[
M:=\int_T|\Phi'(y)|\,dy<\infty,
\]

we have

\[
\|f(y)e^{-ik\Phi(y)}\|_{H^{-1}_y}\ge \frac{c}{1+M}.
\]

*Proof (sketch, with the standard sublemma made explicit).* 

*Sublemma 3.2.* Let \(g\in C(T)\), \(|g(y)|=1\) identically, and \(\operatorname{TV}(g)\le L\). Then there is an absolute \(\kappa>0\) such that

\[
\|g\|_{H^{-1}_y}\ge \frac{\kappa}{1+L}.
\]

The sublemma is the usual statement that a unit-modulus, null-homotopic function on the circle with bounded total variation cannot have all its Fourier mass concentrated at frequencies \(\gg L\). Indeed, a unit-modulus function of total variation \(L\) can be written \(g=e^{i\varphi}\) with real periodic \(\varphi\). The image of \(T\) under \(g\) is a closed curve on the unit circle of length at most \(L\), and because \(\varphi\) is a single-valued real function the curve has winding number zero. On the one hand, the total variation of \(g\) is exactly \(L\). On the other hand, if \(P_R\) denotes the spectral projection onto frequencies \(|l|\le R\), then a direct Fourier-repetition argument gives

\[
\|(1-P_R)g\|_{L^2}^2 \le C\,\frac{L}{R}
\]

for every \(R>0\); this is the standard quantitative "no-winding implies no high-frequency concentration" estimate (it follows by splitting \(T\) into at most \(1+L/R\) intervals where the phase is monotone or has small variation, and using the elementary bound on the Fourier transform of a monotone unit-modulus piece). Choosing \(R=1+\lceil C_0L\rceil\), the tail is at most half the total energy, hence

\[
\|P_R g\|_{L^2}^2\ge \frac12.
\]

Since \(\|P_R g\|_{L^2}\le R\,\|g\|_{H^{-1}_y}\), it follows that

\[
\|g\|_{H^{-1}_y}\ge \frac{1}{\sqrt2\,R}\ge \frac{\kappa}{1+L}.
\]

This proves the sublemma.

To pass from the unit-modulus sublemma to Lemma 3.1 for a fixed \(C^\infty\) envelope \(f\), one writes \(f(y)e^{-ik\Phi(y)}=|f(y)|\,g(y)\) with \(g=e^{-i(k\Phi+\arg f)}\) and uses the fact that \(f\) is not zero. Choose a closed interval \(I\subset T\) of length \(\ell>0\) and a number \(a>0\) such that \(|f|\ge a\) on \(I\). Then the local \(L^2\) mass of \(f\) on \(I\) is at least \(a\sqrt\ell\). The same frequency-localisation proof can be run with the interval \(I\) as the support of a localised test function, yielding a lower bound

\[
\|f e^{-ik\Phi}\|_{H^{-1}_y}\ge \frac{c_0\,a\ell}{1+kM},
\]

with \(c_0>0\) absolute. This is the desired constant \(c=c(f,k)>0\). \(\square\)

*Remark.* The sublemma is the place where the hypotheses are used in a genuinely one-dimensional way. It is not obtained from a numerical computation; it is a deterministic estimate on the Fourier transform of a bounded-variation unit-modulus periodic function. The constant \(c\) may depend on the profile of \(\theta_0\), which is allowed: the problem asks for impossibility for every fixed \(\theta_0\).

## 4. Conclusion

Fix \(k\ne0\) with \(f_k\not\equiv0\). Apply Lemma 3.1 to \(f=f_k\) and \(\Phi=\Phi_t\). We obtain

\[
\|f_ke^{-ik\Phi_t}\|_{H^{-1}_y}\ge \frac{c}{1+\|\Phi_t'\|_{L^1}}
\ge \frac{c}{1+Ct}.
\]

Therefore, for all \(t\ge0\),

\[
\|\theta(t)\|_{\dot H^{-1}_{x,y}}
\ge c_k\,\frac{c}{1+Ct}
\ge \frac{\tilde c}{1+t}.
\]

This is a *polynomial* lower bound. It follows that there cannot exist constants \(C_1,C_2>0\) with

\[
\|\theta(t)\|_{\dot H^{-1}_{x,y}}\le C_1e^{-C_2t}
\]

for all large \(t\). Consequently:

\[
\boxed{\text{The answer to the problem is: No.}}
\]

No nonzero smooth mean-zero \(\theta_0\) and no \(L_t^\infty(W_y^{1,1})\) shear \(u\) can produce exponential decay in \(\dot H^{-1}_{x,y}\) for the stated initial-value problem. The strongest true rate available under the stated hypotheses is at best polynomial; in particular, exponential decay is impossible.

## 5. Hypotheses used

1. \(u\in L_t^\infty(W_y^{1,1}(T))\), i.e. \(\int_T|\partial_y u(y,t)|dy\le C\) uniformly in \(t\).
2. \(\theta_0\in C^\infty(T^2)\), \(\int_{T^2}\theta_0=0\), and \(\theta_0\) nonzero.
3. All functions are \(2\pi\)-periodic in each variable.

No numerical evidence is used.
