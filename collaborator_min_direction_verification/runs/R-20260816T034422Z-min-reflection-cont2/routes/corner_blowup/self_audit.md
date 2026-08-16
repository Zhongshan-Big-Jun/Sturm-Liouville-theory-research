AUDIT_PASS_WITH_SCOPE_LIMITATION

# Boundary and logic audit of MIN-REFL-C2-C

## Audit verdict

The two new blow-up arguments are internally valid and close the stated
triple-corner uniformity gap **conditional on the frozen R14/R17 reduction**.
Together with the boundary pieces explicitly inherited from the frozen
`t0_asymptotic` report, they prove existence of some unknown `t_*>0` on
which all four R17 coefficient gaps are positive.  They do not certify the
dyadic slab `t<=1/64`, do not close the other collar intersections, and do
not cross the non-canonical physical bridge.

## 1. Definition audit: PASS

- `k,t,y` are the exact R17 common-angle base coordinates and
  `z=pi*t/2`.
- `epsilon=1-kb` is an exact reparametrization of the upper negative-phase
  distance; `1-k^2b^2=epsilon(2-epsilon)`.
- The compactifier `u=1/rB` is local notation in this route and is not the
  lower-case endpoint variable called `u` in the older R14 derivation.
  Only the centered R17 variables `U_i` occur beside it.
- The fourth physical coordinate is the contrast `r`.  The Bernstein fiber
  coordinate `xi=(r-1)/(rB-1)` is distinct from both `u` and `z`.
- `rho_i=Pplus*Nhat_i/(g*Knew*cp^4)` is nonnegative on the retained subset,
  and `G_i>0` is exactly `rho_i<1`; no normalization factor changes sign.

## 2. Algebra audit: PASS

The exact replay independently checks:

1. the factorization of `g` after `b=(1-epsilon)/k`;
2. all four `u^2 Nhat_i` identities;
3. the low-chart common ratio factor and the high-chart `d^4v` factor;
4. all eight limiting ratio polynomials;
5. both implicit negative-phase boundary equations and their nonzero
   derivatives;
6. the full rational `W_0,W_1` endpoint scalings and the high-chart
   `g,ebar` limits.

The replay is exact SymPy algebra over `QQ(pi)`.  No floating sign, sampling,
or adaptive subdivision is used.

## 3. Positivity-bound audit: PASS

After multiplying by `u^2`, every coefficient multiplying an endpoint
product in `Nhat_i` is nonnegative for `0<=u<=1`.  Bounding each endpoint
product by `(U_0+U_1)(L_0+L_1)` gives loose coefficient sums
`1/2,5/6,1,1`, all at most one.  Thus the common bound `rho_i<=T` is valid
simultaneously for all four indices.  Positivity of `U_i,L_i` is used only
as a frozen R14 conditional input and is not asserted canonically.

## 4. Compactness and approach-rate audit: PASS

### Low corner

The exact implicit equation has boundary value `sigma=pi` and derivative
one.  Hence `sigma` is analytic near `(k,epsilon)=(0,0)`.  In the chart
`x=z/(k epsilon)`, the exact physical compactifier satisfies
`u/x -> 1/(2pi)`.  Therefore a retained sequence (`u<1`) cannot have
`x->infinity`.  The zero-ratio face is included by the `u^2`
regularization.  The common error is `k^2 epsilon` times a bounded
continuous function.

### High corner

With `d=1-k`, `v=epsilon/d`, `tau=d sigma`, the exact implicit equation has
boundary solution `tau=4/pi` and derivative `-pi^2/8`.  The retained
condition `b>a`, together with `1-a=O(dz^2)`, forces `limsup v<=1`; hence
all retained sequences lie in a fixed compact `v` interval.  In the chart
`x=z/(d epsilon)`, `u/x -> 4/pi`, so the infinite-ratio regime is again
physically empty.  The common error is `d^4v` times a bounded continuous
function, including `v=0,1` and `u=0,1`.

No pointwise remainder is promoted to a uniform one without these compact
extensions.

## 5. Boundary audit: PASS WITH EXPLICIT LIMITATION

- The five old finite face certificates require the other two base
  coordinates to remain in `I=[1/64,63/64]`; they cover no genuine face
  intersection.
- The two new charts cover only the triple corners
  `(k,t,y)=(0,0,1)` and `(1,0,1)` in physical coordinates.
- The full small-`t` conclusion additionally depends on the other analytic
  `t=0` strata frozen in `t0_asymptotic/report.md`.
- The resulting width `t_*` is existential and may be smaller than `1/64`.
- Outside that unknown small-`t` collar, eight non-`t=0` cube edges, the
  four `t=1` vertices, and their surrounding multi-face boxes remain
  uncertified.  `cover_audit.md` gives the exhaustive list.
- At `rB=1` the strict contrast fiber is empty.  At `u=0` (`rB=infinity`)
  the normalized coefficient ratios have finite limits.  Once the four
  Bernstein coefficients are signed at a covered base point, the entire
  compactified contrast fiber `0<=xi<=1` is covered.

## 6. Logical propagation audit: PASS WITH SCOPE LIMITATION

The proved implication is only

```text
frozen R14/R17 definitions and conditional signs
  + frozen non-triple t=0 boundary analysis
  + the two new exact blow-up charts
  => exists unknown t_*>0 with all four conditional R17 gaps positive.
```

The proof does not establish that every premise-complete physical interface
is represented by the frozen reduction, does not promote R14/R17 to trusted
canonical premises, and does not imply canonical determinant orientation or
global reflection symmetry.  The precise restart is an independent,
hash-bound proof of the complete physical/common-angle-to-continuant bridge.

## 7. Reproducibility audit: PASS

The replay command exits zero and its parsed JSON output exactly matches the
frozen `exact_replay_output.json`.  Artifact hashes are recorded in
`artifact_manifest.json`; the manifest deliberately does not self-hash.
