INDEPENDENTLY_AUDITED_PROOF

# Pilot v6 Arm A blind mathematical audit

## Verdict

`PASS`

The candidate proves the frozen task under both readings forced by the wording: the abstract polynomial reading, where `K_c^{-r}` is represented algebraically by `L_poly^{-r}`, and the genuine operator-inverse reading. No load-bearing gap was found.

This is a posthoc neutral audit and is excluded from scored Arm A metrics.

## Isolation and provenance

The mathematical audit used only:

- `frozen_task.md`, SHA-256 `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- `candidate_proof.md`, SHA-256 `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`.

After the proof had been independently checked and the provisional verdict was already `PASS`, the permitted internal audit was read as a comparison check:

- `SUB-O7-global-audit.json`, SHA-256 `046e7db41ea7f1043b85a172b65e5c535b457cc9d46c61b77a25b4f6edf00c3b`.

No repository history, hidden gold, sibling arm, network source, or other project artifact was inspected.

## Statement fidelity

The frozen statement calls the system polynomial while also describing it through `K_c^{-r}`. The candidate does not silently collapse these distinct meanings.

- Under the abstract polynomial reading, it proves `Q_n^(s) in D(K_c^(s/2))` exactly for `n=0,1`, proves failure of canonical equality with the operator domain under the identity on polynomial representatives, constructs the boundary-correcting unitary, and proves that the literal full span is not a subspace of the operator domain.
- Under the genuine spectral inverse reading, it proves that every inverse image lies in the required domain and that the corresponding span is dense. It also correctly notes that these inverse images are generally not polynomials.

Thus all three requested conclusions are answered without changing the quantifiers `c>0`, integer `s>=4`, and `n>=0`.

## Definition and sign audit

With inner products linear in the first variable, integration by parts gives the boundary coefficients

`f'(1)-Delta(f)/2` and `-f'(-1)+Delta(f)/2`.

Their simultaneous vanishing is exactly the stated Krein condition at `1` and `-1`. Also,

`a_0(f,f)=integral |f'-Delta(f)/2|^2`,

so the form is nonnegative and its nullspace is precisely the affine functions. Adding `c||f||_2^2` for `c>0` gives strict positivity and the stated form domain `D(K_c^(1/2))=H^1[-1,1]`. The endpoint signs and the affine equality case are correct.

## Power-domain recursion

For every polynomial `p` and integer `m>=1`, induction on the operator power gives

`p in D(K_c^m)` if and only if `B(L^j p)=0` for `0<=j<m`.

For self-adjoint `A>=cI>0`, spectral integration gives

`D(A^(m+1/2))={f in D(A^m): A^m f in D(A^(1/2))}`.

Once the integer boundary gates hold, `A^m p=L^m p` is again a polynomial and hence belongs to `H^1`. Therefore the candidate's criterion with `0<=j<floor(s/2)` is exact. At the boundary cases `s=4` and `s=5`, the same last integer gate is present, and the odd half-power adds no unverified boundary condition.

## Even and odd orthogonality arguments

In the even case, assuming `v=L_poly^{-1}P_n` lies in `D(K_c)` makes `K_cv=P_n` and `P_n-cv=-v''`, a polynomial of degree at most `n-2`. Orthogonality yields

`0=||K_0v||_2^2+c a_0(v,v)`,

so `v` is affine. Degree preservation of `L_poly^{-1}` contradicts `n>=2`.

In the odd case, form orthogonality of `R_n` to `R_n-cv=-v''`, together with the representation identity and Hermitian symmetry, gives

`0=a_c(R_n,R_n)-c||R_n||_2^2=a_0(R_n,R_n)`.

Thus `R_n` is affine, again contradicting `n>=2`. For `n=0,1`, all relevant polynomials and inverse images are affine, satisfy the Krein condition, and are eigenvectors with eigenvalue `c`, so they belong to every positive power domain. This closes both parity cases uniformly for every allowed `c`, `s`, and `n`.

## Completion and density audit

The abstract maps `L^r` have dense polynomial range in `L^2` for even `s` and in `H^1` with the Krein form norm for odd `s`. The operator maps `K_c^r` are unitary from the corresponding positive power domains to those same target spaces because `K_c>=cI>0`. Their composition therefore gives the claimed boundary-correcting unitary.

Canonical equality under the identity fails exactly: `x^2` is a valid abstract polynomial representative, but `B(x^2)=(2,-2)`, so it is not in `D(K_c)`, hence not in `D(K_c^(s/2))` for `s>=4`.

Under the polynomial reading, the full literal span contains non-domain elements for every `n>=2`, so it is not a subset of the operator-domain Hilbert space and cannot be dense there as a linear subspace. The individually admissible named elements span `span{1,x}`, which is proper and finite-dimensional. Under the genuine inverse reading, `K_c^{-r}` transfers the complete `P_n` or `R_n` system unitarily into the appropriate operator domain, so the tilded span is dense.

Possible cancellations among high-degree linear combinations do not alter the literal-span conclusion: they may affect `span{Q_n^(s)} intersect D(K_c^(s/2))`, but they cannot make the full span a subset of the domain. The frozen task does not require the spectrum of that intersection.

## Four-part audit result

- Definition audit: `PASS`.
- Logic audit: `PASS`.
- Boundary audit: `PASS`.
- Adversarial audit: `PASS`.

## First failing step and repairs

First failing step: none.

Critical errors: none.

Gaps: none.

Repair required: none.

One non-substantive wording improvement is available: `span{1,x}` is a two-dimensional linear space consisting of affine functions, rather than a two-dimensional affine space. The displayed formula and every inference use the correct linear span, so this does not change the verdict.

## Blind score

| Axis | Score | Maximum |
|---|---:|---:|
| Correctness | 40 | 40 |
| Completeness | 25 | 25 |
| Rigor and auditability | 19 | 20 |
| Relevance | 10 | 10 |
| Reproducibility | 5 | 5 |
| Total | 99 | 100 |

The one-point deduction records the isolated linear-space versus affine-space wording and the absence of formal proof-assistant certification. Neither is a mathematical gap.
