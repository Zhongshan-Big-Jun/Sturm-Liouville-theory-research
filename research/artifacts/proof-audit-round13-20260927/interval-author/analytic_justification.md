# R13-03 / R13-04 interval author justification

Status: CANDIDATE_COMPLETE_PROOF for the primitive enclosure contract below.
This is a code author's mathematical justification and selfcheck package. It is
not independent review, a Lean proof, or certification of the complete E1 chain.

## Contract and provenance

The edited file is `/mnt/f/LaTeX/BVE research/misc/rigid1d.py`. Before editing,
HEAD was `4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`, and the actual file bytes
equalled that commit's full blob. Its SHA256 was
`acf9408319ab6e27e1be64e4c772eae96f1ab432a09a0660fed54d7de100df96`.
The actual pre-edit source is preserved as `rigid1d.before.py`.
The audit REPORT and analytic_notes were read as claims to check, not as approval.
Their hashes and the current E1 source hash at intake are in `input_manifest.json`.

For every finite rational interval X=[a,b], a<=b, the public `I_sin`, `I_cos`,
and `I_atan` return finite rational intervals containing, respectively,
{sin(x):x in X}, {cos(x):x in X}, and {atan(x):x in X}.
`NS=12` is a fixed implementation constant. The point Taylor proof below works
for any fixed positive integer NS; mutating module constants is not an API.
Float inputs accepted by `Fraction` mean their exact binary rational value,
not an intended decimal value. No floating-point arithmetic is used to form
the certified endpoints. Infinity and NaN cannot be `Fraction` endpoints.

`I` retains its existing endpoint-order normalization. The theorem concerns
the resulting ordered interval. `I_sin`, `I_cos`, and `I_atan` take `I` objects;
the D and D2 wrappers take their corresponding dual objects.

The proof obligations are: point Taylor remainder; the entire offset range;
interval addition identities; Machin's pi enclosure; terminating monotone
atan evaluation; derivative propagation under explicit domain assumptions;
and checks that cannot disappear under `python -O`.

## 1. Point sin/cos Taylor enclosures on the whole real line

For N=NS>=1 define

    S_N(c) = sum_{k=0}^{N-1} (-1)^k c^(2k+1)/(2k+1)!,
    C_N(c) = sum_{k=0}^{N-1} (-1)^k c^(2k)/(2k)!.

Every derivative of sine and cosine has absolute value at most 1 on R.
Regard S_N as the Taylor polynomial of degree 2N: its last, even coefficient
is zero. Regard C_N as the polynomial of degree 2N-1: its last, odd
coefficient is zero. Taylor's theorem with Lagrange remainder therefore gives

    |sin(c)-S_N(c)| <= |c|^(2N+1)/(2N+1)!,
    |cos(c)-C_N(c)| <= |c|^(2N)/(2N)!

for every real c, including large and negative c. These are exactly the
remainders used by `_sc_series`. Decreasing alternating terms are not a
hypothesis. The midpoint c is evaluated by a Taylor expansion about zero;
the word "center" in the API does not change the expansion point.

All polynomial and remainder calculations for rational c are exact Fraction
operations. Finite, arbitrarily large c is supported mathematically, although
the interval can become very wide and arbitrary-size integer arithmetic has
no uniform resource bound. This is an enclosure claim, not a global accuracy claim.

## 2. Full offset range, including internal extrema

Write X=[c-w,c+w], where c=(a+b)/2 and w=(b-a)/2>=0.

If 0<=w<=1, Taylor's theorem at degree one gives

    cos(t) >= 1-t^2/2 >= 1/2 > 0,   0<=t<=1.

Consequently sin is increasing on [0,1], starts at zero, and is nonnegative
there. Since cos'=-sin, cos is nonincreasing there. Oddness and evenness give
the exact range identities

    sin([-w,w]) = [-sin(w), sin(w)],
    cos([-w,w]) = [cos(w), 1].

Let [Ls,Us], [Lc,Uc] be the point enclosures at w from section 1. Then

    [-min(1,Us), min(1,Us)] and [max(-1,Lc), 1]

enclose these entire ranges. Us>=sin(w)>=0, so the sine endpoints are
ordered. The second upper endpoint must be 1, even when the point interval
around cos(w) excludes 1. At w=0 these enclosures are exactly [0,0], [1,1].

For w>1, `_sc_u` returns [-1,1] for each function. This bound is valid
regardless of the number or location of critical points. Public sine and
cosine return this same safe interval immediately when w>1. A negative
offset radius is explicitly rejected. Thus the cut at 1 is a proved
monotonicity domain, not an assumption about arbitrary inputs.

For w<=1, the addition identities

    sin(c+u) = sin(c)cos(u) + cos(c)sin(u),
    cos(c+u) = cos(c)cos(u) - sin(c)sin(u)

hold for every u in [-w,w]. Exact interval multiplication and addition
include every such product/sum, even when the factors are correlated.
Correlation loss only enlarges the interval. Intersecting the final interval
with [-1,1] remains sound, since the true value belongs to both. This
intersection cannot be empty under the proved contract, so `I`'s endpoint
normalization does not conceal an empty intersection in this argument.

This proof covers intervals containing 0, +/-pi/2, +/-pi, arbitrary
translates, and multiple periods. It does not depend on detecting critical
points numerically. Wide inputs deliberately sacrifice useful accuracy;
the small-offset formula keeps the second-order cosine radius needed for
the narrow E1 cells.

## 3. Certified pi and the atan series

For integer N>=1 and 0<=v<=1, the finite geometric identity is

    1/(1+t^2) = sum_{k=0}^{N-1} (-1)^k t^(2k)
                 + (-1)^N t^(2N)/(1+t^2).

Integrating from 0 to v proves

    atan(v) = sum_{k=0}^{N-1} (-1)^k v^(2k+1)/(2k+1) + R,
    |R| <= v^(2N+1)/(2N+1).

It also gives the sign of the remainder used by the test oracle. The
production helper uses the symmetric enclosure. This proof includes v=0
and v=1 without any limiting or strict-decrease issue. Inputs outside [0,1],
noninteger N, and N<1 are explicitly rejected.

For completeness, put a=atan(1/5), b=atan(1/239). The tangent addition
formulas give tan(2a)=5/12, tan(4a)=120/119, and tan(4a-b)=1.
The integral bounds a>=1/5-(1/5)^3/3=74/375, b<=1/239 show 4a-b>0.
Also 4a-b<4/5<1<pi/2; the last strict inequality follows, for example,
from atan(1)=integral_0^1 1/(1+t^2) dt>1/2. Hence 4a-b=pi/4, proving

    pi = 16 atan(1/5) - 4 atan(1/239).

The interval for pi uses the corresponding lower and upper endpoints in
the correct direction. Its sanity test is an explicit `ArithmeticError`
guard; neither that test nor the historical comparison constants constitute
the proof of the enclosure.

## 4. Terminating atan endpoint enclosures

Let P=[Plo,Phi] contain pi. `_atan_point(v)` handles a rational point as follows.

1. v<0: use atan(v)=-atan(-v) and reverse/negate the endpoints.
2. v=1: use P/4.
3. v>1: use pi/2-atan(1/v). The recursive argument is strictly in (0,1).
4. 1/2<v<1: put t=(1-v)/(1+v), so 0<t<1/3. The identity
   atan(v)=pi/4-atan(t) follows from the tangent addition formula with both
   angles in (0,pi/2). Use the pi interval and the series envelope at t.
5. 0<=v<=1/2: use the series directly.

In case 4, tan(atan(v)+atan(t))=(v+t)/(1-vt)=1; the sum is in (0,pi/2),
which fixes the branch. In case 3 the usual complementary identity holds
on v>0. All denominators are strictly positive on the branches where they
are used. At most one oddness and one reciprocal step occur. No interval is
reciprocated recursively, and no cycle can return to an interval crossing 1.

If [L(a),U(a)] and [L(b),U(b)] enclose the endpoint values, atan'(x)=1/(1+x^2)>0
implies

    atan([a,b]) subset [L(a),U(b)].

The endpoints are ordered because L(a)<=atan(a)<=atan(b)<=U(b). This proves
`I_atan` on every finite interval, including those crossing 0, 1 and -1.
The quarter-pi reduction is needed for useful accuracy near 1; relying only
on a fixed 22-term series there would remain rigorous but much less sharp.

## 5. Dual propagation and rejection boundaries

For a real differentiable input f (twice differentiable for D2), whose value
and derivatives lie in the respective interval fields, the ordinary chain
and product rules and inclusion of interval arithmetic give inclusion of
the returned fields. In particular,

    (atan f)'  = f'/(1+f^2),
    (atan f)'' = f''/(1+f^2) - 2f(f')^2/(1+f^2)^2.

Using `x.v**2`, instead of the dependent product `x.v*x.v`, makes the
denominator interval have lower endpoint at least 1 even when the value
interval crosses zero. This is required by the newly supported all-real
atan contract. The value, derivative and second derivative at different
points need not be correlated by the representation; lost dependence
cannot invalidate inclusion. It can make the result wider.

Integer powers retain the old nonnegative-integer API and its branch
formulas. Type checks now raise `TypeError` for non-`int` exponents, and
`ValueError` for negative integers, in normal and optimized Python alike.
As before, Python bools count as ints. Even a mathematically defined negative
power of a positive interval is outside this API; division remains available.
Fraction(2) as an exponent is also outside the original `int` contract.

For q=m/n>=0, n>0, put k=floor(sqrt(m*n)). Then

    k/n <= sqrt(q) < (k+1)/n.

This proves the existing `isqrt` endpoint construction used by `I.sqrt`;
monotonicity gives the interval result. `I.sqrt` accepts zero and rejects a
negative lower endpoint. Its upper bound may be loose at a rational square,
including zero; no precision change is claimed for this method.

D and D2 sqrt explicitly require a strictly positive value interval.
Under this condition the chain rules f'/(2sqrt(f)) and
f''/(2sqrt(f))-(f')^2/(4sqrt(f)^3) are valid and have nonzero denominators.
Inputs touching zero are rejected even when a special underlying composite
might have a removable derivative singularity; these duals do not encode
the information needed to establish such a removal. Division by intervals
containing zero remains an explicit `ZeroDivisionError`.

The proof assumes the supplied jets really enclose a common differentiable
function; arbitrary interval fields do not establish that fact. It also
assumes a function passed to a Taylor sign helper meets that helper's
differentiability and subdivision contract. The unrelated sign-helper
interfaces have not been redesigned: callers must supply ordered rational
endpoints, a boolean desired sign and valid positive subdivision budgets
(`base_n>=1`, `max_n>=base_n`; adaptive positive stopping width on nondegenerate
domains). This change does not certify unchecked arguments to those APIs.

## 6. Exact negative examples and E1 use

The saved actual source is executed under normal and -O Python in
`reproduce_before.py`. Exact rational comparisons establish:

- Old `I_cos([-1/10,1/10]).hi < 997/1000 < 1`. Therefore the old engine
  claimed `997/1000-cos(x)>0` there, although its value at 0 is -3/1000.
- Old `I_sin([-2,2]).hi < 19/20 < 1`. The certified pi interval places
  pi/2 in [-2,2], where `19/20-sin(x)=-1/20`.
- Old atan([9/10,11/10]) raises RecursionError in both modes.
- Negative powers on the interval [-1,1] are assert-rejected normally but
  accepted for I, D and D2 under -O; the underlying reciprocal has a pole.

The repaired tests use explicit `unittest` assertions, which Python does
not remove under -O. Tests at critical values, exact power/sqrt identities,
domain rejections, and structured rational probes accompany the proof.
They are finite selfchecks and cannot replace sections 1-5.

The reference trig polynomials use 48 terms (96 for the large-center point
checks). The atan reference uses a one-sided 64-term integral remainder,
with an addition formula based at 1/2 rather than production's pi/4 shift.
To control denominator growth for composed reference arguments, a rational
v with a large denominator is replaced by the enclosing endpoints
floor(10^48 v)/10^48 and ceil(10^48 v)/10^48 using integer arithmetic.
Monotonicity of atan proves the resulting reference enclosure. No endpoint
is rounded inward, and the production algorithm and acceptance thresholds
are unaffected. The first, uncompressed reference run was interrupted in
Fraction addition after about 327 seconds; raw logs and the earlier harness
are retained in `attempt1-unbounded-reference`. That interrupted run is not
counted as a completed selfcheck.

Before the coordinator's final freeze request, the E1 checks read the then-current
generator and executed only its named constants and `comps2` definition. Primary
points and derivative cells were read from the new `e1_certificate_io.py` literal
declarations without running that module. The selected AST and extracted JSON
are saved and both full-source hashes are logged for each mode.
The output-generating body, generator predicates, exporters, ledgers, and
tables are not executed or written by this author.

Actual gamma endpoints are 655/1000 and 10472/10000; the 11 primary points
and the h endpoint 13/10 are exercised. The tau argument is the actual
`2*sin(gamma)/cos(gamma)`. All distinct cells in the actual derivative fact
list are exercised, with reference derivative formulas

    tau'(gamma)  = 2/(1+3 sin(gamma)^2),
    tau''(gamma) = -12 sin(gamma)cos(gamma)/(1+3 sin(gamma)^2)^2.

These follow by differentiating atan(2tan(gamma)) where cos(gamma)>0.
The point tests require sine/cosine width < 10^-20 and tau width < 10^-12.
Cell widths are tested against explicit rational bounds in the test source.
Selected actual `comps2` values check B1(17/20)>=1/200,
B1(43/50)<=-1/50, tau(GHI)<=13/10 and TB(GHI)>=1/40.
These thresholds have not been lowered. Running these selected values does
not assert that the coordinator's 55 predicates, exports, or full workflow
have passed. Final run results and remaining limits are recorded separately
in `AUTHOR_REPORT.md` and the raw run logs.

An intermediate pair of runs finished with two test-harness KeyErrors when the
coordinator moved the point/cell lists into the new module. The other 20 test
methods passed in each mode. The failed harness, logs and source identities are
retained in `attempt2-concurrent-e1-layout`. The subsequent completed runs
adapted only the read-only test extractor and passed all 22 tests in both modes.
After the coordinator requested a source freeze, no new generator reads or
executions were started. No full generator invocation occurred in this slice.

## 7. Scope and handoff

Only `misc/rigid1d.py` is modified in the repository. All author artifacts
are in this directory. No historical Decimal implementation or driver,
generator/table/ledger, canonical graph, card, document or AGENTS file is
edited, and no commit is made. The latest exclusive write-set instruction
overrides the general request to maintain AGENTS; this file records the
specific method, authorization, and work instead.

No external novelty claim or external theorem attribution is made; the
elementary finite-series and calculus justifications are given explicitly.
No Lean command was executed. Independent review and integrated E1 acceptance
belong to the coordinator and are not represented by these author checks.
