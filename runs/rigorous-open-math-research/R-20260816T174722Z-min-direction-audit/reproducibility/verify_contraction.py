# -*- coding: utf-8 -*-
"""Verify n>=3, mu=2 interface contraction algebra from min_direction_progress.tex."""
import sympy as sp
import random

X, Y, kappa = sp.symbols('X Y kappa', positive=True)
x, y, rr = sp.symbols('x y r', positive=True)

# Definitions from tex
C = (3*Y-1)*(1-Y)
E = C + 2*Y*(Y-X)
kappa_N = C/E

# D_a expression from tex: D_a = y * [ X^2+2XY-4X+1 - kappa(1-X)(1-3X) ]
d_expr = X**2 + 2*X*Y - 4*X + 1 - kappa*(1-X)*(1-3*X)
D_a_expr = y * d_expr

# Original D_a from mu=2 section
D_a_orig = 3*rr*x**3*y**2 - rr*x**3 - 3*rr*x*y**2 + rr*x + x**4*y + 2*x**2*y**3 - 4*x**2*y + y
# Substitute X=x^2, Y=y^2, kappa = r*x*(3Y-1)/(y(1-3X))
Xsub = x**2
Ysub = y**2
kappa_sub = rr*x*(3*Ysub-1)/(y*(1-3*Xsub))
D_a_new = D_a_expr.subs({X:Xsub, Y:Ysub, kappa:kappa_sub})
print('D_a factorization holds:', sp.simplify(sp.expand(D_a_new) - D_a_orig) == 0)

# a-1 numerator identity
a_minus_1_num = (1-X)*y*(kappa*(1-3*X)+2*X+Y-1)
# Simplify a in X,Y,kappa:
a_expr = sp.simplify(1 + a_minus_1_num/D_a_expr)
print('a simplified:', sp.factor(a_expr))

# kappa_N bracket identity
bracket = kappa_N*(1-3*X)+2*X+Y-1
rhs = -((Y-X)*((1-Y)**2-4*X*Y))/E
print('kappa_N bracket identity holds:', sp.simplify(sp.expand(bracket - rhs)) == 0)

# Numeric sampling with correct D_a
ok_Da = True
ok_a = True
for _ in range(20000):
    Yv = random.uniform(1/3+1e-9, 1-1e-9)
    maxX = (1-Yv)**2/(4*Yv)
    if maxX <= 0:
        continue
    Xv = random.uniform(0, maxX*(1-1e-9))
    Cv = (3*Yv-1)*(1-Yv)
    Ev = Cv + 2*Yv*(Yv-Xv)
    kN = Cv/Ev
    # choose kappa in (0, kN); if actual kappa_0 > 0 this is a superset and should still satisfy a<1 but maybe a>0? a>0 holds anyway.
    kv = random.uniform(0, kN*(1-1e-9))
    yv = Yv**0.5
    dv = Xv**2 + 2*Xv*Yv - 4*Xv + 1 - kv*(1-Xv)*(1-3*Xv)
    Dv = yv * dv
    av = 1 + (1-Xv)*yv*(kv*(1-3*Xv)+2*Xv+Yv-1)/Dv
    if Dv <= 0:
        ok_Da = False
        break
    if not (0 < av < 1):
        ok_a = False
        print('counterexample:', Xv, Yv, kv, kN, Dv, av)
        break
print('D_a > 0 on sampled domain (kappa in (0,kappa_N)):', ok_Da)
print('0 < a < 1 on sampled domain (kappa in (0,kappa_N)):', ok_a)

# Also verify a < 1 symbolically for kappa < kappa_N using b<0
# b = kappa(1-3X)+2X+Y-1; since 1-3X>0 in X<1/3, b increasing in kappa; at kappa_N b<0 => for kappa<kappa_N b<0.
# Verify X<1/3 in domain: 0<X<(1-Y)^2/(4Y). Max at Y? max over Y in (1/3,1) is 1/3 at Y=1/3? Let's check numeric.
maxX_over_domain = max((1-Yv)**2/(4*Yv) for Yv in [1/3+1e-9, 0.4,0.5,0.7,0.9,0.999])
print('max X bound over Y in (1/3,1):', maxX_over_domain, '(should be <=1/3)')
