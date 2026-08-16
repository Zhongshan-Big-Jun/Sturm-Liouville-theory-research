RIGOROUS_PARTIAL_RESULT

# MIN-REFL-A: order-theoretic reflection criterion and the exact symplectic/action obstruction

## 0. Route status

```text
route_id: MIN-REFL-A
target: every finite-R minimum-law exact-2n-switch self-consistent point is reflection fixed
method_family: reflection involution, terminal energy/action, endpoint norming data, cross-Wronskian comparison
current_status: blocked after a rigorous weaker criterion and exact no-go
proved_results:
  - order-preserving reflection on the equal-norm root set forces pointwise reflection symmetry
  - an equivalent pairwise physical bridge and a second one-sided endpoint-defect bridge
  - exact endpoint jump/Pohozaev identities exposing the missing antisymmetric scalar
  - exact insufficiency of the accepted pointwise symplectic/action identities for the bridge
first_failing_step:
  - no accepted identity compares right endpoint norming data between two distinct equal-norm roots
precise_gap:
  - prove the pairwise inequality (2.4), or one fixed sign for the endpoint defect (3.8), on the complete equal-norm minimum root set
gap_strength: strictly weaker than fixed-mu common-terminal uniqueness; it allows multiple reflection-fixed roots
```

No canonical Blueprint file, proposal, review, or receipt is modified by this report.

## 1. Snapshot and trusted inputs

All retrievals were bound to

```text
context: CTX-DEFAULT
blueprint: sha256:76346e2fa9f880fd8c1c02bf4b001b38cb66f2f4688c8497c9d764ebb746c7a7
inventory: sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

The deterministic `math-closure` query confirms that the following claims are proof-input eligible. The claims used below retain their exact semantic hashes:

```text
CLM-NGE2-MPO3A-STRUCTURE
  semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-SYMPLECTIC-NESTED
  semantic-sha256:4c11a291f871bf44dab3d4970f8b6457bbacafcac6842ae950bd9729be4d2c0e
CLM-NGE2-MPO3A-PARAMETER-ACTION-R1
  semantic-sha256:e7b57c2609991baea373a087ffc72da945e4a8b018d4bf33559908d09167ab06
CLM-NGE2-MPO3A-PROPERNESS
  semantic-sha256:b429060dd6662757e95cc783dcb737040dad2920cb3ac9ebc4ed15b13fe43695
CLM-NGE2-MPO3A-SMALL-CONTRAST
  semantic-sha256:975ece9f6048cbe3c8bde1a68e273c92f23b6f4e6f706523ac42483814793f2d
DEF-NGE2-MPO3A-SELFCONSISTENCY
  semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
```

The five proof packages specifically used for the derivations below were read and their bytes independently rehashed. The hashes agree with their canonical inference bindings:

```text
symplectic_nested_reduction/derivation.md
  sha256:b6dc98980a00b8b500e6569ffacdd6f273e50ac0170fd710e9a96a0ad931b878
parameter_variation_fold/derivation_r1.md
  sha256:f151a5e61c782449ebfc6e06b70dff55fede00f810023897a94568f4b7646046
full_relay/derivation.md
  sha256:0e6f919fa94e5f2a3c1c90ee825916346289d0c2c0f5250315a1a7e17da6679f
phase_rigidity/derivation.md
  sha256:62e24a1ab1828cb7aea575d3b3d9f92f57a88702605b087a02eabce021022aba
continuation_compactness/compactness_and_continuation.md
  sha256:0741d7e385a123756bd3886e000c455b84c37fde4e714a88bb627aee1c7e3b74
```

No open or candidate claim is used as a premise.

## 2. A weaker reflection theorem: order on only the equal-norm roots

Fix finite `R>1`, `n>=2`, and `mu>1`. Let `X=X(R,n,mu)` be the set of `q>1` labels of all premise-complete minimum-law common-terminal roots which also satisfy the equal-norm equation. Roots are understood as physical relay trajectories, with duplicate chamber descriptions identified. The accepted full-relay theorem makes `q` a faithful label at fixed `(R,n,mu)`: the indexed zero times determine `L`, and the relay IVP then determines the trajectory.

For a root `q in X`, write

```text
p=U_t(L),       r=V_t(L).
```

The accepted reflection formula defines

```text
h(q)=q_sharp=abs(r)/abs(p)>1,                         (2.1)
```

and reflection preserves `(R,n,mu)`, the common terminal conditions, the event count, the minimum law, and equal norms. Hence `h:X->X`. Reflection twice is the original positively reoriented trajectory, so

```text
h(h(q))=q.                                            (2.2)
```

### Lemma 2.1 (order-preserving involution criterion)

If `h` is nondecreasing on the totally ordered set `X`, then `h=id_X`. Consequently every root in `X` is reflection invariant.

#### Proof

Suppose `q<h(q)`. Monotonicity and (2.2) give

```text
h(q)<=h(h(q))=q,
```

a contradiction. If `h(q)<q`, applying the preceding argument to `h(q)` gives the same contradiction. Thus `h(q)=q` for every `q in X`. The accepted symplectic reflection diagnostic then gives

```text
q_sharp=q  iff  p^2=1  iff  r^2=q^2,                 (2.3)
```

and cellwise relay uniqueness makes the trajectory, hence the weight, reflection invariant. QED.

This criterion is strictly weaker in scope than fixed-`mu` common-terminal uniqueness. It quantifies only roots satisfying equal norm, and it permits any number of reflection-fixed roots.

The accepted terminal energy/reflection identity gives

```text
h(q)^2-1=(q^2-1)/p(q)^2.
```

Therefore the exact physical bridge requested by Lemma 2.1 is

```text
q_1<q_2 in X
  => (q_1^2-1)/p(q_1)^2 <= (q_2^2-1)/p(q_2)^2.        (2.4)
```

No derivative, regular chart, or connectedness of `X` is required. In particular, (2.4) remains meaningful at a singular `q`-Jacobi point and across distinct relay chambers.

## 3. The exact antisymmetric endpoint defect

Let the `2n` relay events be

```text
0<t_1<...<t_(2n)<L,
```

and put `U_j=U(t_j)`. The individual `U` oscillator energy

```text
E_U=U_t^2+rho U^2
```

is constant inside each cell and jumps by

```text
E_U(t_j+)-E_U(t_j-)=Delta rho_j U_j^2.               (3.1)
```

For the minimum word the endpoint cells have material `R` and

```text
Delta rho_j=(R-1)(-1)^j.                             (3.2)
```

Since `U_t(0)=1` and `U(L)=0`, summing (3.1) gives the exact endpoint defect

```text
D:=p^2-1
  =(R-1) sum_(j=1)^(2n) (-1)^j U_j^2.                (3.3)
```

At each event, `S=U^2-mu^2 V^2=0`. The corresponding `V` energy jump is therefore

```text
mu^2 Delta rho_j V_j^2=Delta rho_j U_j^2,
```

and hence

```text
r^2-q^2=D.                                           (3.4)
```

For the reflected, positively reoriented trajectory, the terminal `U` slope has squared magnitude `1/p^2`. Thus

```text
D_sharp=p_sharp^2-1=-D/p^2.                          (3.5)
```

Equations (2.3), (3.3), and (3.5) show exactly what a direct invariant proof must control:

```text
reflection fixed  iff  D=0.                          (3.6)
```

For the mandatory smallest case `n=2`, with no restriction on `mu>1`, this is already the nontrivial four-event balance

```text
D=(R-1)(-U_1^2+U_2^2-U_3^2+U_4^2).                  (3.7)
```

Equal norms do not cancel the four terms pairwise unless reflection symmetry has already been established.

There is a second strictly weaker completion criterion:

```text
D>=0 for every q in X, or D<=0 for every q in X.     (3.8)
```

Indeed the reflected root is also in `X`, while (3.5) reverses the sign unless `D=0`. Either universal one-sided inequality in (3.8) forces `D=0` pointwise. This again allows multiple symmetric roots and is weaker than uniqueness.

## 4. Why equal norm and the accepted action identities do not determine `D`

Put

```text
I_U=integral_0^L rho U^2 dt,
I_V=integral_0^L rho V^2 dt.
```

At a complete root `I_U=I_V=I`. Integration of the global relay energy gives

```text
L(q^2-1)=2(mu^2-1)I.                                 (4.1)
```

This determines the initial energy defect from the mean norm `I/L`, but contains no terminal defect `D`.

The missing rank can be seen without any heuristic. Multiply the `U` equation by `t U_t` and integrate cellwise, retaining all interface terms. This gives

```text
L p^2=2I+sum_j t_j Delta rho_j U_j^2.                (4.2)
```

Doing the same for `V`, and using `mu^2 V_j^2=U_j^2` at every event, gives

```text
L r^2=2mu^2 I+sum_j t_j Delta rho_j U_j^2.           (4.3)
```

Subtracting (4.2) from (4.3) is exactly (4.1) together with the terminal energy relation. It supplies no second equation for the zeroth jump moment (3.3). Multiplication by `(L-t)U_t` merely reproduces the identity `D=p^2-1`. Thus all linear virial/Pohozaev combinations of the two modes collapse at the switching relation rather than forcing the alternating amplitude sum to vanish.

The accepted parameter-action package gives, along a differentiable common-terminal sheet,

```text
((1-q^2)/2)dL=mu I_V dmu.                            (4.4)
```

At fixed `mu`, (4.4) says only `dL=0` for a sheet tangent. It neither compares two disconnected roots nor relates their terminal norming factors `p`. Reflection preserves `mu`, `L`, and the integral ratio, so the equal-norm/action scalar is constant on a two-point reflection orbit by construction.

### Exact separation model for the pointwise identities

The failure is logical, not merely an unsuccessful manipulation. Fix arbitrary `mu>1`, `L>0`, and numbers

```text
1<q_-<q_+,
c=(q_-^2-1)/(q_+^2-1) in (0,1).                     (4.5)
```

Assign squared terminal data

```text
p_-^2=c,          r_-^2=c q_+^2,
p_+^2=1/c,        r_+^2=q_-^2/c,                    (4.6)
I_-=L(q_-^2-1)/[2(mu^2-1)],
I_+=L(q_+^2-1)/[2(mu^2-1)]=I_-/c.                   (4.7)
```

Then every displayed pointwise scalar consequence of terminal energy, equal norm, action, and reflection is satisfied:

```text
p_minus^2-r_minus^2=1-q_minus^2,
p_plus^2-r_plus^2=1-q_plus^2,
abs(r_-)/abs(p_-)=q_+,
abs(r_+)/abs(p_+)=q_-,
p_+^2=1/p_-^2,
I_+=I_-/p_-^2.                                      (4.8)
```

Thus the pointwise identity system admits an order-reversing two-cycle. The `q`-Jacobi endpoint pairing does not remove it: at a singular point its two terminal position components vanish, while at a regular point their pairing constrains only their ratio at that one trajectory. Neither case compares (4.6) between the two roots.

The data (4.5)--(4.8) are deliberately **not** claimed to be a relay trajectory, so they are not a counterexample to the target. They prove the narrower no-go statement needed here: the accepted pointwise symplectic/action consequences alone cannot entail (2.4) or (3.8). A new cross-trajectory or interface-order input is necessary.

## 5. Cross-trajectory comparison and its first exact failure

One natural attempt is to compare a root directly with its reflection. Let `(U,V,rho)` and `(U_sharp,V_sharp,rho_sharp)` be the reflected pair on the common interval `[0,L]`. Lagrange's identity gives

```text
integral_0^L (rho-rho_sharp) U U_sharp dt=0,
integral_0^L (rho-rho_sharp) V V_sharp dt=0.          (5.1)
```

For a reflected pair, however,

```text
rho-rho_sharp is antisymmetric about L/2,
U(t)U_sharp(t) and V(t)V_sharp(t) are symmetric
up to fixed nonzero orientation factors.
```

Hence both equalities in (5.1) are parity tautologies for every coefficient, symmetric or not. They contain no rigidity information.

For two unrelated roots on a common interval, the minimum relay law does give the pointwise antitonicity

```text
(rho_1-rho_2)(S_1-S_2)<=0.                           (5.2)
```

But the Lagrange identity controls the indefinite polarization

```text
C_12=U_1U_2-mu^2 V_1V_2,                            (5.3)
```

not `S_1-S_2`. There is no pointwise sign implication between them. Already the two Minkowski vectors `(U_1,mu V_1)=(2,1)` and `(U_2,mu V_2)=(1,2)` have `S_1=3`, `S_2=-3`, but `C_12=0`. Small perturbations give either sign of `C_12` while retaining opposite signs of `S_1,S_2`. Therefore (5.2) cannot sign the integrand in the cross-Wronskian identity.

This is the first exact obstruction to deriving (2.4) from the minimum relay law plus symplectic/Lagrange identities. If two roots have different terminal lengths, rescaling to the unit interval additionally introduces their distinct spectral scales and does not repair the missing sign.

## 6. Required boundary cases

### 6.1 `n=2`, arbitrary `mu`

Equation (3.7) is valid for every `mu>1`; no `mu=2`, multiple-angle, or symmetric ansatz is used. The two mode Pohozaev equations share the same first interface moment and therefore do not cancel the alternating zeroth moment. A proof for `n=2` must add a genuinely new inequality controlling the four physical event amplitudes, or prove the pairwise order bridge (2.4).

### 6.2 Asymmetric reflected pair

Such a pair necessarily has one endpoint defect negative and the other positive:

```text
D<0  <=> D_sharp>0,
```

by (3.5). Equations (4.5)--(4.8) show that this sign pattern is fully compatible with all accepted pointwise scalar identities. The order criterion detects the pair exactly: it is a two-cycle of `h`, hence reverses the order of its two elements.

### 6.3 Singular `q`-Jacobi point

The accepted symplectic theorem says

```text
partial_q A_n=0
iff the q-Jacobi field has both terminal position components zero.
```

It gives no equation for `D`. Lemma 2.1 and bridge (2.4) remain valid because they use only the root set and reflection, not differentiation. Conversely, a proof obtained by integrating a local `q` derivative cannot cross such a point without an independent singular-root argument. Properness excludes switch collision and endpoint escape, but does not exclude an interior residual singularity.

### 6.4 Relay chamber closures

Every complete target root has exactly `2n` simple events by the trusted structural/full-relay claims, so it has a local premise-complete chamber. Overlapping closure descriptions are identified at the trajectory level before defining `X`. Reflection may exchange chambers, but still induces the well-defined involution `h` on `X`. The missing inequality (2.4) must compare roots across all chambers and disconnected components; chamberwise action identities do not do so.

### 6.5 `R downarrow 1`

At the degenerate anchor `R=1`, the constant-coefficient relay equations give

```text
U(t)=sin(t),
V(t)=(q/mu)sin(mu t),
L=n pi,
mu=(n+1)/n,
I_U=I_V  iff q=mu,
p=(-1)^n,
r=(-1)^(n+1)q.                                      (6.1)
```

Thus the equal-norm root set is a singleton and `h=id`, while `A_n` is independent of `q` and hence `partial_q A_n=0`. This exact boundary calculation shows both that the order criterion survives a `q`-Jacobi singular anchor and that an `A_q`-sign proof cannot simply include `R=1`. The trusted small-contrast theorem establishes reflection symmetry for `1<R<1+epsilon_n`; it does not prevent a later interior symmetry-breaking singularity at finite contrast.

## 7. Precise blocked obligation and restart conditions

The direct route does not prove or refute the frozen target. It reduces the target to either of the following genuinely weaker, non-unique alternatives:

```text
ORDER BRIDGE:
For fixed (R,n,mu), every q_1<q_2 in the complete equal-norm minimum
root set satisfies
  (q_1^2-1)/p(q_1)^2 <= (q_2^2-1)/p(q_2)^2.

ONE-SIDED DEFECT BRIDGE:
For fixed (R,n,mu), D=p^2-1 has one weak sign on every complete
equal-norm minimum root.
```

Either bridge forces every root to be reflection fixed, but neither asserts root uniqueness. The route can be restarted only with a new input of one of these types:

1. a cross-root comparison theorem for left versus right endpoint norming constants on the equal-norm relay set;
2. a noncircular sign theorem for the physical alternating event-amplitude sum (3.3), possibly using the full event continuant rather than energy/action alone;
3. a singularity-compatible order theorem that proves (2.4) directly on the set of roots, including disconnected chambers;
4. an exact premise-complete asymmetric relay root, which would refute the target and realize the two-cycle pattern abstracted in (4.5)--(4.8).

Rearranging the accepted symplectic pairing, the zero-action one-form, or the two Pohozaev identities is not a restart condition: Sections 4--5 prove that those data have no cross-root sign and leave `D` free.

## 8. Epistemic calibration

```text
order-preserving-involution lemma: PROVED
pairwise bridge equivalence: PROVED
endpoint defect/reflection covariance: PROVED
pointwise identity insufficiency: PROVED as an algebraic separation/no-go
cross-Wronskian reflected-pair route: AUDITED FAILURE (parity tautology)
minimum global reflection target: OPEN
formalization_status: not_requested
novelty_status: unknown
```

Confidence:

```text
semantic fidelity: high
mathematical correctness of the displayed lemmas: high
completeness for the frozen target: low (the target remains open)
reproducibility: high (deterministic snapshot and proof-package hashes recorded)
```
