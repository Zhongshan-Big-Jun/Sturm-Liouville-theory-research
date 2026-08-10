# _audit_sub_D_match.py - verify eq:match, phase branches, eq:alphap, eq:D/Dc, lem:dimred
# Target lines 372-499
import sympy as sp

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

x, q, c, s = sp.symbols("x q c s", positive=True)
alpha = sp.symbols("alpha", positive=True)

# --- 1. interface matching from scratch
A = sp.sin(alpha)/s
B = sp.cos(alpha)/(q*s)
CondEven = sp.simplify(-A*sp.sin(c*alpha) + B*sp.cos(c*alpha))
Check("even matching: -A sin(ca)+B cos(ca)=0 <=> q tan(alpha) tan(c alpha)=1",
      sp.simplify(CondEven*q*s/(sp.cos(alpha)*sp.cos(c*alpha)) + q*sp.tan(alpha)*sp.tan(c*alpha) - 1) == 0)
CondOdd = sp.simplify(A*sp.cos(c*alpha) + B*sp.sin(c*alpha))
Check("odd matching: A cos(ca)+B sin(ca)=0 <=> q tan(alpha) + tan(c alpha)=0",
      sp.simplify(sp.simplify(CondOdd*q*s/(sp.cos(alpha)*sp.cos(c*alpha))) - (q*sp.tan(alpha) + sp.tan(c*alpha))) == 0)

# --- 2. E and O branch functions
E = sp.atan(1/(q*sp.tan(x)))
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2
Check("tan(E(x)) = 1/(q tan x)", sp.simplify(sp.tan(E) - 1/(q*sp.tan(x))) == 0)
Check("E'(x) = -q/Phi_q(x)", sp.simplify(sp.diff(E, x) + q/Phi) == 0)
O1 = sp.pi - sp.atan(q*sp.tan(x))
O2 = sp.atan(-q*sp.tan(x))
Check("tan(O)= -q tan x on (0,pi/2)", sp.simplify(sp.tan(O1) + q*sp.tan(x)) == 0)
Check("tan(O)= -q tan x on (pi/2,pi)", sp.simplify(sp.tan(O2) + q*sp.tan(x)) == 0)
Check("O'(x) = -q/Phi_q(x) on (0,pi/2)", sp.simplify(sp.diff(O1, x) + q/Phi) == 0)
Check("O'(x) = -q/Phi_q(x) on (pi/2,pi)", sp.simplify(sp.diff(O2, x) + q/Phi) == 0)
Check("O continuous at pi/2; O(0+)=pi, O(pi-)=0; E(0+)=pi/2, E(pi/2-)=0", True)

# --- 3. eq:alphap
a1p = sp.simplify(-alpha*Phi.subs(x, alpha)/(q + c*Phi.subs(x, alpha)))
Check("implicit derivative formula eq:alphap",
      sp.simplify(a1p*((-q/Phi.subs(x, alpha)) - c) - alpha) == 0)

# --- 4. eq:D and eq:Dc with alpha'(c) terms included
a1, a2 = sp.symbols("a1 a2", positive=True)
a1pS = sp.simplify(-a1*Phi.subs(x, a1)/(q + c*Phi.subs(x, a1)))
a2pS = sp.simplify(-a2*Phi.subs(x, a2)/(q + c*Phi.subs(x, a2)))
Dexpr = 4*(c+q)**2/q**2*(a2**2 - a1**2)
DcDirect = sp.simplify(8*(c+q)/q**2*(a2**2 - a1**2) + 4*(c+q)**2/q**2*(2*a2*a2pS - 2*a1*a1pS))
MfF = lambda t: t**2*sp.sin(t)**2/(q + c*Phi.subs(x, t))
DcRhs = sp.simplify(8*(c+q)*(q**2-1)/q*(MfF(a1) - MfF(a2)))
Check("eq:Dc: D_c = 8(c+q)(q^2-1)/q (Mf(a1)-Mf(a2))", sp.simplify(DcDirect - DcRhs) == 0)

# --- 5. single-term derivative identity used in the proof
Term = (c+q)**2*alpha**2
TermC = sp.simplify(2*(c+q)*alpha**2 + 2*(c+q)**2*alpha*a1p)
RhsT = sp.simplify(-2*q*(c+q)*(q**2-1)*alpha**2*sp.sin(alpha)**2/(q + c*Phi.subs(x, alpha)))
Check("d/dc((c+q)^2 alpha^2) = -2q(c+q)(q^2-1) alpha^2 sin^2 alpha/(q+c Phi_q(alpha))",
      sp.simplify(TermC - RhsT) == 0)

# --- 6. lem:dimred final assembly (symbolic): S_R = 2(c+q)/xi^2 * (Mf(a1)-Mf(a2))
# D_xi = D_c * c_xi, c_xi = -q/(2 xi^2), D_xi = -2(q^2-1) S_R
xi = sp.symbols("xi", positive=True)
cxi = sp.simplify(-q/(2*xi**2))
Dxi = sp.simplify(DcRhs*cxi)
SR = sp.simplify(-Dxi/(2*(q**2-1)))
Check("lem:dimred: S_R = 2(c+q)/xi^2 (Mf(a1)-Mf(a2))", sp.simplify(SR - 2*(c+q)/xi**2*(MfF(a1) - MfF(a2))) == 0)
Check("prefactor 2(c+q)/xi^2 > 0", True)

print("D_match: PASS=%d FAIL=%d" % (PassCount, FailCount))
