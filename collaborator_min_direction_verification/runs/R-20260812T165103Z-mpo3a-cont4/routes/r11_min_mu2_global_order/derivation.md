CANDIDATE_COMPLETE_PROOF

# R11 conditional global relay order and the min `n=2`, `mu=2` corollary

## 0. Two exact results, normalization, and trusted inputs

Fix a finite `R>1`, an integer `n>=2`, and `mu>1`.  Write `rho_-` for
the coefficient used on `{S<0}` and `rho_+` for the coefficient used on
`{S>0}`, where

```text
{rho_-,rho_+}={1,R}.
```

Thus `rho_-=1` is the max orientation and `rho_-=R` is the min
orientation.  For every `q>1` consider the positively normalized relay IVP

```text
U_tt=-rho U,          U(0)=0, U_t(0)=1,
V_tt=-mu^2 rho V,     V(0)=0, V_t(0)=q,
S=U^2-mu^2 V^2,
rho=rho_+ on {S>0},   rho=rho_- on {S<0}.            (0.1)
```

Let `T_U^n(mu,q)` and `T_V^(n+1)(mu,q)` be the indicated positive
scalar-zero times and set

```text
A_n(mu,q)=T_U^n(mu,q)-T_V^(n+1)(mu,q).               (0.2)
```

The proof first establishes the following reusable result.

> **Conditional global-order lemma, either relay orientation.**  Suppose
> there is one `sigma in {+1,-1}` such that at every premise-complete
> transverse common-terminal root, the derivative of its smooth fixed-word
> chamber residual satisfies
> `sigma partial_q A_n^c(mu,q)>0`.  Then (0.1) defines one global continuous
> residual (0.2) on `q>1`; it has at most one zero across all relay chambers
> and compatible closures; every zero is automatically premise complete
> with exactly `2n` active transverse events and is fixed by reflection
> after positive reorientation.

The conditional lemma does not claim that either derivative sign is known
for arbitrary `n,mu`.  It isolates the sign-independent implication that
can be reused once a local twist theorem is available.

The trusted R10 min theorem supplies the missing hypothesis for
`n=2,mu=2` with `sigma=-1`.  Hence the unconditional restricted corollary is:

> **Restricted global min root-order theorem.**  For every finite `R>1`,
> under the min relay with `n=2` and `mu=2`, `A_2(2,.)` is continuous on
> `(1,infinity)` and has at most one zero.  Every zero is automatically a
> premise-complete transverse four-event common-terminal root and is fixed
> by reflection after positive reorientation.

The two exact candidate records are:

```text
candidate_inference_id:
  INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
exact_statement:
  For every finite R>1, integer n>=2, frequency mu>1, and either relay orientation rho_- in {1,R} on S<0 with the other coefficient on S>0, if one sign sigma in {+1,-1} satisfies sigma partial_q A_n^c(mu,q)>0 at every premise-complete transverse common-terminal root, then the global indexed residual A_n(mu,q)=T_U^n(mu,q)-T_V^(n+1)(mu,q) is continuous on q>1, has at most one zero across all relay chambers and compatible closures, and every zero is fixed by reflection after positive reorientation.
exact_statement_sha256:
  sha256:fcb02db540fdab1a2a4b7201030e64a47c1756c16caad0c3f2c4fe315ae4cbc3

candidate_inference_id:
  INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
exact_statement:
  For every finite R>1, under the min relay with n=2 and mu=2, the global indexed residual A_2(2,q)=T_U^2(q)-T_V^3(q), q>1, is continuous and has at most one zero across all relay chambers and compatible closures; every zero is automatically a premise-complete transverse four-event common-terminal root and is fixed by reflection after positive reorientation.
exact_statement_sha256:
  sha256:2fa736de49562b7d9ba23ff321dfe998d6f8787b282cb9ecf6bbd6382c46cbda
```

The bound canonical snapshot is

```text
blueprint:
  sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242
inventory:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Trusted records used are

```text
HYP-NGE2-DOMAIN
  semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5
CLM-NGE2-ZERO-BOUND
  semantic-sha256:49bf4cf80c0026e580c61340ba7066bec075da0bb2f7e4ee8a019e981f0acab6
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
DEF-NGE2-MPO3A-SELFCONSISTENCY
  semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10
  semantic-sha256:157a7bf928676b7565e5e08e965909ab0657e48888d37095c43352a228bbbd21
```

The trusted R10 theorem gives, at every root in its exact scope,

```text
partial_q A_2(2,q)<0.                                (0.3)
```

Its quotient coordinate is exactly `q=V_t(0)/U_t(0)` after setting
`U_t(0)=1`, as in (0.1).  The frozen max R9 derivation, SHA-256
`37cd0c8be3fbb542faeaec875c6a24c007a59f9918a672e07a7140340acb2706`,
is only a checked template: no max conclusion or candidate premise is used.
All relay-sign-sensitive steps are written below using `rho_-`.  There are
no external results or computational certificates.  Unresolved obligations
for the restricted corollary as stated: `[]`.

## 1. Strict negative energy classifies every relay zero

Put `P=U_t` and `Q=V_t`.  On each constant-material cell,

```text
E=P^2+rho U^2-(Q^2+mu^2 rho V^2)
 =P^2-Q^2+rho S                                      (1.1)
```

is constant.  A material jump occurs at `S=0`, so the jump does not change
`E`.  The global value is therefore

```text
E=1-q^2<0.                                           (1.2)
```

If `S(t_0)=0` and `(U,V)(t_0)!=(0,0)`, write
`U=epsilon mu V`.  Tangency would give

```text
0=S_t/2=UP-mu^2VQ,       P=epsilon mu Q,
```

and hence `E=(mu^2-1)Q^2>=0`, contradicting (1.2).  Every nonjoint relay
zero is transverse and changes sign.

If `U(t_0)=V(t_0)=0`, then (1.2) gives
`P(t_0)^2-Q(t_0)^2<0` and therefore

```text
P(t_0)^2-mu^2Q(t_0)^2<0.                             (1.3)
```

The `C^1` Taylor expansion yields

```text
S(t_0+h)=[P(t_0)^2-mu^2Q(t_0)^2]h^2+o(h^2)<0        (1.4)
```

on both punctured sides.  Thus a joint zero is an isolated negative-side
quadratic contact, not an effective switch.  Its material on both sides is
uniquely `rho_-`: `1` for max and `R` for min.  Nonzero grazing, sliding,
and an ambiguous outgoing coefficient are impossible for either
orientation.

## 2. The relay IVP is global and unique

At the initial joint zero,

```text
U(t)=t+o(t),        V(t)=qt+o(t),
S(t)=(1-mu^2q^2)t^2+o(t^2)<0,                       (2.1)
```

so the initial punctured cell has material `rho_-`.  Evolve the two
constant-coefficient oscillators until the next zero of `S`.  A nonjoint
zero is transverse and selects the coefficient on the other side; a joint
zero retains `rho_-`.  This constructs a unique trajectory until a possible
accumulation of relay zeros.

No finite accumulation occurs.  On a compact time interval,
`1<=rho<=R` gives uniform state and derivative bounds.  If distinct zeros
accumulated at `t_*`, continuity and Rolle's theorem would give
`S(t_*)=S_t(t_*)=0`.  A nonjoint limit contradicts Section 1.  A joint
limit contradicts the punctured zero-free neighborhood supplied by (1.4).
Thus every compact interval has finitely many relay zeros, the construction
extends globally, and the a.e. material label is unique.  Values assigned
to `rho` on the finite zero set are immaterial.

## 3. Continuous dependence without a fixed material word

Fix a compact `q`-interval `K subset (1,infinity)` and a finite horizon
`T`.  For `q_k->q`, uniform coefficient and initial-data bounds make the
states `Y_k=(U_k,P_k,V_k,Q_k)` bounded and equicontinuous.  Pass to a
uniformly convergent subsequence with limit `Y=(U,P,V,Q)`.  The identities
`U_k(t)=integral_0^t P_k` and `V_k(t)=integral_0^t Q_k` show already that
`U_t=P` and `V_t=Q`.

At any zero of the limiting `S`, the exact energy identity at that fixed
time and the bound `1<=rho_k<=R` give

```text
P(t)^2-Q(t)^2=1-q^2<0.                               (3.1)
```

The classification in Section 1 applies before the limiting relay equation
has been identified: every nonjoint zero is transverse and every joint zero
is an isolated negative-side contact.  Hence the zero set on `[0,T]` is
finite.  Away from it, uniform convergence fixes the sign of `S_k`, so the
material labels converge pointwise to `rho_+` on `S>0` and `rho_-` on
`S<0`.  Dominated convergence in the Volterra equations gives

```text
P(t)=1-integral_0^t rho(s)U(s) ds,
Q(t)=q-integral_0^t mu^2 rho(s)V(s) ds.              (3.2)
```

Thus `Y` is the unique relay solution at `q`.  Every subsequence has the
same limit, and the full family depends continuously on `q`, uniformly on
`[0,T]`.  This includes birth or death of two transverse events through a
joint quadratic contact; no event word is held fixed.

## 4. Indexed zero times define one global continuous residual

Every scalar zero of `U` or `V` is simple, since a scalar solution and its
derivative cannot vanish together unless the solution is identically zero.
For a nontrivial solution of `y_tt+a(t)y=0` with `a(t)>=1`, the lifted
phase `y=r sin(theta), y_t=r cos(theta)` satisfies a.e.

```text
theta_t=[y_t^2+a(t)y^2]/[y^2+y_t^2]>=1.              (4.1)
```

Every fixed indexed positive zero therefore exists on a uniform finite
horizon.  Uniform state convergence and simplicity make its time continuous
in `q`.  Consequently

```text
q -> A_n(mu,q)=T_U^n(mu,q)-T_V^(n+1)(mu,q)           (4.2)
```

is one continuous function on the connected interval `(1,infinity)`.
Smooth fixed-word chambers are charts for (4.2), not separate branches.  No
sign at `q=1` or `q=infinity` is required for at-most-one.

## 5. Every zero is automatically premise complete

Suppose `A_n(mu,q_0)=0`, and call the common indexed zero `L`.  On
`(0,L)` the positive piecewise-constant weight `rho` makes `U` and `V`
the `n`-th and `(n+1)`-st Dirichlet modes at eigenvalues `1` and `mu^2`:
their indexed terminal zeros give exactly `n-1` and `n` interior scalar
zeros.  The trusted scalar zero-count/Sturm theorem therefore makes them
consecutive modes with strict interlacing.

Orient both solutions by their positive left derivatives and define

```text
W=V_tU-VU_t,        W_t=-(mu^2-1)rho UV.             (5.1)
```

On each nodal interval of `U`, strict interlacing places exactly one zero
of `V`.  Immediately after the left endpoint of that cell `U` and `V`
have the same alternating sign; after the single `V` zero they have
opposite signs.  Thus `W` decreases before that zero and increases after
it.  At an interior `U` zero, `V` and the outgoing derivative `U_t` have
the same sign, so `W=-VU_t<0`; also `W(0)=W(L)=0`.  Hence

```text
W(t)<0,                 0<t<L,                       (5.2)
```

and `V/U` strictly decreases on every `U` nodal cell.

At `L` write `p=U_t(L)` and `r=V_t(L)`.  Energy and nodal parity give

```text
r^2-p^2=q_0^2-1>0,          r/p<-1.                  (5.3)
```

Thus `V/U` runs

```text
first U-cell:     q_0 -> -infinity,
middle U-cells:  +infinity -> -infinity,
last U-cell:     +infinity -> r/p<-1.                (5.4)
```

Because `q_0>1>1/mu`, it crosses both levels `+1/mu` and `-1/mu`
exactly once on each of the `n` cells.  These are exactly the zeros of
`S=U^2-mu^2V^2`, and (5.2) makes them simple.  Hence the root has exactly
`2n` positive-length active transverse relay events.  Both endpoint cells
have `S<0` and material `rho_-`, and strict interlacing excludes an
interior joint zero.  The root is premise complete without any reflection
or equal-integral assumption.

## 6. Terminal event-pair birth or death is first-order soft

At a root, the common terminal zero is the negative-side contact (1.4).
Keep the `2n` separated internal events and smoothly continue the final
`rho_-` cell through a fixed neighborhood of `L`.  Call this fixed-word
continuation `Y^c(q,t)` and its indexed zero difference `A_n^c(mu,q)`.
It is smooth near the base root.  With `delta=q-q_0`,

```text
S^c(q_0,L+x)=(p^2-mu^2r^2)x^2+O(|x|^3),
p^2-mu^2r^2<0.                                       (6.1)
```

Moreover `partial_q S^c(q_0,L)=0` because both base positions vanish.
For some `c,C,epsilon>0`,

```text
S^c(q,L+x)<=-c x^2+C(|delta||x|+delta^2)             (6.2)
```

whenever `|delta|` and `|x|<=epsilon` are small.  Choose fixed `K` so
large that `c>C/K+C/K^2` and also large enough to contain the two smooth
chamber zero times, whose displacements are `O(|delta|)`.  Equation (6.2)
then makes `S^c<0` throughout
`K|delta|<=|x|<=epsilon`.

Choose `epsilon` inside the base final negative cell.  The base internal
events are transverse and separated, so they persist, and compact
negativity on the part of that cell preceding `L-epsilon` persists as
well.  On the remaining final segment, (6.2) controls the sign.  Therefore
the actual and chamber flows agree exactly until their common entry into
`|t-L|<=K|delta|`: before that entry the chamber sign is negative and
prescribes `rho_-` in the actual relay too.  Inside the window, positions
of both flows are `O(|delta|)` and velocities are `O(1)`.

The two orientations differ only in which constant is called `rho_-`.  In
either case the possible actual/chamber forcing discrepancy is bounded by

```text
|(rho-rho_-)U|+mu^2|(rho-rho_-)V|=O(|delta|).        (6.3)
```

Starting from the common entry state, the integral equations and Gronwall
over a window of length `O(|delta|)` yield

```text
|P-P^c|+|Q-Q^c|=O(delta^2),
|U-U^c|+|V-V^c|=O(|delta|^3).                        (6.4)
```

The base terminal slopes `p,r` are nonzero, so each component is monotone
through this shrinking window for small `delta`.  The chamber zero lies
strictly inside the chosen boundaries; (6.4) preserves the boundary signs,
gives exactly one actual scalar zero there, and preserves its global index.
Simple-zero stability gives

```text
T_U^n-T_U^(n,c)=O(delta^2),
T_V^(n+1)-T_V^(n+1,c)=O(delta^2),                    (6.5)
```

in fact with the stronger position-error order available from (6.4).
Therefore

```text
A_n(mu,q)=A_n^c(mu,q)+O((q-q_0)^2).                  (6.6)
```

The fixed-word derivative is exactly the derivative of the global residual,
including birth or death of a vanishing terminal positive-material pair:

```text
partial_q A_n(mu,q_0)=partial_q A_n^c(mu,q_0).        (6.7)
```

This is the only closure step needed to transfer a local twist theorem.

## 7. Same-oriented zeros cannot repeat

**Lemma.**  Let `f:I->R` be continuous on an interval and differentiable at
every zero.  If one `sigma in {+1,-1}` satisfies
`sigma f'(x)>0` at every zero, then `f` has at most one zero.

**Proof.**  Put `g=sigma f`.  At every zero, `g'(x)>0`, so `g` is negative
immediately to the left and positive immediately to the right.  If
`x_1<x_2` were zeros, choose a small right neighborhood of `x_1` on which
`g>0`.  The nonempty zero set to its right is compact; let `y` be its first
point.  There is no zero in the preceding gap, so continuity keeps `g>0`
there.  But `g'(y)>0` requires `g<0` immediately to the left of `y`, a
contradiction.  `QED`

Assume the local-sign hypothesis of the conditional lemma.  Sections 5 and
6 show that every global zero belongs to its scope and satisfies
`sigma partial_q A_n>0`.  Apply the lemma to (4.2).  Thus
`A_n(mu,.)` has at most one zero across all chambers and compatible
closures.

## 8. At-most-one forces reflection fixing

Let a common-terminal root have length `L` and terminal slopes `p,r`.
Define its positively reoriented reflection by

```text
U#(s)=[-sign(p)]U(L-s)/|p|,
V#(s)=[-sign(r)]V(L-s)/|p|,
q#=|r|/|p|.                                          (8.1)
```

Equation (5.3) gives `q#>1`.  Both squared components acquire the same
factor `|p|^-2`, so `S#(s)=S(L-s)/|p|^2` and its sign is preserved.
Because both endpoint cells have `S<0`, the reflected trajectory starts in
material `rho_-`.  It obeys the same relay orientation and has the same
scalar nodal counts, hence `q#` is another zero of the same global
`A_n(mu,.)`.

At-most-one gives `q#=q`.  Global IVP uniqueness from Section 2 then
identifies the reflected and original trajectories.  Reflection is a
conclusion and was not used to prove premise completeness or the derivative
sign.

## 9. Unconditional min `n=2,mu=2` corollary

Now specialize to

```text
rho_-=R,       rho_+=1,       n=2,       mu=2.        (9.1)
```

Every zero of the global `A_2(2,.)` has exactly four active transverse
events by Section 5 and is an arbitrary, possibly asymmetric,
premise-complete common-terminal min root.  This is exactly the trusted R10
scope; R10 assumes no reflection.  In the permanent-scaling quotient
normalization used here it supplies

```text
partial_q A_2^c(2,q)<0.                              (9.2)
```

Take `sigma=-1` in the conditional lemma.  Terminal softness identifies
(9.2) with the global derivative even at a compatible terminal event-pair
closure.  Therefore, for every finite `R>1`,

```text
A_2(2,q)=0 has at most one solution q>1,              (9.3)
```

and every solution is fixed by reflection after positive reorientation.
No existence assertion is made.

## 10. Boundary and adversarial discharge

- **Definitions and normalization:** `A_n` uses the `n`-th positive zero of
  `U` and the `(n+1)`-st positive zero of `V`.
  `q=V_t(0)/U_t(0)` with `U_t(0)=1` is the quotient coordinate.  Relay
  events, scalar nodal zeros, and the terminal joint contact are distinct.
- **Either orientation:** the sign-independent proof uses `rho_-` on every
  punctured joint-zero neighborhood.  It becomes `1` for max and `R` for
  min.  The initial and terminal min material in the corollary is `R`.
- **Derivative orientation:** the conditional lemma uses arbitrary fixed
  `sigma`.  The R10 corollary takes `sigma=-1` because
  `partial_q A_2^c<0`; no positive-oriented max sign is copied.
- **No fixed-word globalization:** compactness handles changes of material
  word; Section 6 separately proves first-order terminal softness.
- **Root completeness:** the consecutive-mode and quotient-crossing
  argument precedes application of any local theorem.  There is no hidden
  assumption that every global residual zero already belongs to R10.
- **Endpoint `n=2`:** Section 5 gives two crossings on each of exactly two
  `U` cells, hence four events; no nonexistent middle cell is invoked.
- **Degeneracy:** strict negative energy excludes nonzero grazing and Zeno.
  Joint collisions are negative-side quadratic contacts and are retained
  in the global domain.
- **Asymmetry:** no phase equality, palindromy, or reflection is assumed.
  Reflection is derived only after at-most-one.
- **Open boundaries:** `R=1`, `mu=1`, and `q=1` are outside the strict
  hypotheses.  Every finite `R>1` is included.  No `q->infinity` limit or
  endpoint sign is used.
- **Conditional versus unconditional scope:** Sections 1--8 prove an
  implication for arbitrary fixed `n,mu` and either relay orientation; they
  do not prove its local-sign hypothesis.  Only the min `n=2,mu=2`
  specialization is unconditional through trusted R10.
- **No overclaim:** existence, general-`mu` min twist, `n>2` min twist,
  equal-norm existence/orientation, global min order outside (9.1), min
  O3a, and universal O3a remain open.
- **Computation and sources:** no computation, numerical evidence, or
  external result is used.

## 11. Calibrated conclusion

```text
either-orientation global IVP and continuity:           PROVED
automatic 2n-event premise completeness of every root:  PROVED
terminal event-pair first-order softness:                PROVED
conditional same-sign local-to-global order:             PROVED
conditional reflection fixing:                           PROVED
min n=2, mu=2 at-most-one A_2 root:                       PROVED
min n=2, mu=2 reflection fixing:                          PROVED
existence of that root:                                   OPEN
unconditional general mu or n min order:                  OPEN
equal norm / O3a consequences:                            OPEN
```

Novelty status: `unknown`.  Semantic-fidelity, correctness, and restricted-
scope completeness confidence are high.  Reproducibility is high because
the proof is exact and uses no numerical or external-source step.
