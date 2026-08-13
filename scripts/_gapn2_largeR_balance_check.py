# -*- coding: utf-8 -*-
"""R-209 M3: validation of the Richardson coefficient extraction and the
symbolic E1/E2 coefficients against direct mpmath evaluation at a test X.
EVIDENCE.
"""
import sys
import numpy as np
import mpmath as mp
import sympy as sp

sys.path.insert(0, r'scripts')
from _gapn2_largeR_balance import eval_e5_e6, richardson, make_symbolic  # noqa: E402


def main():
	X = [3.4, 0.55, 0.27, 1.6, 1.5, -0.4, -0.3, -2.0]
	# extraction check
	u0 = 0.25
	J = 13
	dps = 90
	mp.mp.dps = dps
	Xm = [mp.mpf(str(x)) for x in X]
	us = [mp.mpf(u0)*mp.mpf(2)**(-j) for j in range(J)]
	y5 = []
	y6 = []
	for uu in us:
		e5, e6 = eval_e5_e6(Xm, uu)
		y5.append(e5)
		y6.append(e6)
	c5 = richardson(y5, u0, [2, 4, 6, 8], dps)
	c6 = richardson(y6, u0, [3, 5, 7, 9], dps)
	print('extracted E5 coefficients: c2=%.6e c4=%.6e c6=%.6e c8=%.6e' %
		(c5[2], c5[4], c5[6], c5[8]))
	print('extracted E6 coefficients: c3=%.6e c5=%.6e c7=%.6e c9=%.6e' %
		(c6[3], c6[5], c6[7], c6[9]))
	for uu in [mp.mpf('0.2'), mp.mpf('0.1'), mp.mpf('0.05'), mp.mpf('0.02')]:
		e5, e6 = eval_e5_e6(Xm, uu)
		re5 = c5[2]*uu**2 + c5[4]*uu**4 + c5[6]*uu**6 + c5[8]*uu**8
		re6 = c6[3]*uu**3 + c6[5]*uu**5 + c6[7]*uu**7 + c6[9]*uu**9
		print('u=%.3f  E5=%.6e recon=%.6e err=%.2e  E6=%.6e recon=%.6e err=%.2e'
			% (uu, e5, re5, abs(e5-re5), e6, re6, abs(e6-re6)))
	# symbolic E1/E2 check
	sym = make_symbolic()
	Xl = [float(x) for x in X]
	e10 = float(sym[('E1', 0, 0)](*Xl))
	e12 = float(sym[('E1', 2, 0)](*Xl))
	e14 = float(sym[('E1', 4, 0)](*Xl))
	mp.mp.dps = 60
	for uu in [mp.mpf('0.2'), mp.mpf('0.1'), mp.mpf('0.05')]:
		u = uu
		K, A, B, C = [mp.mpf(str(x)) for x in [3.4, 0.55, 0.27, 1.6]]
		eps = u**3
		k2 = K*u
		k3 = K*u + C*u**5
		p1 = mp.pi/2 + A*u**2
		p3 = mp.pi/4 + B*u**2
		p1t = p1*(1 + C*u**4/K)
		p3t = p3*(1 + C*u**4/K)
		p2 = k2/2 - eps*(p1 + p3)
		p2t = k3/2 - eps*(1 + C*u**4/K)*(p1 + p3)
		E1 = (mp.cos(p2)*mp.sin(p1 + p3) + mp.sin(p2)*mp.cos(p3)*mp.cos(p1)/eps
			- eps*mp.sin(p3)*mp.sin(p2)*mp.sin(p1))
		re1 = e10 + e12*float(u)**2 + e14*float(u)**4
		print('u=%.3f E1=%.6e  recon=%.6e  err=%.2e' % (u, E1, re1, abs(E1-re1)))


if __name__ == '__main__':
	main()
