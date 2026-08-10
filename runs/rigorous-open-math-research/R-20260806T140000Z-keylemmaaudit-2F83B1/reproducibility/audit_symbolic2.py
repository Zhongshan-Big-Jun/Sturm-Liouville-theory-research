# audit_symbolic2.py -- corrected checks for items 12, 13, 14.
import sympy as sp

q, x, v, u, T = sp.symbols('q x v u T', positive=True)

print("=== 12. C4 tail: T^3*K identity with independent symbols (q := u/T) ===")
# K as function of (v, u, q):  K = (q^2+u^2)(5v q - 3u + 2v) - 1.2 u q (1+u^2)
Kfun = (q**2+u**2)*(5*v*q - 3*u + 2*v) - sp.Rational(6,5)*u*q*(1+u**2)
K_sub = sp.simplify(Kfun.subs(q, u/T))
T3K_claimed = (5*v*u**3*(1+T**2) - 3*u**3*T*(1+T**2) + 2*v*u**2*T*(1+T**2)
               - sp.Rational(6,5)*u**2*(1+u**2)*T**2)
print('diff(T^3*K - claimed) =', sp.simplify(T**3*K_sub - T3K_claimed))

print()
print("=== 13. B5: H(q,1/2) = G2(1/2) - G1(1/2) = 2 pi q (q+1)/(2q+1)^{3/2} ===")
cx = q/(q+1); sx = sp.sqrt(2*q+1)/(q+1)
Kq = q**2 - 1
Phh = cx**2 + q**2*sx**2
Dh = q + sp.Rational(1,2)*Phh
# alpha_1 = x:  W(x),  sin x = sx, cos x = cx
W1 = 3 + 2*x*cx/sx
G1h = sp.simplify((-Phh*W1/Dh + 2*sp.Rational(1,2)*x*Phh*Kq*sx*cx/Dh**2))
# alpha_2 = pi - x:  W(pi-x), sin = sx, cos = -cx
A2 = sp.pi - x
W2 = 3 + 2*A2*(-cx)/sx
G2h = sp.simplify((-Phh*W2/Dh + 2*sp.Rational(1,2)*A2*Phh*Kq*(-sx*cx)/Dh**2))
cfB5 = 2*sp.pi*q*(q+1)/(2*q+1)**sp.Rational(3,2)
print('diff(G2h - G1h - cfB5) =', sp.simplify(G2h - G1h - cfB5))
print('H(1/2;q) simplified =', sp.simplify(G2h - G1h))

print()
print("=== 14. B4: Fp(q,1/2) = M1 G1 - M2 G2 closed form ===")
M1h = x**2*sx**2/Dh
M2h = A2**2*sx**2/Dh
Fp_half = sp.simplify(M1h*G1h - M2h*G2h)
Px = 3*x**2 + 6*x*sp.sin(x) - 3*sp.pi*x - 3*sp.pi*sp.sin(x) + sp.pi**2
cfB4 = sp.simplify(2*sp.pi*(sp.cos(x)-1)**3*Px/sp.sin(x)**3)
print('diff(Fp_half - cfB4) =', sp.simplify(Fp_half - cfB4))
print('P(x) - (pi-3x)^2 - 3(x-sin x)(pi-2x) =', sp.simplify(Px - (sp.pi-3*x)**2 - 3*(x-sp.sin(x))*(sp.pi-2*x)))
print('Fp_half factor (for sign analysis):', sp.factor(Fp_half))

print()
print("=== 14b. sign of Fp(q,1/2) via x domain: q>1 <=> x in (0, pi/3) ===")
# express Fp_half in terms of x with q = cos x/(1 - cos x)
qx = sp.cos(x)/(1 - sp.cos(x))
Fp_x = sp.simplify(Fp_half.subs(q, qx))
print('Fp(q(x),1/2) simplified:', sp.factor(Fp_x))
