# -*- coding: utf-8 -*-
"""zz_verify_e1.py: rigorous exact-rational verification of all 1D facts for the E1 proof of J2_2d<0.
Uses rigid1d (interval arithmetic + D2 Taylor sign verifier over exact Fractions)."""
import sys, math, time
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D2, d2_sin, d2_cos, d2_atan, PI, der_sign2

GLO, GHI = F(655,1000), F(10472,10000)
mconst = F(791,2500)   # 0.3164

def comps2(g):
    """g: D2; returns dict of D2-valued quantities."""
    A = PI - g
    sg = d2_sin(g); cg = d2_cos(g)
    D2v = I(1) + 3*sg*sg
    B1 = A*cg - 2*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    tan = sg/cg
    tmax = d2_atan(2*tan)
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2v*D2v)
    TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2v*D2v)
    TC = mconst*G5*A*sg*cg*cg
    TB = 2*A**3*sg*sg*tmax*cg**5/(D2v*D2v*D2v.sqrt())
    z = cg*cg/D2v
    Qlo = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    Fv = tmax*tmax*cg*sg*sg
    return dict(A=A, sg=sg, cg=cg, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7,
                G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TC=TC, TB=TB, Qlo=Qlo, Fv=Fv)

def val_bound(fn, x, lo_b, hi_b=None, name=''):
    g = D2(I(x, x), I(1), I(0))
    v = fn(g).v
    ok = (lo_b is None or v.lo >= lo_b) and (hi_b is None or v.hi <= hi_b)
    return ok, v

t0 = time.time()
results = []
def add(name, ok): results.append((name, ok)); print('%s: %s' % (name, 'PASS' if ok else 'FAIL'), flush=True)

# ---- B1 ----
ok, _ = val_bound(lambda g: comps2(g)['B1'], F(85,100), F(1,100));           add('B1(0.85) >= 1/100', ok)
ok, _ = val_bound(lambda g: comps2(g)['B1'], F(86,100), None, F(-1,50));     add('B1(0.86) <= -1/50', ok)
ok, n = der_sign2(lambda g: comps2(g)['B1'], GLO, GHI, False);               add('B1 decreasing on [0.655,1.0472]', ok)
# B1 decreasing -> B1>0 on [0.655,0.85] (since B1(0.85)>0), B1<0 on [0.86,1.0472]
ok, _ = val_bound(lambda g: comps2(g)['B2'], GLO, None, F(0));               add('B2 < 0 on [0.655,1.0472]', ok)
ok, _ = val_bound(lambda g: comps2(g)['M'], GLO, None, F(0));                add('M < 0 on [0.655,1.0472]', ok)

# ---- TA monotonicity (B2 branch on [0.655,0.85]; M branch on [0.86,1.0472]) ----
ok, n = der_sign2(lambda g: comps2(g)['TA_B2'], GLO, F(72,100), True);       add('TA(B2) inc [0.655,0.72]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_B2'], F(72,100), F(724,1000), True);add('TA(B2) inc [0.72,0.724]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_B2'], F(724,1000), F(73,100), False); add('TA(B2) dec [0.724,0.73]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_B2'], F(73,100), F(85,100), False); add('TA(B2) dec [0.73,0.85]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_B2'], F(85,100), F(86,100), False); add('TA(B2) dec [0.85,0.86]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_M'], F(85,100), F(86,100), False); add('TA(M) dec [0.85,0.86]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TA_M'], F(86,100), GHI, False);       add('TA(M) dec [0.86,1.0472]', ok)

# ---- TC ----
ok, n = der_sign2(lambda g: comps2(g)['TC'], GLO, F(82,100), True);         add('TC inc [0.655,0.82]', ok)
ok, n = der_sign2(lambda g: comps2(g)['TC'], F(83,100), GHI, False);        add('TC dec [0.83,1.0472]', ok)

# ---- TB ----
ok, n = der_sign2(lambda g: comps2(g)['TB'], GLO, GHI, False);              add('TB dec [0.655,1.0472]', ok)

# ---- Qlo ----
ok, n = der_sign2(lambda g: comps2(g)['Qlo'], GLO, GHI, True);              add('Qlo inc [0.655,1.0472]', ok)
ok, _ = val_bound(lambda g: comps2(g)['Qlo'], F(10014,10000), None, F(-1,10000)); add('Qlo(1.0014) <= -1/10000', ok)

# ---- F ----
ok, n = der_sign2(lambda g: comps2(g)['Fv'], F(10014,10000), GHI, True);    add('F inc [1.0014,1.0472]', ok)

# ---- endpoint value bounds ----
E = [
  ('TA_B2(0.655) >= 11/5',  lambda g: comps2(g)['TA_B2'], F(655,1000), F(11,5), None),
  ('TA_B2(0.72) >= 13/5',   lambda g: comps2(g)['TA_B2'], F(72,100),  F(13,5), None),
  ('TA_B2(0.73) >= 13/5',   lambda g: comps2(g)['TA_B2'], F(73,100),  F(13,5), None),
  ('TA_B2(0.82) >= 2',      lambda g: comps2(g)['TA_B2'], F(82,100),  F(2,1),  None),
  ('TA_B2(0.83) >= 2',      lambda g: comps2(g)['TA_B2'], F(83,100),  F(2,1),  None),
  ('TA_B2(0.85) >= 19/10',  lambda g: comps2(g)['TA_B2'], F(85,100),  F(19,10),None),
  ('TA_M(0.86) >= 9/5',     lambda g: comps2(g)['TA_M'],  F(86,100),  F(9,5),  None),
  ('TA_M(1.0014) >= 3/5',   lambda g: comps2(g)['TA_M'],  F(10014,10000), F(3,5), None),
  ('TA_M(1.0472) >= 3/8',   lambda g: comps2(g)['TA_M'],  GHI, F(3,8), None),
  ('TB(0.72) >= 3/10',      lambda g: comps2(g)['TB'], F(72,100), F(3,10), None),
  ('TB(0.73) >= 3/10',      lambda g: comps2(g)['TB'], F(73,100), F(3,10), None),
  ('TB(0.82) >= 3/20',      lambda g: comps2(g)['TB'], F(82,100), F(3,20), None),
  ('TB(0.83) >= 3/20',      lambda g: comps2(g)['TB'], F(83,100), F(3,20), None),
  ('TB(0.85) >= 1/10',      lambda g: comps2(g)['TB'], F(85,100), F(1,10), None),
  ('TB(0.86) >= 1/10',      lambda g: comps2(g)['TB'], F(86,100), F(1,10), None),
  ('TB(1.0014) >= 1/25',    lambda g: comps2(g)['TB'], F(10014,10000), F(1,25), None),
  ('TB(1.0472) >= 1/40',    lambda g: comps2(g)['TB'], GHI, F(1,40), None),
  ('TC(0.655) >= 57/50',    lambda g: comps2(g)['TC'], F(655,1000), F(57,50), None),
  ('TC(0.72) >= 3/2',       lambda g: comps2(g)['TC'], F(72,100), F(3,2), None),
  ('TC(0.73) >= 3/2',       lambda g: comps2(g)['TC'], F(73,100), F(3,2), None),
  ('TC(0.82) >= 19/10',     lambda g: comps2(g)['TC'], F(82,100), F(19,10), None),
  ('TC(0.83) >= 19/10',     lambda g: comps2(g)['TC'], F(83,100), F(19,10), None),
  ('TC(1.0472) >= 11/10',   lambda g: comps2(g)['TC'], GHI, F(11,10), None),
  ('F(1.0472) <= 63/100',   lambda g: comps2(g)['Fv'], GHI, None, F(63,100)),
  ('Qlo(1.0472) <= 33/200', lambda g: comps2(g)['Qlo'], GHI, None, F(33,200)),
  ('G5(0.655) >= 19/5',     lambda g: comps2(g)['G5'], F(655,1000), F(19,5), None),
  ('G5(1.0472) >= 38/5',    lambda g: comps2(g)['G5'], GHI, F(38,5), None),
  ('B4(1.0472) >= 9/25',    lambda g: comps2(g)['B4'], GHI, F(9,25), None),
]
for name, fn, x, lo_b, hi_b in E:
    ok, v = val_bound(fn, x, lo_b, hi_b)
    add(name, ok)

print()
allok = all(ok for _, ok in results)
print('ALL PASS' if allok else 'SOME FAILED', flush=True)
print('elapsed %.1f s' % (time.time()-t0))
