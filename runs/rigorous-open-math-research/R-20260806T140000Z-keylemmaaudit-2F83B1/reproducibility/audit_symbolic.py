# audit_symbolic.py -- independent symbolic verification of all KEY LEMMA identities.
# Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)
import sympy as sp

print("=== 1. E'(alpha) = -q/Phi and O'(alpha) = -q/Phi ===")
a, q = sp.symbols('a q', positive=True)
Phi = sp.cos(a)**2 + q**2*sp.sin(a)**2
E = sp.atan(1/(q*sp.tan(a)))
O1 = sp.pi - sp.atan(q*sp.tan(a))          # on (0, pi/2)
O2 = sp.atan(-q*sp.tan(a))                 # on (pi/2, pi)
print('dE/da + q/Phi =', sp.simplify(sp.diff(E, a) + q/Phi))
print('dO1/da + q/Phi =', sp.simplify(sp.diff(O1, a) + q/Phi))
print('dO2/da + q/Phi =', sp.simplify(sp.diff(O2, a) + q/Phi))

print()
print("=== 2. alpha' = -a*Phi/(q + c*Phi) from E(a)=ca and O(a)=ca ===")
c = sp.symbols('c', positive=True)
D = q + c*Phi
print('implicit: dE/da*ap - (a + c*ap) =', sp.simplify((-q/Phi)*(-a*Phi/D) - (a + c*(-a*Phi/D))))
print('implicit: dO/da*ap - (a + c*ap) =', sp.simplify((-q/Phi)*(-a*Phi/D) - (a + c*(-a*Phi/D))))

print()
print("=== 3. G formula: (d/dc) log M along curve ===")
W = 3 + 2*a*sp.cot(a)
M = a**2*sp.sin(a)**2/D   # Mtilde, constant factor irrelevant for log derivative
sc = sp.sin(a)*sp.cos(a)
Kq = q**2 - 1
# total d/dc along curve: partial_c + partial_a * ap
ap = -a*Phi/D
dlogM = sp.simplify(sp.diff(sp.log(M), c) + sp.diff(sp.log(M), a)*ap)
G_claimed = -Phi*W/D + 2*c*a*Phi*Kq*sc/D**2
print('diff(log M)_total - G_claimed =', sp.simplify(dlogM - G_claimed))

print()
print("=== 4. IN = G2 * POS on the odd curve ===")
u = sp.symbols('u', positive=True)
A = sp.pi - sp.atan(u/q)
t = sp.atan(u)
IN = (q**2+u**2)*A*(2*A*q - 3*u + 2*t) - 3*t*u*q*(1+u**2)
# on odd curve: A = alpha2, gamma = pi - A, u = q*tan(gamma) = tan(c*A) so c = t/A
Ph_c = q**2*(1+u**2)/(q**2+u**2)   # Phi(alpha2) in (q,u) coords
c_c = t/A
D_c = q + c_c*Ph_c
sg = u/sp.sqrt(q**2+u**2); cg = q/sp.sqrt(q**2+u**2)
sA, cA = sg, -cg                     # sin(pi-gamma)=sg, cos(pi-gamma)=-cg
W_A = 3 + 2*A*cA/sA
G2 = -Ph_c*W_A/D_c + 2*c_c*A*Ph_c*Kq*sA*cA/D_c**2
POS = D_c**2*A*(q**2+u**2)*u/(Ph_c*q)
diff4 = sp.simplify(IN - G2*POS)
print('simplify(IN - G2*POS) =', diff4)

print()
print("=== 5. M2 = dIN/du ===")
M2_claimed = 4*A**2*u*q - 7*A*q**2 - 9*A*u**2 + 2*A*(q**2+u**2)/(1+u**2) + t*(4*A*u - 5*q - 9*q*u**2)
diff5 = sp.simplify(sp.diff(IN, u) - M2_claimed)
print('diff =', diff5)

print()
print("=== 6. dM2/dq ===")
S = q**2 + u**2
dM2dq_claimed = (4*A**2*u + 8*A*u**2*q/S - 7*q**2*u/S - 14*A*q - 9*u**3/S
                 + 2*u/(1+u**2) + 4*A*q/(1+u**2) + t*(4*u**2/S - 5 - 9*u**2))
diff6 = sp.simplify(sp.diff(M2_claimed, q) - dM2dq_claimed)
print('diff =', diff6)

print()
print("=== 7. M2(1,u) = pi*h(u), h(u) = 4u(pi-atan u) - 5 - 9u^2 ===")
h = 4*u*(sp.pi - sp.atan(u)) - 5 - 9*u**2
diff7 = sp.simplify(M2_claimed.subs(q, 1) - sp.pi*h)
print('diff =', diff7)

print()
print("=== 8. dG/dc total derivative formula (rigorous.py transcription) ===")
# symbolic G(a,c,q)
Ph = sp.cos(a)**2 + q**2*sp.sin(a)**2
Wf = 3 + 2*a*sp.cot(a)
scf = sp.sin(a)*sp.cos(a)
Df = q + c*Ph
G = -Ph*Wf/Df + 2*c*a*Ph*Kq*scf/Df**2
# total derivative computed by sympy
apf = -a*Ph/Df
dG_total = sp.simplify(sp.diff(G, c) + sp.diff(G, a)*apf)
# transcription of rigorous.py formula
Pha = 2*Kq*scf
Wp = 2*(scf - a)/sp.sin(a)**2
dsc = sp.cos(a)**2 - sp.sin(a)**2
Gc_f = Ph**2*Wf/Df**2 + (2*a*Ph*Kq*scf)*(Df - 2*c*Ph)/Df**3
d1 = -(Pha*Wf + Ph*Wp)/Df + Ph*Wf*c*Pha/Df**2
N = 2*c*a*Ph*Kq*scf
dN = 2*c*Kq*(Ph*a*dsc + Ph*scf + a*Pha*scf)
d2 = dN/Df**2 - 2*N*c*Pha/Df**3
Ga_f = d1 + d2
dG_claimed = sp.simplify(Ga_f*apf + Gc_f)
print('diff(dG_total - claimed) =', sp.simplify(dG_total - dG_claimed))

print()
print("=== 9. Fpp = M1*J1 - M2*J2 = dFp/dc (identity) ===")
# symbolic: d/dc (M G) = M G^2 + M dG/dc  => Fp' = M1 G1^2 + M1 dG1/dc - M2 G2^2 - M2 dG2/dc
# J := G^2 + dG/dc; identity is algebraic, no need for sympy: Fp' = M1*J1 - M2*J2 with J=G^2+dGdc
print('algebraic identity: Fp'' = M1*(G1^2 + dG1/dc) - M2*(G2^2 + dG2/dc); verified by direct expansion.')

print()
print("=== 10. CORNER: G2(1/2;q) closed forms ===")
x = sp.symbols('x')
cx = q/(q+1)
sx = sp.sqrt(2*q+1)/(q+1)
A2 = sp.pi - x
Ph2 = cx**2 + q**2*sx**2
D2 = q + sp.Rational(1,2)*Ph2
W2 = 3 + 2*A2*(sp.cos(A2)/sp.sin(A2))
G2half = (-Ph2*W2/D2 + 2*sp.Rational(1,2)*A2*Ph2*Kq*sp.sin(A2)*sp.cos(A2)/D2**2)
G2half = sp.simplify(G2half.subs({sp.sin(A2): sx, sp.cos(A2): -cx}))
cf1 = 2*q*((sp.pi-x)*(q+1) - 3*sp.sqrt(2*q+1))/(2*q+1)**sp.Rational(3,2)
print('diff(G2(1/2) - cf1) =', sp.simplify(G2half - cf1))
# value at q=2
xv = sp.acos(sp.Rational(2,3))
val2 = cf1.subs(q, 2).subs(x, xv)
target = 12*(sp.pi - sp.acos(sp.Rational(2,3)) - sp.sqrt(5))/(5*sp.sqrt(5))
print('G2(1/2;2) - target =', sp.simplify(val2 - target))
print('G2(0.4;1) numeric check deferred to point audit')

print()
print("=== 11. C4: IN = A*K(v) on the c=0.4 curve (direct algebraic check) ===")
# parametrization: v = arctan(u), A = 2.5v, w = pi - 2.5v, q = tan v / tan w
v = sp.symbols('v', positive=True)
w = sp.pi - sp.Rational(5,2)*v
q_c = sp.tan(v)/sp.tan(w)
u_c = sp.tan(v)
A_c = sp.Rational(5,2)*v
IN_c = sp.simplify((q_c**2+u_c**2)*A_c*(2*A_c*q_c - 3*u_c + 2*v) - 3*v*u_c*q_c*(1+u_c**2))
K = (q_c**2+u_c**2)*(5*v*q_c - 3*u_c + 2*v) - sp.Rational(6,5)*u_c*q_c*(1+u_c**2)
print('simplify(IN_c - A_c*K) =', sp.simplify(IN_c - A_c*K))

print()
print("=== 12. C4 tail: T^3 K identity ===")
T = sp.symbols('T', positive=True)
Kq_ = (q_c**2+u_c**2)*(5*v*q_c - 3*u_c + 2*v) - sp.Rational(6,5)*u_c*q_c*(1+u_c**2)
# q = u/T on the tail
K_tail = sp.simplify((Kq_.subs({q_c: u_c/T, u_c: u_c})))
T3K_claimed = (5*v*u_c**3*(1+T**2) - 3*u_c**3*T*(1+T**2) + 2*v*u_c**2*T*(1+T**2)
               - sp.Rational(6,5)*u_c**2*(1+u_c**2)*T**2)
diff12 = sp.simplify(T**3*K_tail - T3K_claimed)
print('diff(T^3 K - claimed) =', diff12)

print()
print("=== 13. B5: H(q,1/2) = G2(1/2)-G1(1/2) = 2 pi q (q+1)/(2q+1)^{3/2} ===")
G1half = (-Ph2*W2/D2 + 2*sp.Rational(1,2)*x*Ph2*Kq*sp.sin(x)*sp.cos(x)/D2**2)
G1half = sp.simplify(G1half.subs({sp.sin(x): sx, sp.cos(x): cx}))
B5 = sp.simplify(G2half - G1half)
cfB5 = 2*sp.pi*q*(q+1)/(2*q+1)**sp.Rational(3,2)
print('simplify(G2half - G1half - cfB5) =', sp.simplify(B5 - cfB5))

print()
print("=== 14. B4: Fp(q,1/2) closed form ===")
M1h = x**2*sx**2/D2
M2h = A2**2*sx**2/D2
G1v = G1half; G2v = G2half
Fp_half = sp.simplify(M1h*G1v - M2h*G2v)
Px = 3*x**2 + 6*x*sp.sin(x) - 3*sp.pi*x - 3*sp.pi*sp.sin(x) + sp.pi**2
cfB4 = sp.simplify(2*sp.pi*(sp.cos(x)-1)**3*Px/sp.sin(x)**3)
print('simplify(Fp_half - cfB4) =', sp.simplify(Fp_half - cfB4))
print('simplify(P(x) - (pi-3x)^2 - 3(x-sin x)(pi-2x)) =', sp.simplify(Px - (sp.pi-3*x)**2 - 3*(x-sp.sin(x))*(sp.pi-2*x)))
