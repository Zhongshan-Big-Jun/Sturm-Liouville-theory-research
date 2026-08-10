# -*- coding: utf-8 -*-
"""H3 exact structure: compute u_m, v_m, w_m = u_m - 2c^2 v_m exactly (Fractions), look for patterns."""
from fractions import Fraction as F
import math

def solve_even(c, nu1, D, N):
	c = F(c); nu = [F(0)]*(N+1); nu[1] = F(nu1)
	for j in range(2, N+1):
		Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
		Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
		Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
		Tm = F(4)*j*(4*j-5)
		rhs = Pm*nu[j-1] - Qm*nu[j-2] + (Rm*nu[j-3] if j >= 3 else F(0)) + Tm*D
		nu[j] = rhs/(c*c)
	return nu

for c in (3,):
	N = 14
	u = solve_even(c, 1, 0, N)
	v = solve_even(c, 0, 1, N)
	print(f"c={c}: u_m (nu1=1,D=0):")
	for m in range(0, N+1):
		print(f"  m={m}: u={u[m]}   z=u/((m!)^2 (4/c)^m) = {u[m]/F(math.factorial(m))**2/F(F(4)/c)**m if m>0 else u[m]}")
	print("v_m (nu1=0,D=1):")
	for m in range(0, N+1):
		z = v[m]/F(math.factorial(m))**2/F(F(4)/c)**m if m > 0 else v[m]
		print(f"  m={m}: v={v[m]}   z={z}")
	print("w_m = u_m - 2c^2 v_m:")
	for m in range(0, N+1):
		w = u[m] - F(2)*c*c*v[m]
		z = w/F(math.factorial(m))**2/F(F(4)/c)**m if m > 0 else w
		print(f"  m={m}: w={w}   z={z}")
	# z as decimal
	print("w z decimals:")
	for m in range(1, N+1):
		w = u[m] - F(2)*c*c*v[m]
		z = w/F(math.factorial(m))**2/F(F(4)/c)**m
		print(f"  m={m}: {float(z):.12f}")
