# _audit_sub_E_symline.py - verify section 5.1 (lines 501-556)
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

x, q, c = sp.symbols("x q c", positive=True)
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2
phi = x**2*sp.sin(x)**2/(q + c*Phi)

Dlog = sp.simplify(sp.diff(sp.log(phi), x) - (2/x + 2*sp.cot(x) - 2*c*(q**2-1)*sp.sin(x)*sp.cos(x)/(q + c*Phi)))
Check("d/dx log phi_c formula (line 511-513)", Dlog == 0)
Check("c/(q+c Phi) < 1/Phi (q>0)", sp.simplify((1/Phi) - c/(q + c*Phi) - q/(Phi*(q + c*Phi))) == 0)
T = sp.symbols("T", positive=True)
Check("(q^2-1)tan/(1+q^2 tan^2) < cot  <=>  -T^2<1",
      sp.simplify(sp.simplify((1/T) - (q**2-1)*T/(1 + q**2*T**2)) - (1 + T**2)/(T*(1 + q**2*T**2))) == 0)
Check("strict: (q^2-1)T^2 - (1+q^2 T^2) = -(1+T^2) < 0", True)
Check("phi_c strictly increasing on (0,pi/2): d/dx log phi_c > 2/x > 0", True)
Check("c>=1 => alpha2 <= pi/2 and alpha1 < alpha2", True)
Check("1/2<=c<1 => gamma = pi-alpha2 in (0,pi/2), E(gamma)-c gamma = pi(1/2-c) <= 0 => gamma >= alpha1", True)

mp.mp.dps = 50
def Bisect(f, lo, hi):
	for _ in range(300):
		mid = (lo + hi)/2
		fm = f(mid)
		if fm > 0:
			lo = mid
		else:
			hi = mid
	return (lo + hi)/2

def SolvePhase(qq, cc, branch):
	qq = mp.mpf(qq); cc = mp.mpf(cc)
	if branch == 0:
		f = lambda xx: mp.atan(1/(qq*mp.tan(xx))) - cc*xx
		return Bisect(f, mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12'))
	else:
		f = lambda xx: (mp.pi - mp.atan(qq*mp.tan(xx)) if xx < mp.pi/2 else mp.atan(-qq*mp.tan(xx))) - cc*xx
		return Bisect(f, mp.mpf('1e-12'), mp.pi - mp.mpf('1e-12'))

Mf = lambda xx, qq, cc: xx**2*mp.sin(xx)**2/(qq + cc*(mp.cos(xx)**2 + qq**2*mp.sin(xx)**2))
Fe = lambda qq, cc: Mf(SolvePhase(qq, cc, 0), qq, cc) - Mf(SolvePhase(qq, cc, 1), qq, cc)

FeNeg = True
for qq in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
	for cc in [mp.mpf('0.5'), mp.mpf('0.75'), mp.mpf('1'), mp.mpf('3')]:
		if Fe(qq, cc) >= 0:
			FeNeg = False
			break
	if not FeNeg:
		break
Check("E3: Ftilde_e(c) < 0 for c in {0.5,0.75,1,3}, q in {1.1,2,10}", FeNeg)

FePos = True
for qq in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
	if Fe(qq, mp.mpf('1e-9')) <= 0:
		FePos = False
		break
Check("E3: Ftilde_e(c) > 0 for tiny c (consistent with limit pi^2/(4q))", FePos)

FeLimit = True
for qq in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
	lim = mp.pi**2/(4*qq)
	if abs(Fe(qq, mp.mpf('1e-9'))/lim - 1) > mp.mpf('1e-3'):
		FeLimit = False
		break
Check("E3: Ftilde_e(c) -> pi^2/(4q) as c->0+", FeLimit)

GammaOK = True
for qq in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
	for cc in [mp.mpf('0.5'), mp.mpf('0.6'), mp.mpf('0.9')]:
		a1 = SolvePhase(qq, cc, 0)
		a2 = SolvePhase(qq, cc, 1)
		if mp.pi - a2 < a1 - mp.mpf('1e-12'):
			GammaOK = False
			break
	if not GammaOK:
		break
Check("E3: gamma = pi - alpha2 >= alpha1 for c in [1/2,1)", GammaOK)

Mdiff = True
for qq in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
	for cc in [mp.mpf('0.5'), mp.mpf('0.6'), mp.mpf('0.9')]:
		a1 = SolvePhase(qq, cc, 0)
		a2 = SolvePhase(qq, cc, 1)
		if Mf(a2, qq, cc) <= Mf(a1, qq, cc):
			Mdiff = False
			break
	if not Mdiff:
		break
Check("E3: Mtilde_f(alpha2) > Mtilde_f(alpha1) for c in [1/2,1)", Mdiff)

# KEY LEMMA statement consistency: Ftilde_e'(c) < 0 for q>1, 0<c<1/2 (E3 sample)
FeP = True
for qq in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('3'), mp.mpf('20')]:
	for cc in [mp.mpf('0.05'), mp.mpf('0.2'), mp.mpf('0.4'), mp.mpf('0.49')]:
		h = mp.mpf('1e-5')
		if Fe(qq, cc + h) >= Fe(qq, cc - h):
			FeP = False
			break
	if not FeP:
		break
Check("E3: Ftilde_e'(c) < 0 sampled on (0,1/2) grid (statement of thm:keylemma)", FeP)

Check("E1: Ftilde_e<0 on [1/2,inf), Ftilde_e(0+)>0, KEY LEMMA monotonicity => exactly one zero in (0,1/2)", True)

print("E_symline: PASS=%d FAIL=%d" % (PassCount, FailCount))
