# Round 8 exact rational replacement certificate

This is an **author submission, awaiting independent final review**. It replaces the computational obligations for T3 and the scalar constants formerly delegated to scripts 05 and 19. It does not certify the complete INF limit, the deep-sliver region, phase-branch selection, or all inequalities of Lemma A''. No main TeX, repository, library, canonical knowledge or Git files were changed.

`certificate.py` is standalone Python standard-library code. Its default path uses exact integers and `Fraction` for proof arithmetic, with `Decimal` used only after the comparisons to print directed bounds. It imports neither the old scripts nor the supplied checker. Its 19 check groups evaluate the finite arithmetic obligations in the analytic argument below; they are not a formal proof of Python, a Lean development, or 19 independently reviewed theorems.

## Contract and source identity

The frozen proof is `inputs/sources/docs/SL_gap_n1_inf_limit_proof.tex`, corresponding to the coordinator's baseline `d1462eb444938554b17da1db398763b31efb4ef4`. Its SHA-256 is `82bec420ccfacb145bf9431dc6cf3fc9123fd2c073929477c5112a806487ef31`. The frozen historical scripts 05 and 19, submitted checker, analytic supplement, audit report, original results and original failure log are preserved under `inputs/`. `inputs/manifest.json` records their actual source locations and intake-verified SHA-256 hashes. No historical script was executed wholesale.

In this contract, the one-variable function G(a) is distinct from the source's two-parameter spectral gap G(R,u). For a in (pi/2, pi), define

\[
 G(a)=8a^3\sin^2a-\pi^2(2a-\sin2a),\qquad
 u(a)=\frac{a}{2(a-\tan a)},\qquad
 \bar D(u(a))=\frac{a^2-\pi^2/4}{u(a)^2}.
\]

Let a_star be the unique zero of G on this interval, u_star=u(a_star), and D_star=Dbar(u_star). The claims are:

1. The exact decimal rationals
   a_L=2.27651323902643307501655540074525185589672 and
   a_H=2.27651323902643307501655540074525185589673 satisfy
   G(a_L)>0>G(a_H), so a_L<a_star<a_H.
2. u_star lies strictly inside [0.32992250812006654958, 0.32992250812006654960], and D_star lies strictly inside [24.9438661384324768968, 24.9438661384324769084]. Also 25-D_star>0.0561 and 3pi^2-D_star>4.664947.
3. For every t in (pi/2,pi), with v=-t cot(t), B(t)=2t^4/(t^2+v^2+v)<9.
4. Cz=(8/pi-(1+sqrt(2)))/(pi/8) satisfies 0<Cz<337/1000.
5. The scalar ratio described below is strictly less than 8256/10000. Applying it to def2/def1 additionally requires the upstream analytic inequalities and their stated parameter restrictions. Those are not established by a run of this certificate.

Exact rational endpoints are stored in `results.json` and `results_optimized.json`. A 60-significant-digit outward display from the actual normal run is:

| Quantity | Lower endpoint | Upper endpoint |
| --- | --- | --- |
| u_star | 0.329922508120066549592808055011934819609541809855626912410304 | 0.329922508120066549592808055011934819609544576124996436522485 |
| D_star | 24.9438661384324769025843376842235317942033484534874224042288 | 24.9438661384324769025843376842235317942041850311825840111996 |
| Cz | 0.336811399010865299678739064149761090797329474928831180132453 | 0.336811399010867846157828534475133392937543435158623731486786 |

These displays are outward bounds, not decimal approximations used as proof inputs.

## Exact interval and transcendental arithmetic

An `Interval(lo, hi)` holds two exact Fractions, and its constructor explicitly requires lo<=hi. Addition, subtraction and four-product multiplication are the usual inclusion extensions. If an interval [l,h] excludes zero, its reciprocal is [1/h,1/l], including when both endpoints are negative. Even powers use lower endpoint zero when the input crosses zero; odd powers preserve order. Division by any interval containing zero raises an exception.

The input boundary accepts only an actual integer or a Fraction, rejecting floats, Decimal values and booleans. Strings appear only in explicit `Fraction("exact decimal")` constructors for fixed rational witnesses. The sole `float(...)` call is in the negative control that demonstrates rejection before arithmetic begins. There are no `assert` guards in the certificate; every guard executes under `python -O`.

### Machin identity and its branch

Put t=arctan(1/5), s=arctan(1/239). The double-angle formulas give tan(2t)=5/12, tan(4t)=120/119 and tan(4t-s)=1. To settle the branch without assuming a decimal value of pi, the integral of 1/(1+x^2) from 0 to 1 is greater than 1/2, so pi>2. Also t<1/5 and s>0 give 4t-s<4/5<pi/2. The alternating-series lower bound t>1/5-(1/5)^3/3 and the upper bound s<1/239 give 4t-s>0. Thus 4t-s=pi/4, and

\[
 \pi=16\arctan(1/5)-4\arctan(1/239).
\]

For 0<x<1, the terms x^(2k+1)/(2k+1) decrease to zero. Therefore the sum of n terms and the adjacent sum of n+1 terms enclose arctan(x). `atan_small` uses n=85 and n=28, respectively; its exact interval combination encloses pi. No floating-point pi or oracle enters the calculation. The arithmetic also establishes 3<pi<22/7 and pi^2<12, used below.

### Taylor remainder and exact outward reduction

For a rational x and integer N>=1, `trig_point` forms the degree-N Maclaurin polynomials for both sin and cos. The coefficients of the wrong parity are zero. Since every derivative of sin and cos has absolute value at most 1 on the real axis, Taylor's theorem gives, for either function,

\[
 |f(x)-P_N(x)|\le \frac{|x|^{N+1}}{(N+1)!}.
\]

The recurrence term_k=term_(k-1)*x/k evaluates the polynomials and remainder in Fraction arithmetic. This argument works for negative x and for either parity of N; it does not confuse a truncated polynomial with an enclosure. Used degrees are 110 for ordinary phase points, 130 for sin(2a), 80 for sin(2), 90 at 23/10, and 30 at the small cotangent witness.

To keep denominators manageable, each Taylor interval and the Machin interval is enlarged onto a rational grid with denominator 10^90. For [l,h] the returned endpoints are

\[
 \frac{\lfloor 10^{90}l\rfloor}{10^{90}},\qquad
 \frac{\lceil 10^{90}h\rceil}{10^{90}}.
\]

Integer floor division computes these exactly, including for negative endpoints. This is a proof-preserving enlargement, independent of Decimal contexts. The quotient of the sine and cosine enclosures is used only after division has excluded zero in the denominator interval. Every evaluated phase is explicitly checked to lie above PiBox.hi/2 and below PiBox.lo.

### Display is not comparison

All root signs, interval containment and threshold comparisons use Fraction endpoints. Only afterward does `encode` serialize each exact numerator/denominator together with displays. `directed_decimal` divides Decimal integers at 60 significant digits under ROUND_FLOOR for lower displays and ROUND_CEILING for upper displays. The numerical equality or ordering of printed strings is never consulted by the certificate. The exact fractions remain authoritative. `verify_bundle.py` independently parses all stored display bounds back into exact rationals and checks their directions.

## Root identity, uniqueness and monotone propagation

This section supplies the analytic argument linking the finite root signs to the intended mathematical object; it is not inferred from sampling.

Write s=sin(a), c=cos(a), and

\[
 h(a)=3+3a\cot a-a^2\csc^2a,\quad
 \widetilde K(a)=s^2h(a),\quad
 J(a)=4a^3\cot a+6a^2-\pi^2.
\]

Differentiation gives

\[
 h'(a)s^3=3cs^2-5as+2a^2c<0,\quad
 J'(a)=4a\widetilde K(a)/s^2,\quad
 G'(a)=4s^2J(a).
\]

Here a>0, s>0 and c<0, so each term in the first numerator is strictly negative. Because h(pi/2)=3-pi^2/4>0 and h tends to minus infinity at pi, h has exactly one zero. Consequently J first increases and then decreases; J(pi/2)=pi^2/2>0 and J tends to minus infinity, so it has exactly one zero. Consequently G first increases and then decreases; G(pi/2)=0, it is positive until its interior maximum, and G(pi)=-2pi^3<0. It has exactly one interior zero, with positive-to-negative crossing. The two certified endpoint signs therefore isolate that zero.

The parametrization u(a) is increasing and maps (pi/2,pi) onto (0,1/2), since

\[
 u'(a)=\frac{a-\sin(2a)/2}{2\cos^2(a)(a-\tan a)^2}>0,
\]

and its endpoint limits are 0 and 1/2. Its denominator is positive and sin(2a)<0 in the open interval. To verify the identity with the extremum of Dbar directly, set b=a-tan(a), so b'=-tan^2(a) and Dbar(u(a))=4b^2-pi^2 b^2/a^2. Differentiation and s^2+c^2=1 give

\[
 \frac{d}{da}\bar D(u(a))=-\frac{bG(a)}{a^3c^2},\qquad
 \bar D'(u(a))=-\frac{4b^3G(a)}{a^3(2a-\sin2a)}.
\]

The latter multiplier of G is negative, so Dbar decreases before u_star and increases after it. This establishes the identity of the T3 point and its unique global minimum within the limiting system, without invoking the deep-sliver argument.

### General rule: lower(L), upper(H)

For any nondecreasing function f on [L,H], suppose a sound evaluator returns
I_L=[lower(L),upper(L)] containing f(L), and I_H=[lower(H),upper(H)] containing f(H). For every x in [L,H],

\[
 \operatorname{lower}(L)\le f(L)\le f(x)\le f(H)\le\operatorname{upper}(H).
\]

Thus the general sound image enclosure is [lower(L),upper(H)]. Using lower(H) as the right endpoint is unjustified. An ordering test on two computed values cannot establish monotonicity: `increasing_image` explicitly relies on the analytic monotonicity proof of its caller. For T3 it returns [u_point(a_L).lo,u_point(a_H).hi]. The value enclosure is then obtained by ordinary interval extension of (a^2-pi^2/4)/u^2. No monotonicity of Dbar across its minimum is assumed.

The inverse root formulation in old script 05 has the same rule. For 0<u<1/2, let

\[
 F(a;u)=\tan a+a\left(\frac1{2u}-1\right).
\]

On (pi/2,pi), F_a=tan^2(a)+1/(2u)>0 and F_u=-a/(2u^2)<0. The endpoint limits give a unique root a(u), and implicit differentiation gives a'(u)>0. Each proposed bracket must pass **upper(F(lower;u))<0** and **lower(F(upper;u))>0**, with both endpoints in the phase domain. Only after these checks may `monotone_root_image` map [L,H] to [lower_root(L),upper_root(H)].

The certificate exercises this API with L=1/3, H=3/8, the bracket [2,12/5] at L, and the preserved old narrow bracket at H. At the exact old lower endpoint

\[
 A_{old,L}=\frac{57422840420798164132636532169819408433127719830251}{23384026197294446691258957323460528314494920687616},
\]

the enclosure of F(a;3/8) is strictly negative, about -1.3569474947*10^-40. At the genuine upper endpoint

\[
 A_{old,H}=\frac{14355710105199541033159133042454852108282351614991}{5846006549323611672814739330865132078623730171904},
\]

it is strictly positive, about 8.8020322201*10^-42. The right endpoint selected by the rejected old rule is therefore strictly smaller than a(3/8). The `old-upper-endpoint` control feeds that bad right endpoint through the actual root-image API and fails its positive-sign guard. This is a general propagation defect; it does not assert that the old main run's particular interval must have missed u_star.

## B(t)<9 over the entire open interval

Since sin(t)>0 and cos(t)<0 on (pi/2,pi), multiplying the defining denominator by sin^2(t) gives

\[
 B(t)=\frac{2t^3\sin^2t}{t-\sin t\cos t}\le 2t^2\sin^2t.
\]

The following three ranges exhaust the interval, including the tail approaching mathematical pi:

| Range | Analytic estimate | Certified rational upper bound |
| --- | --- | --- |
| pi/2<t<=2 | sin^2(t)<=1 | 8 |
| 2<=t<=23/10 | sin decreases; sin(2)<91/100 | 2(23/10)^2(91/100)^2=4380649/500000=8.761298 |
| 23/10<=t<pi | q(t)=t sin(t) is positive and decreasing here | 2((23/10)(3/4))^2=4761/800=5.95125 |

For the last row, q''(t)=2cos(t)-t sin(t)<0 throughout (pi/2,pi). Taylor bounds certify sin(23/10)<3/4 and cos(23/10)<-3/5, hence q'(23/10)<3/4-(23/10)(3/5)=-63/100<0. Thus q decreases thereafter and remains positive, justifying squaring the bound. The script checks the trigonometric endpoint bounds, cutpoint placement, negative derivative bound and all three strict rational comparisons with 9. There is no floating grid or omitted pi-tail.

## Cz and the scalar ratio

The square inequalities for 1.414213562373095 and 1.414213562373096 enclose sqrt(2). The half-angle identity gives cot(pi/8)=1+sqrt(2), so interval arithmetic on

\[
 C_z=\frac{1/(\pi/8)-(1+\sqrt2)}{\pi/8}
\]

proves 0<Cz<337/1000.

For completeness the scalar remainder inequality need not rely on the incorrectly indexed cotangent series in the old text. Put r(z)=(1/z-cot(z))/z on (0,pi). Then

\[
 r'(z)=\frac{N(z)}{z^3\sin^2 z},\qquad
 N(z)=z^2+z\sin z\cos z-2\sin^2 z,
\]

and N''(z)=4sin(z)(sin(z)-z cos(z))>0. Indeed sin(z)-z cos(z) vanishes at zero and has derivative z sin(z)>0. Since N(0)=N'(0)=0, r'(z)>0. Its removable value at zero is 1/3 by Taylor expansion. Therefore 1/z-cot(z)<=Cz*z for 0<z<=pi/8, with the removable zero limit as needed. This is an elementary analytic argument, not a sampled monotonicity claim.

Let epsilon0=1/sqrt(1500). Exact square comparisons and the sqrt(2) enclosure give

\[
 \varepsilon_0<10/387,\qquad \tan(\pi/8)=\sqrt2-1<29/70.
\]

Consequently the exact checks establish

\[
 \pi>333/106,\quad
 \pi/2-\varepsilon_0\tan(\pi/8)>
 \mathrm{PiBox.lo}/2-29/2709>39/25,
\]
\[
 1-\pi^2\varepsilon_0^2/192>
 1-\mathrm{PiBox.hi}^2(10/387)^2/192>24999/25000.
\]

Also 2*(337/1000)/1500<45/100000 and

\[
 \frac1{1-45/100000}<\frac{100046}{100000}.
\]

Here is the precise scalar interface for the last comparison. Suppose 0<C<=Cz, 0<=B<=9, d<=epsilon0*tan(pi/8), c>=1-pi^2*epsilon0^2/192, A>=1 and 0<=delta<=45/100000. Then all denominators below are positive and

\[
 \frac{4CB}{3\pi(\pi/2-d)c}\frac1{1-\delta/A}
 < Q:=\frac{4(337/1000)9(100046/100000)}
 {3(333/106)(39/25)(24999/25000)}
 =\frac{893460803}{1082206710}<\frac{516}{625}=0.8256.
\]

An outward upper display of Q is 0.825591631195855364822123492470306342861245057332900846641397. In the intended application, A=1+v(v+1)/(t theta)>=1. The certificate establishes these scalar bounds; the inequalities connecting the spectral deficits to them remain analytic obligations of the main proof. In particular this certificate does not imply full deep-sliver coverage or the complete INF-limit theorem.

## Exact tests of the unsafe cot construction

The separate `legacy_diagnostics.py` runs the inspected minimal transcriptions in the unchanged supplied checker using the actual installed mpmath/libm. Here the specified binary input is

\[
 x=\frac{4889224211780879}{1152921504606846976}
 \quad(\texttt{0x1.15eb9385ed50fp-8}).
\]

The observed `nextafter(cos(x)/sin(x), +/-infinity)` bounds were
235.80726580993837 and 235.80726580993843, exactly

\[
 L=\frac{1037091322688373}{4398046511104},\qquad
 H=\frac{4148365290753493}{17592186044416}.
\]

The new certificate recomputes cot(x) with rational Taylor arithmetic and proves its upper bound is strictly below L, with gap greater than 8.77736015657416*10^-15. Its `unsafe-cot-enclosure` control consequently fails. Pinning these exact inputs makes that mathematical comparison portable. It does **not** claim every OS/libm produces this same bad pair; the diagnostic's `supplied_miss_reproduced_here` records the actual local observation. On this platform it is true. A different platform's failure to reproduce the leak would be reported as such, not patched into success.

The exact binary rational 884279719003555/281474976710656 is also strictly below the Machin lower bound for pi. It cannot close an interval claimed to reach mathematical pi.

## Replays, dependency evidence and failure preservation

All executions are copied into numbered `runs/` directories. Each retains the executed scripts, raw `stdout.txt` and `stderr.txt`, any actual result file, `imports.json`, and `record.json` with command, cwd, time, actual exit code, expectation, and hashes. Numbering appends; no failed source snapshot or receipt is overwritten. The files called `results.json` inside supplied runs are generated there; their original copies are separate in `inputs/submitted/`.

`trace_execution.py` reports the modules present in `sys.modules` after target execution, including its own support imports, with file paths/hashes and exposed versions. It does not filter external imports and is not a complete event log of modules that might have been unloaded. The observed runtime is Python 3.14.4, Linux/WSL2 with glibc 2.43, mpmath 1.3.0 and SymPy 1.14.0. The latter two are used only by the supplied mixed-evidence checker and separate diagnostic. The certificate's observed imports are standard library modules. No packages were installed or modified.

Isolation here means private input copies, private working directories, `-B` and `PYTHONDONTWRITEBYTECODE=1`. It is **not** an OS security sandbox, virtual environment, or prevention of arbitrary imports. Code was read before execution, and outputs were directed into the author directory.

| Replay | Actual result | Meaning |
| --- | --- | --- |
| `001-supplied-normal` | Exit 0, 22 confirmed groups | Unchanged supplied checker; mixed exact, symbolic and numerical evidence |
| `002-supplied-optimized` | Exit 0, 22 confirmed groups | Same unchanged checker under -O |
| `003-legacy-platform-diagnostics` | Exit 0 | Actual platform observation and exact witness extraction |
| `004-certificate-normal` | Exit 0, 19 arithmetic groups | New scoped author certificate |
| `019-certificate-optimized` | Exit 0, 19 arithmetic groups | Same exact results under -O |
| `005`-`018`, `020`-`033` | Exit 1 each | 14 negative controls in each interpreter mode |

The 14 controls reject: wrong G right endpoint; the old lower-as-upper endpoint; wrong u and D enclosures; the unsafe cot pair; binary pi as an enclosure; wrong sqrt(2) bounds; an omitted Taylor remainder; a zero-containing divisor; reversed interval; float input; invalid Taylor degree; invalid arctan domain; and an unsupported tighter scalar comparison. The final control shows failure to certify Q<0.825, not a counterexample to every conceivable sharper analytic estimate. `verify_bundle.py` checks each control's specific exception text, not merely a nonzero process exit. Thus an unrelated syntax or import failure cannot be counted as the intended rejection.

`inputs/submitted/initial_symbolic_check_failure.log` preserves the supplied author's earlier Wronskian simplification failure with SHA-256 `2eaf2f29275858450bd331ed42a716ccdd7204bb74e5ee5e60975c2b76901fad`. The old failed source revision and its original process exit-code receipt were not supplied; neither is reconstructed. The later supplied success does not erase that log. The new certificate's first positive runs succeeded; its planned negative-control failures are retained separately. Every later author execution, including any failure of the bundle verifier, likewise remains in `runs/`.

`continue_supplied.py` is a fallback diagnostic hook for a platform on which the unmodified supplied checker stops at a `require` failure. It records all reached conditions, retains false ones and exits 1 if any are false. It is clearly labelled as a modified diagnostic, cannot stand in for an unchanged replay, and was **not needed or run** in this submission.

## Reproduce

For just the standalone certificate, any ordinary current Python 3 supporting these standard-library features is sufficient; this submission actually tested the recorded 3.14.4 interpreter. Run within this directory:

```bash
python3 -B certificate.py --output fresh_results.json
python3 -B -O certificate.py --output fresh_results_optimized.json
python3 -B certificate.py --negative old-upper-endpoint
python3 -B -O certificate.py --negative unsafe-cot-enclosure
```

The last two commands are supposed to exit 1 and print the rejecting exception. For append-only captured runs:

```bash
python3 -B replay.py supplied
python3 -B replay.py certificate
python3 -B replay.py verify
```

The supplied stage requires the already installed mpmath/SymPy and verifies frozen inputs against the coordinator's intake. It never installs them. The certificate itself is portable without the intake or those dependencies. The replay driver is tied to this author's parent round directory. `verify_bundle.py` validates all completed receipts, successful-result equality, directed displays, recorded negative errors, standard-library provenance and source style. `replay_summary.json` and `artifact_hashes.json` provide the delivered summary and file inventory; neither is an independent review verdict.
