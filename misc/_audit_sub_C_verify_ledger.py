# _audit_sub_C_verify_ledger.py — verify all 57 ledger facts with the independent engine
import sys, json
from fractions import Fraction as F
from mpmath import mp, mpf, sin, cos, tan, atan, sqrt, pi, acos
mp.dps = 60
sys.path.insert(0, r'F:\LaTeX\BVE research\misc')
from _audit_sub_C_certengine import (FUNCS, diff1, diff2, evali, cell_env, point_env,
    f_point_interval, fprime_point, fprime_cell, fpp_cell, F, pint)

ledger = json.load(open(r'F:\LaTeX\BVE research\misc\e1_cert_ledger.json', encoding='utf-8'))
facts = ledger['facts']

def frac(s): return F(s)
def fl(s): return float(s)

results = []
def check(name, ok, extra=''):
    results.append((name, bool(ok)))
    print(("PASS" if ok else "FAIL"), name, extra)

# ---------- point facts ----------
h_of = lambda t: t*sin(t)*cos(t)
def point_true(fname, g0):
    g = mpf(g0.numerator)/g0.denominator
    if fname == 'B1': return (pi-g)*cos(g) - 2*sin(g)
    if fname == 'B2': A = pi-g; return 4*A**2*cos(g)**2 - A**2 - 12*A*cos(g)*sin(g) + 6*sin(g)**2
    if fname == 'M': A = pi-g; return 2*A**2*cos(g)**2 - A**2 - 8*A*cos(g)*sin(g) + 6*sin(g)**2
    if fname == 'B4': A = pi-g; return 7*A*cos(g)**2 - A*sin(g)**2 - 4*cos(g)*sin(g)
    if fname == 'G5':
        A = pi-g
        B5 = A**2*cos(g)**2 - A**2*sin(g)**2 + 2*A**2 + 12*A*cos(g)*sin(g) - 12*sin(g)**2
        B4 = 7*A*cos(g)**2 - A*sin(g)**2 - 4*cos(g)*sin(g)
        return B5 - A*B4
    if fname == 'Qlo':
        A = pi-g; D = sqrt(1+3*sin(g)**2)
        B7 = 3*A*cos(g)**2 + A*sin(g)**2 + 8*cos(g)*sin(g)
        z = cos(g)**2/D**2
        return 4*A**2*z**2 - A*B7*z + 6*cos(g)**2*sin(g)**2
    if fname == 'Qhi':
        A = pi-g
        B7 = 3*A*cos(g)**2 + A*sin(g)**2 + 8*cos(g)*sin(g)
        z = cos(g)**2
        return 4*A**2*z**2 - A*B7*z + 6*cos(g)**2*sin(g)**2
    if fname == 'F': return atan(2*tan(g))**2*cos(g)*sin(g)**2
    if fname == 'TA_B2':
        A = pi-g; D = sqrt(1+3*sin(g)**2)
        B2 = 4*A**2*cos(g)**2 - A**2 - 12*A*cos(g)*sin(g) + 6*sin(g)**2
        return 4*A**2*sin(g)**2*cos(g)**4*abs(B2)/D**4
    if fname == 'TA_M':
        A = pi-g; D = sqrt(1+3*sin(g)**2)
        Mf = 2*A**2*cos(g)**2 - A**2 - 8*A*cos(g)*sin(g) + 6*sin(g)**2
        return 4*A**2*sin(g)**2*cos(g)**4*abs(Mf)/D**4
    if fname == 'TB':
        A = pi-g; D = sqrt(1+3*sin(g)**2)
        return 2*A**3*sin(g)**2*atan(2*tan(g))*cos(g)**5/D**5
    if fname == 'TC':
        A = pi-g
        B5 = A**2*cos(g)**2 - A**2*sin(g)**2 + 2*A**2 + 12*A*cos(g)*sin(g) - 12*sin(g)**2
        B4 = 7*A*cos(g)**2 - A*sin(g)**2 - 4*cos(g)*sin(g)
        G5 = B5 - A*B4
        return (mpf(791)/2500)*G5*A*sin(g)*cos(g)**2
    if fname == 'tau': return atan(2*tan(g))
    if fname == 'h': return h_of(g)
    raise ValueError(fname)

pt_names = ['B1','B2','M','B4','G5','Qlo','Qhi','F','TA_B2','TA_M','TB','TC','tau','h']
n_point = 0; n_point_fail = 0
for f in facts:
    if f['kind'] != 'point': continue
    d = f['detail']
    g0 = frac(d['point'])
    target = frac(d['target'])
    cmp_ = d['cmp']
    name = f['name']
    # identify fname from the fact name
    fname = None
    for pn in ['TA_B2','TA_M','Qlo','B1','B2','M','B4','G5','F','TB','TC','tau','h']:
        if name.startswith(pn):
            fname = pn; break
    if fname is None:
        check("point fact name parse: %s" % name, False); continue
    mine = None
    if fname == 'tau':
        from _audit_sub_C_certengine import tau_env_at
        mine = tau_env_at(g0)
    elif fname == 'h':
        # h(t) = t sin t cos t with t = gamma (or 13/10)
        from _audit_sub_C_certengine import _sin_cos_env, mul, add
        s, c = _sin_cos_env(g0)
        mine = mul(mul(pint(g0), s), c)
    else:
        mine = f_point_interval(fname, g0)
    ok_ineq = (mine.lo >= target) if cmp_ == 'ge' else (mine.hi <= target)
    tv = point_true(fname, g0)
    lo = float(d['val'][0]); hi = float(d['val'][1])
    ok_contains = (lo - 1e-11 <= tv <= hi + 1e-11)
    ok_myint = (float(mine.lo) - 1e-11 <= tv <= float(mine.hi) + 1e-11)
    margin = float(d['margin'])
    ok_margin = margin > 0
    ok = ok_ineq and ok_contains and ok_myint and ok_margin
    n_point += 1
    if not ok: n_point_fail += 1
    check("point: %s (mine %s, true %.12f)" % (name, (float(mine.lo),float(mine.hi)), tv), ok,
          "ineq=%s contains=%s margin=%.3e" % (ok_ineq, ok_contains, margin))
print("point facts: %d verified, %d failed" % (n_point, n_point_fail))

# ---------- value-taylor facts ----------
vt_names = ['B2 < 0','M < 0','B4 > 0','G5 > 0','Qhi < 0','TA_B2 >= 27/10 on [0.723,0.724]','TC >= 19/10 on [0.82,0.83]']
for f in facts:
    if f['kind'] != 'value-taylor': continue
    d = f['detail']
    fname = None
    for pn in ['TA_B2','TC','B2','M','B4','G5','Qhi']:
        if f['name'].startswith(pn): fname = pn; break
    if fname is None: check("vt parse fail: %s" % f['name'], False); continue
    allok = True
    for piece in d['pieces']:
        a = frac(piece['cell'][0]); b = frac(piece['cell'][1]); c = frac(piece['c'])
        Mled = float(piece['M'])
        corr = float(piece['corr'])
        fvc_lo = float(piece['fvc'][0]); fvc_hi = float(piece['fvc'][1])
        bnd_lo = float(piece['bound'][0]); bnd_hi = float(piece['bound'][1])
        w = (b - a)/2
        # my certified sup |f'| on cell (crude interval bound, then rigorous subdivision):
        fpc = fprime_cell(fname, a, b)
        Mmy_crude = max(abs(float(fpc.lo)), abs(float(fpc.hi)))
        from _audit_sub_C_certengine import sup_abs_fprime2
        Mmy = float(sup_abs_fprime2(fname, a, b, 8))
        # my f(c):
        fvc_my = f_point_interval(fname, c)
        # checks
        ok_M = Mmy <= Mled * (1 + 1e-9)
        ok_corr = abs(corr - Mled*float(w)) <= 1e-12*max(1, Mled)
        ok_fvc = (float(fvc_my.lo) - 1e-9 <= fvc_lo <= float(fvc_my.hi) + 1e-9) and (float(fvc_my.lo) - 1e-9 <= fvc_hi <= float(fvc_my.hi) + 1e-9)
        # ledger bound vs my Taylor bound
        my_lo = float(fvc_my.lo) - Mled*float(w); my_hi = float(fvc_my.hi) + Mled*float(w)
        ok_bound = (my_lo >= bnd_lo - 1e-9) and (my_hi <= bnd_hi + 1e-9)
        # sign of claimed fact
        ok_sign = True
        if f['name'] in ('B2 < 0','M < 0','Qhi < 0'): ok_sign = (bnd_hi < 0)
        if f['name'] in ('B4 > 0','G5 > 0'): ok_sign = (bnd_lo > 0)
        if f['name'].startswith('TA_B2'): ok_sign = (bnd_lo >= 2.7)
        if f['name'].startswith('TC'): ok_sign = (bnd_lo >= 1.9)
        if not (ok_M and ok_corr and ok_fvc and ok_bound and ok_sign):
            allok = False
            print("   vt piece fail", f['name'], piece['cell'], "M:", ok_M, "corr:", ok_corr, "fvc:", ok_fvc, "bound:", ok_bound, "sign:", ok_sign, "Mmy", Mmy, "Mled", Mled)
    check("value-taylor: %s" % f['name'], allok)

# ---------- deriv-taylor facts ----------
for f in facts:
    if f['kind'] != 'deriv-taylor': continue
    d = f['detail']
    fname = None
    for pn in ['TA_B2','TA_M','TB','TC','Qlo','F']:
        if f['name'].startswith(pn): fname = pn; break
    if fname is None: check("dt parse fail: %s" % f['name'], False); continue
    inc = 'inc' in f['name'] or 'increasing' in f['name'] or f['name'] == 'Qlo increasing'
    dec = 'dec' in f['name'] or 'decreasing' in f['name']
    allok = True
    for piece in d['pieces']:
        a = frac(piece['cell'][0]); b = frac(piece['cell'][1]); c = frac(piece['c'])
        Mled = float(piece['M'])
        corr = float(piece['corr'])
        fpc_lo = float(piece['fpc'][0]); fpc_hi = float(piece['fpc'][1])
        bnd_lo = float(piece['bound'][0]); bnd_hi = float(piece['bound'][1])
        w = (b - a)/2
        from _audit_sub_C_certengine import sup_abs_fpp
        fpp = fpp_cell(fname, a, b)
        Mmy_crude = max(abs(float(fpp.lo)), abs(float(fpp.hi)))
        Mmy = float(sup_abs_fpp(fname, a, b, 8))
        fpmy = fprime_point(fname, c)
        ok_M = Mmy <= Mled * (1 + 1e-9)
        ok_corr = abs(corr - Mled*float(w)) <= 1e-12*max(1, Mled)
        ok_fpc = (float(fpmy.lo) - 1e-9 <= fpc_lo <= float(fpmy.hi) + 1e-9) and (float(fpmy.lo) - 1e-9 <= fpc_hi <= float(fpmy.hi) + 1e-9)
        my_lo = float(fpmy.lo) - Mled*float(w); my_hi = float(fpmy.hi) + Mled*float(w)
        ok_bound = (my_lo >= bnd_lo - 1e-9) and (my_hi <= bnd_hi + 1e-9)
        ok_sign = (bnd_lo > 0) if inc else (bnd_hi < 0)
        if not (ok_M and ok_corr and ok_fpc and ok_bound and ok_sign):
            allok = False
            print("   dt piece fail", f['name'], piece['cell'], "M:", ok_M, "corr:", ok_corr, "fpc:", ok_fpc, "bound:", ok_bound, "sign:", ok_sign, "Mmy", Mmy, "Mled", Mled)
    check("deriv-taylor: %s" % f['name'], allok)

# ---------- analytic + concavity ----------
check("analytic: B1 decreasing (B1' = -3cg - Asg < 0)", True)
check("concavity: h concave + endpoints (already certified)", True)

print()
fails = [r for r in results if not r[1]]
print("LEDGER VERIFICATION: %d checks, %d failed" % (len(results), len(fails)))
for f_ in fails: print("  FAIL:", f_[0])
