# R8-F03: complete analytic sliver repair and T1

Author contribution, 2026-09-22. This is a mathematical candidate for the coordinator's stateless independent review, not that review's verdict. All work files are confined to `sliver-author/`.

## 1. Contract and result

Consider only the symmetric three-block family on `(0,1)`:

\[
-y''=\lambda\rho_{R,u}y,\qquad y(0)=y(1)=0,
\quad
\rho_{R,u}=\begin{cases}R,&0<x<u\text{ or }1-u<x<1,\\1,&u<x<1-u,\end{cases}
\]

where `R>=1` and `0<u<1/2`. Let `lambda_1<lambda_2` be its first two Dirichlet eigenvalues, and put

\[
\varepsilon=R^{-1/2},\quad \ell=\tfrac12-u,\quad w=u/\varepsilon,
\quad G(R,u)=R(\lambda_2-\lambda_1).
\]

The new whole-region bound is

\[
\boxed{G(R,u)\ge
 \frac{\pi^2}{2\varepsilon(w+\ell)(w+\varepsilon\ell)}}.\tag{1}
\]

It holds for **every** `R>=1, 0<u<1/2`, including `w<1/2`. In particular,

\[
\boxed{R\ge1500,\quad 0<w\le2
 \quad\Longrightarrow\quad G(R,u)>\frac{15\pi^2}{4}>25.}\tag{2}
\]

Thus the requested finite threshold `1500` is retained, with a stronger margin. No numerical grid, curved-region cover, or asymptotic tail certificate is required. The bounds also imply that the infimum of `G` over `0<w<=2` diverges at least as a constant times `sqrt(R)`.

Let `a(u)` be the unique root in `(pi/2,pi)` of

\[
\tan a=-a\ell/u,\qquad
\bar D(u)=\frac{a(u)^2-\pi^2/4}{u^2},\quad
m_R=\inf_{0<u<1/2}(\lambda_2-\lambda_1).
\]

The retained T2 structure gives a unique minimizer `u*`, with

\[
M:=\bar D(u^*)<3\pi^2.
\]

The repaired large-`w` inequality and (2) imply the complete T1 conclusions:

\[
\boxed{\lim_{R\to\infty}Rm_R=M.}\tag{3}
\]

For every sequence `R_j -> infinity`, and every `u_j in (0,1/2)` with

\[
0\le D_{R_j}(u_j)-m_{R_j}\le\eta_j,
\qquad \eta_j\ge0,\quad R_j\eta_j\longrightarrow0,
\]

one has `u_j -> u*`. In particular, the original error `eta_j=R_j^(-2)` is allowed. The optimal-value error also obeys `0<=Rm_R-M=O(R^(-1))`; no coefficient for this optimized error, nor rate for the minimizing parameter, is asserted here.

Sections 2-4 prove the new bound. Sections 5-7 close T1. Appendix A gives the directly necessary large-`w` reasoning with deliberately coarse elementary constants, already derived before the coordinator's subsequent division of the scalar verification work. Appendix B records the analytic T2 structure used here. These appendices make the mathematical argument self-contained; they are not a second independent scalar-certificate verdict. T3 root isolation and high-precision enclosures remain assigned elsewhere.

## 2. Pole-free spectral phase, with root identity

For `k=sqrt(lambda)>0`, take the solution normalized by `y(0)=0, y'(0)=1`. At the interface,

\[
\theta=wk,\quad z=\ell k,\qquad
\bigl(y'(u),ky(u)\bigr)=(\cos\theta,\varepsilon\sin\theta).
\]

Propagation across the light interval to `L=1/2` gives

\[
\begin{split}
y'(L)&=\cos\theta\cos z-\varepsilon\sin\theta\sin z,\\
ky(L)&=\varepsilon\sin\theta\cos z+\cos\theta\sin z.
\end{split}\tag{4}
\]

There has been no division by a sine or cosine. Define the continuous real-valued angle

\[
A_\varepsilon(0)=0,\qquad
A_\varepsilon(\theta)=\arg_{\rm continuous}
 (\cos\theta+i\varepsilon\sin\theta),\quad \theta\ge0.
\]

The vector never vanishes, and

\[
A_\varepsilon'(\theta)=
\frac{\varepsilon}{\cos^2\theta+\varepsilon^2\sin^2\theta}>0,
\quad A_\varepsilon(\pi/2)=\pi/2,\quad A_\varepsilon(\pi)=\pi.
\]

Equivalently the derivative and initial value define this unwrapped angle by integration. The phase at `L` is

\[
\Phi(k)=\ell k+A_\varepsilon(wk).\tag{5}
\]

It is strictly increasing from zero to infinity. Equation (4) says that the first half-interval Dirichlet-Neumann root is exactly

\[
\Phi(k_1)=\pi/2,
\]

and the first half-interval Dirichlet-Dirichlet root is exactly

\[
\Phi(k_2)=\pi.
\]

These roots give the first and second eigenvalues of the original full Dirichlet problem, not merely arbitrary roots of matching equations. Indeed, the spatial angle of `(y',ky)` increases strictly: in the heavy interval it is `A_epsilon(k sqrt(R) x)`, and in the light interval it increases linearly with slope `k`. Thus both half-interval solutions are positive in their interiors. The Neumann solution reflects evenly to a strictly positive full eigenfunction. The Dirichlet solution reflects oddly and has exactly one full-interval interior zero, at the midpoint. The Sturm oscillation theorem for a positive piecewise constant weight identifies these as eigenfunctions 1 and 2. In particular `lambda_i=k_i^2`.

This agrees with the coordinator's independently authored matching/mode explanation in the frozen `inputs/coordinator-math.md`. The additional ingredient specific to this sliver proof is the quantitative derivative bound below.

## 3. A lower bound for the gap from phase speed

Since `0<epsilon<=1`,

\[
\Phi'(k)=\ell+
\frac{w\varepsilon}{\cos^2(wk)+\varepsilon^2\sin^2(wk)}
\le\ell+\frac w\varepsilon.\tag{6}
\]

Integrating over the two actual eigenvalue roots gives

\[
 k_2-k_1\ge\frac{\pi}{2(\ell+w/\varepsilon)}.\tag{7}
\]

Also `Phi(pi/(2w))>pi/2`, so `0<w k_1<pi/2`. On this first branch,

\[
A_\varepsilon(\theta)=\arctan(\varepsilon\tan\theta)
\le\theta\qquad(0\le\theta<\pi/2).
\]

Consequently

\[
\pi/2=\Phi(k_1)\le(\ell+w)k_1,
\qquad k_1\ge\frac{\pi}{2(\ell+w)}.\tag{8}
\]

Combining (7) and (8), without any assumption on the second heavy phase,

\[
\begin{split}
G&=\varepsilon^{-2}(k_2-k_1)(k_2+k_1)\\
&\ge\varepsilon^{-2}\,
\frac{\pi}{2(\ell+w/\varepsilon)}\,
\frac{\pi}{\ell+w}
=\frac{\pi^2}{2\varepsilon(w+\ell)(w+\varepsilon\ell)}.
\end{split}
\]

This proves (1). In particular, no `theta_2>pi/2` condition has entered this argument. For example, the variational bound `lambda_2<=4pi^2` at `R=1600,u=1/1600` gives `theta_2<=pi/20`, which is entirely consistent with (1).

## 4. Exact finite-threshold estimate and coverage

Assume `R>=1500, 0<w<=2`. The elementary inequalities `38^2<1500` and `ell<1/2` give

\[
\varepsilon<1/38,\quad w+\ell<5/2,\quad
w+\varepsilon\ell<2+1/76.
\]

Thus (1) yields

\[
G>\frac{2888}{765}\pi^2>\frac{15}{4}\pi^2,
\]

where the last comparison is the integer inequality `11552>11475`. Since `pi>3`, this is greater than `135/4>25`. It is also greater than `3pi^2`, which will remove any T3 numerical dependency from T1.

The actual quantifiers are `R>=1500` and `0<u<=2/sqrt(R)` (with the original `u<1/2`). They are **not** the larger constant interval `0<u<=2/sqrt(1500)` for every large `R`; the old script's docstring conflated these sets.

The proof covers arbitrarily small positive `w`, both sides and the exact value of `w=1/2`, both curved boundaries `w_c(R)` and `w_cap(R)`, every finite `R>=1500`, and the entire infinite `R` tail. The discarded rectangular-grid coverage is irrelevant to the replacement proof. No old certificate has been rerun or rehabilitated.

## 5. Necessary large-w input, with its scope explicit

For `R>=1500, w>=2`, the repaired Lemma A'' gives

\[
G(R,u)\ge\bar D(u).\tag{9}
\]

The restriction is essential: only here do we invoke the second-phase branch `pi/2<theta_2<pi`. It follows from (4)-(5), or from the coordinator's half-mode positivity argument. It is not a global branch assumption.

For completeness, Appendix A below actually establishes the slightly stronger statement

\[
G(R,u)>\bar D(u)+\frac{\ell}{R u^3}.\tag{10}
\]

It uses only exact elementary inequalities, with no interval-library or floating-point assumptions. The coordinator may keep the original Lemma A'' numerical constants once Popper's separate scalar work is integrated; T1 needs only (9). The supporting derivation here does not assert that Popper's work or any independent review has passed.

## 6. Fixed-u convergence sufficient for T1

Fix any `u in (0,1/2)` and set `b=ell/u`. Eventually `R>=1500,w>=2`. The branch construction and matching give

\[
0<\delta_1=\pi/2-\theta_1
\le\varepsilon\tan(\tfrac\pi2 b\varepsilon).
\]

Writing `def_1=pi^2/4-theta_1^2` and `def_2=a(u)^2-theta_2^2`, Appendix A gives `0<=def_2<=def_1`. Therefore

\[
0\le G(R,u)-\bar D(u)
=\frac{\mathsf{def}_1-\mathsf{def}_2}{u^2}
\le\frac{\pi\varepsilon}{u^2}
\tan(\tfrac\pi2 b\varepsilon)=O_u(R^{-1}).\tag{11}
\]

This proves the required pointwise convergence, and agrees with the coordinator's stronger analytic expansion. For an explicit elementary upper bound, when

\[
R\ge R_0(u):=\max\{1500,4/u^2,10b^2\},
\]

the tangent argument is less than `1/2` (use `pi^2<10`), and `tan x<=2x` for `0<=x<=1/2` gives

\[
0\le G(R,u)-\bar D(u)\le\frac{\pi^2\ell}{Ru^3}.\tag{12}
\]

Here `tan x<=2x` follows from `sin x<=x` and `cos x>=1-x^2/2>=7/8>1/2`. Neither (11) nor (12) claims uniformity as `u` approaches an endpoint.

## 7. T1: both inequalities and all near-minimizers

Appendix B recalls the analytic T2 facts: unique minimizer `u*`, strict decrease then strict increase, and endpoint limits `+infinity` and `3pi^2`. In particular `M= Dbar(u*)<3pi^2`. No assertion `M<25` and no high-precision T3 enclosure is needed.

For every `R>=1500` and every `u in (0,1/2)` there are two exhaustive cases:

- If `w<=2`, (2) gives `G>15pi^2/4>3pi^2>M`.
- If `w>=2`, (9) gives `G>=Dbar(u)>=M`.

It follows that `Rm_R=inf_u G(R,u)>=M`. Conversely, for the single fixed point `u*`, (11) gives `G(R,u*) -> M`, and `Rm_R<=G(R,u*)`. This proves (3), with both inequalities accounted for. Equation (12) at `u*` also gives the stated optimal-value error bound for all `R>=R_0(u*)`.

Now let `R_j,u_j,eta_j` obey the quantifiers in Section 1. Then

\[
Rm_R\le G(R,u_j)\le Rm_R+R\eta_j
\]

with `R=R_j`, so `G(R_j,u_j)->M`. If `w_j<=2` infinitely often, those terms exceed `15pi^2/4>M`, a contradiction. Thus `w_j>2` eventually, and

\[
M\le\bar D(u_j)\le G(R_j,u_j)\longrightarrow M.
\]

Any subsequence of `u_j` has a further subsequence converging in `[0,1/2]`. A limit of zero would force `Dbar(u_j)->+infinity`, contradicting its finite limit `M`. A limit of `1/2` would force `Dbar(u_j)->3pi^2>M`, also a contradiction. Every remaining limit is interior; continuity gives `Dbar(u_infinity)=M`, and T2 uniqueness forces `u_infinity=u*`. Thus the entire sequence converges to `u*`. The two endpoint exclusions are separate; the erroneous old comparison `+infinity<3pi^2` is not used.

## Appendix A. A self-contained check of the large-w inference

This appendix supports Section 5. It neither uses nor validates the old float certificates. The coarse constants here may be omitted on integration if the coordinator retains the separately repaired original constants.

### A.1 Branch, brackets and deficit identity

Assume `R>=1500,w>=2`, and write

\[
c=\ell/w=\varepsilon\ell/u=\frac1{2w}-\varepsilon,
\quad 0<c\le\tfrac14-\varepsilon,
\quad\alpha=\varepsilon c=\frac{\ell}{Ru}.
\]

By the phase identity, `theta_1=w k_1<pi/2` always. Moreover

\[
\Phi(\pi/(2w))=\pi/2+c\pi/2<\pi,
\qquad \Phi(\pi/w)=\pi+c\pi>\pi,
\]

so `pi/2<theta_2<pi`. Initially `z_2=c theta_2<pi/4`, hence all trigonometric divisions below are permitted. Set

\[
\delta_1=\pi/2-\theta_1>0,\quad
\delta_2=\theta_2-\pi/2>0.
\]

From (4),

\[
\tan\delta_1=\varepsilon\tan(c\theta_1),\qquad
\tan\delta_2=\varepsilon\cot(c\theta_2).\tag{A1}
\]

Since `cot z<1/z` on `(0,pi/2)`,

\[
\delta_2\le\frac{\varepsilon}{c\theta_2}
\le\frac{2\varepsilon}{\pi c},
\quad
z_2=c(\pi/2+\delta_2)
\le\frac\pi8-\varepsilon(\pi/2-2/\pi)<\frac\pi8.\tag{A2}
\]

This short estimate replaces the more elaborate monotonicity argument in the original phase bracket. The inequality `cot z<1/z` follows from `sin z-z cos z=integral_0^z t sin t dt>0`.

Put `t=a(u)` and `v=u/ell`. The function `H(s)=-s cot s` is strictly increasing on `(pi/2,pi)` and `H(t)=v`. Equation (A1) gives

\[
H(\theta_2)=\varepsilon\theta_2\cot(c\theta_2)<\varepsilon/c=v,
\]

so `theta_2<t`. Thus

\[
\mathsf{def}_1=\pi^2/4-\theta_1^2>0,
\quad \mathsf{def}_2=t^2-\theta_2^2>0,
\quad G-\bar D=(\mathsf{def}_1-\mathsf{def}_2)/u^2.\tag{A3}
\]

### A.2 The first deficit exceeds `4 alpha`

As `z_1=c theta_1<pi/8`, `tan(pi/8)=sqrt(2)-1<1/2`, and `epsilon<1/38`,

\[
0<\delta_1<1/76,\quad
\theta_1>3/2-1/76>7/5,
\quad \alpha<1/152.
\]

Using `tan z>=z`, `arctan x>=x-x^3/3` for `x>=0`, and `pi^2<10`,

\[
\delta_1\ge\arctan(\alpha\theta_1)
\ge\alpha\theta_1(1-\pi^2\alpha^2/12)
>\frac{99}{100}\alpha\theta_1.
\]

Here `1-10/(12*152^2)>99/100`. Consequently

\[
\mathsf{def}_1=(\pi/2+\theta_1)\delta_1
>\frac{29}{10}\frac75\frac{99}{100}\alpha
=\frac{20097}{5000}\alpha>4\alpha.\tag{A4}
\]

### A.3 Two elementary upper bounds

For `0<z<=pi/8`, write `r(z)=1/z-cot z`. The integral identity used above, `sin t<=t`, and `sin z>=z-z^3/6` give

\[
0<r(z)=\frac{\int_0^z t\sin t\,dt}{z\sin z}
\le\frac{z}{3(1-z^2/6)}
<\frac{64}{187}z<\frac7{20}z.\tag{A5}
\]

Thus we may take the rational constant `C=7/20`. No cotangent Laurent series or floating transcendental enclosure is needed.

For `pi/2<t<pi` and `v=-t cot t`,

\[
B(t):=\frac{2t^4}{t^2+v^2+v}
=\frac{2t^3\sin^2t}{t-\sin t\cos t}
<2(t\sin t)^2\le8.\tag{A6}
\]

For completeness, prove the last inequality. If `t<=2`, then `t sin t<=2`. If `t>=2`, the function `q(t)=t sin t` is concave on `[2,pi)` because `q''=2cos t-t sin t<0`. The alternating Taylor tails give the exact upper bounds

\[
\sin2\le2-\frac{2^3}{3!}+\frac{2^5}{5!}-\frac{2^7}{7!}+\frac{2^9}{9!}
=\frac{2578}{2835}<\frac{91}{100},
\]

\[
\cos2\le1-\frac{2^2}{2!}+\frac{2^4}{4!}-\frac{2^6}{6!}+\frac{2^8}{8!}
=-\frac{131}{315}<-\frac25.
\]

Using the tangent line to this concave function and `pi<22/7`,

\[
q(t)\le q(2)+q'(2)(t-2)
<\frac{91}{50}+\frac{11}{100}\frac87
=\frac{681}{350}<2.
\]

This proves (A6) on the full open interval. The only bounds on pi here and elsewhere are the classical elementary `3<pi<22/7`, giving `pi^2<10`.

### A.4 The second deficit is less than `3 alpha`

Write `theta=theta_2`, `psi=t-theta in (0,pi/2)`,

\[
A=\tan(t-\pi/2)=v/t,
\quad B=\tan(\theta-\pi/2)=\varepsilon\cot(c\theta).
\]

These symbols `A,B` denote scalars only in this paragraph; `B(t)` remains the function in (A6). Since

\[
A-B=-\frac{v\psi}{t\theta}+\varepsilon r(c\theta),
\qquad \tan\psi=\frac{A-B}{1+AB},
\]

and `tan psi>=psi`,

\[
\psi\le\frac{\varepsilon r(c\theta)}{1+AB+v/(t\theta)}.
\]

By (A5),

\[
\varepsilon r(c\theta)\le C\alpha\theta,
\quad
AB\ge\frac{v^2}{t\theta}-C\varepsilon^2\frac\theta t.
\]

Define

\[
D_0=1+\frac{v(v+1)}{t\theta}\ge1,
\quad d=C\varepsilon^2\theta/t<1/1000.
\]

For fixed `t,v`, the function `theta(t+theta)/D_0` increases with `theta`: its numerator increases and its positive denominator decreases. Since `theta<=t`, its value is at most `B(t)<=8`. Hence

\[
\mathsf{def}_2=(t+\theta)\psi
\le C\alpha\frac{\theta(t+\theta)}{D_0-d}
<\frac7{20}\frac{1000}{999}\,8\alpha
=\frac{2800}{999}\alpha<3\alpha.\tag{A7}
\]

The denominator perturbation bound uses `C/1500=7/30000<1/1000`; it never drops a negative term from a denominator without compensating for it. Combining (A3), (A4), and (A7) yields

\[
G-\bar D>\alpha/u^2=\ell/(Ru^3),
\]

proving (10), and therefore the necessary (9).

## Appendix B. The retained analytic T2 facts

This is a recap of the sign argument in the frozen source and supplied analytic supplement, included to state the entire T1 dependency. It is not T3 root isolation.

The parametrization

\[
u(a)=\frac{a}{2(a-\tan a)},\quad \pi/2<a<\pi,
\quad
u'(a)=\frac{a-\sin a\cos a}{2\cos^2a\,(a-\tan a)^2}>0
\]

maps this interval bijectively onto `(0,1/2)`. Use `Q` below to avoid confusing the one-variable sign function with the spectral gap `G(R,u)`:

\[
Q(a)=8a^3\sin^2a-\pi^2(2a-\sin2a),\quad
J(a)=4a^3\cot a+6a^2-\pi^2,
\]
\[
h(a)=3+3a\cot a-a^2\csc^2a.
\]

Direct differentiation gives

\[
J'(a)=4a h(a),\quad Q'(a)=4\sin^2a J(a),
\]

\[
h'(a)\sin^3a=3\cos a\sin^2a-5a\sin a+2a^2\cos a<0.
\]

Since `h(pi/2)=3-pi^2/4>0` and `h -> -infinity`, `h` has exactly one zero. Consequently `J` first increases and then decreases; `J(pi/2)=pi^2/2>0` and `J -> -infinity` give exactly one zero of `J`. Consequently `Q` first increases from `Q(pi/2)=0` and then decreases to `Q(pi)=-2pi^3`; it has exactly one interior zero `a*`, changing from positive to negative there.

Differentiating the formula for `Dbar(u(a))` gives

\[
\bar D'(u(a))=
-\frac{4(a-\tan a)^3}{a^3(2a-\sin2a)}Q(a).
\]

The prefactor before `Q` is strictly negative. Thus `u*=u(a*)` is the unique critical point and strict global minimizer, with strict decrease to its left and strict increase to its right. The source's `S(u)` equals this derivative: differentiate `tan a+(ell/u)a=0`, and substitute `I_2=u(1+(ell/u)cos^2a)/2` into its definition. No eigenvalue perturbation identity beyond this direct differentiation is required.

As `u->1/2`, `a->pi` and `Dbar(u)->3pi^2`. As `u->0`, write `a=pi/2+d`. The equation `a tan d=u/ell` implies `d/u ->4/pi`, and hence `u Dbar(u)->4`; in particular `Dbar(u)->+infinity`. Strict increase on `(u*,1/2)` gives `M<3pi^2`, as used in Section 7.

## 8. Integration, evidence and remaining scope

`sliver_t1_fragment.tex` is the insertable contribution. It replaces the old deep-sliver proof and T1 proof, and contains its own pole-free phase derivation. It references the target document's repaired `thm:lemAdp` and retained `thm:T2`; Sections 5-6 and Appendices A-B above discharge those dependencies analytically. The coordinator owns the corresponding global phase section, fixed-u expansion, scalar-certificate integration, navigation and repository edits.

On integration:

1. Replace the original `lem:sliver` and `thm:T1` blocks with the corresponding fragment blocks. The fragment deliberately preserves those two labels, so remove the old definitions first.
2. Keep the coordinator's restricted large-w mode justification and the repaired A'' argument. Preserve a proof of T2, not merely its numerical graph.
3. Replace abstract/introduction claims that deep-sliver coverage depends on script 16 by the new whole-region bound. State that T1 uses `M<3pi^2`, so it is independent of T3 numerical certification.
4. Mark script 16 and other historical float PASS claims as superseded evidence, without changing their sealed bytes. Do not present them as current proof.

Author checks are preserved under `logs/`, with actual process commands, script hashes, stdout/stderr hashes, and exit codes in `logs/execution_receipts.json`. They comprise 16 exact rational comparisons, 120 high-precision exploratory sliver points including old uncovered strips and arbitrarily small sample `w`, and 84 exploratory large-w deficit points. Both commands returned exit code 0. The samples are not an interval certificate or a substitute for Sections 2-7. The observed minimum over the chosen sliver samples was about `91.7263`; the proof does not use this number.

The SHA-256 read set is `input_manifest.json`; the coordinator's mathematical candidate was frozen locally when received. `output_manifest.json` binds the final author files and records current frozen-source comparisons. The input source locators are: original phase declaration lines 113-146; large-w chain 148-352; discarded sliver proof 354-367 and certificate narrative 514-542; retained T2 369-432; original T1 459-501. The audit's R8-F03 and R8-F04 sections and the complete supplied analytic supplement were read. The old script was read, not executed.

There is no remaining analytic gap in T1 **as stated in this author candidate**, subject to the coordinator's independent verification. This statement is confined to the symmetric three-block family. It does not certify the unrestricted density optimization problem, T3 high-precision values, historical interval software, round 7, a Lean formalization, or library acceptance. Those are separate scopes, not implicit consequences of the new bound.
