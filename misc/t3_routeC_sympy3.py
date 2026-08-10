# -*- coding: utf-8 -*-
"""t3_routeC_sympy3.py: stepwise closed forms, light simplify."""
import sympy as sp
x, q, p = sp.symbols('x q p', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
th = sp.symbols('th', positive=True)

Phi = q**2*s**2 + b**2        # cos x = -b, sin x = s
D = q + p*Phi
u = x*Phi/D
A0 = sp.Rational(3)/x - 2*b/s
H = -2*p*(q**2-1)*s*b/D
V = H - A0
# derivatives at fixed q,p: d/dx with ds/dx = -b? NO: sin x = s, d(sin x)/dx = cos x = -b; d(cos x)/dx = -sin x = -s, b = -cos x so db/dx = s.
# Phi depends on x via s and b: dPhi/dx = 2q^2 s *(-b) + 2b * s = 2bs(1-q^2)
Phix = 2*s*b*(1-q**2)
Dx = p*Phix
ux = (Phi + x*Phix)/D - x*Phi*Dx/D**2
A0x = -3/x**2 - 2/s**2      # d/dx(-2b/s) = d/dx(2 cot x) = -2 csc^2 x; check: b/s = -cot x, so -2b/s = 2cot x, derivative -2csc^2 x = -2/s^2
# H = -2p(q^2-1) s b / D ; dH/dx = -2p(q^2-1) [ (s b)_x D - s b Dx ]/D^2, (s b)_x = s*(s) + (-b)*(b) = s^2 - b^2
Hx = -2*p*(q**2-1)*((s**2-b**2)*D - s*b*Dx)/D**2
G = u*V
Gx = ux*V + u*(Hx - A0x)
# Gc = dG/dp at fixed (x,q): du/dp = -x Phi^2/D^2 ; dH/dp = -2(q^2-1) s b (D - p Phi)/D^2 = -2(q^2-1) s b q /D^2
Gc = (-x*Phi**2/D**2)*V + u*(-2*(q**2-1)*s*b*q/D**2)

subs = {q: S*b/(C*s), p: th/x}
for nm, ex in [('Phi',Phi),('u',u),('A0',A0),('H',H),('V',V),('ux',ux),('A0x',A0x),('Hx',Hx),('Gx',Gx),('Gc',Gc)]:
    e = sp.cancel(ex.subs(subs))
    print('== %s ==' % nm)
    print(sp.factor(sp.expand(e)))
    print()
H2 = sp.cancel(u*Gx).subs(subs)
print('== H2 ==')
print(sp.factor(sp.expand(H2)))
import pickle
pickle.dump({'Phi':Phi.subs(subs),'u':u.subs(subs),'A0':A0.subs(subs),'H':H.subs(subs),'V':V.subs(subs),
            'ux':ux.subs(subs),'A0x':A0x.subs(subs),'Hx':Hx.subs(subs),'Gx':Gx.subs(subs),'Gc':Gc.subs(subs)},
           open('misc/t3_routeC_forms.pkl','wb'))
print('saved')
