# Agent C - O3b Boundary Bounds: Deliverable

Run: R-20260805T000000Z-gapn1-a1b2c3
Date: 2026-08-05
Obligation: O3b (boundary of the 2-parameter barrier/well families)
Subclaims: (1) 2-block bounds 3*pi^2/R < D(t) < 3*pi^2; (2) symmetric critical
configs beat the constants; (3) [bonus] direct 2-parameter symmetry b = 1 - a.

## Verdicts (summary)

| Subclaim | Verdict | One-line reason |
|---|---|---|
| 1. 2-block bounds | PROVED | full proof via phase coordinates; three regimes; both orientations |
| 2. symmetric critical values | PARTIAL | all-R proof conditional on O2 sign structure; R->1+ first order proved (explicit c ~ 2.0812 > 0); R->inf limits verified (4*pi^2, 24.943866...) |
| 3. direct symmetry b = 1 - a | PARTIAL | reduction to uniqueness (reflection) + strong numerics; core implication unproved |

---

## 0. Setup and the phase-coordinate reduction

Problem: Dirichlet string on [0,1], -y'' = lambda*rho*y, y(0)=y(1)=0, with a
two-block density rho.  Heavy-right (HR): rho = 1 on [0,t], rho = R on (t,1].
Heavy-left (HL): the mirror.  R > 1, t in (0,1).  D(t) = lambda_2(t) - lambda_1(t).

Define mu := sqrt(R) > 1, and for each t in (0,1) put

    c := mu*(1-t)/t  in (0, +infinity),   t = mu/(mu + c).

Let theta(x) := arctan(mu*tan(x)) taken on the continuous branch
(theta(0) = 0, theta(x + pi) = theta(x) + pi), and let x_1(mu,c) < x_2(mu,c)
be the first two roots of

    theta(x) + c*x = k*pi,   k = 1, 2.

Proposition 0.1 (reduction).  For the HR two-block string,
lambda_k = x_k^2*(mu + c)^2/mu^2 and D(t) = (mu+c)^2*(x_2^2 - x_1^2)/mu^2.
For HL, D_HL(t) = D_HR(1 - t).

Proof.  On [0,t] the solution with y(0) = 0 is y = A*sin(s*x); on (t,1] it is
y = C*sin(s*mu*x) + D*cos(s*mu*x), s = sqrt(lambda).  Continuity of y and y'
at t together with y(1) = 0 give the secular equation

    sin(s*t)*cos(s*mu*(1-t)) + (1/mu)*cos(s*t)*sin(s*mu*(1-t)) = 0.

Dividing by cos(st)cos(s*mu*(1-t)) (nonzero at the roots) yields
tan(s*mu*(1-t)) = -mu*tan(s*t), i.e. theta(s*t) + s*mu*(1-t) = k*pi on the
continuous branch.  With x = s*t and c = mu*(1-t)/t this is theta(x) + c*x = k*pi
and s = x*(mu + c)/mu, giving the formula.  The HL claim is the mirror image
x -> 1 - x, under which D is invariant.  QED.

Consequence.  Subclaim 1 is equivalent to: for all mu > 1 and all c > 0,

    3*pi^2  <  W(mu,c) := (mu + c)^2*(x_2^2 - x_1^2)  <  3*pi^2*mu^2.      (Eq W)

Both endpoints are attained only as limits: as c -> 0 (t -> 1), x_k -> k*pi,
W -> 3*pi^2*mu^2, D -> 3*pi^2; as c -> +infinity (t -> 0), x_k ~ k*pi/(c+mu),
W -> 3*pi^2, D -> 3*pi^2/mu^2 = 3*pi^2/R.

Basic facts used throughout.  theta is C^1 on (0,2*pi) with
theta(0)=0, theta(pi/2)=pi/2, theta(pi)=pi, theta(3*pi/2)=3*pi/2, theta(2*pi)=2*pi,
strictly increasing, and

    theta'(x) = mu*(1 + tan^2 x)/(1 + mu^2*tan^2 x)  in  [1/mu, mu],

with theta' = mu exactly at x in {0, pi, 2*pi} and theta' = 1/mu only in the
limit |tan x| -> infinity.  On (0,pi/2) and (pi,3*pi/2) theta is concave (above
its chords, so theta(x) >= x there); on (pi/2,pi) and (3*pi/2,2*pi) it is convex
(below its chords, so theta(x) <= x there).  Finally x_k'(c) = -x_k/(theta'(x_k)+c) < 0,
so x_1, x_2 are strictly decreasing in c, and x_1 = pi/2 iff c = 1,
x_2 = 3*pi/2 iff c = 1/3.

---

## 1. Subclaim 1: 3*pi^2/R < D(t) < 3*pi^2 for two-block densities (PROVED)

### 1.1 Lower bound (proof)

From theta(x_1) + c*x_1 = pi and theta' < mu strictly on (0,x_1]:

    pi = theta(x_1) + c*x_1 < mu*x_1 + c*x_1 = (mu + c)*x_1,       so x_1 > pi/(mu+c).

From the difference of the two secular equations, theta(x_2)-theta(x_1) =
pi - c*(x_2-x_1), and theta' < mu on a set of positive measure in (x_1,x_2):

    pi - c*(x_2-x_1) < mu*(x_2-x_1),                               so x_2 - x_1 > pi/(mu+c).

Hence x_1 + x_2 = 2*x_1 + (x_2-x_1) > 3*pi/(mu+c) and

    W = (mu+c)^2*(x_2-x_1)*(x_2+x_1) > (mu+c)^2 * [pi/(mu+c)] * [3*pi/(mu+c)] = 3*pi^2.  QED

### 1.2 Upper bound (proof)

Regime I (c >= 1).  Here x_1 in (0, pi/2], so theta(x_1) >= x_1 and
pi = theta(x_1) + c*x_1 >= (1+c)*x_1, i.e. x_1 <= pi/(1+c).  From theta' >= 1/mu:

    x_2 - x_1 <= pi/(c + 1/mu) = pi*mu/(1 + mu*c),
    x_2       <= 2*pi/(c + 1/mu) = 2*pi*mu/(1 + mu*c).

Therefore

    W <= (mu+c)^2 * [pi*mu/(1+mu*c)] * [2*pi*mu/(1+mu*c) + pi/(1+c)] =: 3*pi^2*mu^2*G(mu,c),

    G(mu,c) := (mu+c)^2/(3*mu^2) * [2*mu^2/(1+mu*c)^2 + mu/((1+mu*c)*(1+c))].

Claim: G(1,c) = 1 (immediate substitution) and dG/dmu < 0 for all mu > 1, c >= 1.
Direct differentiation gives the exact factorization (certified by sympy):

    dG/dmu = -(c+mu)*(6*c^3*mu^2 + 4*c^2*mu^2 + 3*c^2*mu - 5*c*mu^2 + c - 4*mu^2 - mu)
                 / (3*mu^2*(c+1)*(1+mu*c)^3).

With s := mu - 1 >= 0 and t := c - 1 >= 0 the numerator equals
-(s+t+2)*P(s,t) with

    P(s,t) = 6*s^2*t^3 + 22*s^2*t^2 + 21*s^2*t + s^2 + 12*s*t^3 + 47*s*t^2
             + 48*s*t + 4*s + 6*t^3 + 25*t^2 + 28*t + 4  >=  4  >  0,

and the denominator equals 3*(s+1)^2*(t+2)*(s*t+s+t+2)^3 > 0.  Hence
dG/dmu < 0 strictly for mu > 1, c >= 1, so G(mu,c) < G(1,c) = 1 and
W < 3*pi^2*mu^2.  QED

Regime II (1/3 <= c <= 1).  Then x_1 in [pi/2, pi] (convex branch, theta(x_1) <= x_1),
so pi = theta(x_1) + c*x_1 <= (1+c)*x_1, i.e. x_1 >= pi/(1+c); and
x_2 in [pi, 3*pi/2] (concave branch, theta(x_2) >= x_2), so
2*pi = theta(x_2) + c*x_2 >= (1+c)*x_2, i.e. x_2 <= 2*pi/(1+c).  Hence

    x_2^2 - x_1^2 <= (2*pi/(1+c))^2 - (pi/(1+c))^2 = 3*pi^2/(1+c)^2,

    W <= 3*pi^2*(mu+c)^2/(1+c)^2 < 3*pi^2*mu^2,

because (mu+c)^2 < mu^2*(1+c)^2 is equivalent to c < mu*c, i.e. mu > 1.  QED

Regime III (0 < c <= 1/3).  Here x_1 in (pi/2, pi) and x_2 in (3*pi/2, 2*pi).
Put eps_k := k*pi - x_k in (0, pi/2) and delta_k := c*x_k.  On these branches
theta(k*pi - eps) = k*pi - arctan(mu*tan(eps)), so the secular equations give

    tan(delta_k) = mu*tan(eps_k) > 0,   k = 1, 2.

Since delta_2 = c*x_2 in (0, 2*pi/3) and tan(delta_2) > 0, we have
delta_2 in (0, pi/2); hence s_2 > s_1 > 0 for s_k := tan(delta_k).  Also

    p_k := theta'(x_k) = mu*(1+tan^2 x_k)/(1 + mu^2*tan^2 x_k)
                        = (mu^2 + s_k^2)/(mu*(1 + s_k^2)).

Differentiate x_k(c): x_k' = -x_k/(p_k + c).  With U := x_2^2 - x_1^2,

    W' = 2*(mu+c)*U + (mu+c)^2*U',    U' = -2*x_2^2/(p_2+c) + 2*x_1^2/(p_1+c).

We show W' < 0.  Indeed W' < 0 is equivalent (divide by 2*(mu+c)) to

    U < (mu+c)*x_2^2/(p_2+c) - (mu+c)*x_1^2/(p_1+c).                (Eq C)

Now (mu+c)/(p_k+c) = f(s_k) with

    f(s) := mu*(mu+c)*(1+s^2)/(mu*(mu+c) + s^2*(1+mu*c)),   f(s)-1 = s^2*(mu^2-1)/(mu*(mu+c) + s^2*(1+mu*c)).

Hence RHS(Eq C) - U = (f(s_2)-1)*x_2^2 - (f(s_1)-1)*x_1^2
    = (mu^2-1)*[ h(s_2,x_2) - h(s_1,x_1) ],

where h(s,x) := s^2*x^2/(mu*(mu+c) + s^2*(1+mu*c)) is strictly increasing in
both arguments (partial derivatives > 0 for s, x > 0).  Since s_2 > s_1 and
x_2 > x_1, the bracket is positive, so W' < 0 on (0,1/3].  By continuity at
c = 0 (x_k -> k*pi), W(mu,c) < W(mu,0) = 3*pi^2*mu^2.  QED

Combining the three regimes proves the upper bound for all c > 0, and with
Section 1.1 and Proposition 0.1, Subclaim 1.  QED

Note on the "wiggles": W is not monotone in c (W' changes sign; f has exactly
two zeros with pattern -,+,-, so D has exactly one interior local max and one
interior local min), but both extremal values lie strictly inside the interval
(3*pi^2/R, 3*pi^2).  See the numerics below.

### 1.3 Numerical verification (Subclaim 1)

Direct transfer-matrix computation of D(t) (independent of the phase reduction),
both orientations, R in {1.05, 1.2, 1.5, 2, 4, 10, 100, 1e4}, t on 250-point
grids in [0.002, 0.998]:

- violations of the lower bound 3*pi^2/R: 0 of 4000
- violations of the upper bound 3*pi^2: 0 of 4000
- worst relative lower margin (D - 3*pi^2/R)/D = +1.25e-8 (tightest at large R, t ~ 0)
- worst relative upper margin (3*pi^2 - D)/3*pi^2 = +1.28e-6 (tightest at t ~ 1)

Phase-coordinate identity: D_HR(t) = Q(mu,c) := W(mu,c)/mu^2 to 1e-13 for all
tested (t,R); D_HL(t) = D_HR(1-t) to machine precision.

Proof-inequality audit: all three regime chains of Section 1.2 were verified on
1100 (mu,c) points (mu in {1.02,...,1e4}, c across all three regimes): the
sector bounds, the Chain-2 bound, and W' < 0 in Regime III all hold.

High precision (mpmath, 60 digits) at the tight corners:
mu=1.001, c=1e-6: W - 3*pi^2 = +5.92e-2 > 0; W - 3*pi^2*mu^2 = -1.95e-18 < 0,
consistent with the leading-order margin ~ 10*mu*(mu^2-1)*pi^4*c^3/(mu+c)^2.
mu=100, c=1e-6: W - 3*pi^2*mu^2 = -9.74e-14 < 0.

Wiggle structure (interior local extrema of D, heavy-right; both inside the
open interval):

| R | local max at t | D there | local min at t | D there | interval |
|---|---|---|---|---|---|
| 1.5 | 0.4735 | 24.7517 | 0.6334 | 24.0524 | (19.739, 29.609) |
| 2 | 0.5117 | 22.0452 | 0.6697 | 20.9799 | (14.804, 29.609) |
| 4 | 0.6008 | 17.3231 | 0.7502 | 15.6128 | (7.402, 29.609) |
| 10 | 0.7060 | 13.5958 | 0.8359 | 11.2227 | (2.961, 29.609) |
| 100 | 0.8824 | 9.8443 | 0.9487 | 5.7604 | (0.296, 29.609) |

f(t) = lambda_1*u_1(t)^2 - lambda_2*u_2(t)^2 has exactly two zeros (pattern
-,+,-) for every tested R, matching the two critical points of D.

Feynman-Hellmann cross-check: dD/dt = -(R-1)*f(t) for HR (and dD/dt = +(R-1)*f(t)
for HL) was verified to 4e-6 (finite-difference precision) on 200-point t grids
for R in {2, 4}.

Endpoint limits: D(t) -> 3*pi^2 as t -> 1- and D(t) -> 3*pi^2/R as t -> 0+,
confirmed numerically (e.g. R=4: D(0.998) = 29.585 vs 29.609; D(0.002) = 7.404
vs 7.402) and exactly by the phase formula.

---

## 2. Subclaim 2: symmetric critical configs beat the constants (PARTIAL)

Setup.  SUP config rho = 1 on [0,u] u [1-u,1], R on (u,1-u); INF config the
mirror.  Half-problem reduction (standard, verified numerically): lambda_1 = s_0^2,
lambda_2 = s_1^2 where s_0 is the first DN root and s_1 the first DD root on
[0,1/2] of the two-block string with densities (1,R) [SUP] or (R,1) [INF];
u* is the unique zero in (0,1/2) of
f(u) = s_0^2*y_0(u)^2/(2*N_0) - s_1^2*y_1(u)^2/(2*N_1) (y_k = sin(s_k*x)/s_k on the
first block, N_k = int_0^{1/2} rho*y_k^2).  dD/du = -2*(R-1)*f(u) [SUP] and
+2*(R-1)*f(u) [INF], verified to 1e-6.

Claim (i): D_SUP(u*) > 3*pi^2.  Claim (ii): D_INF(u*) < 3*pi^2/R.  Both for all R > 1.

### 2.1 Conditional proof (modulo O2, the unique-crossing structure)

Fact (endpoint values; exact):
D_SUP(0) = 3*pi^2/R (rho ~ R a.e.), D_SUP(1/2) = 3*pi^2 (rho ~ 1 a.e.);
D_INF(0) = 3*pi^2, D_INF(1/2) = 3*pi^2/R.

Fact (O2, Agent A, PARTIAL - numerically verified, proof open): f has a unique
zero u* in (0,1/2), f < 0 on (0,u*), f > 0 on (u*,1/2).

Then for SUP: D' = -2*(R-1)*f > 0 on (0,u*) and < 0 on (u*,1/2), so D is
strictly increasing then strictly decreasing, with its unique global maximum at
u*.  Hence D_SUP(u*) > D_SUP(1/2) = 3*pi^2 and D_SUP(u*) > D_SUP(0) = 3*pi^2/R.
For INF: D' = +2*(R-1)*f < 0 on (0,u*) and > 0 on (u*,1/2), so D has its unique
global minimum at u*; hence D_INF(u*) < D_INF(1/2) = 3*pi^2/R and
D_INF(u*) < D_INF(0) = 3*pi^2.  This proves (i) and (ii) for every R > 1,
conditional on O2.

### 2.2 Unconditional first-order analysis at R -> 1+

Write R = 1 + eps.  First-order perturbation theory (FH at rho = 1):
for rho = 1 + eps*chi_B, dD/deps(0) = int_B f_0 dx with
f_0(x) = lambda_1*u_1^2 - lambda_2*u_2^2 = 2*pi^2*(sin^2(pi*x) - 4*sin^2(2*pi*x))
(u_k = sqrt(2)*sin(k*pi*x), lambda_k = k^2*pi^2 at rho = 1).  Let
f~ := sin^2(pi*x) - 4*sin^2(2*pi*x) and note f_0 = 2*pi^2*f~.

SUP barrier B = (u, 1-u): D_SUP(u, eps) = 3*pi^2 + 4*pi^2*eps*int_u^{1/2} f~ + O(eps^2).
The derivative in u vanishes where f~(u) = 0, i.e. 4*sin^2(2*pi*u) = sin^2(pi*u)
with u in (0,1/2), giving cos(pi*u) = 1/4, i.e. u_0 = arccos(1/4)/pi ~ 0.41957.
So u*(eps) -> u_0 and

    D_SUP(u*) = 3*pi^2 + c*eps + O(eps^2),
    c = 4*pi^2*I,  I := int_{u_0}^{1/2} f~ dx
      = (3/2)*u_0 + 9*sqrt(15)/(64*pi) - 3/4
      = 3*(-16*pi + 3*sqrt(15) + 32*arccos(1/4))/(64*pi) ~ 0.052718,
    c ~ 2.081216 > 0.

INF well B = [0,u] u [1-u,1]: D_INF(u*, eps) = 3*pi^2 - 4*pi^2*eps*((3/2)*u_0 + 9*sqrt(15)/(64*pi)) + O(eps^2)
and 3*pi^2/R = 3*pi^2*(1 - eps + O(eps^2)), so

    3*pi^2/R - D_INF(u*) = c*eps + O(eps^2)  with the same c ~ 2.081216 > 0.

Because the leading terms are positive and the error terms are o(eps), (i) and
(ii) hold for all R in (1, 1+delta) for some delta > 0.  (The O(eps^2) remainder
is uniform on a neighbourhood of u_0 by the implicit function theorem and
continuity of the data.)

Numerical confirmation of the constant: (D_SUP - 3*pi^2)/eps = 2.0636, 2.0768,
2.0803, 2.0810 and (3*pi^2/R - D_INF)/eps = 2.0174, 2.0650, 2.0780, 2.0806 for
eps = 0.02, 0.005, 0.001, 0.0002, converging to c ~ 2.0812.

### 2.3 Asymptotics at R -> +infinity (verified numerically; constants explicit)

SUP: u* -> 1/2 (defect (1/2 - u*)*sqrt(R) ~ 0.119), lambda_1 = s_0^2 -> 0,
lambda_2 = s_1^2 -> pi^2/u*^2 -> 4*pi^2 (the odd mode localizes on the light
half-block [0,u*] as the R-barrier becomes impenetrable), so

    D_SUP -> 4*pi^2 = 39.478417604...  (numerically D_SUP(10^6) = 39.457121,
    D_SUP(10^4) = 39.267381, approaching 4*pi^2 from below).

Since 4*pi^2 > 3*pi^2, (i) holds for all sufficiently large R.

INF: u* -> u_inf = 0.32992251, R*lambda_1 -> pi^2/(4*u_inf^2) (even mode),
R*lambda_2 -> a^2/u_inf^2 where a in (pi/2, pi) solves tan(a) = a*(1 - 1/(2*u_inf))
(odd mode), hence

    D_INF*R -> (a^2 - pi^2/4)/u_inf^2 = 24.9438661384...  <  3*pi^2 = 29.6088.

So D_INF < 3*pi^2/R for all sufficiently large R, i.e. (ii) holds for large R.
(Verified: D_INF*R = 24.94542 at R=10^4 and 24.94388 at R=10^6, converging to
24.9438661384; the closed form reproduces 24.9438661384329 at u = 0.32992251.)

### 2.4 Numerical verification table (all R tested; margins strictly positive)

R | SUP u* | D_SUP | D_SUP - 3*pi^2 | INF u* | D_INF | D_INF*R | 3*pi^2/R - D_INF
1.02 | 0.42008 | 29.6501 | +0.0413 | 0.41905 | 28.9879 | 29.5677 | +0.0403
1.05 | 0.42084 | 29.7107 | +0.1019 | 0.41830 | 28.1025 | 29.5076 | +0.0964
1.2  | 0.42426 | 29.9928 | +0.3840 | 0.41478 | 24.3622 | 29.2346 | +0.3118
1.5  | 0.42983 | 30.4730 | +0.8642 | 0.40881 | 19.1954 | 28.7931 | +0.5438
2    | 0.43670 | 31.1023 | +1.4935 | 0.40104 | 14.1278 | 28.2555 | +0.6766
4    | 0.45149 | 32.6140 | +3.0052 | 0.38260 | 6.78448 | 27.1379 | +0.6177
10   | 0.46693 | 34.4513 | +4.8425 | 0.36131 | 2.60892 | 26.0892 | +0.3520
100  | 0.48853 | 37.5470 | +7.9382 | 0.33480 | 0.25093 | 25.0933 | +0.0452
1e4  | 0.49881 | 39.2674 | +9.6586 | 0.32998 | 0.0024945 | 24.9454 | +0.00047
1e6  | 0.49988 | 39.4571 | +9.8483 | 0.32992 | 2.494e-5 | 24.9439 | +4.7e-6

Also at R=1.02/1.05 the SUP margin is +0.041/+0.102 in agreement with
c*(R-1) = 2.08*(R-1).

### 2.5 Verdict

PARTIAL.  The full R-range claims (i), (ii) are proved conditional on O2 (the
unique zero / sign structure of f_sym, numerically verified, proof open).  The
R -> 1+ first-order statements are proved unconditionally with the explicit
positive constant c = 4*pi^2*((3/2)*u_0 + 9*sqrt(15)/(64*pi) - 3/4) ~ 2.0812;
the R -> infinity limits are verified with explicit constants (4*pi^2 and
24.9438661384 < 3*pi^2).  Numerics confirm (i), (ii) for every tested R.

---

## 3. Subclaim 3 (bonus): direct 2-parameter symmetry b = 1 - a (PARTIAL)

Statement: any sign-consistent interior critical point (a,b) of the barrier
family rho = 1 on [0,a] u [b,1], R on (a,b), with f(a) = f(b) = 0 and
{f > 0} = (a,b), satisfies b = 1 - a.

### 3.1 What is available

Equations (exact): with s_k = sqrt(lambda_k) and the transfer matrix of the
three blocks, the secular conditions are M01(s_1;a,b) = 0, M01(s_2;a,b) = 0,
where s*M01 = cos(s(1-b))[cos(s*mu*(b-a))*sin(s*a) + sin(s*mu*(b-a))*cos(s*a)/mu]
+ sin(s(1-b))[cos(s*mu*(b-a))*cos(s*a) - mu*sin(s*mu*(b-a))*sin(s*a)].
The critical conditions are f(a) = f(b) = 0, i.e. with u_k = y_k/||y_k||,
lambda_1*u_1(a)^2 = lambda_2*u_2(a)^2 and lambda_1*u_1(b)^2 = lambda_2*u_2(b)^2;
equivalently (v := u_2/u_1 strictly decreasing, from the Wronskian) v(a) = q,
v(b) = -q with q = sqrt(lambda_1/lambda_2) in (0,1).

Reduction obtained (this work): the reflection x -> 1-x maps the critical point
(a,b) to the sign-consistent critical point (1-b, 1-a) of the same family with
the same D and the same eigenvalue data.  Therefore the claim b = 1 - a is
equivalent to uniqueness of the interior sign-consistent critical point up to
reflection (obligation O3a), which is open.  Boundary critical points (a = 0 or
b = 1) are exactly the two-block configurations and are covered by Subclaim 1;
f(0) = 0 and f(1) = 0 hold identically, so they are not interior critical points.

### 3.2 Numerical search (no counterexample)

Solving f(a) = f(b) = 0 on the barrier family (Newton/hybr from 25 random seeds
per R, R in {1.5, 2, 4, 10}) gives only:

- the symmetric interior point: (u*, 1-u*) with a + b = 1 to 1e-12 for all R
  (saddle of D; matches Agent B's fixed points and the SUP maximizer of O2), and
- boundary/degenerate solutions (a ~ 0 or b ~ 1), which are the two-block
  configurations of Subclaim 1.

Agent B's continuation data (agentB_fixedpoints.json, agentB_goodbranches.json)
independently finds the same symmetric fixed point for R in {1.05, ..., 100}
with Hessian sign pattern (saddle) and no asymmetric branch.

### 3.3 Attempted proof routes and why they stall

1. v-ratio + reflection: v(a) = q, v(b) = -q and v strictly decreasing only
   imply the reflected pair (1-b, 1-a) is also critical with the same data;
   without injectivity of the critical-point map (i.e. without uniqueness) this
   does not force a + b = 1.
2. First-order in R - 1: the critical point tends to (u_0, 1-u_0); the
   first-order correction (a_1, b_1) satisfies a linear system whose solution is
   symmetric only if one assumes the uniqueness of the nearby critical point
   (the reflection symmetry alone gives b_1 = -a_1 if the point is unique).
3. Direct elimination in the 3-block secular determinant + critical equations:
   the resulting system does not factor by (a + b - 1) in an obvious way; the
   algebraic elimination is the same difficulty as O3a.

### 3.4 Verdict

PARTIAL.  Reduction to uniqueness-up-to-reflection established; numerics give
strong evidence (unique symmetric interior critical point, no asymmetric
solutions found); the core implication b = 1 - a is not proved.  It is exactly
the open obligation O3a.

---

## 4. Failed attempts and failure mechanisms (honest log)

1. Ratio route for Subclaim 1 (lambda_2 <= 4*lambda_1 would give D <= 3*lambda_1
   < 3*pi^2).  REFUTED for two-block strings: max lambda_2/lambda_1 over the
   family exceeds 4; phase-coordinate computation gives ~ 9.0 at mu = 10^4,
   c ~ 2.0.  Mechanism: ratio is large when lambda_1 is small while D stays
   bounded; the factor 3*lambda_1 is far too crude.
2. Early "regime A" sector bound with x_1 >= pi/(1+c) for c >= 1.  WRONG: the
   inequality theta(x) >= x holds only on (0,pi/2); for c >= 1, x_1 <= pi/2 so
   the correct bound is x_1 <= pi/(1+c), and x_2 < pi for c > 1 (not in
   (pi, 3*pi/2)).  Replaced by the Chain-2 bound (Section 1.2, Regime I) with
   the proven sign of dG/dmu.
3. Independent bracketing of eps_1, eps_2 in Regime C (arctan(tan(c*k*pi/2)/mu)
   style bounds).  FAILS: the individual bounds are far too crude for the
   delicate cancellation; the bracketed lower bound was negative by several
   units.  Mechanism: the inequality is tight to leading order in c; endpoint
   bounds destroy it.  Replaced by the exact W' < 0 proof using the joint
   constraint tan(c*x_k) = mu*tan(eps_k).
4. W' < 0 for all c (monotonicity of W).  FALSE: W' changes sign (positive on
   c in [0.5, 1.3]-ish); W has an interior local max, still below W(0).
   Mechanism: the "wiggle" of D(t); only the regime (0,1/3] has W' < 0.
5. Eigenfunction normalization bug in early FH checks (y'(0) = 1 normalization
   dropped the factor 1/s on the first block).  Fixed; after the fix,
   dD/dt = -(R-1)*f verified to 4e-6.  Lesson: the C^1 matching requires
   y(t) = sin(s*t)/s, y'(t) = cos(s*t).
6. Crude direct root-finding at extreme R (R = 1e4) with coarse s-grids gives
   spurious roots (ratio 8.85 etc.); the phase-coordinate formulation is the
   reliable instrument there.
7. W(mu,c) < W(mu,0) via "w decreasing in mu": false for c <= 0.1 (wiggles);
   monotonicity in mu holds only for c >= 1/3.  Not needed in the final proof.

---

## 5. Exact remaining gaps

G1 (Subclaim 2): a proof of the O2 key lemma (f_sym has a unique zero u* in
(0,1/2) with sign - then +; equivalently g(u)/u strictly decreasing, Agent A's
Section 2.9).  With it, (i) and (ii) follow for all R > 1 by Section 2.1.
Without it, the all-R statements rest on numerics + the two proven asymptotic
ends.

G2 (Subclaim 2): a rigorous proof of the R -> infinity limits (u* -> 1/2 for
SUP with defect O(1/sqrt(R)); u* -> u_inf and the closed form for INF).  The
constants are explicit and numerically verified to 6-9 digits; only the
convergence proof is missing.

G3 (Subclaim 3): uniqueness up to reflection of interior sign-consistent
critical points of the barrier family (equivalently the direct implication
b = 1 - a from the four explicit equations).  This is the crux obligation O3a;
all three attempted routes stall exactly here (Section 3.3).

---

## 6. Reproducibility

All scripts live in this run directory and run with
C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe.

- Subclaim 1: agentC_verify1.py / agentC_verify2.py (phase identity to 1e-13;
  4000-point bound grid, 0 violations), agentC_chains.py (regime bound chains;
  worst Chain2 ratio 0.99983 < 1), agentC_symG.py / agentC_symcert.py (symbolic
  dG/dmu factorization, P >= 4 > 0), agentC_wpc.py (W' < 0 on (0,1/3] for all
  mu > 1, mpmath 50 digits; mu = 1 degenerate with W' = 0 is excluded),
  agentC_Qp.py (Q' < 0, x2 - x1 < pi), agentC_wiggle.py (interior local extrema
  via zeros of f), agentC_fsign.py (f pattern -,+,- for both orientations),
  agentC_fh5.py (FH identity dD/dt = -(R-1)f to ~5e-6), agentC_phase.py.
- Subclaim 2: agentC_sub2c.py (full table R = 1.02..1e6), agentC_sub2v.py
  (first-order constant c ~ 2.0812, R -> 1+ and R -> inf convergence),
  agentC_suplim.py (SUP R -> inf structure), agentC_inflim2.py (INF closed form
  24.9438661384; min-Dr scan).
- Subclaim 3: agentC_sub3c.py (random-seed critical-point search; only the
  symmetric interior point plus degenerate two-block configurations found).

Fixes applied in this session (previously fragile tails): agentC_sub2c.py main
block guarded for import; agentC_sub2v.py now imports the robust grid-based
solver from agentC_sub2c (its old brentq-on-wide-bracket root finder failed at
extreme R); agentC_inflim2.py final brentq replaced by a scan (Dr has an
interior minimum, so both endpoints sit above the target); agentC_wpc.py moved
to mpmath 50 digits (the margin W' ~ (mu^2-1)*c^2 is below double precision
near c = 0); agentC_wiggle.py / agentC_fsign.py / agentC_fh5.py rewritten on
the fast monotone phase solver (the M01-grid versions were too slow).
