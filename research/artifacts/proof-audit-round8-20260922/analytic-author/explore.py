"""Exploratory high precision phase roots. NOT an interval certificate or proof."""
import json
import mpmath as mp
mp.mp.dps = 70


def half_phase(Theta, Epsilon):
	if Theta <= 0:
		return mp.mpf('0')
	if Theta >= mp.pi:
		return mp.pi
	return mp.atan2(Epsilon*mp.sin(Theta), mp.cos(Theta))


def bisect(Function, Lo, Hi, Iterations=250):
	for _ in range(Iterations):
		Mid = (Lo+Hi)/2
		if Function(Mid)>0:
			Hi = Mid
		else:
			Lo = Mid
	return (Lo+Hi)/2


def roots(R, U):
	Eps = 1/mp.sqrt(R)
	W = U/Eps
	Ell = mp.mpf('0.5')-U
	def phase(K):
		return Ell*K+half_phase(W*K, Eps)
	Kone = bisect(lambda K: phase(K)-mp.pi/2, mp.mpf(0), mp.pi/(2*W))
	Ktwo = bisect(lambda K: phase(K)-mp.pi, Kone, mp.pi/W)
	Gap = R*(Ktwo**2-Kone**2)
	Lower = mp.pi**2/(2*Eps*(W+Ell)*(W+Eps*Ell))
	if not Gap >= Lower*(1-mp.mpf('1e-45')):
		raise ArithmeticError('phase lower bound failed')
	return Gap, Lower, W*Kone, W*Ktwo

Sliver = []
for Rstr in ['1500', '1507.5', '1600', '10000', '100000000', '1000000000']:
	R = mp.mpf(Rstr)
	Eps = 1/mp.sqrt(R)
	Wc = 1/(2*(1+Eps))
	Wcap = mp.mpf('0.5')/mp.sqrt(1+25/(mp.pi**2*R))
	Ws = [mp.mpf(S) for S in ['1e-12', '1e-9', '.01', '.1', '.19', '.48743', '.4995815', '.4999999995', '.5', '.503', '.6', '1', '1.5', '2']]
	Ws += [Wc*(1+S*mp.mpf('1e-7')) for S in [-1,0,1]]
	Ws += [Wcap*(1+S*mp.mpf('1e-7')) for S in [-1,0,1]]
	for W in Ws:
		Gap, Lower, T1, T2 = roots(R, W*Eps)
		Sliver.append({'R': Rstr, 'w': mp.nstr(W,25), 'G': mp.nstr(Gap,25), 'analytic_bound': mp.nstr(Lower,25), 'theta2_over_pi': mp.nstr(T2/mp.pi,20)})

Large = []
for Rstr in ['1500', '1600', '10000', '1000000000']:
	R = mp.mpf(Rstr)
	Eps = 1/mp.sqrt(R)
	Umin = 2*Eps
	for J in range(21):
		U = Umin+(mp.mpf('0.499999')-Umin)*J/20
		Ell = mp.mpf('.5')-U
		Gap, Lower, T1, T2 = roots(R,U)
		A = bisect(lambda T: -T*mp.cot(T)-U/Ell, mp.pi/2, mp.pi)
		Bar = (A*A-mp.pi**2/4)/(U*U)
		Alpha = Ell/(R*U)
		DefOne = mp.pi**2/4-T1*T1
		DefTwo = A*A-T2*T2
		if not (DefOne>4*Alpha and DefTwo<3*Alpha and Gap>Bar+Ell/(R*U**3)):
			raise ArithmeticError('large-w deficit estimate failed')
		Large.append({'R':Rstr,'u':mp.nstr(U,25),'def1_over_alpha':mp.nstr(DefOne/Alpha,25),'def2_over_alpha':mp.nstr(DefTwo/Alpha,25),'scaled_margin':mp.nstr((Gap-Bar)*R*U**3/Ell,25)})

R = mp.mpf(1600)
Gap, Lower, T1, T2 = roots(R,1/R)
Result = {'kind':'high precision exploratory samples, NOT proof or interval certification', 'mpmath_version':mp.__version__, 'decimal_precision':mp.mp.dps, 'sliver_sample_count':len(Sliver), 'large_w_sample_count':len(Large), 'branch_counterexample':{'R':1600,'u':'1/1600','theta2_over_pi':mp.nstr(T2/mp.pi,30),'theta2_less_than_pi_over_20':bool(T2<mp.pi/20)}, 'sliver':Sliver,'large_w':Large}
print(json.dumps(Result, indent=2))
