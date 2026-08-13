# -*- coding: utf-8 -*-
"""R-209 route (iii) core: exact epsilon-expansion of the n=2 symmetric branch.

Closed 6x6 system in (k2,k3,p1,p1t,p3,p3t), eps = 1/sqrt(R):
  E1  D-half secular at lam2 = k2^2:  cos p2 sin(p1+p3) + sin p2 cos p3 cos p1/eps
      - eps sin p3 sin p2 sin p1 = 0
  E2  N-half secular at lam3 = k3^2:  cos p2t cos p1t cos p3t
      - sin p3t sin p2t cos p1t/eps - sin p3t cos p2t sin p1t
      - eps cos p3t sin p2t sin p1t = 0
  E3  shared x1: p1/k2 = p1t/k3
  E4  shared x3: p3/k2 = p3t/k3
  E5  band at x1 (D/C = sin p1/sin p1t):  I_D sin^2 p1t = I_N sin^2 p1
  E6  band at x2 (u3(x2) = -c u2(x2)): sin p1(eps cos p2t + sin p2t cot p1t)
      + eps cos p2 sin p1 + sin p2 cos p1 = 0
with p2 = k2/2 - eps(p1+p3), p2t = k3/2 - eps(p1t+p3t) and the exact mass
integrals I_D = int_0^{1/2} rho v1^2 / C^2 (same for I_N).  All numerics
EVIDENCE; the system itself is exact (verified at R=350 to 1e-12/1e-16).
"""
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

eps = sp.symbols('eps', positive=True)
k0 = sp.symbols('k0', positive=True)
k2_1, k2_2, k2_3, k2_4 = sp.symbols('k2_1 k2_2 k2_3 k2_4')
k3_1, k3_2, k3_3, k3_4 = sp.symbols('k3_1 k3_2 k3_3 k3_4')
q1_0, q1_1, q1_2, q1_3, q1_4 = sp.symbols('q1_0 q1_1 q1_2 q1_3 q1_4')
r1_0, r1_1, r1_2, r1_3, r1_4 = sp.symbols('r1_0 r1_1 r1_2 r1_3 r1_4')
p3_0, p3_1, p3_2, p3_3, p3_4 = sp.symbols('p3_0 p3_1 p3_2 p3_3 p3_4')
p3t_0, p3t_1, p3t_2, p3t_3, p3t_4 = sp.symbols('p3t_0 p3t_1 p3t_2 p3t_3 p3t_4')

k2 = k0 + eps*k2_1 + eps**2*k2_2 + eps**3*k2_3 + eps**4*k2_4
k3 = k0 + eps*k3_1 + eps**2*k3_2 + eps**3*k3_3 + eps**4*k3_4
p1 = sp.pi/2 + eps*q1_0 + eps**2*q1_1 + eps**3*q1_2 + eps**4*q1_3
p1t = sp.pi/2 + eps*r1_0 + eps**2*r1_1 + eps**3*r1_2 + eps**4*r1_3
p3 = p3_0 + eps*p3_1 + eps**2*p3_2 + eps**3*p3_3 + eps**4*p3_4
p3t = p3t_0 + eps*p3t_1 + eps**2*p3t_2 + eps**3*p3t_3 + eps**4*p3t_4
p2 = k2/2 - eps*(p1 + p3)
p2t = k3/2 - eps*(p1t + p3t)


def mass(k, p1_, p2_, p3_):
	"""I = int_0^{1/2} rho u^2 / C^2 for the D- or N-half problem (exact)."""
	BC = -(eps*sp.cos(p2_)*sp.sin(p1_)/k + sp.sin(p2_)*sp.cos(p1_)/k)/sp.sin(p3_)
	m1 = (p1_ - sp.sin(2*p1_)/2)*eps/(2*k**3)
	m3 = BC**2*(p3_ - sp.sin(2*p3_)/2)/(2*k*eps)
	a = eps*sp.sin(p1_)/k
	b = sp.cos(p1_)/k
	mL = ((a*a + b*b)*p2_/(2*k) + (a*a - b*b)*sp.sin(2*p2_)/(4*k)
		+ a*b*(1 - sp.cos(2*p2_))/(2*k))
	return m1 + m3 + mL


E1 = (sp.cos(p2)*sp.sin(p1 + p3) + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps
	- eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1))
E2 = (sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t)
	- sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps
	- sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t)
	- eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t))
E3 = p1/k2 - p1t/k3
E4 = p3/k2 - p3t/k3
ID = mass(k2, p1, p2, p3)
IN = mass(k3, p1t, p2t, p3t)
E5 = ID*sp.sin(p1t)**2 - IN*sp.sin(p1)**2
E6 = (sp.sin(p1)*(eps*sp.cos(p2t) + sp.sin(p2t)*sp.cos(p1t)/sp.sin(p1t))
	+ eps*sp.cos(p2)*sp.sin(p1) + sp.sin(p2)*sp.cos(p1))


def coeff_at(eq, n):
	"""Coefficient of eps^n in the series expansion of eq (order n+2)."""
	return sp.expand(sp.Poly(sp.series(eq, eps, 0, n + 2).removeO(), eps).coeff_monomial(eps**n))


def main():
	# order 0 coefficients
	c0 = [coeff_at(e, 0) for e in (E1, E2, E3, E4)]
	c1 = [coeff_at(e, 1) for e in (E5, E6)]
	print('E1@0 =', c0[0])
	print('E2@0 =', c0[1])
	print('E3@0 =', c0[2])
	print('E4@0 =', c0[3])
	print('E5@1 =', c1[0])
	print('E6@1 =', c1[1])
	# solve order-0: q1_0, r1_0 from E1@0, E2@0 (branch q1 = cot p2)
	q1_sol = sp.solve(sp.together(c0[0]), q1_0)
	print('q1_0 candidates:', q1_sol)
	r1_sol = sp.solve(sp.together(c0[1]), r1_0)
	print('r1_0 candidates:', r1_sol)


if __name__ == '__main__':
	main()
