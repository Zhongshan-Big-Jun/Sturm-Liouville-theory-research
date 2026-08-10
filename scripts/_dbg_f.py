import numpy as np
from _well_rigid_verify import eigs_well, y_well, norm2_well, fval
R=4.0; a=0.3825796794951109; b=0.6174203205048892
lam1,lam2=eigs_well(a,b,R)
s1=np.sqrt(lam1); s2=np.sqrt(lam2)
n1=norm2_well(a,b,R,s1,n=4000); n2=norm2_well(a,b,R,s2,n=4000)
xs=np.linspace(0,1,4001)
y1=np.array([y_well(t,a,b,R,s1) for t in xs])
y2=np.array([y_well(t,a,b,R,s2) for t in xs])
print("mode2 y at xs near a,b,0.5:", y2[np.argmin(np.abs(xs-a))], y2[np.argmin(np.abs(xs-b))], y2[np.argmin(np.abs(xs-0.5))])
print("y_well direct at a,b,0.5 (mode2):", y_well(a,b,R,s2,a), y_well(b,a,b,R,s2), y_well(0.5,a,b,R,s2))
f=lam2*y2**2/n2 - lam1*y1**2/n1
print("f array at nearest grid to a,b,0.2,0.5:", f[np.argmin(np.abs(xs-a))], f[np.argmin(np.abs(xs-b))], f[np.argmin(np.abs(xs-0.2))], f[np.argmin(np.abs(xs-0.5))])
print("fval direct at 0.2,0.5:", fval(a,b,R,0.2), fval(a,b,R,0.5))
sg=np.sign(f); print("sign changes:", int(np.sum(np.abs(np.diff(sg))>0)))
print("y2 zero index:", np.argmin(np.abs(y2)), "x:", xs[np.argmin(np.abs(y2))])
