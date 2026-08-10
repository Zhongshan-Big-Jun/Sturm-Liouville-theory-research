from fractions import Fraction as F
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
def Pscal(a,s):
    return [s*x for x in a]
def pv(p,n): return sum(p[k]*F(n)**k for k in range(len(p)))
c=F(3); j=5; lam=F(4)/c
P_e = F(8)*c*j*j - F(4)*c*j + c*c*F(j,j-1)
Q_e = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
R_e = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
t1=P_e; t2=-F(2)*Q_e/((j-1)*(2*j-1)*lam); t3=F(4)*R_e/(lam*lam*(j-1)*(j-2)*(2*j-1)*(2*j-3)); t4=-c*c*j*lam*(2*j+1)/F(2)
D = Pmul([F(2)], Pmul([F(-1),F(1)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)]))))
denomA = Pmul([F(2)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)])))
NA = Pmul(denomA, [F(0),F(4)*c+c*c,-F(12)*c,F(8)*c])
Qe = Pmul(Pmul([F(0),F(4)],[F(-3),F(2)]), Padd(Pmul([F(-1),F(1)],[F(-1),F(2)]),[F(c)]))
denomB = Pmul([F(2)], Pmul([F(-2),F(1)],[F(-3),F(2)]))
NB = Pscal(Pmul(denomB,Qe), -F(2)/lam)
Re = Pmul(Pmul(Pmul([F(0),F(4)],[F(-2),F(1)]),[F(-3),F(2)]),[F(-5),F(2)])
denomC = [F(2)]
NC = Pscal(Pmul(denomC,Re), F(4)/(lam*lam))
denomR = D
NR = Pscal(Pmul(Pmul(denomR, [F(1),F(2)]), [F(0),F(1)]), F(c)*c*lam/F(2))
print("D at 5:", pv(D,j), "want 1512")
print("NA/D:", pv(NA,j)/pv(D,j), "want", t1)
print("NB/D:", pv(NB,j)/pv(D,j), "want", t2)
print("NC/D:", pv(NC,j)/pv(D,j), "want", t3)
print("NR/D:", pv(NR,j)/pv(D,j), "want", -t4)
print("sum:", (pv(NA,j)+pv(NB,j)+pv(NC,j)-pv(NR,j))/pv(D,j))
# also check symbolic: is N identically zero?
N = None
