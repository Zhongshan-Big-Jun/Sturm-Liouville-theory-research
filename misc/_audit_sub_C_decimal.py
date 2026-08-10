# _audit_sub_C_decimal.py — Decimal directed-rounding point-fact verification (second engine)
from decimal import Decimal as D, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
import json

getcontext().prec = 120
FLOOR = ROUND_FLOOR; CEIL = ROUND_CEILING

def dfloor(x): return x
class Itv:
    __slots__ = ('lo','hi')
    def __init__(self, lo, hi):
        self.lo = D(lo); self.hi = D(hi)
        assert self.lo <= self.hi
    def __repr__(self): return "[%s,%s]" % (self.lo, self.hi)

def add(a,b):
    c = getcontext(); c.rounding = FLOOR; lo = a.lo + b.lo
    c.rounding = CEIL; hi = a.hi + b.hi
    return Itv(lo, hi)
def sub(a,b):
    c = getcontext(); c.rounding = FLOOR; lo = a.lo - b.hi
    c.rounding = CEIL; hi = a.hi - b.lo
    return Itv(lo, hi)
def mul(a,b):
    c = getcontext()
    vals = []
    for (x,y) in [(a.lo,b.lo),(a.lo,b.hi),(a.hi,b.lo),(a.hi,b.hi)]:
        c.rounding = FLOOR; vals.append(x*y)
    c.rounding = CEIL
    vals2 = []
    for (x,y) in [(a.lo,b.lo),(a.lo,b.hi),(a.hi,b.lo),(a.hi,b.hi)]:
        c.rounding = CEIL; vals2.append(x*y)
    return Itv(min(vals), max(vals2))
def div(a,b):
    assert not (b.lo <= 0 <= b.hi)
    c = getcontext()
    c.rounding = FLOOR
    lo1 = a.lo / b.hi
    c.rounding = CEIL
    hi1 = a.hi / b.lo
    return Itv(lo1, hi1)
def ipow(a, n):
    n = int(n); assert n >= 0
    if n == 0: return Itv(1,1)
    if n % 2 == 0:
        c = getcontext(); c.rounding = FLOOR
        lo = min(a.lo**n, a.hi**n)
        c.rounding = CEIL
        hi = max(a.lo**n, a.hi**n)
        return Itv(lo, hi)
    c = getcontext(); c.rounding = FLOOR
    lo = a.lo**n
    c.rounding = CEIL
    hi = a.hi**n
    return Itv(lo, hi)

def _series_bracket(terms):
    # terms: list of Decimal (already computed with directed rounding to be safe we compute each twice)
    S = []
    acc = D(0)
    for t in terms:
        acc = acc + t
        S.append(acc)
    return S

def _sin_env(x):
    # x interval with lo,hi in [0.655,1.0472]
    out = []
    for xv, rnd in ((x.lo, FLOOR), (x.hi, CEIL)):
        getcontext().rounding = rnd
        x2 = xv*xv
        term = xv; S = [term]
        for k in range(1, 40):
            term = term * x2 / D((2*k)*(2*k+1))
            S.append(S[-1] + term if k % 2 == 0 else S[-1] - term)
        out.append(S)
    loS = out[0]; hiS = out[1]
    # bracketing: sin x between consecutive partial sums (alternating, decreasing)
    lo = min(loS[38], loS[39]); hi = max(hiS[38], hiS[39])
    return Itv(lo, hi)

def _cos_env(x):
    out = []
    for xv, rnd in ((x.lo, FLOOR), (x.hi, CEIL)):
        getcontext().rounding = rnd
        x2 = xv*xv
        term = D(1); S = [term]
        for k in range(1, 40):
            term = term * x2 / D((2*k-1)*(2*k))
            S.append(S[-1] - term if k % 2 == 1 else S[-1] + term)
        out.append(S)
    loS = out[0]; hiS = out[1]
    lo = min(loS[38], loS[39]); hi = max(hiS[38], hiS[39])
    return Itv(lo, hi)

def _atan_series(x):
    # x in (0,1)
    out = []
    for xv, rnd in ((x.lo, FLOOR), (x.hi, CEIL)):
        getcontext().rounding = rnd
        x2 = xv*xv
        term = xv; S = [term]
        for k in range(1, 80):
            term = term * x2
            S.append(S[-1] + term/D(2*k+1) if k % 2 == 0 else S[-1] - term/D(2*k+1))
        out.append(S)
    lo = min(out[0][78], out[0][79]); hi = max(out[1][78], out[1][79])
    return Itv(lo, hi)

def _pi_env():
    a5 = _atan_series(Itv(D(1)/D(5), D(1)/D(5)))
    a239 = _atan_series(Itv(D(1)/D(239), D(1)/D(239)))
    return sub(mul(Itv(16,16), a5), mul(Itv(4,4), a239))

PI = _pi_env()

def _sqrt_env(r):
    c = getcontext(); c.rounding = FLOOR
    lo = r.lo.sqrt()
    c.rounding = CEIL
    hi = r.hi.sqrt()
    return Itv(lo, hi)

def point_env(g0):
    g = Itv(D(g0.numerator)/D(g0.denominator), D(g0.numerator)/D(g0.denominator))
    sg = _sin_env(g); cg = _cos_env(g)
    A = sub(PI, g)
    Dv = _sqrt_env(add(Itv(1,1), mul(Itv(3,3), mul(sg,sg))))
    tanv = div(sg, cg)
    t2 = mul(Itv(2,2), tanv)
    inv = div(Itv(1,1), t2)
    at = _atan_series(inv)
    tau = sub(div(PI, Itv(2,2)), at)
    return {'sg':sg,'cg':cg,'A':A,'D':Dv,'tau':tau}

def evalf(expr, env):
    # expr: string name
    A = env['A']; sg = env['sg']; cg = env['cg']; tau = env['tau']; Dv = env['D']
    if expr == 'B1': return sub(mul(A,cg), mul(Itv(2,2),sg))
    if expr == 'B2':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg)
        return sub(add(sub(mul(Itv(4,4),mul(A2,c2)), A2), mul(Itv(6,6),s2)), mul(Itv(12,12),mul(mul(A,cg),sg)))
    if expr == 'M':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg)
        return sub(add(sub(mul(Itv(2,2),mul(A2,c2)), A2), mul(Itv(6,6),s2)), mul(Itv(8,8),mul(mul(A,cg),sg)))
    if expr == 'B4':
        c2 = mul(cg,cg); s2 = mul(sg,sg)
        return sub(add(mul(Itv(7,7),mul(A,c2)), sub(Itv(0,0), mul(A,s2))), mul(Itv(4,4),mul(cg,sg)))
    if expr == 'G5':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg)
        B5 = add(add(sub(mul(A2,c2), mul(A2,s2)), mul(Itv(2,2),A2)), sub(mul(Itv(12,12),mul(mul(A,cg),sg)), mul(Itv(12,12),s2)))
        B4 = sub(add(mul(Itv(7,7),mul(A,c2)), sub(Itv(0,0), mul(A,s2))), mul(Itv(4,4),mul(cg,sg)))
        return sub(B5, mul(A,B4))
    if expr == 'Qlo':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg); D2 = mul(Dv,Dv)
        B7 = add(mul(Itv(3,3),mul(A,c2)), add(mul(A,s2), mul(Itv(8,8),mul(cg,sg))))
        z = div(c2, D2)
        return add(sub(mul(Itv(4,4),mul(A2,mul(z,z))), mul(mul(A,B7),z)), mul(Itv(6,6),mul(c2,s2)))
    if expr == 'Qhi':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg)
        B7 = add(mul(Itv(3,3),mul(A,c2)), add(mul(A,s2), mul(Itv(8,8),mul(cg,sg))))
        z = c2
        return add(sub(mul(Itv(4,4),mul(A2,mul(z,z))), mul(mul(A,B7),z)), mul(Itv(6,6),mul(c2,s2)))
    if expr == 'F':
        # F = tau^2 * cg * sg^2  (tau = pi/2 - arctan(1/(2 tan g)) = atan(2 tan g))
        return mul(mul(tau, tau), mul(cg, mul(sg,sg)))
    if expr == 'TA_B2':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg); D2 = mul(Dv,Dv); D4 = mul(D2,D2)
        B2 = evalf('B2', env)
        # B2 < 0 certified -> |B2| = -B2
        nb2 = sub(Itv(0,0), B2)
        return div(mul(mul(mul(Itv(4,4),mul(A2,s2)), mul(c2,c2)), nb2), D4)
    if expr == 'TA_M':
        A2 = mul(A,A); c2 = mul(cg,cg); s2 = mul(sg,sg); D2 = mul(Dv,Dv); D4 = mul(D2,D2)
        Mf = evalf('M', env)
        nm = sub(Itv(0,0), Mf)
        return div(mul(mul(mul(Itv(4,4),mul(A2,s2)), mul(c2,c2)), nm), D4)
    if expr == 'TB':
        A3 = mul(mul(A,A),A); c5 = mul(c2:=mul(cg,cg), mul(c2,cg)); s2 = mul(sg,sg)
        D5 = mul(mul(Dv,Dv), mul(mul(Dv,Dv), Dv))
        num = mul(mul(mul(Itv(2,2),A3), s2), mul(tau, c5))
        return div(num, D5)
    if expr == 'TC':
        A2 = mul(A,A); c2 = mul(cg,cg)
        G5 = evalf('G5', env)
        return mul(mul(Itv(D(791)/D(2500), D(791)/D(2500)), mul(G5, A)), mul(sg, c2))
    if expr == 'tau': return tau
    if expr == 'h':
        return mul(mul(g0v(), sg), cg)
    raise ValueError(expr)

def g0v(): return Itv(D(0),D(0))  # placeholder, unused

ledger = json.load(open(r'F:\LaTeX\BVE research\misc\e1_cert_ledger.json', encoding='utf-8'))
facts = ledger['facts']
pt = [f for f in facts if f['kind'] == 'point']
fails = 0; n = 0
for f in pt:
    d = f['detail']
    g = F(d['point'])
    target = F(d['target'])
    cmp_ = d['cmp']
    name = f['name']
    fname = None
    for pn in ['TA_B2','TA_M','Qlo','B1','B2','M','B4','G5','F','TB','TC','tau','h']:
        if name.startswith(pn): fname = pn; break
    if fname is None:
        print('FAIL parse', name); fails += 1; continue
    env = point_env(g)
    if fname == 'h':
        gi = Itv(D(g.numerator)/D(g.denominator), D(g.numerator)/D(g.denominator))
        val = mul(mul(gi, env['sg']), env['cg'])
    elif fname == 'tau':
        val = env['tau']
    else:
        val = evalf(fname, env)
    ok = (val.lo >= D(target.numerator)/D(target.denominator)) if cmp_=='ge' else (val.hi <= D(target.numerator)/D(target.denominator))
    n += 1
    if not ok:
        fails += 1
        print('FAIL', name, 'interval', val, 'target', target)
    else:
        print('PASS', name, 'margin-ok, interval', val)
print('decimal point facts: %d checked, %d failed' % (n, fails))
