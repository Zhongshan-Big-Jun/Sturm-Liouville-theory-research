import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-keylemmaaudit-2F83B1\reproducibility")
import importlib, audit_iv
importlib.reload(audit_iv)
from audit_iv import *
import mpmath as mp
mp.mp.dps = 120
ok = True
for t in ['0', '0.1', '0.49', '0.5', '0.7', '0.999', '1', '1.5', '2', '3.06', '3.08', '6.4', '1000']:
    tv = mp.mpf(t)
    for f_iv, f_mp, name in [(iv_atan, mp.atan, 'atan'), (iv_sin, mp.sin, 'sin'), (iv_cos, mp.cos, 'cos')]:
        r = f_iv(Iv.pt(t))
        exact = f_mp(tv)
        if not (mp.mpf(str(r.lo)) <= exact <= mp.mpf(str(r.hi))):
            ok = False
            print('FAIL', name, t, mp.nstr(mp.mpf(str(r.lo)),30), mp.nstr(mp.mpf(str(r.hi)),30), mp.nstr(exact,35))
for (a, b) in [('0.2','0.5'), ('1','1.3'), ('3.0','3.1'), ('0','1.5'), ('0.4','0.5'), ('1.2','1.3')]:
    for f_iv, f_mp, name in [(iv_atan, mp.atan, 'atan'), (iv_sin, mp.sin, 'sin'), (iv_cos, mp.cos, 'cos')]:
        r = f_iv(Iv(a, b))
        # dense scan inside the interval
        n = 50
        for i in range(n+1):
            t = mp.mpf(a) + (mp.mpf(b)-mp.mpf(a))*i/n
            e = f_mp(t)
            if not (mp.mpf(str(r.lo)) <= e <= mp.mpf(str(r.hi))):
                ok = False
                print('INTERVAL FAIL', name, (a,b), 'at', mp.nstr(t,6), mp.nstr(mp.mpf(str(r.lo)),30), mp.nstr(mp.mpf(str(r.hi)),30), mp.nstr(e,35))
print('PI contains true pi:', mp.mpf(str(PI.lo)) <= mp.pi <= mp.mpf(str(PI.hi)))
print('PI width:', float(PI.hi - PI.lo))
print('HALF_PI:', HALF_PI)
x = Decimal(2)
with localcontext() as ctx:
    ctx.prec = 80; ctx.rounding = ROUND_FLOOR; sl = x.sqrt()
    ctx.rounding = ROUND_CEILING; sh = x.sqrt()
ok = ok and sl <= Decimal(str(mp.sqrt(2))) <= sh
print('sqrt2 directed ok:', sl <= Decimal(str(mp.sqrt(2))) <= sh, 'width', float(sh-sl))
print('ALL SANITY OK' if ok else 'SANITY FAILED')
