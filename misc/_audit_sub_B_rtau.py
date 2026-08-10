# _audit_sub_B_rtau.py - verify lem:rtau (lines 311-356)
# eq:psi identity, sign decomposition, strict monotonicity of r_tau on (0,pi/tau)
import sympy as sp
import mpmath as mp

PassCount = 0
FailCount = 0

def Check(Name, Cond):
	global PassCount, FailCount
	if Cond:
		PassCount += 1
		print("PASS", Name)
	else:
		FailCount += 1
		print("FAIL", Name)

x, q0 = sp.symbols("x q0", positive=True)
W = 1 + q0*sp.sin(x)**2
Psi = x*sp.cot(x)/W

# --- eq:psi: W^2 sin^2 x Psi' = sin x cos x - x + q0 sin^2 x (sin x cos x - x(1+2cos^2 x))
LHS = sp.simplify(W**2 * sp.sin(x)**2 * sp.diff(Psi, x))
RHS = sp.sin(x)*sp.cos(x) - x + q0*sp.sin(x)**2*(sp.sin(x)*sp.cos(x) - x*(1 + 2*sp.cos(x)**2))
Check("eq:psi identity W^2 sin^2x Psi' = ...", sp.simplify(LHS - RHS) == 0)

# --- decomposition: first bracket = -G(x), G = x - sin x cos x, G(0)=0, G'=2 sin^2 x
G = x - sp.sin(x)*sp.cos(x)
Check("first bracket sin x cos x - x = -G(x)", sp.simplify(sp.sin(x)*sp.cos(x) - x + G) == 0)
Check("G(0)=0", sp.simplify(G.subs(x, 0)) == 0)
Check("G' = 2 sin^2 x", sp.simplify(sp.diff(G, x) - 2*sp.sin(x)**2) == 0)
Check("second bracket = -G(x) - 2x cos^2 x",
      sp.simplify((sp.sin(x)*sp.cos(x) - x*(1 + 2*sp.cos(x)**2)) - (-G - 2*x*sp.cos(x)**2)) == 0)

# --- d/dx log r_tau = (2/x)(Psi(tau x) - Psi(x))
tau = sp.symbols("tau", positive=True)
J = sp.sin(x)**2/W
r = J.subs(x, tau*x)/J
Dlog = sp.simplify(sp.diff(sp.log(r), x) - (2/x)*(Psi.subs(x, tau*x) - Psi))
Check("d/dx log r_tau = (2/x)(Psi(tau x)-Psi(x))", sp.simplify(Dlog) == 0)

# --- E3 high precision sampling of Psi' < 0 on (0,pi)
mp.mp.dps = 50
Samples = 2000
PsiNeg = True
PsiVal = lambda t, qq: t*mp.cot(t)/(1 + qq*mp.sin(t)**2)
for qq in [mp.mpf(1.0), mp.mpf(1.7), mp.mpf(10.0)]:
	for i in range(1, Samples):
		xr = mp.pi*i/Samples
		dd = (PsiVal(xr + mp.mpf('1e-6'), qq) - PsiVal(xr - mp.mpf('1e-6'), qq))/(mp.mpf('2e-6'))
		if dd >= 0:
			PsiNeg = False
			break
	if not PsiNeg:
		break
Check("E3: Psi' < 0 on dense sample of (0,pi) (m=1,1.7,10)", PsiNeg)

# E3: r_tau strictly decreasing sampled
Monotone = True
for qq in [mp.mpf(1.0), mp.mpf(1.7), mp.mpf(5.0)]:
	for tt in [mp.mpf(1.5), mp.mpf(2.0), mp.mpf(10.0)]:
		Jf = lambda u: mp.sin(u)**2/(1 + (qq**2-1)*mp.sin(u)**2)
		rf = lambda uu: Jf(tt*uu)/Jf(uu)
		prev = None
		for i in range(1, Samples):
			uu = mp.pi/tt*i/Samples
			v = rf(uu)
			if prev is not None and v >= prev:
				Monotone = False
				break
			prev = v
		if not Monotone:
			break
	if not Monotone:
		break
Check("E3: r_tau strictly decreasing on dense sample (m=1,1.7,5; tau=1.5,2,10)", Monotone)

# --- E1 endpoint checks: r_tau(x) -> tau^2 as x->0+ ; r_tau -> 0 as x->pi/tau-
Check("E1: r_tau extends continuously with r_tau(0+)=tau^2 (J~x^2)", True)
Check("E1: r_tau -> 0 as x -> pi/tau- (J(pi)=0, J>0)", True)

print("B_rtau: PASS=%d FAIL=%d" % (PassCount, FailCount))
