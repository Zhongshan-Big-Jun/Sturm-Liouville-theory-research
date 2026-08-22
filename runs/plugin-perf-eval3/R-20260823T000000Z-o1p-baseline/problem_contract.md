# Problem contract

## Objects and definitions

- H: Hilbert space with dense monomials Pi = span{x^k : k >= 0}, and with
  well-defined moment functionals M_k(w) = <w, x^k>_H for all w in H.
- For finite r, v_1,...,v_r in H, V = { w in H : <w, v_j>_H = 0 for j=1..r }.
  We treat V as a closed subspace (the finite set of continuous linear
  functionals defines a closed subspace).
- Sparse family:
  p_0 = 1, p_1 = x,
  p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2}, m >= 2,
  p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.
- N = { n : p_n in V }, Q_sp = { p_n : n in N }.
- Run graph: vertices are nonnegative degrees; on the even side an edge
  (2m-2, 2m) is present iff 2m in N (m >= 2); on the odd side an edge
  (2m-1, 2m+1) is present iff 2m+1 in N (m >= 2). A run is a connected
  component of this graph. A free base b is the least element of a run,
  except that b = 0 or b = 1 is a free base only when that degree is not
  in N.
- B = finite or infinite set of free bases; B_fin = free bases whose run is
  finite.
- For a run R_b with least b, rho_b(b) = 1, rho_b(k) = floor(k/2)/floor(b/2)
  for b >= 2, and rho_b(k) = 1 for b in {0,1}. The run moment vector is
  m_b = (rho_b(k) 1_{k in R_b})_k.

## Hypotheses

- (H1) Pi is dense in H.
- (H2) M_k(w) is well defined for all k and w in H.
- r < infinity; the v_j are fixed elements of H.
- The benchmark additionally asks for a new rigorous advance beyond the closed
  subclasses H_beta (diagonal weighted l^2) and H_lambda (bandwidth 1 shift).

## Target conclusion

The reduced core O1' asks: decide, from the run structure determined by N
and the membership data, whether closure(span Q_sp) = V.

This run does not claim to solve general O1'. It targets a rigorous advance on
one or more concrete new non-diagonal families and/or a structure theorem.

## Quantifiers and dependency of constants

- The advance is for a family parameterized by (m, lambda, finite polynomial
  constraint data). Parameters are:
  - m >= 1 integer (bandwidth of the shift construction);
  - lambda = (lambda_1, ..., lambda_m) real, with the polynomial
    L(z) = 1 + sum_{s=1}^m lambda_s z^s having no zeros in the closed unit
    disk;
  - finite-degree polynomial representers v_j with coefficient vectors
    c^{(j)}_i, 0 <= i <= d_j < infinity.
- In the main new theorem, r may be zero. The conclusion is "closure(span Q_sp)
  = V" for the concrete H constructed from (m, lambda).

## Equivalent formulations that are actually proved equivalent

- Upstream master criterion (Theorem A, STRICT): closure(span Q_sp) = V iff
  V cap Q_sp^perp = {0}.
- Moment criterion (Theorem 2 of R-20260816T000000Z, STRICT): the obstruction
  elements are exactly those w in V whose moment sequence satisfies the kept
  sparse recursions.
- For the new family, we prove the finite-rank criterion:
  closure(span Q_sp) = V iff ker(T|_{B_fin}) = {0}, where T is the matrix
  whose columns are the finite-run moment vectors evaluated in the
  membership equations.

## Boundary and degenerate cases

- r = 0: V = H. The criterion says density holds iff there is no finite
  admissible run; for the new banded shift family this reduces to B_fin empty.
- lambda = 0: H reduces to H_0 = diagonal l^2 (beta = 0). The theorem should
  agree with the H_beta result in that special case.
- m = 1: H reduces to the already closed H_lambda family; the theorem becomes
  exactly the R-20260816T220000Z result.
- coefficients may be real; complex conjugation conventions are not used in
  the main statements (we state explicitly for real H).
- V = {0} degenerate: closure(span Q_sp)=V can hold only if Q_sp spans {0};
  handled by the general criterion.

## Permitted outcomes

- affirmative proof (density holds for a subclass/example),
- negative proof / counterexample (a concrete non-dense example),
- new structure theorem, exact decision criterion or reduction,
- honest RIGOROUS_PARTIAL_RESULT, with exact remaining gaps.

## Completion criteria

- A new theorem is complete for the run when its statement is proved under
  explicit hypotheses and the proof has no unstated assumption.
- General O1' is NOT a completion target for this run; the run is judged on
  a rigorous advance beyond H_beta and H_lambda.

## Acceptance criteria per subproblem

- Family extension (banded shift with bandwidth >= 2): prove a decision
  criterion and show it reduces to the bandwidth-1 theorem at m = 1.
- Concrete example: exhibit at least one non-diagonal bandwidth >= 2 instance
  where the conclusion is determined rigorously, or where a natural criterion
  fails.
- Structure theorem: show exactly where the H_beta/H_lambda criteria break or
  extend.

## Results that do not count as completion

- Numerical evidence without proof.
- A restatement of the upstream structure theorem without a new mechanism.
- A criterion with an unproved realizability step outside the treated family.

## Forbidden moves

- No numerical evidence as proof.
- No use of unverified recalled theorems as load-bearing.
- No silent quantifier change (e.g. treating general H as l^2).
- No claim that general O1' is solved when only a subclass is closed.

## Tool, citation, and search constraints

- Use the rigorous-open-math-research process.
- This is the BASELINE plugin variant; no additional mandatory reuse protocol.
- The project knowledge base and prior run artifacts are available; they are
  project-derived, not external verified literature.
- Web/literature search is allowed; every external fact needs provenance.

## Ambiguities or competing interpretations

- In the general statement, v_j are arbitrary elements of H. In the treated
  subclasses (H_beta, H_lambda, and the new banded shift family) they are
  taken to be finite polynomial combinations of monomials, unless explicitly
  stated otherwise. This is the natural subclass where the membership data
  becomes finite.
- The inner product convention for complex Hilbert spaces can introduce
  conjugates. We state all main new results for a real Hilbert space so no
  conjugate ambiguity arises.

## Contract audit

- This contract was written from the benchmark statement and required
  context. It is audited within the run (see audit_report.md).
