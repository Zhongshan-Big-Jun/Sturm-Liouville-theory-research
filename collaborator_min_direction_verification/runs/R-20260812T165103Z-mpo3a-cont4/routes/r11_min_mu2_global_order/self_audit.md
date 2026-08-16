AUTHOR_SELF_AUDIT

# R11 conditional global-order / restricted min corollary self-audit

This is the author-side audit of the frozen candidate derivation.  It is
not the independent audit required for proposal promotion and it changes no
canonical or previously frozen route file.

## Immutable binding and exact scope

```text
derivation:
  routes/r11_min_mu2_global_order/derivation.md
derivation_bytes:
  20003
derivation_sha256:
  sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93
canonical_blueprint:
  sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242
canonical_inventory:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
trusted_R10_semantic:
  semantic-sha256:157a7bf928676b7565e5e08e965909ab0657e48888d37095c43352a228bbbd21
trusted_R10_derivation:
  sha256:44da5f1d76b4d8208366b3d055e4ad5456e372bd2f14077a39e51577a4353f19
sign_independent_R9_template:
  sha256:37cd0c8be3fbb542faeaec875c6a24c007a59f9918a672e07a7140340acb2706
external_results:
  []
computational_certificates:
  []
```

The package proves two deliberately separated records.

1. `INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11` is a conditional
   theorem for fixed finite `R>1`, `n>=2`, `mu>1` and either relay
   orientation.  Its hypothesis is a single strict sign
   `sigma partial_q A_n^c>0` at every premise-complete common-terminal
   root.  It does not prove that hypothesis.
2. `INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11` is unconditional in its
   restricted scope because trusted R10 supplies that hypothesis with
   `sigma=-1`.

Their exact-statement hashes are, respectively,

```text
sha256:fcb02db540fdab1a2a4b7201030e64a47c1756c16caad0c3f2c4fe315ae4cbc3
sha256:2fa736de49562b7d9ba23ff321dfe998d6f8787b282cb9ecf6bbd6382c46cbda
```

## 1. Definition audit: PASS

1. The relay is parameterized by the coefficient `rho_-` on `S<0` and
   `rho_+` on `S>0`, with `{rho_-,rho_+}={1,R}`.  Thus max has
   `rho_-=1` and min has `rho_-=R`.  No sign-sensitive statement is left
   with an unqualified material label.
2. `S=U^2-mu^2V^2` and the scalar equations use the same `mu^2`
   normalization.  At `mu=2` this becomes `S=U^2-4V^2` and
   `V_tt=-4rho V`, exactly the R10 convention.
3. `A_n=T_U^n-T_V^(n+1)` uses positive scalar zeros; for the corollary this
   is `A_2=T_U^2-T_V^3`.  Relay-interface zeros, scalar nodal zeros, and the
   common terminal joint zero are never identified with one another.
4. `q=V_t(0)/U_t(0)` after the positive normalization `U_t(0)=1` is the
   permanent-common-scaling quotient coordinate in which R10 states
   `partial_q A_2<0`.
5. `A_n^c` denotes only the smooth fixed-word continuation of the final
   negative-sign cell.  `A_n` denotes the global indexed residual.  Their
   values and first derivatives at a root are connected by the separately
   proved softness estimate, not by definition.
6. The reflection normalization gives `U#_t(0)=1` and
   `V#_t(0)=|r|/|p|`.  Independent signs on `U,V` do not alter `S` because
   both squared terms receive the common factor `|p|^-2`.

## 2. Logic audit: PASS

1. Cellwise energy conservation glues exactly at `S=0`.  Its strict value
   `1-q^2<0` excludes every nonjoint tangency.  At a joint zero it gives
   `P^2-mu^2Q^2<0` and hence a punctured `S<0` neighborhood with material
   `rho_-`.
2. The global IVP construction uses only transverse sign selection and the
   joint-contact classification.  The no-Zeno argument treats both possible
   accumulation limits and therefore does not assume a uniform positive
   lower bound on cell length.
3. Continuous dependence is proved by compactness, not a fixed event word.
   At a limiting relay zero, the energy identity survives before the limit
   ODE is identified; this makes the limiting zero set finite and licenses
   pointwise coefficient convergence and dominated convergence.
4. The phase inequality `theta_t>=1` gives existence of every required
   indexed scalar zero on a uniform finite horizon.  Simplicity plus uniform
   state convergence makes each indexed zero time continuous.
5. At a residual zero, scalar nodal counts place `1` and `mu^2` at
   consecutive Dirichlet indices.  Strict interlacing and the exact
   Wronskian sign make `V/U` decrease through both `+1/mu` and `-1/mu`
   once per `U` cell.  Hence there are exactly `2n` active transverse
   events before any local twist theorem is invoked.
6. The terminal softness argument keeps the final `rho_-` chamber.  The
   potential coefficient mismatch acts for `O(|delta|)` time on positions
   of size `O(|delta|)`.  Starting from the common entry state gives
   velocity error `O(delta^2)` and position error `O(|delta|^3)`; nonzero
   terminal slopes then preserve the indexed scalar zeros and give
   `A_n-A_n^c=O(delta^2)`.
7. The oriented-zero lemma is applied to `sigma A_n`.  Thus it covers both
   positive and negative local derivatives and needs differentiability only
   at zeros.
8. Trusted R10 is applied only after the global min `A_2` zero has been
   proved to be a premise-complete four-event, possibly asymmetric root.
   R10 supplies `partial_q A_2^c<0` without a reflection premise; Section 6
   transfers it to the global derivative.
9. Reflection is used only after at-most-one.  The reflected root has the
   same `R,n,mu`, relay orientation and nodal indices, so uniqueness of the
   root parameter gives `q#=q`; IVP uniqueness then gives trajectory fixing.
10. The general result remains an implication.  The only unconditional
    local-sign input used is trusted R10 at min `n=2,mu=2`.

## 3. Boundary audit: PASS

- The conditional lemma covers every fixed finite `R>1`, integer `n>=2`,
  `mu>1`, and both choices of `rho_-`, but only under its explicit
  same-sign local derivative hypothesis.
- The unconditional theorem covers every finite `R>1` only at min
  `n=2,mu=2`.  It includes arbitrary asymmetric roots and does not assume
  reflection.
- For `n=2` the proof uses exactly two `U` nodal cells and obtains four
  active events directly; no internal-cell induction or nonexistent middle
  case is used.
- `R=1`, `mu=1`, and `q=1` are excluded by strict hypotheses.  No endpoint
  value at `q->1+` or `q->infinity` is required for at-most-one.
- Nonzero grazing is impossible.  Interior event collisions and terminal
  event-pair birth/death are retained as negative-side joint contacts and
  treated explicitly.
- Both initial and terminal min punctured cells use material `R`.  The
  terminal continuation is not copied with the max coefficient `1`.
- A root need not exist.  General-`mu` min twist, `n>2` min twist,
  equal-norm existence/orientation, min O3a and universal O3a remain open.

## 4. Adversarial audit: PASS within the declared scopes

- **Initial-material attack:** `S=(1-mu^2q^2)t^2+o(t^2)<0` fixes
  `rho_-`; the min specialization therefore starts with `R`.
- **Wrong terminal material attack:** every terminal common zero has
  `S<0` on both punctured sides, and the chamber continuation uses
  `rho_-`, hence `R` for min.
- **Fixed-word branch attack:** Sections 3--4 construct one global residual
  independently of material words; chambers are used only for local
  differentiation.
- **Hidden invalid-root attack:** Section 5 derives the complete `2n`
  event structure from nodal indexing and strict interlacing before R10 is
  called.
- **Generic relay-softness attack:** the proof does not claim softness for a
  generic discontinuous vector field.  It uses that this relay's
  acceleration jump is proportional to the two positions vanishing at the
  terminal contact.
- **First-order mismatch attack:** a possible `O(1)` coefficient jump is
  multiplied by `U,V=O(|delta|)` inside an `O(|delta|)` window; the
  resulting velocity error is second order.
- **Derivative-sign attack:** min R10 gives a negative derivative and the
  proof takes `sigma=-1`.  No positive max orientation is reused.
- **Closure-derivative attack:** `A_n=A_n^c+O(delta^2)` proves equality of
  first derivatives at the closure rather than assuming it.
- **Repeated-zero-set attack:** the zero set used in the oriented-zero lemma
  is closed on the compact interval between two alleged roots, and every
  zero is isolated by its nonzero derivative; the first subsequent zero is
  therefore well defined.
- **Reflection circularity attack:** neither premise completeness nor the
  local derivative uses reflection.  Reflection appears only after global
  at-most-one.
- **Scaling attack:** positive normalization and the terminal
  `|p|`-division are explicit; `q#=|r|/|p|>1` follows from the exact energy.
- **Generalization attack:** the conditional arbitrary-`n,mu` lemma is not
  reported as an unconditional min theorem.  The only closed new theorem is
  min `n=2,mu=2` global at-most-one/reflection rigidity.

## Proof-obligation map and verdict

```text
conditional lemma:
  local same-sign twist: EXPLICIT HYPOTHESIS
  global IVP / continuity: DISCHARGED
  automatic premise completeness: DISCHARGED
  terminal first-variation transfer: DISCHARGED
  at-most-one / reflection fixing: DISCHARGED

restricted min n=2, mu=2 corollary:
  local negative twist: DISCHARGED BY TRUSTED R10
  all sign-independent obligations: DISCHARGED ABOVE
  unresolved_mathematical_obligations: []

definition audit: PASS
logic audit: PASS
boundary audit: PASS
adversarial audit: PASS WITHIN DECLARED SCOPES
independent audit before proposal: REQUIRED
proposal/canonical mutation in this task: NONE
```
