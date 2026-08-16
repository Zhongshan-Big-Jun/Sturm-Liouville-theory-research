RIGOROUS_PARTIAL_RESULT

# Symplectic reduction of the nested full-relay uniqueness problem

Proof package binding:

```text
inference_id: INF-NGE2-MPO3A-SYMPLECTIC-NESTED
inference_statement_sha256: 522848b2fcfb6bde8e248864259ae9f8a2d080fbbf74df3f608c21d3587d9181
context_id: CTX-DEFAULT
premise CLM-NGE2-MPO3A-FULL-RELAY:
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
definition DEF-SL-BOX-ADJ-GAP:
  semantic-sha256:c6ee9a0ef59b085763d3be78055528f0bf910eb75698f61b04d0ae3e01f8b13f
definition DEF-NGE2-MPO3A-SELFCONSISTENCY:
  semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
unresolved_obligations: []
author: codex-root-r4
run_id: R-20260812T165103Z-mpo3a-cont4
```

Exact bound inference statement:

> The accepted full-relay reduction, direct Hamiltonian-saltation algebra,
> homogeneity, symplectic conservation, simple terminal zeros, relay energy,
> and reflection imply the Jacobi derivative, conjugate-point, and
> reflected-pair identities in
> CLM-NGE2-MPO3A-SYMPLECTIC-NESTED.

## 1. Scope

Fix `n>=2`, finite `R>1`, one max/min relay law, and a transverse
full-relay trajectory with parameters `(mu,q)` and a common indexed terminal
time `L`:

```text
U(L)=V(L)=0,
Theta_U(L)=n*pi,
Theta_V(L)=(n+1)*pi.
```

Do not assume the equal-integral condition. Put

```text
p=U_t(L),   r=V_t(L),
A_n=T_U^n-T_V^(n+1).
```

The accepted full-relay theorem guarantees simplicity of the indexed terminal
zeros at an actual self-consistent root. The identities below apply on any
transverse chamber where the displayed common terminal conditions hold.

## 2. Hamiltonian and two exact Jacobi fields

Use state order `z=(U,P,V,Q)` and the signed symplectic form

```text
omega=dU wedge dP-dV wedge dQ.
```

Put `S=U^2-mu^2 V^2`. For the max sign define the continuous piecewise
linear function `Phi(S)=S/2` on `S<=0` and `Phi(S)=R S/2` on `S>=0`; reverse
the two slopes for the min sign. With the convention
`i_(X_H)omega=dH`, the piecewise quadratic Hamiltonian

```text
H=(P^2-Q^2)/2+Phi(S)                                  (2.1)
```

gives exactly

```text
U_t=P, P_t=-rho U, V_t=Q, Q_t=-mu^2 rho V.
```

It is continuous across `S=0` and homogeneous of degree two. Constant-cell
flows are therefore symplectic. At a transverse event put

```text
nabla S=(2U,0,-2mu^2V,0)^T,
d=(nabla S)^T f_- !=0,
a=f_+-f_-=(0,-Delta rho U,0,-mu^2 Delta rho V)^T.
```

The exact saltation matrix is

```text
Xi=I+a (nabla S)^T/d.                                (2.2)
```

The signed symplectic matrix sends `a` to a scalar multiple of `nabla S`,
and `(nabla S)^T a=0`. Direct expansion of (2.2) therefore gives

```text
Xi^T Omega Xi=Omega.                                 (2.3)
```

Thus the complete exact hybrid variational flow preserves `omega`; no
unaudited numerical derivative or external Hamiltonian theorem is used.

Because the relay surface and vector field are homogeneous, common scaling of
the initial slopes leaves every event time fixed and scales the complete
trajectory. Its Jacobi field is therefore

```text
xi=z,
xi(0)=(0,1,0,q),
xi(L)=(0,p,0,r).                                      (2.4)
```

Let `eta=partial_q z` at fixed `mu` and fixed physical time. It includes all
moving-event corrections through the exact saltation updates and has

```text
eta(0)=(0,0,0,1).                                    (2.5)
```

At the initial endpoint, `omega(xi,eta)=0`. Symplectic conservation and
(2.1) give the exact terminal identity

```text
-p eta_U(L)+r eta_V(L)=0.                            (2.6)
```

No reflection symmetry, norm equality, or numerical approximation is used.

## 3. Exact derivative of the common-zero-time residual

Simplicity of the terminal zeros gives

```text
partial_q T_U^n=-eta_U(L)/p,
partial_q T_V^(n+1)=-eta_V(L)/r.                     (3.1)
```

The global relay energy equals `1-q^2`. At the common terminal point this is

```text
p^2-r^2=1-q^2.                                       (3.2)
```

Substituting (2.3) into (3.1) yields

```text
partial_q A_n
 =-eta_U(L)/p+eta_V(L)/r
 =(1-q^2) eta_U(L)/(p r^2).                          (3.3)
```

For `q>1`, neither terminal derivative vanishes. Hence

```text
partial_q A_n=0
iff eta_U(L)=eta_V(L)=0.                             (3.4)
```

Thus the first nested monotonicity/nondegeneracy obligation is exactly a
hybrid conjugate-point exclusion for the single `q`-Jacobi field. It is not a
collection of event-time sign assumptions; the previously proved failure of
successive-event monotonicity does not decide (3.4).

## 4. Reflection involution on the common-terminal set

Reflect and positively reorient the trajectory as in the accepted full-relay
theorem. The reflected initial slope ratio is

```text
q_sharp=abs(r)/abs(p)>1.                              (4.1)
```

Equation (3.2) gives

```text
q_sharp^2-1=(q^2-1)/p^2.                             (4.2)
```

The reflected trajectory has the same `mu`, `R`, sign, `L`, indexed terminal
phases, and event count. Both square integrals are multiplied by the same
factor `p^(-2)`, so

```text
log(I_U/I_V)_sharp=log(I_U/I_V).                     (4.3)
```

Reflection is an involution. Its fixed points satisfy any of the equivalent
conditions

```text
q_sharp=q  iff p^2=1 iff r^2=q^2.                    (4.4)
```

When (4.4) holds, the reflected and original trajectories have identical
labels `(mu,q,L,R,sign)`. Cellwise IVP uniqueness across transverse events
then makes the coefficient reflection invariant.

## 5. Strictly reduced completion route

The following two statements would prove the universal max/min target when
combined with the accepted properness and small-contrast theorem:

1. For every fixed `mu` and every premise-complete common-terminal chamber,
   `A_n(mu,q)=0` has at most one `q>1`. Reflection then forces (4.4), hence
   symmetry, for every complete root.
2. On that unique common-terminal branch, the invariant scalar residual
   `C_n=log(I_U/I_V)` has exactly one zero.

The first statement may be replaced by a global no-conjugate-point/order
theorem whose local content is (3.4). The second may be replaced by a degree
theorem including all chamber boundaries. Neither statement is proved here;
each is strictly stronger than the displayed identities and remains close to
the corresponding branch target.

Conversely, any asymmetric complete root must have `p^2!=1` and occurs with
its distinct reflected partner `(mu,q_sharp)`, with the same equal-integral
residual. This gives an exact counterexample-search diagnostic.

## 6. Boundary and adversarial audit

* `R=1` is excluded; there the relay labels merge and the nested map is
  degenerate.
* `q>1` is used only after the accepted terminal theorem or at a
  premise-complete candidate. It makes the equivalences in (3.4) and (4.4)
  nondegenerate.
* Grazing events are not silently included. The formulas are chamberwise;
  target roots are transverse by the accepted structural theorem.
* The fixed-time `q` derivative is distinguished from the moving terminal
  derivative, which is introduced only in (3.1).
* The scaling Jacobi field includes saltation exactly because relay event
  times are invariant under common state scaling.
* Reversibility alone is not claimed to imply symmetry. The missing global
  uniqueness/no-conjugate-point theorem is explicit.

Novelty status: `unknown`. No external theorem and no numerical evidence is
used in the derivation.
