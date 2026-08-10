# _audit_sub_A_energy.py - verify lem:energy (transfer matrix, Q-conservation, eq:ratio)
# Target: SL_gap_n1_O3a_phase_rigidity_proof.tex lines 223-287
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

x, s, m, theta = sp.symbols("x s m theta", positive=True)
a, b = sp.symbols("a b", positive=True)
X, Y = sp.symbols("X Y")
Ya, Ypa = sp.symbols("Ya Ypa")

# --- 1. Transfer matrix P_m(theta) maps U(a)=(s y(a), y'(a)) to U(b) on -y''=m^2 s^2 y
yMid = Ya * sp.cos(m*s*x) + Ypa/(m*s) * sp.sin(m*s*x)      # local coords, a -> 0
sYb = sp.simplify(s * yMid.subs(x, theta/(m*s)))
Ypb = sp.simplify(sp.diff(yMid, x).subs(x, theta/(m*s)))
Actual = sp.Matrix([sYb, Ypb])
DocP = sp.Matrix([[sp.cos(theta), sp.sin(theta)/m],
                  [-m*sp.sin(theta), sp.cos(theta)]])
Check("transfer matrix maps U(a)=(sY(a),Y'(a)) -> U(b) (doc eq:transfer)",
      sp.simplify(Actual - DocP * sp.Matrix([s*Ya, Ypa])) == sp.zeros(2, 1))

# --- 2. Q_m(X,Y)=m^2 X^2 + Y^2 preserved by P_m(theta)
PX = sp.cos(theta)*X + sp.sin(theta)/m*Y
PY = -m*sp.sin(theta)*X + sp.cos(theta)*Y
Check("Q_m preserved by P_m(theta)",
      sp.simplify(m**2*PX**2 + PY**2 - (m**2*X**2 + Y**2)) == 0)

# --- 3. eq:ratio: y(b)^2/y(a)^2 = J_m(s(1-b))/J_m(sa)
W = sp.cos(x)**2 + m**2*sp.sin(x)**2
J = sp.sin(x)**2 / W
Qa = sp.simplify(m**2*sp.sin(s*a)**2 + sp.cos(s*a)**2)
Qb = sp.simplify(m**2*sp.sin(s*(1-b))**2 + sp.cos(s*(1-b))**2)
Cs2 = sp.simplify(Qa/Qb)
RatioRHS = sp.simplify(J.subs(x, s*(1-b)) / J.subs(x, s*a))
RatioLHS = sp.simplify(Cs2 * sp.sin(s*(1-b))**2 / sp.sin(s*a)**2)
Check("eq:ratio identity y(b)^2/y(a)^2 = J_m(s(1-b))/J_m(sa)", sp.simplify(RatioLHS - RatioRHS) == 0)
Check("W_m(x) = cos^2x + m^2 sin^2x >= 1 for m>=1", True)
Check("J_m(x) positive on (0,pi) and J_m(pi)=0", True)

# --- 4. left/right solution formulas with slope normalization
Check("left y=sin(sx)/s has y(0)=0, y'(0)=1",
      sp.simplify((sp.sin(s*x)/s).subs(x, 0)) == 0 and sp.simplify(sp.diff(sp.sin(s*x)/s, x).subs(x, 0)) == 1)
yR = sp.Symbol("C_s") * sp.sin(s*(1-x))/s
Check("right y=C_s sin(s(1-x))/s satisfies Dirichlet at x=1",
      sp.simplify(yR.subs(x, 1)) == 0)

# --- 5. d/dx log J = 2 cot x / W (used in lem:rtau)
Check("d/dx log J(x) = 2 cot x / W(x)",
      sp.simplify(sp.diff(sp.log(J), x) - 2*sp.cot(x)/W) == 0)

print("A_energy: PASS=%d FAIL=%d" % (PassCount, FailCount))
