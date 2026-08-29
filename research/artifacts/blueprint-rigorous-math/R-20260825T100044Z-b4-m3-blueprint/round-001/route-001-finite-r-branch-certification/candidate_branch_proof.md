CANDIDATE_COMPLETE_PROOF

# Exact finite-R seed branch in the corrected closed M3 system

## Package identity and scope

- Local inference ID: `INF-R001-FINITE-R-BRANCH-V1`.
- Target node: `CLM-SL-B4-M3-TARGET-V1` (seed-branch part only; no observable or sector-determinant claim).
- Statement artifact: `branch_theorem_statement.txt`, SHA-256 `b717ff0832a4ee050668eb04dc51d0056d8853235ce47d9af38cbc16a31870f2`.
- Context: `R-20260825T100044Z-b4-m3-blueprint`, round `round-001`, route `route-001-finite-r-branch-certification`.
- Author/researcher: `finite-branch-researcher`.
- Formalization: off.
- Status: candidate proof pending independent review. This package proves the finite seed branch and does not claim that the run-level determinant/observable target is complete.

## Bound premises, definitions, and equation map

The proof uses the frozen problem data and the exact four residuals in
`scripts/_gapn2_largeR_closed.py`, SHA-256
`e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`.
No repository existence, numerical-fit, hard-odd-term, or cascade conclusion is
used as a premise. The other five bound-source hashes are recorded in
`computation_manifest.json`.

Let

\[
u=R^{-1/6}>0,\quad k_2=Ku,\quad k_3=Ku+Cu^5,
\quad p_1=\frac\pi2+Au^2,\quad p_3=\frac\pi4+Bu^2.
\]

Set

\[
p_{1t}=\frac{k_3}{k_2}p_1,\quad p_{3t}=\frac{k_3}{k_2}p_3,
\quad p_2=\frac{k_2}{2}-u^3(p_1+p_3),
\quad p_{2t}=\frac{k_3}{2}-u^3\frac{k_3}{k_2}(p_1+p_3).
\]

`E1` is the Dirichlet-at-the-center half-mode characteristic residual,
`E2` is the Neumann-at-the-center half-mode characteristic residual, and
`E5,E6` are the normalized band equalities at the first and second switches.
Reflection supplies the third and fourth switch equalities. The half widths are

\[
w_1=w_5=\frac{u^3p_1}{k_2}=\frac{u^2p_1}{K},\quad
w_2=w_4=\frac{p_2}{k_2}=\frac12-\frac{u^2(p_1+p_3)}K,
\quad w_3=\frac{2u^3p_3}{k_2}=\frac{2u^2p_3}{K}.
\]

These sum exactly to one.

## Ordered proof

### 1. Analyticity and the rank-one singular endpoint

In the chart `K != 0`, all apparent singularities at `u=0` are removable.
For example, `sin(p2)=u` times an analytic function and
`cos(p1)=u^2` times an analytic function, so the terms divided by `u^3`
in `E1,E2` are analytic. In each mass formula the boundary coefficient is
`u^2` times an analytic function, while `k*eps` is `u^4` times a nonzero
analytic function; the remaining mass terms have the same cancellation.
The phase denominators tend to

\[
\sin p_{1t}=1,\qquad \sin p_3=2^{-1/2},\qquad
\cos p_{3t}=2^{-1/2}.
\]

The exact leading residuals are

\[
E_{1,0}=-\frac{\sqrt2}{4}(AK-2),\quad
E_{2,0}= \frac{\sqrt2}{4}(AK-2),\quad
E_{6,3}=-(AK-2),
\]

and `E5_2` also has the factor `AK-2`. Their Jacobian on `AK=2`
has rank one, with null directions represented by
`(-K^2/2,1,0,0)`, `(0,0,1,0)`, and `(0,0,0,1)` in `(K,A,B,C)`.
Thus an ordinary endpoint IFT is invalid, but this is a method failure rather
than a refutation.

### 2. First exact blow-up

Introduce

\[
\Delta=\frac{AK-2}{u^2},\qquad A=\frac{2+u^2\Delta}{K}.
\]

The exact endpoint of
`(E1/u^2,E2/u^2,E5/u^4,E6/u^5)` is the four-expression map printed by
`finite_r_direct_check.py`. Its first two equations give

\[
C_0(K)=\frac{16}{\pi K},\qquad
\Delta_0(K)=-\frac{K^3-18\pi+24}{6K}.
\]

Direct substitution into the corrected exact mass expression makes both the
`E5/u^4` endpoint and the `E6/u^5` endpoint identically zero. The exact
coefficient `E5_5` is also zero. In particular, no odd correction is forced at
this level.

### 3. Second blow-up and exact seed

Write

\[
\Delta=\Delta_0(K)+u^2X,\qquad C=C_0(K)+u^2Y,
\]

and define the analytically extended residual map

\[
G(u,K,B,X,Y)=\left(\frac{E_1}{u^4},\frac{E_2}{u^4},
\frac{E_5}{u^6},\frac{E_6}{u^7}\right).
\]

The cancellations in Steps 1-2 prove divisibility by the displayed powers in
the analytic local ring. At `u=0`, solving the first two rows for `X,Y` gives

\[
Y=\frac{4K}{3\pi}-\frac{128}{\pi^2K^2}+\frac{48}{K^2},
\]

\[
X=\frac{-1440BK-K^6-120K^3+90\pi K^3-4320\pi+4800+1620\pi^2}
{360K^2}.
\]

After these substitutions, the two remaining rows reduce exactly to

\[
\frac{2(6\pi^2BK+\pi K^3-24\pi^2+48)}{3\pi K^6}=0,
\qquad \frac{8(BK-1)}{K^2}=0.
\]

Hence

\[
B_0=K_0^{-1},\qquad \pi K_0^3-18\pi^2+48=0.
\]

There is exactly one positive root,

\[
\kappa:=K_0=\left(18\pi-\frac{48}{\pi}\right)^{1/3}
=3.45576417140853820024\ldots,
\]

because the radicand is positive and the cubic is strictly increasing on the
positive axis. Thus

\[
B_0=\kappa^{-1},\quad C_0=\frac{16}{\pi\kappa},\quad
\Delta_0=\frac{8/\pi-4}{\kappa}.
\]

The corresponding auxiliary values are

\[
X_0=-\frac{\kappa^6-90\pi\kappa^3+120\kappa^3-1620\pi^2-3360+4320\pi}
{360\kappa^2},
\]

\[
Y_0=\frac{4(\pi\kappa^3-96+36\pi^2)}{3\pi^2\kappa^2}.
\]

### 4. Exact nondegeneracy and finite-u branch

For variables `(K,B,X,Y)`, the exact endpoint Jacobian determinant reduces at
the seed to

\[
\det D_{(K,B,X,Y)}G(0,z_0)
=\frac{\pi\kappa^3-36\pi^2+96}{\kappa^8}
=-\frac{6(3\pi^2-8)}{\kappa^8}<0.
\]

This is an exact certificate; `pi>3` already implies `3*pi^2-8>0`.
The real-analytic implicit-function theorem therefore gives `u0>0` and a
unique real-analytic branch `z(u)=(K,B,X,Y)` near `z0` for `|u|<u0`.

The map `G` is even in `u`: `p1,p3,p1t,p3t` are even, `p2,p2t,k2,k3,eps`
are odd, `E1,E2,E5` are even, and `E6` is odd; division by
`u^4,u^4,u^6,u^7` leaves four even components. Local uniqueness implies
`z(u)=z(-u)`. Hence there are constants `M,u0>0` such that

\[
\lVert z(u)-z_0\rVert\le M u^2\qquad (|u|<u_0).
\]

Consequently

\[
K=\kappa+O(u^2),\quad B=\kappa^{-1}+O(u^2),\quad
C=\frac{16}{\pi\kappa}+O(u^2),\quad A=\frac2\kappa+O(u^2),
\]

with actual absolute remainder bounds by constants times `u^2`. In original
variables,

\[
k_2=\kappa u+O(u^3),\quad
k_3-k_2=\frac{16}{\pi\kappa}u^5+O(u^7),
\]

\[
p_1=\frac\pi2+\frac2\kappa u^2+O(u^4),\qquad
p_3=\frac\pi4+\frac1\kappa u^2+O(u^4).
\]

Thus `K1=C1=0`; the source addendum's odd-forcing claim is false for the
hash-bound exact residual. Setting `R=u^-6` supplies one exact solution for
every `R>u0^-6`, not merely a formal series.

For `u>0`, the coordinate map from `(K,B,X,Y)` to `(k2,k3,p1,p3)` is
invertible: its determinant is a nonzero multiple of `u^16/K`. Row rescaling
from `E` to `G` is also invertible. Therefore the exact finite-u residual
Jacobian in `(k2,k3,p1,p3)` is nonzero on the branch after decreasing `u0`.

### 5. Positive widths, eigenvalue indexing, and INF band signs

For small positive `u`, `K,C,A,B` are positive and

\[
p_1,p_{1t}\in(\pi/2,\pi),\quad p_3,p_{3t}\in(0,\pi/2),
\quad p_2,p_{2t}\in(0,\pi/2).
\]

The exact width formulas above are therefore positive, symmetric, and have
the INF placement: the outer and central blocks carry `R`, the two intervening
blocks carry `1`.

On the left low block, each half-mode has the form
`q(t)=a cos(t)+b sin(t)`, `0<=t<=p2` (or `p2t`), with `a>0`, `b<0`.
The exact endpoint expansions, reduced modulo the seed cubic, are

\[
q_D(p_2)=\frac{2}{\kappa^2}u^4+O(u^6)>0,\qquad
q_N(p_{2t})=-\frac{2}{\kappa^2}u^4+O(u^6)<0.
\]

Since `q'(t)=-a sin(t)+b cos(t)<0` on these small phase intervals, the
Dirichlet-at-center half-mode has no low-block zero and the Neumann-at-center
half-mode has exactly one. The outer and central high blocks have no
additional zeros by their displayed phase ranges. Odd reflection of the
Dirichlet half-mode gives exactly one global interior zero (the center), while
even reflection of the Neumann half-mode gives two. The Sturm nodal theorem
therefore identifies them as `lambda_2` and `lambda_3` respectively.

`E5=E6=0` and reflection give all four switch equalities `f(x_j)=0`.
To determine the signs without assuming band consistency, normalize the two
modes in `L2_rho` and replay the bound structural calculation: the block
energy difference

\[
H=(u_2'^2+\lambda_2\rho u_2^2)
 -(u_3'^2+\lambda_3\rho u_3^2)
\]

is constant across switches because `f(x_j)=0`, and integration gives
`H=-2(lambda_3-lambda_2)<0`. This yields endpoint slope ratios of magnitude
greater than one and hence `f<0` near both endpoints. The Wronskian is strictly
negative by the standard nodal-cell argument, so `u_3/u_2` is strictly
decreasing in each `u_2` nodal cell. It follows that `f` has exactly four
simple zeros. Since the four switches are already zeros, the signs alternate
as `(-,+,-,+,-)`. This is precisely the INF pattern for the `R,1,R,1,R`
blocks. No numerical branch data enter this argument.

## Boundary and adversarial audit

- `K -> 0`: excluded by the exact positive seed and a neighborhood with
  `K>=kappa/2`; no denominator was cleared at `K=0`.
- Singular `u=0` versus finite `R`: discharged by the analytic extension of
  `G` and the IFT for every `0<u<u0`.
- Odd correction: direct exact replay gives `E5_5=0`; evenness forces
  `K1=C1=0`.
- Denominators: `k2,k3>0` for `u>0`, and the three phase denominators remain
  separated from zero by their endpoint values.
- Realness and widths: the IFT is over the real variables and all five widths
  are positive for sufficiently small positive `u`.
- Symmetry and band consistency: built into the half-domain reflection and
  proved by the nodal/sign audit in Step 5.
- Spurious truncated roots and branch switching: the theorem uses the exact
  residual, and endpoint nondegeneracy gives local uniqueness in the complete
  blow-up chart. It does not assert global uniqueness outside that chart.
- Singular ordinary seed Jacobian: explicitly detected (rank one) and replaced
  by the exact nonzero third-blow-up Jacobian.

## External theorem contracts

1. Real-analytic implicit-function theorem: an analytic map with invertible
   variable Jacobian has a unique local analytic solution branch. Applied to
   the explicitly extended map `G` and the exact determinant above.
2. Sturm nodal theorem for a positive piecewise-constant Dirichlet string: the
   eigenfunction with `j-1` interior zeros is the `j`th eigenfunction. Applied
   only after the explicit zero count in Step 5.

Both are standard mathematical infrastructure; no open repository claim is
imported through them.

## Computation certificate and limitations

Exact symbolic replay is implemented in `finite_r_direct_check.py`, SHA-256
`d38ba50947a95a8c47bd3faa03f2ddfc0b742408b21ece638fbdf8cab500eac2`.
Its validity predicate is:

1. the closed source hash equals the frozen hash;
2. all four first-blow-up endpoint expressions equal the displayed formulas;
3. `E5_5` is exactly zero;
4. the reduced third-blow-up equations equal the two displayed scalar rows;
5. the seed polynomial and `BK-1` vanish;
6. the Jacobian numerator reduces modulo the seed polynomial to
   `-6*(3*pi^2-8)`; and
7. the two half-mode endpoint coefficients reduce to `+2/K^2` and `-2/K^2`.

Arithmetic is exact SymPy expression arithmetic. The 100-decimal residual
sequence in the script is only an adversarial transcription check and is not
used in the proof. `finite_r_replay.py` reproduces the invalid bound series
builder and is evidence for the separately recorded source audit, not a proof
dependency.

## Obligation map

- Exact finite nonzero seed: discharged in Step 3.
- Certified nondegeneracy: discharged in Step 4.
- Exact finite-R correspondence and remainder: discharged in Step 4 by the
  analytic IFT and the even `O(u^2)` bound. The constants are existential and
  not numerically optimized.
- Positive widths, realness, symmetry, eigenvalue indices, and INF signs:
  discharged in Step 5.
- Source hard-odd assertion: refuted for the exact closed formula by the audit
  artifact.
- Run-level observables and sector determinants: outside this route and still
  open; they are not unresolved premises of this branch theorem.

`unresolved_obligations: []` for `INF-R001-FINITE-R-BRANCH-V1`.

## Provenance and calibrated confidence

- Human contribution: frozen problem and route contracts only.
- Model contribution: blow-up selection, exact derivation, proof, and audits.
- Tool contribution: hash checks and deterministic exact symbolic replay.
- Numerical evidence: used only for falsification/transcription checking.
- Novelty: `unknown`; no novelty claim is made.
- Confidence: semantic fidelity high; correctness high but pending independent
  review; completeness high for the route theorem; novelty unknown;
  reproducibility high.
