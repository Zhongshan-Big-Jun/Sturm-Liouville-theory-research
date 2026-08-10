# -*- coding: utf-8 -*-
"""H3 v17b: verify ODD moment system (fix negative moment indices)."""
from fractions import Fraction as F

c = F(3)
def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def l2(p, q):
	n = max(len(p), len(q)); P = list(p)+[F(0)]*(n-len(p)); Q = list(q)+[F(0)]*(n-len(q))
	return sum(P[j]*Q[k]*F(2, j+k+1) for j in range(n) for k in range(n) if (j+k)%2==0)
def h1(p, q):
	return -F(1,2)*(ev(p,F(1))-ev(p,F(-1)))*(ev(q,F(1))-ev(q,F(-1))) + l2(deriv(p),deriv(q)) + c*l2(p,q)
def kc(p):
	n = len(p)-1; out=[F(0)]*(n+1)
	for j in range(n+1):
		out[j] += c*p[j]
		if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
	return out
def p_odd(m):
	p = [F(0)]*(2*m+2)
	p[2*m+1] = F(1)
	p[2*m-1] = -F(m, m-1)
	return p
def Po(j): return F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
def Qo(j): return F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
def Ro(j): return F(4)*j*(j-2)*(2*j-1)*(2*j-3)
def To(j): return F(4)*j*(4*j-3)

w = [F(0)]*4; w[3] = F(1)   # w = x^3
S = ev(w,F(1))-ev(w,F(-1))
def mu(k):
	if k < 0: return F(0)
	q = [F(0)]*(k+1); q[k] = F(1)
	return l2(w, q)

print("=== odd moment system: w = x^3, c = 3 ===")
for m in (2, 3, 4, 5):
	p = p_odd(m)
	lhs = h1(w, kc(p))
	rhs = c*c*mu(2*m+1) - Po(m)*mu(2*m-1) + Qo(m)*mu(2*m-3) - Ro(m)*mu(2*m-5) - To(m)*S
	print("  m={}: (w,K_c p_{})_1 = {} ; formula = {} ; match: {}".format(m, 2*m+1, lhs, rhs, lhs == rhs))
print("  recurrence:")
for m in (2, 3, 4, 5):
	val = Po(m)*mu(2*m-1) - Qo(m)*mu(2*m-3) + Ro(m)*mu(2*m-5) + To(m)*S
	print("    c^2 mu_{} == formula: {}".format(2*m+1, c*c*mu(2*m+1) == val))

print("=== even moment system re-verification: w = x^2, c = 3 ===")
def p_even(m):
	p = [F(0)]*(2*m+1)
	p[2*m] = F(1)
	p[2*m-2] = -F(m, m-1)
	return p
def Pe(j): return F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
def Qe(j): return F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
def Re(j): return F(4)*j*(j-2)*(2*j-3)*(2*j-5)
def Te(j): return F(4)*j*(4*j-5)
w2 = [F(0)]*3; w2[2] = F(1)
D = ev(w2,F(1))+ev(w2,F(-1))
def mu2(k):
	if k < 0: return F(0)
	q = [F(0)]*(k+1); q[k] = F(1)
	return l2(w2, q)
for m in (2, 3, 4, 5):
	p = p_even(m)
	lhs = h1(w2, kc(p))
	rhs = c*c*mu2(2*m) - Pe(m)*mu2(2*m-2) + Qe(m)*mu2(2*m-4) - Re(m)*mu2(2*m-6) - Te(m)*D
	print("  m={}: match: {}".format(m, lhs == rhs))
