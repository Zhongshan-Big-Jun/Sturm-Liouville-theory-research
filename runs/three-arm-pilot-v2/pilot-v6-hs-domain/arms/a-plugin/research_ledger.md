# Research ledger

## 2026-08-28 — Run initialization

- Authoritative input: frozen user statement in the active conversation.
- Restrictions copied literally into `problem_contract.md`.
- Deliberately did not list/read existing project files, inspect `.git`, query the
  network, or consult a known solution.  This overrides the skill's normal
  repository-state and literature checks.
- Read only the requested installed skill protocol and its contract,
  closure-first, and orchestration references outside the working directory;
  these are workflow instructions, not mathematical context.
- Created a fresh namespaced artifact directory to avoid touching unknown files.

## Contract normalization and audit

- Found a material notation collision between genuine operator inverse and formal
  polynomial inverse.  Froze both readings rather than silently choosing one.
- Built the shortest obligation chain.  Selected O1 as the first open
  load-bearing claim.
- No mathematical route portfolio or research child was opened before the
  contract audit.

## Closure-first preflight: O1

- Direct proof: Cauchy--Schwarz gives nonnegativity of the Krein form; its
  equality case gives exactly the affine kernel.  Integration by parts plus
  surjectivity of the endpoint trace gives both boundary equations.
- Cheap exact probes: \(1,x\) give zero and \(x^2\) gives \(8/3\); independent
  endpoint trace choices confirm neither boundary equation is redundant.
- Decision: `CLOSED`.  Next first open load-bearing claim is O2.

## Direct proof round: O2

- For a positive self-adjoint \(A\), spectral calculus gives
  \(D(A^{m+1/2})=\{f\in D(A^m):A^mf\in D(A^{1/2})\}\) and the usual recursive
  criterion for \(D(A^m)\).  Applied to a polynomial, every residual Sobolev
  regularity condition is automatic, leaving exactly the boundary equations
  for \(L^jp\), \(0\le j<m\).
- Odd-half-power falsification probe: \(s=5\) requires the conditions on \(p,Lp\)
  but no condition on \(L^2p\), only \(L^2p\in H^1\); this matches the formula.
- Decision: O2 `CLOSED` at coordinator level.

## Mechanism-distinct parity round: O3E and O3O

- Even route: assuming \(v=L_{\rm poly}^{-1}P_n\in D(K_c)\), L2 orthogonality
  to \(P_n-cv=-v''\) yields
  \(\|K_cv\|^2=c\langle K_cv,v\rangle\).  Thus
  \(\langle(K_0+c)v,K_0v\rangle=0\), so \(v\in\ker K_0\), impossible for
  \(n\ge2\).
- Odd route: assuming \(v=L_{\rm poly}^{-1}R_n\in D(K_c)\), form orthogonality
  to \(R_n-cv=-v''\) yields
  \(a_c(R_n,R_n)=c\|R_n\|_2^2\), hence \(a_0(R_n,R_n)=0\), impossible for
  degree \(n\ge2\).
- In both routes degrees 0 and 1 are affine eigenfunctions with eigenvalue \(c\),
  hence lie in every positive power domain.  Decision: O3E/O3O/O4 `CLOSED` at
  coordinator level.

## Completion and density round: O5 and O6

- \(L^r\) identifies the abstract even completion with \(L^2\), and the abstract
  odd completion with the \(H^1\) form space.  \(K_c^r\) identifies the matching
  operator domain with the same base.  The resulting unitary applies boundary
  correction and is not the identity on degree \(n\ge2\) polynomial
  representatives.
- Therefore canonical equality fails although unitary equivalence holds.
- The literal polynomial OPS span contains elements outside the operator domain,
  so it is not a dense linear subspace there.  The genuine operator-inverse images
  are, by contrast, a dense orthogonal basis.
- Decision: O5/O6 `CLOSED` at coordinator level; independent audit O7 remains.

## Exact computation probe

- Protocol: `reproducibility/computation_protocol.md`; exact symbolic arithmetic,
  finite \(0\le n\le8\), \(1\le r\le4\), falsification only.
- First replay failed after all \(r=1\) cases because the script encoded
  \(c-q''\) instead of \(cq-q''\) in the \(r>1\) recurrence assertion.  This is
  an implementation counterexample, not mathematical evidence.  The exact line
  was repaired locally; the full replay must pass before the script is retained.

## Exact replay result

- The repaired deterministic replay exited 0 and printed
  `ALL_EXACT_CHECKS_PASS`.  It checked only the finite symbolic domain in the
  computation protocol and was not used to close a universal obligation.

## Independent global audit: O7

- One isolated verifier read only the four packet-listed, SHA256-bound inputs.
- Verdict: `PASS`; `critical_errors=[]`, `gaps=[]`, `first_error=null`.
- Covered all \(c>0\), integers \(s\ge4\), all \(n\ge0\), even/odd powers,
  both inverse readings, all three conclusions, and definition/logic/boundary/
  adversarial categories.
- Full audit-file hash:
  `046e7db41ea7f1043b85a172b65e5c535b457cc9d46c61b77a25b4f6edf00c3b`.
- The auditor's detached-content convention was independently reproduced:
  `6c35d10326702369a50821314d7a69be54fbda2f93926a5b14c6c21363ba52d9`.
- Decision: O7 `CLOSED`.  No proof revision was requested.

## Fresh-context convergence check: first pass

- Hash verification passed and O0--O7 were all recognized as closed.
- State returned `DIVERGING` solely because four route records, one audit-matrix
  cell, and two status sentences retained pre-audit/pending language.
- Exact repair applied to those metadata owners.  Candidate proof, contract, and
  independent audit inputs were not changed.
- A hash-bound second pass is required before terminal reporting.

## Fresh-context convergence check: repaired pass

- State: `CONVERGING`; every listed hash and every exact metadata repair verified.
- Closed obligations: O0--O7; first open obligation: null; issues: none.
- Status consistency: `INDEPENDENTLY_AUDITED_PROOF`; terminal ready: true.
- Raw JSON full-file SHA256:
  `2cba1b8beab8818b06fa05a98cb4f7f630246d614c375a8ada513fe865422367`.
