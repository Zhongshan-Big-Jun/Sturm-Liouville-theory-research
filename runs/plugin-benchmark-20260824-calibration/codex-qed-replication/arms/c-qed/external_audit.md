# Arm C external anonymous audit

Verdict: `PASS`.

First erroneous or unsupported step: none.

Complete gap list: empty.

## Review protocol

This is the final label-blind review. The frozen task and candidate were copied to a neutral content-only directory whose names disclosed neither the arm nor the system. The fresh reviewer was instructed to inspect only those two files and had no repository, git, network, memory, skill, plugin, benchmark metadata, prior solution, or conversation context.

An earlier independent reviewer also returned `PASS`, but that review's source path contained the Arm C label. It is retained only as corroboration and is not the basis for the label-blind claim.

## Independent checks

- Transfer order is correct. For the spatial sequence `L,H_s,L,...,H_s,L`, column-state propagation gives `L(H_sL)^n`, and direct multiplication yields the stated `C_s=H_sL`.
- With initial state `(0,1/sqrt(lambda))^T`, `F(lambda)=u(1,lambda)=G(y)/sqrt(lambda)`. Thus, on `0<y<pi`, zeros of `G` correspond bijectively to positive Dirichlet eigenvalues below `lambda_*=(pi/(st))^2`.
- At `y=pi`, every block matrix is `-I`. The resulting eigenfunction vanishes precisely at the `2n` internal interfaces and nowhere inside a block. Sturm oscillation therefore indexes `lambda_*` as `lambda_{2n+1}`, giving exactly `2n` eigenvalues below it.
- The Lagrange identity has the correct sign:

  ```text
  (u' dot(u)-u dot(u)')' = rho u^2.
  ```

  Hence

  ```text
  u'(1,lambda_k) F'(lambda_k) = integral_0^1 rho u^2 dx > 0.
  ```

  Differentiating `F=G(y)/sqrt(lambda)` at a zero gives

  ```text
  F'(lambda_k) = st G'(y_k)/(2 lambda_k),
  ```

  so analytic simplicity transfers correctly.
- For `n=1`,

  ```text
  G = q ((s+2+s^(-1))c^2-s),
  ```

  whose two interior roots satisfy `|c|=s/(s+1)` and are simple.
- Endpoint and special-value checks are correct:

  ```text
  G'(0)=(n+1)+n/s,
  G'(pi)=-((n+1)+n/s),
  G(pi/2)=(-s)^n != 0.
  ```

- At `R=1`, `G(y)=sin((2n+1)y)`, giving exactly `2n` simple interior zeros.

The review was performed after the scored QED run and is excluded from Arm C usage.
