# Approach registry

## Route R-DOM — spectral/domain recursion

- **route_key:** `spectral-power-recursion`
- **Target:** O2.
- **Core mechanism:** the spectral definition of positive self-adjoint powers,
  followed by the operator-domain recursion and smoothness of polynomials.
- **Why easier:** it reduces a fractional-domain question to finitely many
  endpoint equations.
- **Tier/minimal probe:** Tier 1; check \(s=4,5\) explicitly.
- **Falsification:** test whether an odd half-power adds an endpoint condition.
- **Result:** `PROVED`.  For polynomials it adds only the requirement
  \(L^m p\in H^1\), which is automatic.
- **Exact gap:** none; independent global audit PASS.

## Route R-EVEN — L2 orthogonality and spectral positivity

- **route_key:** `even-orthogonality-affine-kernel`
- **Target:** O3E/O4 for \(s=2r\).
- **Core mechanism:** if \(v=L_{\rm poly}^{-1}P_n\) obeyed the Krein condition,
  then \(P_n=K_cv\); orthogonality to \(P_n-cv=-v''\) forces equality in the
  spectral lower bound \(K_c\ge cI\), hence \(v\in\ker K_0\).
- **Tier/minimal probe:** Tier 1; degrees \(0,1,2\).
- **Falsification:** the proof must not infer a boundary condition from formal
  inversion; it assumes it only for contradiction.
- **Result:** `PROVED`; precisely \(n=0,1\).
- **Exact gap:** none; independent global audit PASS.

## Route R-ODD — form orthogonality and equality kernel

- **route_key:** `odd-form-orthogonality-affine-kernel`
- **Target:** O3O/O4 for \(s=2r+1\).
- **Core mechanism:** with \(R_n=K_cv\), form orthogonality to
  \(R_n-cv=-v''\) forces \(a_0(R_n,R_n)=0\), hence \(R_n\) is affine.
- **Tier/minimal probe:** Tier 1; degrees \(0,1,2\).
- **Falsification:** verify the representation identity is used with the
  operator-domain argument in the correct slot.
- **Result:** `PROVED`; precisely \(n=0,1\).
- **Exact gap:** none; independent global audit PASS.

## Route R-COMP — compare completions by their base-space transforms

- **route_key:** `canonical-vs-unitary-completion`
- **Target:** O5/O6.
- **Core mechanism:** compare the algebraic isometries \(L^r\) with the true
  operator isometries \(K_c^r\).
- **Tier/minimal probe:** Tier 1; evaluate both inverses on one degree-2
  polynomial.
- **Falsification:** do not call unitary equivalence literal equality.
- **Result:** `PROVED` at coordinator level.  The spaces are naturally unitary
  through boundary correction, but not equal under the identity on polynomial
  representatives.  The literal polynomial span is not even contained in the
  operator domain; the genuine operator-image span is dense.
- **Exact gap:** none; independent global audit PASS.

## Avoid list

- Treating \(L_{\rm poly}^{-1}\) and \(K_c^{-1}\) as the same map.
- Inferring density from orthogonality in the wrong completion.
- Inferring that only affine *linear combinations* lie in the domain from the
  fact that only the individual OPS members of degrees 0 and 1 do.
