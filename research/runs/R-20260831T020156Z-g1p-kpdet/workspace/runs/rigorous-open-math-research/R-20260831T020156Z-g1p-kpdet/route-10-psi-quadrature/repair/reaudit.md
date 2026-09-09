# Narrow independent re-audit of the E binding

## Verdict

`PASS`.

Audit ID: `REAUDIT-DIRECT-E-BINDING-01`.

This re-audit checks only immutable E provenance, equations E1-E6, the repaired Q7-Q8 identity, and strict sign preservation. It does not reopen Q1-Q6 and does not attempt or approve Q9.

## Input integrity

All three authorized SHA-256 values were independently recomputed before use and matched exactly.

| Input | Verified SHA-256 |
| --- | --- |
| `route-08-common-beta-orientation/prover_result.md` | `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d` |
| `route-10-psi-quadrature/audit/independent_audit.json` | `cc54e0dc73e2d8de402a669818f3145176f4d7e94e5f4f15fad869642998dd04` |
| `route-10-psi-quadrature/repair/e_binding_repair.md` | `f5956bc3c6b00c28ed02237095fda7b0478bb5718f6c88098db588753172bf3c` |

The immutable Route 08 source states the exact denominator-safe E formula as equation (13). The repair reproduces that formula as E0 without changing a factor, exponent, or denominator term. This closes the provenance omission identified by the first Route 10 audit.

## Verification of E1-E4

Use

```text
r=sigma^(-2),
M=m^2,
k=M-1,
sin(d)=sqrt(r)sin(g).
```

The last equality has the positive square root because all acute-branch sines are positive. Then

```text
sigma=r^(-1/2),
(sigma^2-1)^2=(1-r)^2/r^2,
cos(g)^2+M sin(g)^2=1+k sin(g)^2,
cos(d)^2+M sin(d)^2=1+k r sin(g)^2.
```

Thus E1 is exact. Substitution in the E0 numerator gives

```text
c k(1-r)^2 sin(g)cos(d)cos(g)/r^(3/2),
```

which is E2. The E0 denominator becomes

```text
m r^(-1/2)
[cos(d)(1+k sin(g)^2)
 +c sqrt(r)cos(g)(1+k r sin(g)^2)],
```

which is E3. Dividing E2 by E3 cancels `r^(-1/2)` and leaves one factor `1/(mr)`. Therefore

```text
mrE=
c k(1-r)^2 sin(g)cos(d)cos(g)
/
[cos(d)(1+k sin(g)^2)
 +c sqrt(r)cos(g)(1+k r sin(g)^2)].
```

This is E4 with no omitted scaling factor.

## Verification of E5-E6

The positive lock gives

```text
sin(A)=sqrt(r)sin(B),
sigma=r^(-1/2).
```

Substitution in

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)]
```

gives

```text
mrq=[c cos(B)-sqrt(r)cos(A)]/sin(B),
```

which is E5. The first term of Q7 is E5 and the second term is E4. Their difference is therefore

```text
Q_quad=mr(q-E),
q-E=Q_quad/(mr).
```

This verifies E6 and the repaired Q7-Q8 identity.

## Strict sign audit

On the stated acute branch,

```text
m>1,
r>0,
c>0,
k>0,
0<d,g<pi/2.
```

Hence every factor in

```text
cos(d)(1+k sin(g)^2)
+c sqrt(r)cos(g)(1+k r sin(g)^2)
```

is positive, and the denominator is strictly positive. Also `mr>0`. Division in E4 and E6 is safe and preserves the strict sign of `q-E` exactly. No squaring or numerical approximation supplies a sign choice.

## Global status

The sole dependency gap identified in the first Route 10 audit is repaired. Q7-Q8 are accepted as exact denominator-safe identities. Q1-Q6 remain accepted without being reopened.

Q9 is still open and is neither attempted nor approved here. Complete `c>2/3` `PHI-SIGN` and KP-DET remain open. No numerical evidence is used.
