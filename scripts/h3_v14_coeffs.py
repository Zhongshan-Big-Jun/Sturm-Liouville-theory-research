# -*- coding: utf-8 -*-
"""H3 v14: verify odd z-recurrence coefficients numerically; test power ansatz residuals."""
import numpy as np, math

c = 3.0
lam = 4.0/c
def coeffs(j, par):
	if par=='e':
		Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
		Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
		Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
	else:
		Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
		Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
		Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
	A = Pm/(4.0*c*j*j)
	B = -Qm/(16.0*j*j*(j-1)*(j-1))
	C = c*Rm/(64.0*j*j*(j-1)*(j-1)*(j-2)*(j-2))
	return A, B, C

for par in ('e','o'):
	print("=== parity", par)
	for j in (10**3, 10**6, 10**7):
		A, B, C = coeffs(j, par)
		print("  j={:>8}: A-2 = {:+.10f}   B+1 = {:+.10f}   C*j^2 = {:.10f}   (A+B+C-1)*j^2 = {:.10f}".format(
			j, A-2, B+1, C*j*j, (A+B+C-1)*j*j))
	# residual of power ansatz z_j = j^alpha: R_j = z_j - A z_{j-1} - B z_{j-2} - C z_{j-3}
	print("  residual of z_j=j^alpha, parity", par, ":")
	for alpha in (2.5, 1.5, 0.5, -0.5):
		R = []
		for j in (10**6, 2*10**6):
			A, B, C = coeffs(j, par)
			z = j**alpha - A*(j-1)**alpha - B*(j-2)**alpha - C*(j-3)**alpha
			R.append(z/j**(alpha-2))
		print("    alpha={:+.1f}: R/j^(alpha-2) at 1e6,2e6: {:.6e}, {:.6e}".format(alpha, R[0], R[1]))
