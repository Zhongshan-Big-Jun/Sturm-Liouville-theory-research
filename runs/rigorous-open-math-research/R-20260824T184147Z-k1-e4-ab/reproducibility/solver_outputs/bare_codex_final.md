COMPLETE_PROOF

The conjecture is true. The normalized backward limit exists, is the unique normalized minimal solution, and has the exact representation

\[
\boxed{\mu_j^*
 =2e(2j)!\sum_{r=j+2}^{\infty}
 \frac{r-j-1}{(2r-1)!}}
\qquad(j\ge0).
\]

Consequently,

\[
\boxed{\lim_{j\to\infty}j^3\mu_j^*=\frac e4}.
\]

## 1. Exact factorization of the recurrence

Set

\[
a_j=2j(2j-1),\qquad
c_j=\frac{j}{j-1},\qquad
b_j=2j(2j-3).
\]

Then direct algebra gives

\[
P_j=2a_j+c_j,
\]

\[
Q_j=(a_j+c_j)a_{j-1}+b_j,
\]

and

\[
R_j=b_ja_{j-2}.
\]

Indeed,

\[
(a_j+c_j)a_{j-1}+b_j
=4j(j-1)(2j-1)(2j-3)+4j(2j-3).
\]

For any solution of (R), define

\[
d_j=\mu_j-a_j\mu_{j-1}\qquad(j\ge1).
\]

The recurrence is then equivalent, for \(j\ge3\), to

\[
d_j=(a_j+c_j)d_{j-1}-b_jd_{j-2}. \tag{1}
\]

Let

\[
h_j=(2j)!,\qquad \rho_j=\frac{d_j}{h_j}.
\]

Since \(h_j=a_jh_{j-1}\), equation (1) becomes

\[
\rho_j=(1+t_j)\rho_{j-1}-t_j\rho_{j-2},
\qquad
t_j=\frac1{(2j-1)(2j-2)}.
\]

Thus

\[
\rho_j-\rho_{j-1}
=t_j(\rho_{j-1}-\rho_{j-2}). \tag{2}
\]

Define

\[
S_j=\sum_{r=1}^{j}\frac1{(2r-1)!}.
\]

Because

\[
\frac{S_j-S_{j-1}}{S_{j-1}-S_{j-2}}
=\frac1{(2j-1)(2j-2)},
\]

all solutions of (2) have the form

\[
\rho_j=A+BS_j. \tag{3}
\]

This also proves that no solutions were lost in the factorization.

## 2. Complete description and uniqueness of the minimal solution

Put

\[
u_j=\frac{\mu_j}{(2j)!}.
\]

From the definition of \(d_j\),

\[
u_j-u_{j-1}=\rho_j.
\]

Consequently every solution of (R) has the form

\[
u_j=C+Aj+B\sum_{m=1}^{j}S_m. \tag{4}
\]

Let

\[
s=\sum_{r=1}^{\infty}\frac1{(2r-1)!}=\sinh 1
\]

and

\[
T_m=s-S_m
=\sum_{r=m+1}^{\infty}\frac1{(2r-1)!}.
\]

The convergent quantity

\[
L=\sum_{m=1}^{\infty}T_m
\]

allows (4) to be written as

\[
u_j=(A+Bs)j+(C-BL)+B\,U_j, \tag{5}
\]

where

\[
U_j=\sum_{m=j+1}^{\infty}T_m.
\]

The sums contain only nonnegative terms, so rearrangement gives

\[
U_j
=\sum_{r=j+2}^{\infty}
 \frac{r-j-1}{(2r-1)!}. \tag{6}
\]

In particular \(U_j\to0\).

A solution satisfies

\[
\mu_j=o((2j)!)
\]

if and only if \(u_j\to0\). By (5), this requires

\[
A+Bs=0,\qquad C-BL=0.
\]

Hence the space of subfactorial solutions is one-dimensional and is spanned by

\[
\phi_j=(2j)!U_j. \tag{7}
\]

Every linearly independent solution has

\[
\frac{\mu_j}{(2j)!}=pj+q+o(1)
\]

with \((p,q)\ne(0,0)\). Therefore \(\phi_j/\mu_j\to0\). Thus (7) is also the unique Perron-minimal solution up to multiplication.

Its zeroth component is

\[
\begin{aligned}
\phi_0
&=\sum_{r=2}^{\infty}\frac{r-1}{(2r-1)!}\\
&=\frac12\left(
\sum_{r=2}^{\infty}\frac1{(2r-2)!}
-\sum_{r=2}^{\infty}\frac1{(2r-1)!}
\right)\\
&=\frac12\bigl((\cosh1-1)-(\sinh1-1)\bigr)
=\frac1{2e}. \tag{8}
\end{aligned}
\]

It is positive, so normalization at \(j=0\) is legitimate. Dividing (7) by (8) gives

\[
\mu_j^*=2e(2j)!U_j,
\]

which is the asserted exact formula.

## 3. Exact finite backward approximants

For the \(N\)-th backward solution set

\[
u_j^{(N)}=\frac{\mu_j^{(N)}}{(2j)!}.
\]

The terminal data imply

\[
u_{N-1}^{(N)}=u_N^{(N)}=0,\qquad
u_{N+1}^{(N)}=\frac1{(2N+2)!}.
\]

Hence

\[
\rho_N^{(N)}=0,\qquad
\rho_{N+1}^{(N)}=\frac1{(2N+2)!}.
\]

Writing \(\rho_j^{(N)}=A_N+B_NS_j\) and subtracting these two equations yields

\[
\frac{B_N}{(2N+1)!}=\frac1{(2N+2)!},
\qquad
B_N=\frac1{2N+2}.
\]

For \(0\le j\le N-1\),

\[
\begin{aligned}
u_j^{(N)}
&=\frac1{2N+2}\sum_{m=j+1}^{N}(S_N-S_m)\\
&=\frac1{2N+2}
  \sum_{r=j+2}^{N}\frac{r-j-1}{(2r-1)!}.
\end{aligned}
\]

Therefore

\[
\boxed{
\mu_j^{(N)}
=\frac{(2j)!}{2N+2}
 \sum_{r=j+2}^{N}\frac{r-j-1}{(2r-1)!}}
\qquad(0\le j\le N-1). \tag{9}
\]

In particular,

\[
\mu_0^{(N)}
=\frac1{2N+2}\sum_{r=2}^{N}\frac{r-1}{(2r-1)!}>0
\]

for every \(N\ge3\), not merely eventually.

For fixed \(k\) and \(N\ge k+2\), (9) gives

\[
\widehat\mu_k^{(N)}
=(2k)!
\frac{\displaystyle\sum_{r=k+2}^{N}
             \frac{r-k-1}{(2r-1)!}}
     {\displaystyle\sum_{r=2}^{N}
             \frac{r-1}{(2r-1)!}}.
\]

Both positive factorial series converge, and the denominator tends to \(1/(2e)\) by (8). Hence

\[
\lim_{N\to\infty}\widehat\mu_k^{(N)}
=2e(2k)!\sum_{r=k+2}^{\infty}
 \frac{r-k-1}{(2r-1)!}.
\]

This proves the existence of every fixed-index limit and identifies it with the unique normalized minimal solution.

## 4. Evaluation of the asymptotic constant

Writing \(r=j+\ell+1\) in the exact formula gives

\[
\mu_j^*
=2e\sum_{\ell=1}^{\infty}
 \ell\,\frac{(2j)!}{(2j+2\ell+1)!}. \tag{10}
\]

The first term is

\[
\frac{2e}{(2j+1)(2j+2)(2j+3)},
\]

so

\[
j^3\frac{2e}{(2j+1)(2j+2)(2j+3)}
\longrightarrow \frac e4. \tag{11}
\]

For the remainder, put \(x_j=(2j+1)^{-1}\). Since every factor in the factorial quotient is at least \(2j+1\),

\[
\frac{(2j)!}{(2j+2\ell+1)!}
\le x_j^{2\ell+1}.
\]

Thus

\[
\begin{aligned}
0&\le
j^3\sum_{\ell=2}^{\infty}
 \ell\frac{(2j)!}{(2j+2\ell+1)!}\\
&\le
j^3x_j^5
\left(
\frac{2}{1-x_j^2}
+\frac{x_j^2}{(1-x_j^2)^2}
\right)
=O(j^{-2}),
\end{aligned}
\]

which tends to zero. Combining this with (11) proves

\[
\boxed{\lim_{j\to\infty}j^3\mu_j^*=\frac e4}.
\]

## 5. Index and sign audit

At \(j=3\),

\[
a_3=30,\quad c_3=\frac32,\quad b_3=18,\quad
a_2=12,\quad a_1=2.
\]

Therefore

\[
P_3=2a_3+c_3=\frac{123}{2},
\]

\[
Q_3=(a_3+c_3)a_2+b_3=396,
\qquad
R_3=b_3a_1=36.
\]

These agree exactly with the stated coefficients. In particular \(R_3\ne0\), so the last backward step determining \(\mu_0^{(N)}\) is valid.

At the upper terminal end, (9) gives

\[
\mu_{N-2}^{(N)}
=\frac{(2N-4)!}{(2N+2)(2N-1)!}
=\frac1{R_{N+1}},
\]

because

\[
R_{N+1}
=(2N+2)(2N-2)(2N-1)(2N-3).
\]

Thus the \(j=N+1\) recurrence reads

\[
\mu_{N+1}^{(N)}
=R_{N+1}\mu_{N-2}^{(N)}=1,
\]

with the prescribed zeros at \(N\) and \(N-1\). This confirms the terminal indexing and all signs.

All rearranged infinite sums above have nonnegative terms; hence Tonelli’s theorem applies directly. Every limiting series is absolutely convergent. No derivative or generating-function interchange is used.

Citations: none required; the argument is self-contained apart from the elementary exponential-series identities for \(\sinh1\) and \(\cosh1\).

Remaining gaps: none.

Full resolution: yes.