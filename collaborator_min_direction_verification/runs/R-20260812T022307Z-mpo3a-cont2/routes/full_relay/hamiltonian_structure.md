# Continuous Hamiltonian and symplectic saltation of the full relay

This note is an auxiliary exact observation for the relay in
`derivation.md`.  It is not a nondegeneracy theorem.

Use state coordinates `z=(U,P,V,Q)=(U,U_t,V,V_t)` and the signed symplectic
form

```text
omega=dU wedge dP-dV wedge dQ.                       (1.1)
```

We use the convention `i_{X_H} omega=dH`.

Put `S=U^2-mu^2 V^2`.  Define the continuous piecewise-linear potential

```text
Phi_max(S)=S/2 for S<=0,  R S/2 for S>=0,
Phi_min(S)=R S/2 for S<=0, S/2 for S>=0.             (1.2)
```

Then both saturation signs are Hamiltonian systems with

```text
H_e(z)=1/2(P^2-Q^2)+Phi_e(S).                         (1.3)
```

Indeed Hamilton's equations for (1.1) give

```text
U_t=P, P_t=-rho U, V_t=Q, Q_t=-mu^2 rho V,           (1.4)
```

where `rho=2 Phi_e'(S)` away from `S=0`.  Moreover `2H_e` is exactly the
global relay energy `E` from Theorem 3.1.  The Hamiltonian is continuous at
every event because the two material Hamiltonians differ by

```text
H_+-H_-=(Delta rho/2)S,                               (1.5)
```

which vanishes on the switching surface.

At a transverse event, let `f_-` and `f_+` be the two smooth vector fields
and let

```text
n=grad S=(2U,0,-2mu^2 V,0)^T,
d=n^T f_-=S'!=0,
a=f_+-f_-=(0,-Delta rho U,0,-mu^2 Delta rho V)^T.     (1.6)
```

The exact variational jump is the saltation matrix

```text
Xi=I+a n^T/d.                                         (1.7)
```

Since `n^T a=0`, the matrix determinant lemma gives

```text
det Xi=1.                                             (1.8)
```

More strongly, (1.5) makes `a` the Hamiltonian vector field of a scalar
multiple of `S`.  Equivalently, if `Omega` is the matrix of (1.1), then
`Omega a` is proportional to `n`.  Substitution in (1.7) gives

```text
Xi^T Omega Xi=Omega.                                  (1.9)
```

Every constant-cell fundamental matrix is also symplectic for (1.1).
Therefore the complete transverse fixed-parameter four-dimensional state
monodromy, including all moving event-time corrections, is symplectic and
has determinant one.  Parameter-augmented sensitivity maps are not asserted
to be symplectic.

Consequences and limitation:

- finite-difference Jacobians that omit (1.7) are not the exact relay
  variational flow;
- a kernel/nondegeneracy argument may be recast as a Lagrangian-intersection
  or conjugate-point problem for the symplectic monodromy;
- volume preservation or symplecticity alone does not exclude conjugate
  points and does not prove `det D_x G_e!=0`.

Epistemic status: exact auxiliary lemma, pending independent audit.
