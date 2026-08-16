RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-D: positive-cell defect decomposition and translation speed

## 0. Route record

```text
route_id: MIN-REFL-C2-D
target: one-sided sign of D=p^2-1 on every fixed-(R,n,mu) equal-norm minimum root set
method_family: exact event-amplitude recursion; spatial translation of all switches
current_status: active partial result; cellwise-sign subroute refuted
proved_results:
  - D is a sum of explicit normalized positive-cell drift functions Phi_mu(theta,z)
  - Phi_mu(theta,1/z)=-Phi_mu(theta,z)
  - strict first-crossing physical positive cells realize both signs exactly
  - D/I is the common translation speed of the two adjacent eigenvalues at a full root
first_failing_step:
  - negative-cell momentum gluing and the global endpoint/norm equations have not been shown to cancel the odd drift sum
precise_gap:
  - prove a signed global inequality for the coupled sum of Phi, or exhibit a complete asymmetric relay root
restart_condition:
  - a cross-cell monotone cocycle retaining negative-cell gluing, or a translation-curvature theorem using more than stationarity of the gap
```

This report is bound to Blueprint
`sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0`
and inventory
`sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
It uses only the trusted full-relay, structure, internal-phase, symplectic,
and endpoint-defect claims listed in the run contract.

## 1. One strict positive cell

Take one internal positive relay cell of a minimum-law trajectory. Its
material is `1`. Write its phase length as

```text
0<theta<pi/(mu+1),
s=sin(theta), c=cos(theta), S=sin(mu theta), C=cos(mu theta).
```

At the left event orient `mu V=epsilon U` and put `U=A`. At the right event
the label is opposite and, because this cell contains a zero of `V` but no
zero of `U`, write

```text
U_right=z A,       mu V_right=-epsilon z A,       z>0.
```

The two exact oscillator propagations give

```text
U'_left=A(z-c)/s,
V'_left=-epsilon A(z+C)/S,

U'_right=A(zc-1)/s,
V'_right=-epsilon A(1+zC)/S.                         (1.1)
```

Let `C0=q^2-1>0` be the absolute value of the global negative relay energy.
At either event the potential terms cancel, so (1.1) yields

```text
C0=A^2 E_mu(theta,z),
E_mu(theta,z)=(z+C)^2/S^2-(z-c)^2/s^2.               (1.2)
```

Define

```text
k_mu(theta)=sin((mu-1)theta/2)/sin((mu+1)theta/2).
```

The sharp phase range gives `0<k_mu(theta)<1`. Exact factorization gives

```text
E_mu(theta,z)
 =(S^2-s^2)(1/k_mu-z)(z-k_mu)/(s^2 S^2).             (1.3)
```

Indeed the two factors before division by `s^2S^2` are

```text
s(z+C)-S(z-c)=(S-s)(1/k_mu-z),
s(z+C)+S(z-c)=(S+s)(z-k_mu).
```

Consequently the strict negative-energy branch is exactly

```text
k_mu(theta)<z<1/k_mu(theta).                         (1.4)
```

## 2. Exact decomposition of the endpoint defect

For completeness, derive the alternating event-amplitude identity directly.
On every open cell the low-frequency energy

```text
E_U=U_t^2+rho U^2
```

is constant.  Across event `t_j`, continuity of `U,U_t` gives

```text
E_U(t_j+)-E_U(t_j-)=Delta rho_j U(t_j)^2.
```

The minimum word starts and ends in material `R` and has
`Delta rho_j=(R-1)(-1)^j`.  Summing all energy jumps and using
`U(0)=U(L)=0`, `U_t(0)=1`, and `U_t(L)=p` therefore gives

```text
D=p^2-1=(R-1) sum_(j=1)^(2n) (-1)^j U(t_j)^2.
```

The `n` positive internal cells are precisely the pairs
`(t_(2a-1),t_(2a))`, so regrouping consecutive terms gives

```text
D/(R-1)
 =sum_(a=1)^n [U(t_(2a))^2-U(t_(2a-1))^2].           (2.1)
```

Apply (1.2) to each positive cell. If `theta_(2a-1)` and `z_(2a-1)` are
its phase and signed-positive amplitude ratio, then

```text
D=(R-1) C0 sum_(a=1)^n Phi_mu(theta_(2a-1),z_(2a-1)),

Phi_mu(theta,z)=(z^2-1)/E_mu(theta,z).                (2.2)
```

This is an exact full-root identity, not an independent-cell relaxation.
It isolates the only remaining coupling: which tuples `(theta,z)` can be
glued through all negative cells and the two terminal cells while satisfying
common terminal time and equal norm.

Direct algebra using `c^2+s^2=C^2+S^2=1` gives

```text
z^2 E_mu(theta,1/z)=E_mu(theta,z),
Phi_mu(theta,1/z)=-Phi_mu(theta,z).                   (2.3)
```

Thus reversal changes the sign of each drift after reversing its amplitude
normalization, exactly matching `D_sharp=-D/p^2` at the full-trajectory
level.

## 3. Exact refutation of a cellwise one-sign proof

The ambiguity in (1.4) is physical, not caused by discarding the two
oscillator momenta. Set

```text
mu=2,       theta=pi/6,       z=1/2 or z=2.
```

Both values lie strictly between
`k=(sqrt(3)-1)/2` and `1/k`. The inward transversality factors

```text
D_L=(z-c)/s+mu(z+C)/S,
D_R=mu(1+Cz)/S-(cz-1)/s
```

and the energy and drift are exactly

```text
z=1/2:
  D_L=1+sqrt(3)/3,
  D_R=2+7sqrt(3)/6,
  E=(-8+6sqrt(3))/3>0,
  Phi=-9/[8(-4+3sqrt(3))]<0;

z=2:
  D_L=4+7sqrt(3)/3,
  D_R=2+2sqrt(3)/3,
  E=(-32+24sqrt(3))/3>0,
  Phi=+9/[8(-4+3sqrt(3))]>0.                         (3.1)
```

These are also strict first-crossing cells, not merely endpoint matches.
With `x=tan(t/2)` and `0<x<2-sqrt(3)`, the checker factors the numerator of
`U(t)^2-4V(t)^2`. In each case its only boundary factors are
`x` and `x-(2-sqrt(3))`; the remaining two displayed quadratics are strictly
negative on the closed interval (their endpoint values are negative and
they are convex). Together with the two fixed-sign linear factors this
makes the switching function strictly positive in the open cell.

Therefore a proof that assigns a fixed sign to every positive-cell summand
in (2.2) is impossible even after imposing exact two-frequency propagation,
negative energy, transversality, the sharp phase range, and first crossing.
Any successful sign theorem must use cross-cell momentum gluing and global
closure.

## 4. Translation interpretation of `D`

There is a second exact interpretation. Extend the common endpoint material
`R` slightly beyond both endpoints and translate every internal switch to
the right by `h`, keeping the interval fixed. Let `T_R(h,lambda)` be the
constant-`R` transfer matrix and `M(lambda)` the original monodromy. For
small `h`,

```text
M_h(lambda)=T_R(-h,lambda) M(lambda) T_R(h,lambda).   (4.1)
```

At a Dirichlet eigenvalue, normalize the solution by `u(0)=0,u'(0)=1` and
write `p=u'(L)`, `I=int rho u^2`. Symplecticity gives

```text
M(lambda)=[[1/p,0],[m,p]].                           (4.2)
```

For the generator `A_R=[[0,1],[-lambda R,0]]`, differentiating (4.1) gives
`M A_R-A_R M`. Its `(1,2)` entry is `1/p-p`. The standard differentiated
Dirichlet identity is

```text
partial_lambda M_12=I/p.
```

Implicit differentiation of `M_h(lambda(h))_12=0` therefore yields

```text
lambda'(0)=(p^2-1)/I.                                (4.3)
```

For the two relay modes, the second mode normalized to left slope one has
terminal slope `r/q` and norm `I_V/q^2`. At an equal-norm full root,
`r^2-q^2=p^2-1=D` and `I_U=I_V=I`, so

```text
lambda_n'(0)=D/I=lambda_(n+1)'(0).                   (4.4)
```

Thus `D` is the common spectral translation speed. Equation (4.4) explains
why translating all switches cannot determine its sign from first-order
minimality of the gap: the adjacent eigenvalues drift together and the gap
derivative cancels identically. A new translation argument must control a
second derivative or another spectral functional; first-order stationarity
is exhausted.

## 5. Exact remaining obligation

The route has not proved a one-sided sign for `D` and therefore has not
proved reflection. Its first unresolved statement is now the coupled one:

> On every complete minimum equal-norm relay root, prove that the sum in
> (2.2) has one weak sign on the entire fixed-`(R,n,mu)` root set, using the
> negative-cell momentum matches and terminal closure; or certify a root
> for which it does not.

This is not discharged by a cellwise inequality (Section 3 refutes that
mechanism) or by first-order translation of the gap (Section 4 shows exact
cancellation). A valid restart must introduce a signed cross-cell cocycle,
translation curvature, or a complete asymmetric root.

## 6. Boundary audit and limitations

- `n=2`: (2.2) has two positive-cell terms; both can have either local sign.
- `n>=3`: the same decomposition holds with `n` terms.
- equality `z=1`: the local drift is zero but the cell remains strict; no
  conclusion about the other cells follows.
- reflection: (2.3) is covariance, not an assumption of palindromy.
- endpoint cells: they do not occur in (2.1), but they remain essential in
  deciding which internal tuples close globally.
- `R downarrow 1`: the prefactor tends to zero; no uniform division by
  `R-1` is used in a claimed boundary theorem.
- no local cell is claimed to be a complete root or a counterexample.
- novelty status: `unknown`.

Replay from the project root:

```text
E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe runs\R-20260816T034422Z-min-reflection-cont2\routes\defect_amplitude\exact_checker.py
```
