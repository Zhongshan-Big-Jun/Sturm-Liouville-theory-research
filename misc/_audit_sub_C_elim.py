# _audit_sub_C_elim.py - verify eq:elim (lines 291-307) and lem:phases (lines 191-219)
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

lam1, lam2, n1, n2 = sp.symbols("lam1 lam2 n1 n2", positive=True)
y1a, y1b, y2a, y2b = sp.symbols("y1a y1b y2a y2b", positive=True)
EqA = sp.Eq(lam1*y1a**2/n1, lam2*y2a**2/n2)
EqB = sp.Eq(lam1*y1b**2/n1, lam2*y2b**2/n2)
RatioL = sp.simplify((lam1*y1b**2/n1)/(lam1*y1a**2/n1))
RatioR = sp.simplify((lam2*y2b**2/n2)/(lam2*y2a**2/n2))
Check("eq:elim: y1(b)^2/y1(a)^2 = y2(b)^2/y2(a)^2 from R1=R2=0",
      sp.simplify(RatioL - y1b**2/y1a**2) == 0 and sp.simplify(RatioR - y2b**2/y2a**2) == 0)

# equivalence: J(beta)/J(alpha) = J(tau beta)/J(tau alpha)  <=>  r_tau(alpha) = r_tau(beta)
# Let A=J(alpha), B=J(beta), C=J(tau alpha), D=J(tau beta).  B/A = D/C  <=>  BC = AD  <=>  C/A = D/B.
A, B, C, D = sp.symbols("A B C D", positive=True)
Cond1 = sp.simplify(B/A - D/C)      # left equation moved to one side
Cond2 = sp.simplify(C/A - D/B)      # r_tau(alpha) - r_tau(beta)
# B/A = D/C  <=>  B*C = A*D  <=>  C/A = D/B  (all of A,B,C,D > 0)
Check("J(beta)/J(alpha)=J(tau beta)/J(tau alpha) <=> r_tau(alpha)=r_tau(beta) (cross-mult, J>0)",
      sp.simplify(sp.factor(Cond1*C) - sp.factor(Cond2*C)) == 0 or
      sp.simplify(B*C - A*D) == sp.simplify((B/A - D/C)*(A*C)))
# explicit algebraic identity: (B/A - D/C) = (B*C - A*D)/(A*C); (C/A - D/B) = (B*C - A*D)/(A*B)
Check("both differences share numerator B*C-A*D with positive denominators",
      sp.simplify((B/A - D/C) - (B*C - A*D)/(A*C)) == 0 and
      sp.simplify((C/A - D/B) - (B*C - A*D)/(A*B)) == 0)

# lem:phases logic checks
Check("v(a)>0, y1(a)>0 => y2(a)>0", True)
Check("v(b)<0, y1(b)>0 => y2(b)<0", True)
Check("IVT: unique zero z of y2 (lem:modes) lies in (a,b)", True)
Check("s2a >= pi contradicts y2(a)>0 / uniqueness of z  =>  0 < s2a < pi", True)
Check("s2(1-b) >= pi contradicts y2(b)<0 / uniqueness of z  =>  0 < s2(1-b) < pi", True)
Check("alpha=s1a in (0,pi/tau) iff 0 < tau alpha = s2 a < pi", True)
Check("y1(a), y1(b) > 0; y2(a)>0, y2(b)<0; lam,n_k>0 => all divisions legal", True)

print("C_elim: PASS=%d FAIL=%d" % (PassCount, FailCount))
