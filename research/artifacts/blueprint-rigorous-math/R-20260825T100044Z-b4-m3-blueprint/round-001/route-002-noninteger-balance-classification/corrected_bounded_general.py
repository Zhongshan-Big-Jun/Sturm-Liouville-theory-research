"""Correct general finite-K bounded chart and secondary Newton face."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[6]
BOUND = REPO / "scripts/_gapn2_largeR_closed.py"
EXPECTED = "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4"
if hashlib.sha256(BOUND.read_bytes()).hexdigest() != EXPECTED:
    raise SystemExit("closed-equation source hash mismatch")

u = sp.symbols("u", positive=True)
K,q,B,C,q2,c2 = sp.symbols("K q B C q2 c2", real=True)
eps=u**3; k2=K*u; k3=K*u+C*u**5; r=1+C*u**4/K
p1=sp.pi/2+(2*u**2+q*u**4)/K
p3=sp.pi/4+B*u**2
p2=k2/2-eps*(p1+p3)
p1t,p3t,p2t=sp.expand(r*p1),sp.expand(r*p3),sp.expand(r*p2)


def S(expr,n=10): return sp.series(expr,u,0,n).removeO().expand()
def trig(x): return S(sp.sin(x)),S(sp.cos(x))


s1,c1=trig(p1);s2,c2p=trig(p2);s3,c3=trig(p3)
s1t,c1t=trig(p1t);s2t,c2t=trig(p2t);s3t,c3t=trig(p3t)
sin2p1,sin2p2,sin2p3=S(sp.sin(2*p1)),S(sp.sin(2*p2)),S(sp.sin(2*p3))
sin2p1t,sin2p2t,sin2p3t=S(sp.sin(2*p1t)),S(sp.sin(2*p2t)),S(sp.sin(2*p3t))
cos2p2,cos2p2t=S(sp.cos(2*p2)),S(sp.cos(2*p2t))

E1=S(c2p*S(sp.sin(p1+p3))+s2*c3*c1/eps-eps*s3*s2*s1,7)
E2=S(c2t*c1t*c3t-s3t*s2t*c1t/eps-s3t*c2t*s1t-eps*c3t*s2t*s1t,7)
E6=S(s1*(eps*c2t+s2t*S(c1t/s1t))+eps*c2p*s1+s2*c1,9)

bcD=S(-(eps*c2p*s1/k2+s2*c1/k2)*S(1/sp.sin(p3)),8)
m3D=S(bcD**2*S(p3-sin2p3/2)/(2*k2*eps),8)
m1D=S((p1-sin2p1/2)*eps/(2*k2**3),8)
aaD,bbD=S(eps*s1/k2),S(c1/k2)
mLD=S((aaD**2+bbD**2)*p2/(2*k2)
       +(aaD**2-bbD**2)*sin2p2/(4*k2)
       +aaD*bbD*(1-cos2p2)/(2*k2),8)
ID=S(m1D+m3D+mLD,8)

bcN=S((eps*c2t*s1t/k3+s2t*c1t/k3)*S(1/sp.cos(p3t)),8)
m3N=S(bcN**2*S(p3t+sin2p3t/2)/(2*k3*eps),8)
m1N=S((p1t-sin2p1t/2)*eps/(2*k3**3),8)
aaN,bbN=S(eps*s1t/k3),S(c1t/k3)
mLN=S((aaN**2+bbN**2)*p2t/(2*k3)
       +(aaN**2-bbN**2)*sin2p2t/(4*k3)
       +aaN*bbN*(1-cos2p2t)/(2*k3),8)
IN=S(m1N+m3N+mLN,8)
E5=S(ID*S(s1t**2)-IN*S(s1**2),8)

f12=sp.factor(E1.coeff(u,2)); g14=sp.factor(E1.coeff(u,4))
f22=sp.factor(E2.coeff(u,2)); g24=sp.factor(E2.coeff(u,4))
f65=sp.factor(E6.coeff(u,5)); g67=sp.factor(E6.coeff(u,7))
f54=sp.factor(E5.coeff(u,4)); g56=sp.factor(E5.coeff(u,6))

q0=(18*sp.pi-24-K**3)/(6*K); c0=16/(sp.pi*K)
sub0={q:q0,C:c0}
q2sol=sp.factor(-g14.subs(sub0)/sp.diff(f12,q).subs(sub0))
c2sol=sp.factor(-(g24.subs(sub0)+sp.diff(f22,q).subs(sub0)*q2sol)/sp.diff(f22,C).subs(sub0))
h6=sp.factor((g67+sp.diff(f65,q)*q2sol+sp.diff(f65,C)*c2sol).subs(sub0))
h5=sp.factor((g56+sp.diff(f54,q)*q2sol+sp.diff(f54,C)*c2sol).subs(sub0))

print(f"sympy={sp.__version__}")
for name,val in (("F12",f12),("F22",f22),("F65",f65),("F54",f54),
                 ("G14",g14),("G24",g24),("G67",g67),("G56",g56),
                 ("Q0",q0),("C0",c0),("Q2",q2sol),("C2",c2sol),
                 ("H6",h6),("H5",h5)):
    print(f"{name}={sp.factor(val)}")

num6=sp.factor(sp.together(h6).as_numer_denom()[0])
num5=sp.factor(sp.together(h5).as_numer_denom()[0])
print(f"H6_NUM={num6}")
print(f"H5_NUM={num5}")
res=sp.factor(sp.resultant(num6,num5,B))
print(f"RESULTANT_B={res}")

