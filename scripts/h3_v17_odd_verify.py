# -*- coding: utf-8 -*-
"""H3 v17: verify ODD moment system by direct exact computation (w = x^3, c=3)."""
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

# odd basis p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}
def p_odd(m):
	p = [F(0)]*(2*m+2)
	p[2*m+1] = F(1)
	p[2*m-1] = -F(m, m-1)
	return p

def Po(j): return F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
def Qo(j): return F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
def Ro(j): return F(4)*j*(j-2)*(2*j-1)*(2*j-3)
def To(j): return F(4)*j*(4*j-3)

print("=== odd moment system verification: w = x^3, c = 3 ===")
# w = x^3 is odd; w(1)-w(-1) = 2, w(1)+w(-1) = 0
w = [F(0)]*4; w[3] = F(1)
S = ev(w,F(1))-ev(w,F(-1))
# moments
def mu(k):
	q = [F(0)]*(k+1); q[k] = F(1)
	return l2(w, q)
for m in (2, 3, 4, 5):
	p = p_odd(m)
	kp = kc(p)
	lhs = h1(w, kp)   # (w, K_c p_{2m+1})_1
	mu21 = mu(2*m+1); mu2m1 = mu(2*m-1); mu2m3 = mu(2*m-3); mu2m5 = mu(2*m-5)
	rhs = c*c*mu21 - Po(m)*mu2m1 + Qo(m)*mu2m3 - Ro(m)*mu2m5 - To(m)*S
	print("  m={}: (w,K_c p_{})_1 = {} ; formula = {} ; match: {}".format(m, 2*m+1, lhs, rhs, lhs == rhs))
# verify the odd recurrence itself: c^2 mu_{2m+1} = Po(m) mu_{2m-1} - Qo(m) mu_{2m-3} + Ro(m) mu_{2m-5} + To(m) S
print("  recurrence check:")
for m in (2, 3, 4, 5):
	val = Po(m)*mu(2*m-1) - Qo(m)*mu(2*m-3) + Ro(m)*mu(2*m-5) + To(m)*S
	print("    c^2 mu_{} = {} ; Po*mu - Qo*mu + Ro*mu + To*S = {} ; match: {}".format(
		2*m+1, c*c*mu(2*m+1), val, c*c*mu(2*m+1) == val))

print("")
print("=== also verify the '(w, K_c^2 p) + boundary' identity for odd ===")
# (w, K_c p_{2m+1})_1 = (K_c p_{2m+1})(1)*S + (w, K_c^2 p_{2m+1})  [check: boundary coeff should be -T_o(m)? or +?]
for m in (2, 3):
	p = p_odd(m)
	kp = kc(p)
	k2p = kc(kp)   # K_c^2 p
	lhs = h1(w, kp)
	rhs = ev(kp, F(1))*S + l2(w, k2p)
	print("  m={}: (w,K_c p)_1 = {} ; kp(1)*S + (w,K_c^2 p) = {} ; match: {}".format(m, lhs, rhs, lhs == rhs))
	print("    kp(1) = {} ; -T_o(m) = {}".format(ev(kp, F(1)), -To(m)))
