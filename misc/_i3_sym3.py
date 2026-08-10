# -*- coding: utf-8 -*-
"""J in gamma = pi - x coordinates for B2. Check structure."""
import sympy as sp
import mpmath as mp

# symbolic in y = gamma, x = pi - y
y, c, q = sp.symbols('y c q', positive=True)
sy = sp.sin(y); cy = sp.cos(y)
Ph = cy**2 + q**2*sy**2
D = q + c*Ph
W = 3 - 2*(sp.pi - y)*cy/sy
G = -Ph*W/D - 2*c*(sp.pi - y)*Ph*(q**2-1)*sy*cy/(D**2)

# derivative along curve: G' = dG/dc at fixed curve point. In gamma coords:
# alpha2(c) = pi - y(c), y'(c) = -alpha2'(c) = alpha2*Phi/D = (pi-y)*Ph/D
# dG/dc = G_y * y' + G_c
yp = (sp.pi - y)*Ph/D
Gc = sp.diff(G, c)
Gy = sp.diff(G, y)
Gp = sp.simplify(Gy*yp + Gc)
J = sp.simplify(G**2 + Gp)

num, den = sp.fraction(sp.together(J))
print("den =", sp.factor(den))
num = sp.expand(num)
print("num ops:", sp.count_ops(num))
# save to file for inspection
with open(r"misc/_i3_J2_num.txt","w") as f:
    f.write(sp.sstr(num))
print("saved. Sample:")
# numeric check in gamma coords
mp.mp.dps = 40
def PhiN(x,q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def GN(x,c,q):
    Ph = PhiN(x,q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def JN(x,c,q):
    Ph = PhiN(x,q); D = q + c*Ph; xp = -x*Ph/D
    Gv = GN(x,c,q)
    h = mp.mpf('1e-6')
    Gpv = ((GN(x+h,c,q)-GN(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    W = 3 + 2*x/mp.tan(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
# compare sympy J with numeric at y=0.9, c=0.5, q=1.5
pts = [(0.9, 0.5, 1.5), (1.0472, 0.5, 1.0), (0.6557, 0.4, 2.0)]
for (yv,cv,qv) in pts:
    xv = mp.pi - mp.mpf(yv)
    Jsym = float(J.subs({y: mp.mpf(yv), c: mp.mpf(cv), q: mp.mpf(qv)}))
    Jnum = float(JN(xv, mp.mpf(cv), mp.mpf(qv)))
    print("y=%.4f c=%.2f q=%.2f: sym=%.6f num=%.6f" % (yv,cv,qv,Jsym,Jnum))
