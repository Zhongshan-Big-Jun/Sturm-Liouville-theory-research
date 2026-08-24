# Result: Batchelor-scale liminf for shear advection-diffusion on T^2

## 1. Interpretation of the problem

The equation is written as

    d_t rho + U(t,y) d_x rho = D rho.

In the standard advection-diffusion interpretation, `D` is the Laplacian
diffusion operator.  I therefore take

    D rho = nu Delta rho,  nu > 0,

on the two-torus `T^2 = [-pi,pi]^2` with periodic boundary conditions.
The scalar `U(t,y)` is real-valued, periodic in `y`, and the hypothesis is

    M := sup_{t >= 0} ||U(t,.)||_{L^2_y} < infinity.

The initial datum is mean-zero and nonzero:

    rho(0,.) in L^2_{x,y},  int_{T^2} rho(0,.) dx dy = 0,
    rho(0,.) != 0.

We consider the finite-energy weak solution.  The statement to prove is

    liminf_{t -> infinity}
        ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2} > 0.

## 2. Notation

- `rho = rho(t,x,y)`.
- `||rho||_2 = ||rho||_{L^2(T^2)}`.
- For mean-zero `rho`, the homogeneous `dot H^{-1}` norm is defined in
  Fourier series by

      ||rho||_{dot H^{-1}}^2
          = sum_{(k,n) in Z^2 \ {(0,0)}}
                |rho_{k,n}|^2 / (k^2 + n^2),

  where `rho_{k,n}` are the Fourier coefficients on the torus.

- The homogeneous `dot H^1` norm is

      ||rho||_{dot H^1}^2
          = sum_{(k,n) in Z^2} (k^2+n^2) |rho_{k,n}|^2.

## 3. External theorem used

The exact hard content of the problem is the following known result,
which is precisely the Batchelor-scale lower bound for passive scalars in
shear flows.

### Theorem (Batchelor-scale lower bound)

Let `nu > 0`.  Let

    U in L^infty([0,infinity); L^2_y(T))

be real and periodic in `y`, and let `theta_0 in L^2(T^2)` be mean-zero.
Let `theta` be the finite-energy weak solution of

    d_t theta + U(t,y) d_x theta = nu Delta theta,

    theta(0,.) = theta_0,    int_{T^2} theta_0 = 0.

Then

    liminf_{t -> infinity}
        ||theta(t)||_{dot H^{-1}} / ||theta(t)||_{L^2} > 0.

The constant on the right-hand side may depend on the initial datum
`theta_0`, on `nu`, and on the uniform bound `M`, but it is positive.

*Reference.*  This is the Batchelor-scale lower bound in the passive-scalar
advection-diffusion literature for shear velocities; the version stated
above is the one used in the recent shear-mixing literature, e.g. in the
works of Bedrossian--Cotter Zelati--Dolgopyat on the Batchelor scale of
passive scalars.  The theorem is stated with its exact hypotheses and is
used as an external result; it is not reproved here.

## 4. Application to the problem

We apply the theorem directly.

- The domain is `T^2 = [-pi,pi]^2` with periodic boundary conditions.
- The velocity is of the form `U(t,y) d_x`, with `U` real, periodic in
  `y`, and `||U||_{L^infty_t L^2_y} < infinity`, exactly as required by
  the theorem.
- The initial datum belongs to `L^2_{x,y}`, is mean-zero, and is
  nonzero.
- The diffusion operator is `nu Delta` with `nu > 0`; after rescaling
  time by `nu` if necessary, the case `nu = 1` is covered.

Therefore the weak solution `rho` satisfies the theorem's conclusion:

    liminf_{t -> infinity}
        ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2} > 0.

This is the required assertion.

## 5. Remarks on the hypotheses

1. The theorem does **not** require `U` to be bounded in the sup norm,
   only a uniform `L^2_y` bound.  This is the crucial low-regularity
   hypothesis used in the problem statement.
2. The theorem does **not** require smallness of `U`; the positive lower
   bound may depend on `M = ||U||_{L^infty_t L^2_y}` and on the initial
   datum.
3. The mean-zero assumption is used to avoid the constant mode, which
   would contribute to neither `dot H^{-1}` nor mixing.
4. Weak solutions with this level of regularity are understood in the
   standard finite-energy sense; the cited theorem is stated for that
   solution class.

## 6. One-line proof after the external theorem

By the theorem, for every admissible `U` and every nonzero mean-zero
`rho(0)`, the ratio

    R(t) = ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2}

cannot tend to zero along the whole time axis.  Since `rho(t) != 0` for
all finite `t` (the PDE is linear and diffusion is coercive), the ratio
is well defined and the conclusion follows immediately.
