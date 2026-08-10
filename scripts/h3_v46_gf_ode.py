# -*- coding: utf-8 -*-
"""H3 v46: derive exact ODE for G(z)=sum nu_n z^n from the polynomial-coefficient
recurrence (n-1)*[c^2 nu_n - P_e nu_{n-1} + Q_e nu_{n-2} - R_e nu_{n-3}] = (n-1)T_e D,
valid n>=2, nu_{-1}:=0.  Exact rational arithmetic."""
from fractions import Fraction as F

C = F(3)

def Pmul(a,b):
    r=[F(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            r[i+j]+=ai*bj
    return r
def Padd(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0))
    return r
def Psub(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))-(b[i] if i<len(b) else F(0))
    return r
def Pscal(a,s):
    return [s*x for x in a]
def polyval(p,n):
    return sum(p[k]*F(n)**k for k in range(len(p)))
def poly_str(p):
    return "+".join("%s z^%d"%(p[k],k) for k in range(len(p)) if p[k]!=0)

# coefficients as polynomials in n (low->high)
c=C
q0 = [ -c*c, c*c ]                       # c^2(n-1)
q1 = [ F(0), -(4*c+c*c), 12*c, -8*c ]    # -(n-1)P_e(n) = -(8cn^3-12cn^2+(4c+c^2)n)
# verify (n-1)P_e = 8cn^3-12cn^2+(4c+c^2)n

# (n-1)Q_e(n): Q_e = 4n(2n-3)(2n^2-3n+1+c)
q2 = [F(0), F(12)+F(12)*c, -(F(56)+F(20)*c), F(92)+F(8)*c, -F(64), F(16)]
# (n-1)R_e(n): R_e = 4n(n-2)(2n-3)(2n-5); (n-1)*R_e
# expand 4n(n-1)(n-2)(2n-3)(2n-5)
q3raw = Pmul([F(0),F(1)],[F(0),F(1)])            # n(n-1) not used; do manually below
# compute directly: (n-1)R_e(n) = 4n(n-1)(n-2)(2n-3)(2n-5)
p_nm1 = [F(-1),F(1)]
p_nm2 = [F(-2),F(1)]
p_2n3 = [F(-3),F(2)]
p_2n5 = [F(-5),F(2)]
prod = Pmul(p_nm1,Pmul(p_nm2,Pmul(p_2n3,p_2n5)))
prod = Pmul([F(0),F(4)],prod)
q3 = Pscal(prod,F(-1))
# (n-1)T_e(n): T_e=4n(4n-5)
qrhs = Pmul([F(-1),F(1)], Pmul([F(0),F(4)],[F(-5),F(4)]))

print("q0 =",poly_str(q0))
print("q1 =",poly_str(q1))
print("q2 =",poly_str(q2))
print("q3 =",poly_str(q3))
print("rhs(n) =",poly_str(qrhs))

# quick sanity: check recurrence polynomial identity on a few n by generating
# a random solution and verifying (n-1)*[orig] == q0 nu_n + q1 nu_{n-1}+...
def solve_even(cF, nu1, D, N):
    c=cF; nu=[F(0)]*(N+1); nu[1]=F(nu1)
    for j in range(2,N+1):
        Pe=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
        Qe=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
        Re=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Te=F(4)*j*(4*j-5)
        rhs=Pe*nu[j-1]-Qe*nu[j-2]+(Re*nu[j-3] if j>=3 else F(0))+Te*D
        nu[j]=rhs/(c*c)
    return nu
nu = solve_even(c, F(1), F(2), 8)
ok=True
for n in range(2,8):
    lhs = polyval(q0,n)*nu[n]+polyval(q1,n)*nu[n-1]+polyval(q2,n)*nu[n-2]+polyval(q3,n)*nu[n-3]
    rhs = polyval(qrhs,n)*F(2)
    if lhs!=rhs:
        ok=False; print("  MISMATCH n=%d: %s vs %s"%(n,lhs,rhs))
print("polynomial recurrence identity check:", ok)


