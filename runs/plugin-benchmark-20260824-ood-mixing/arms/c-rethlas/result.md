# Exponential mixing by a bounded shear on $T^2$: impossibility

**Answer: No.** For every nonzero $\theta_0 \in C^\infty(T^2)$ with zero mean and every time-dependent shear $u \in L^\infty_t(W^{1,1}_y(T))$ satisfying the stated bound, the solution of the initial value problem does **not** satisfy an exponential decay estimate $\|\theta(t)\|_{\dot H^{-1}_{x,y}} \le C_1 e^{-C_2 t}$. In fact we prove the quantitative lower bound stated in Theorem thm:main below.

All lemmas are stated with their hypotheses and proved from scratch; no external theorem is used.

## notation

- $T = [-\pi,\pi]$ with Lebesgue measure $dy$; $T^2 = T \times T$.
- For $f \in L^1(T)$, the Fourier coefficients are
  $$\hat f_l = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(y) e^{-ily}\,dy,\qquad l \in \mathbb{Z},$$
  so that $f(y) = \sum_l \hat f_l e^{ily}$ and $\int_T |f|^2 dy = 2\pi\sum_l |\hat f_l|^2$ (Parseval).
- For $\theta \in L^1(T^2)$, the Fourier coefficients are
  $$\hat\theta(k,l) = \frac{1}{4\pi^2}\int_{T^2} \theta(x,y) e^{-i(kx+ly)}\,dx\,dy,\qquad (k,l)\in\mathbb{Z}^2,$$
  and the norm of the problem is
  $$\|\theta\|_{\dot H^{-1}_{x,y}}^2 = \sum_{\substack{(k,l)\in\mathbb{Z}^2\\(k,l)\ne(0,0)}} \frac{|\hat\theta(k,l)|^2}{k^2+l^2}.$$
- $W^{1,1}(T)$ denotes the Sobolev space of functions on $T$ with a weak derivative in $L^1(T)$; equivalently, absolutely continuous $2\pi$-periodic functions whose derivative is in $L^1$. For such $f$, $\mathrm{Var}(f) = \int_T |f'|dy$ (total variation equals the $L^1$ norm of the derivative), and $W^{1,1}(T) \hookrightarrow C(T)$.

## remark rem:rate

The proof shows more than absence of exponential decay: in Case 2 the squared norm is bounded below by a polynomial,
$$\|\theta(t)\|_{\dot H^{-1}_{x,y}}^2 \ge c(t), \qquad c(t)\,(1+t)^4 \to \frac{\pi^4 E^3}{2 A_0^4} > 0,$$
so no decay faster than algebraic is possible. The exponent $4$ is not claimed to be sharp; e.g. for the stationary shear $u(y)=y$ and data $\theta_0 = \cos x\,\cos y$ one computes exactly $\|\theta(t)\|_{\dot H^{-1}}^2 = \tfrac18(\tfrac{1}{1+(t-1)^2}+\tfrac{1}{1+(t+1)^2}) \sim \tfrac{1}{4t^2}$, algebraic but not exponential. The obstruction is the cumulative-variation budget $\|\partial_y U(\cdot,t)\|_{L^1} \le Ct$, which forces the Fourier mass of $e^{-ikU}v_0$ to satisfy the tail bound of Lemma lem:wb11-decay and hence prevents exponential spreading to high frequencies.

## lemma lem:explicit-solution

### statement

Let $\theta_0 \in C^\infty(T^2)$, let $u \in L^\infty_t(W^{1,1}_y(T))$ with
$$\int_T |\partial_y u(y,t)|\,dy \le C \quad\text{for a.e. } t \ge 0,$$
and define the cumulative shear
$$U(y,t) := \int_0^t u(y,s)\,ds.$$
Then:

1. The unique solution of $\partial_t\theta + u(y,t)\partial_x\theta = 0$ with $\theta(x,y,0)=\theta_0(x,y)$ is
   $$\theta(x,y,t) = \theta_0\big(x - U(y,t),\, y\big).$$
2. For every $t \ge 0$, $U(\cdot,t) \in W^{1,1}(T)$ and
   $$\|\partial_y U(\cdot,t)\|_{L^1(T)} \le C t.$$
3. For each $k \in \mathbb{Z}$, the $k$-th $x$-Fourier coefficient evolves as
   $$\tilde\theta_k(y,t) := \frac{1}{2\pi}\int_{-\pi}^{\pi}\theta(x,y,t)e^{-ikx}\,dx
   = e^{-ikU(y,t)}\,\tilde\theta_{k,0}(y),\qquad
   \tilde\theta_{k,0}(y) := \frac{1}{2\pi}\int_{-\pi}^{\pi}\theta_0(x,y)e^{-ikx}\,dx.$$
   In particular, for $k = 0$ the sector is frozen: $\tilde\theta_0(y,t) = \tilde\theta_{0,0}(y)$ for all $t$, i.e. $\hat\theta(0,l,t) = \hat\theta_0(0,l)$ for all $l$.
4. For each $k$, the $y$-spectrum of the sector is conserved:
   $$\sum_{l\in\mathbb{Z}}|\hat\theta(k,l,t)|^2 = \sum_{l\in\mathbb{Z}}|\hat\theta(k,l,0)|^2 \quad\text{for all } t.$$

### proof

1. For each fixed $y$, the equation is the one-dimensional transport equation
   $\partial_t\theta + u(y,t)\partial_x\theta = 0$ with speed $u(y,t)$ in the $x$ variable; the characteristics are $\dot x = u(y,t)$, $\dot y = 0$, so $x(t) = x_0 + U(y,t)$, $y(t) = y_0$. Since $u(\cdot,t) \in W^{1,1}(T) \hookrightarrow C(T)$ with a uniform bound in $L^\infty_t L^\infty_y$, $U$ is well defined, continuous in $y$ and Lipschitz in $t$ for a.e. $y$, and $\theta_0 \in C^\infty(T^2)$; the method of characteristics gives the classical solution $\theta(x,y,t) = \theta_0(x-U(y,t),y)$. Uniqueness in the classical class is standard; in any case the formula directly satisfies the equation:
   $$\partial_t\theta = -\partial_x\theta_0(x-U(y,t),y)\,\partial_t U = -u(y,t)\,\theta_x.$$

2. By the triangle inequality (Minkowski's integral inequality),
   $$\|\partial_y U(\cdot,t)\|_{L^1(T)} = \left\|\int_0^t \partial_y u(\cdot,s)\,ds\right\|_{L^1(T)}
   \le \int_0^t \|\partial_y u(\cdot,s)\|_{L^1(T)}\,ds \le C t.$$

3. Substitute $x' = x - U(y,t)$:
   $$\tilde\theta_k(y,t) = \frac{1}{2\pi}\int_{-\pi}^{\pi}\theta_0(x-U(y,t),y)e^{-ikx}\,dx
   = e^{-ikU(y,t)}\frac{1}{2\pi}\int_{-\pi}^{\pi}\theta_0(x',y)e^{-ikx'}\,dx'
   = e^{-ikU(y,t)}\tilde\theta_{k,0}(y).$$
   Taking $k=0$ gives the frozen sector. Equivalently, $\hat\theta(0,l,t) = \hat\theta_0(0,l)$ for all $l$.

4. Since $|e^{-ikU(y,t)}| = 1$, multiplication by $e^{-ikU(\cdot,t)}$ is a unitary map on $L^2(T)$; hence
   $$\sum_l|\hat\theta(k,l,t)|^2 = \frac{1}{2\pi}\|\tilde\theta_k(\cdot,t)\|_{L^2(T)}^2
   = \frac{1}{2\pi}\|\tilde\theta_{k,0}\|_{L^2(T)}^2 = \sum_l|\hat\theta(k,l,0)|^2.$$

$\square$

## lemma lem:wb11-decay

### statement

Let $f \in W^{1,1}(T)$. Then for every integer $l \ne 0$,
$$|\hat f_l| \le \frac{\|f'\|_{L^1(T)}}{2\pi\,|l|},$$
and consequently, for every $N \ge 1$,
$$\sum_{|l| > N} |\hat f_l|^2 \le \frac{\|f'\|_{L^1(T)}^2}{2\pi^2 N}.$$

### proof

A function in $W^{1,1}(T)$ has an absolutely continuous (hence continuous, periodic) representative; integration by parts is therefore valid and the boundary terms cancel by periodicity:
$$\hat f_l = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(y)e^{-ily}\,dy
= \frac{1}{2\pi il}\int_{-\pi}^{\pi} f'(y)e^{-ily}\,dy,\qquad l \ne 0.$$
Taking absolute values yields the pointwise bound. For the tail estimate, use $\sum_{|l|>N} l^{-2} \le 2\sum_{l>N} l^{-2} \le 2\int_N^\infty x^{-2}dx = 2/N$:
$$\sum_{|l|>N}|\hat f_l|^2 \le \frac{\|f'\|_{L^1}^2}{4\pi^2}\sum_{|l|>N}\frac{1}{l^2} \le \frac{\|f'\|_{L^1}^2}{2\pi^2 N}.$$

$\square$

## lemma lem:energy

### statement

Let $k \in \mathbb{Z}\setminus\{0\}$, $v_0 \in C^\infty(T)$, and let $U(\cdot,t) \in W^{1,1}(T)$ satisfy $\|\partial_y U(\cdot,t)\|_{L^1(T)} \le Ct$ for all $t \ge 0$. Define
$$\tilde v(y,t) := e^{-ikU(y,t)}\,v_0(y).$$
Then $\tilde v(\cdot,t) \in W^{1,1}(T)$ for every $t$, and
$$\|\partial_y \tilde v(\cdot,t)\|_{L^1(T)} \le A_0\,(1+t),
\qquad A_0 := \max\Big(\|v_0'\|_{L^1(T)},\ |k|\,C\,\|v_0\|_{L^\infty(T)}\Big).$$

### proof

Since $U(\cdot,t) \in W^{1,1}(T)$ and $y \mapsto e^{-ikU(y,t)}$ is the composition of a $W^{1,1}$ function with a $C^1$ function of bounded derivative, the chain rule holds in the distributional sense:
$$\partial_y\tilde v = e^{-ikU}\,\partial_y v_0 - ik\,(\partial_y U)\,e^{-ikU}\,v_0,$$
and both terms lie in $L^1(T)$. Taking $L^1$ norms:
$$\|\partial_y\tilde v\|_{L^1} \le \|v_0'\|_{L^1} + |k|\,\|\partial_y U\|_{L^1}\,\|v_0\|_{L^\infty}
\le \|v_0'\|_{L^1} + |k|Ct\,\|v_0\|_{L^\infty} \le A_0(1+t).$$

$\square$

## lemma lem:sector

### statement

Let $\theta_0 \in C^\infty(T^2)$, $u \in L^\infty_t(W^{1,1}_y(T))$ with $\|\partial_y u(\cdot,t)\|_{L^1} \le C$ a.e., and let $\theta$ be the solution of the initial value problem. Fix $k \ne 0$ and assume
$$E := \sum_{l\in\mathbb{Z}}|\hat\theta(k,l,0)|^2 > 0.$$
Define $v_0(y) := \tilde\theta_{k,0}(y)$ and $A_0 := \max\big(\|v_0'\|_{L^1},\ |k|C\|v_0\|_{L^\infty}\big)$. Then for every $t \ge 0$,
$$\sum_{l\in\mathbb{Z}}\frac{|\hat\theta(k,l,t)|^2}{k^2+l^2}
\ \ge\ \frac{E/2}{k^2 + \left(1 + \dfrac{A_0^2(1+t)^2}{\pi^2 E}\right)^2}.$$

### proof

By Lemma lem:explicit-solution(3), $\tilde\theta_k(y,t) = e^{-ikU(y,t)}v_0(y)$ with $U$ as in Lemma lem:explicit-solution; by Lemma lem:energy,
$$\|\partial_y \tilde\theta_k(\cdot,t)\|_{L^1(T)} \le A_0(1+t).$$
Writing $v_l(t) := \hat\theta(k,l,t) = \widehat{\tilde\theta_k(\cdot,t)}(l)$, Lemma lem:wb11-decay gives, for every $N \ge 1$,
$$T_N(t) := \sum_{|l|>N}|v_l(t)|^2 \le \frac{\|\partial_y\tilde\theta_k(\cdot,t)\|_{L^1}^2}{2\pi^2 N}
\le \frac{A_0^2(1+t)^2}{2\pi^2 N}.$$
Conservation (Lemma lem:explicit-solution(4)) gives $\sum_l |v_l(t)|^2 = E$. Hence, since $k^2+l^2 \le k^2+N^2$ for $|l|\le N$,
$$\sum_l\frac{|v_l(t)|^2}{k^2+l^2}
\ge \frac{1}{k^2+N^2}\sum_{|l|\le N}|v_l(t)|^2
= \frac{E - T_N(t)}{k^2+N^2}
\ge \frac{E - \dfrac{A_0^2(1+t)^2}{2\pi^2 N}}{k^2+N^2}.$$
Choose
$$N = N(t) := \max\left(1,\ \left\lceil \frac{A_0^2(1+t)^2}{\pi^2 E}\right\rceil\right) \ge 1,$$
so that $\dfrac{A_0^2(1+t)^2}{2\pi^2 N} \le E/2$ (if $A_0 = 0$ the tail $T_N(t)$ vanishes identically and the inequality is trivial) and $N \le 1 + \dfrac{A_0^2(1+t)^2}{\pi^2 E}$. Then
$$\sum_l\frac{|v_l(t)|^2}{k^2+l^2}
\ge \frac{E/2}{k^2 + N(t)^2}
\ge \frac{E/2}{k^2 + \left(1 + \dfrac{A_0^2(1+t)^2}{\pi^2 E}\right)^2}.$$

$\square$

## lemma lem:kmode

### statement

Let $\theta_0 \in C^\infty(T^2)$, $u$ as above, and $\theta$ the solution. If $\hat\theta_0(0,l_0) \ne 0$ for some $l_0 \in \mathbb{Z}$, then
$$\hat\theta(0,l_0,t) = \hat\theta_0(0,l_0)\quad\text{for all } t \ge 0.$$
In particular, if $\hat\theta_0(0,l_0)\ne 0$ with $l_0 \ne 0$, then
$$\|\theta(t)\|_{\dot H^{-1}_{x,y}}^2 \ge \frac{|\hat\theta_0(0,l_0)|^2}{l_0^2} > 0 \quad\text{for all } t \ge 0.$$

### proof

By Lemma lem:explicit-solution(3) with $k=0$, $\tilde\theta_0(y,t) = \tilde\theta_{0,0}(y)$; taking the $l_0$-th Fourier coefficient in $y$ gives $\hat\theta(0,l_0,t) = \hat\theta_0(0,l_0)$. The $\dot H^{-1}$ norm contains the term $|\hat\theta(0,l_0,t)|^2/l_0^2$, so the displayed lower bound follows.

$\square$

## theorem thm:main

### statement

Let $T^2 = [-\pi, \pi]^2$ with periodic functions of period $2\pi$ in each variable. A function $\theta(x,y)$ with $(x,y) \in T^2$ is considered periodic.

**Problem.** Can you find a nonzero function $\theta_0(x,y) \in C^\infty(T^2)$ with

$$\int_{T^2} \theta_0(x,y) dx dy = 0,$$

and a time-dependent shear $u(y,t) \in L_t^\infty(W_y^{1,1}(T))$ (equivalently $\int_T |\partial_y u(y,t)| dy \le C$ for some constant $C$), such that the solution of the initial value problem

$$\theta_t + u(y,t) \partial_x \theta = 0,$$
$$\theta(x,y,0) = \theta_0(x,y)$$

satisfies

$$\|\theta\|_{\dot H^{-1}_{x,y}}(t) \le C_1 e^{-C_2 t}$$

for some constants $C_1$ and $C_2$? Here

$$\|\theta\|_{\dot H^{-1}_{x,y}}(t)^2 = \sum_{|n| > 0, n \in \mathbb{Z}^2} (1/|n|^2) |\hat \theta(n,t)|^2,$$

and $\hat \theta(n)$ denotes the Fourier coefficient of $\theta$ over $T^2$.

Answer one of the following with a complete proof:
1. Yes: give an explicit construction, verify all hypotheses, and prove the exponential decay.
2. No: prove that for every nonzero smooth mean-zero $\theta_0$ and every $u$ satisfying the stated bound, exponential decay is impossible.

**Conclusion (answer 2): No.** For every nonzero $\theta_0 \in C^\infty(T^2)$ with $\int_{T^2}\theta_0 = 0$ and every shear $u \in L^\infty_t(W^{1,1}_y(T))$ with $\int_T|\partial_y u(y,t)|dy \le C$ for a.e. $t$, there are no constants $C_1, C_2 > 0$ such that $\|\theta(t)\|_{\dot H^{-1}_{x,y}} \le C_1 e^{-C_2 t}$ for all $t \ge 0$.

### proof

Fix any nonzero $\theta_0 \in C^\infty(T^2)$ with $\int_{T^2}\theta_0 = 0$ and any admissible $u$. Let $\theta$ be the solution (given explicitly by Lemma lem:explicit-solution).

Because $\theta_0$ has zero mean, $\hat\theta_0(0,0) = 0$.

**Case 1: some $x$-independent mode is nonzero.** Suppose $\hat\theta_0(0,l_0)\ne 0$ for some $l_0 \in \mathbb{Z}$. Then $l_0 \ne 0$ (as $\hat\theta_0(0,0)=0$), and Lemma lem:kmode gives
$$\|\theta(t)\|_{\dot H^{-1}_{x,y}}^2 \ge \frac{|\hat\theta_0(0,l_0)|^2}{l_0^2} > 0\quad\text{for all } t.$$
The norm does not decay at all, so no exponential decay estimate can hold.

**Case 2: all $x$-independent modes vanish.** Suppose $\hat\theta_0(0,l) = 0$ for every $l \in \mathbb{Z}$. Since $\theta_0 \not\equiv 0$, there is some $(k_*, l) \in \mathbb{Z}^2$ with $k_* \ne 0$ and $\hat\theta_0(k_*,l) \ne 0$; in particular
$$E := \sum_{l\in\mathbb{Z}}|\hat\theta(k_*,l,0)|^2 = \sum_{l\in\mathbb{Z}}|\hat\theta_0(k_*,l)|^2 > 0.$$
Let $v_0(y) := \tilde\theta_{k_*,0}(y) \in C^\infty(T)$ and $A_0 := \max(\|v_0'\|_{L^1}, |k_*|C\|v_0\|_{L^\infty})$, which is finite. Lemma lem:sector yields, for every $t \ge 0$,
$$\|\theta(t)\|_{\dot H^{-1}_{x,y}}^2
\ge \sum_{l\in\mathbb{Z}}\frac{|\hat\theta(k_*,l,t)|^2}{k_*^2+l^2}
\ge \frac{E/2}{k_*^2 + \left(1 + \dfrac{A_0^2(1+t)^2}{\pi^2 E}\right)^2}
=: c(t).$$
Note that $A_0 = 0$ is possible only when $C = 0$ and $v_0$ is constant (then $c(t) = (E/2)/(k_*^2+1)$ is constant in $t$, and an exponential bound is immediately impossible). In the remaining cases $A_0 > 0$, and as $t \to \infty$,
$$c(t)\,(1+t)^4 \ \longrightarrow\ \frac{E}{2}\left(\frac{\pi^2 E}{A_0^2}\right)^2
= \frac{\pi^4 E^3}{2 A_0^4} > 0.$$
Now suppose, toward a contradiction, that $\|\theta(t)\|_{\dot H^{-1}_{x,y}} \le C_1 e^{-C_2 t}$ for all $t \ge 0$ with $C_1, C_2 > 0$. Then $C_1^2 e^{-2C_2t} \ge c(t)$ for all $t$, so
$$C_1^2\, e^{-2C_2 t}(1+t)^4 \ge c(t)(1+t)^4
\ \longrightarrow\ \frac{\pi^4 E^3}{2 A_0^4} > 0.$$
But $e^{-2C_2t}(1+t)^4 \to 0$ as $t\to\infty$, so the left-hand side tends to $0$. Contradiction.

Hence in both cases no exponential decay estimate holds. Since $\theta_0$ and $u$ were arbitrary, the answer to the problem is **No**: exponential decay of $\|\theta\|_{\dot H^{-1}_{x,y}}$ is impossible for every nonzero smooth mean-zero initial datum and every shear satisfying $\|\partial_y u(\cdot,t)\|_{L^1} \le C$.

$\square$


## remark rem:literature

The proof above is self-contained and uses no external results. For context, we record how it relates to the known literature on mixing by shear flows. All statements below concern the *geometric mixing scale* in Bressan's sense, defined for initial datum $u_0 = \tfrac12\mathbf 1_{x_1\le\pi} - \tfrac12\mathbf 1_{x_1>\pi}$ by
$$\mathrm{mix}(b) := \sup\Big\{ \mathrm{radius}(B) : \Big|\tfrac{1}{|B|}\textstyle\int_B u(1,x)\,dx\Big| > 1 \Big\},$$
where $u$ solves the transport equation with velocity $b$; they are recorded here only to delineate the boundary of the problem's hypothesis class and are **not** used in the proof.

**Source 1 (geometric obstruction for $W^{1,1}$-budgeted shears).** Cooperman, "Exponential mixing by shear flows", arXiv:2206.14239, Theorem 1 (paper_id: arXiv:2206.14239, arXiv id: 2206.14239). *Statement (verbatim up to notation):* Let $b \in L^1([0,1];W^{1,1}(\mathbb{T}^2;\mathbb{R}^2))$ be a divergence-free shear at every time $t\in[0,1]$, i.e. $b(t,x)$ is parallel to $b(t,y)$ for all $t\ge 0$ and $x,y\in\mathbb{T}^2$. Then there is a constant $C>0$ such that $|\log \mathrm{mix}(b)| \le C\|Db\|_{L^1}$. *Hypotheses used:* the velocity is a shear with spatial gradient in $L^1$ integrated in time. *Relevance:* under the problem's uniform bound $\|\partial_y u(\cdot,t)\|_{L^1}\le C$, the time-integrated budget over $[0,t]$ is at most $Ct$, so this result yields a geometric-scale lower bound $\mathrm{mix}\ge e^{-C't}$; it concerns the geometric scale rather than the $\dot H^{-1}$ functional norm, and the latter is controlled more sharply (polynomially) by Theorem thm:main.

**Source 2 (exponential mixing by shears exists only outside the hypothesis class).** (a) Cooperman, arXiv:2206.14239, Theorem 2 (paper_id: arXiv:2206.14239): for $\tau_n$ i.i.d. uniform on $[0,T]$ with $T$ large, the random field $b^{\alpha}_{\bar\tau}(t,x) := \alpha\,\bar b_{\bar\tau}(\alpha t,x)$ alternating between the shears $\tau_n(\sin x_2,0)$ and $\tau_n(0,\sin x_1)$ satisfies, almost surely for some $c(T)>0$ and every $\alpha>0$,
$$|\log\mathrm{mix}(b^{\alpha}_{\bar\tau})| \ge c\,\|Db^{\alpha}_{\bar\tau}\|_{L^1}.$$
(b) Zhang, "Exponential mixing for Hamiltonian shear flow", arXiv:2502.09123, Theorem 1.3 (paper_id: arXiv:2502.09123, arXiv id: 2502.09123): for random alternating Hamiltonian shears $-\tau_{\lceil t\rceil}X_2$, $-\tau_{\lceil t\rceil}X_1$ with $X_1=(f_1(p),0)$, $X_2=(0,f_2(q))$, $f_i$ nonconstant real analytic satisfying (H1) $C_{f_i}\cap C_{f_i'}=\emptyset$ (and Lie-algebra conditions (H2), (H3)), with $b^{\rho}_{\tau}(t,x):=\rho\, b_{\tau}(\rho t,x)$, there is a random variable $\xi>0$ a.s. with, for every integer $\rho>0$ a.s.,
$$|\log\mathrm{mix}(b^{\rho}_{\tau})| \ge \xi(\tau)\,\|Db^{\rho}_{\tau}\|_{L^1([0,1]\times\mathbb{T}^2)}.$$
*Why these do not apply to the problem:* both constructions accelerate the flow (factor $\alpha$ or $\rho$), so the per-time norm $\|D b^{\alpha}(t,\cdot)\|_{L^1} = \alpha\,\|Db(\alpha t,\cdot)\|_{L^1}$ is unbounded; the problem instead requires $u\in L^\infty_t(W^{1,1}_y)$, i.e. a *uniform* per-time bound $\|\partial_y u(\cdot,t)\|_{L^1}\le C$. Under that uniform bound the cumulative budget is only $Ct$, and Theorem thm:main shows the $\dot H^{-1}$ norm decays at most polynomially. Moreover, these results bound the *geometric* mixing scale, which is not equivalent to the $\dot H^{-1}$ functional norm (finely oscillating scalar fields can have small geometric scale while their $\dot H^{-1}$ norm decays only algebraically); Theorem thm:main addresses the norm in which the problem's exponential decay is posed.

**Source 3 (numerical evidence, no proof).** "Numerical Evidence of Exponential Mixing by Alternating Shear Flows", arXiv:2111.00093: simulations of alternating horizontal/vertical wedge shears suggest fast mixing; it is not a rigorous statement about $\dot H^{-1}$ under uniform $W^{1,1}$ bounds and is not used here.

In summary, the known exponential-mixing constructions for shears all operate with an $L^1$-in-time gradient budget (equivalently unbounded per-time $W^{1,1}$ norms) and with geometric-scale diagnostics; the problem's hypothesis class — uniformly bounded $W^{1,1}_y$ shear and the $\dot H^{-1}$ functional norm — admits only polynomial decay, exactly as proved in Theorem thm:main.

