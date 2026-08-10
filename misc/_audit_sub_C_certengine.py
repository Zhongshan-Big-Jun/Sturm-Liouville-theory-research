# _audit_sub_C_certengine.py - INDEPENDENT exact-rational interval certificate engine
from fractions import Fraction as F
import json, math
import sympy as sp

class I:
    __slots__ = ('lo','hi')
    def __init__(self, lo, hi):
        self.lo, self.hi = F(lo), F(hi)
        assert self.lo <= self.hi, (self.lo, self.hi)
    def __repr__(self): return "[%s,%s]" % (self.lo, self.hi)
def pint(v): return I(F(v), F(v))
def add(a,b): return I(a.lo+b.lo, a.hi+b.hi)
def sub(a,b): return I(a.lo-b.hi, a.hi-b.lo)
def mul(a,b):
    vals = (a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi)
    return I(min(vals), max(vals))
def div(a,b):
    assert b.lo > 0 or b.hi < 0
    vals = (a.lo/b.lo, a.lo/b.hi, a.hi/b.lo, a.hi/b.hi)
    return I(min(vals), max(vals))
def ipow(a, n):
    assert n >= 0 and isinstance(n, int)
    if n == 0: return pint(1)
    if n % 2 == 0:
        return I(min(a.lo**n, a.hi**n), max(a.lo**n, a.hi**n))
    return I(a.lo**n, a.hi**n)
def iabs(a):
    if a.lo >= 0: return I(a.lo, a.hi)
    if a.hi <= 0: return I(-a.hi, -a.lo)
    return I(F(0), max(abs(a.lo), abs(a.hi)))

def _sin_cos_env(x):
    s_terms = [F((-1)**k)*x**(2*k+1)/math.factorial(2*k+1) for k in range(14)]
    c_terms = [F((-1)**k)*x**(2*k)/math.factorial(2*k) for k in range(14)]
    S11 = sum(s_terms[:12]); S12 = sum(s_terms[:13])
    C11 = sum(c_terms[:12]); C12 = sum(c_terms[:13])
    return I(min(S11,S12), max(S11,S12)), I(min(C11,C12), max(C11,C12))

def _arctan_series_env(x):
    terms = [F((-1)**k)*x**(2*k+1)/F(2*k+1) for k in range(24)]
    A21 = sum(terms[:22]); A22 = sum(terms[:23])
    return I(min(A21,A22), max(A21,A22))

_pi_cache = None
def _pi_env():
    global _pi_cache
    if _pi_cache is None:
        a = _arctan_series_env(F(1,5)); b = _arctan_series_env(F(1,239))
        _pi_cache = sub(mul(pint(16), a), mul(pint(4), b))
    return _pi_cache

def arctan_env(x):
    assert x > 0
    if x <= 1: return _arctan_series_env(x)
    return sub(div(_pi_env(), pint(2)), _arctan_series_env(F(1)/x))

def sqrt_env(r):
    assert r >= 0
    if r == 0: return pint(0)
    p, q = r.numerator, r.denominator
    n = math.isqrt(p*q)
    return I(F(n,q), F(n+1,q))

def sin_env(x): return _sin_cos_env(x)[0]
def cos_env(x): return _sin_cos_env(x)[1]
def tan_env(x): return div(sin_env(x), cos_env(x))

def arctan_env_interval(vi):
    assert vi.lo > 0 and vi.hi <= 1
    lo = _arctan_series_env(vi.lo).lo
    hi = _arctan_series_env(vi.hi).hi
    return I(lo, hi)

def tau_env_at(x):
    t = tan_env(x)
    v = div(pint(1), mul(pint(2), t))
    return sub(div(_pi_env(), pint(2)), arctan_env_interval(v))

def cell_env(a, b):
    sa, ca = _sin_cos_env(a); sb, cb = _sin_cos_env(b)
    sg = I(sa.lo, sb.hi)
    cg = I(cb.lo, ca.hi)
    pi_i = _pi_env()
    A = I(pi_i.lo - b, pi_i.hi - a)
    D = I(sqrt_env(F(1)+3*sa.lo**2).lo, sqrt_env(F(1)+3*sb.hi**2).hi)
    ta = tau_env_at(a); tb = tau_env_at(b)
    tau = I(ta.lo, tb.hi)
    return {'sg': sg, 'cg': cg, 'A': A, 'D': D, 'tau': tau}

def point_env(g0):
    sg, cg = _sin_cos_env(g0)
    pi_i = _pi_env()
    A = I(pi_i.lo - g0, pi_i.hi - g0)
    D = I(sqrt_env(F(1)+3*sg.lo**2).lo, sqrt_env(F(1)+3*sg.hi**2).hi)
    tau = tau_env_at(g0)
    return {'sg': sg, 'cg': cg, 'A': A, 'D': D, 'tau': tau}

A, sg, cg, tau, D = sp.symbols('A sg cg tau D', positive=True)
mm = sp.Rational(791,2500)
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
Mf = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.simplify(B5 - A*B4)
z = sp.Symbol('z')
Q = 4*A**2*z**2 - A*B7*z + 6*cg**2*sg**2
Qlo = sp.simplify(Q.subs(z, cg**2/D**2))
Qhi = sp.simplify(Q.subs(z, cg**2))
Ff = tau**2*cg*sg**2
TA_B2 = 4*A**2*sg**2*cg**4*(-B2)/D**4   # B2 < 0 certified => |B2| = -B2
TA_M = 4*A**2*sg**2*cg**4*(-Mf)/D**4   # M < 0 certified => |M| = -M
TB = 2*A**3*sg**2*tau*cg**5/D**5
TC = mm*G5*A*sg*cg**2
FUNCS = {'B1':B1,'B2':B2,'M':Mf,'B4':B4,'G5':G5,'Qlo':Qlo,'Qhi':Qhi,'F':Ff,'TA_B2':TA_B2,'TA_M':TA_M,'TB':TB,'TC':TC}

dA = sp.Integer(-1)
dsg = cg; dcg = -sg; dtau = 2/D**2; dD = 3*sg*cg/D

def diff1(expr):
    return sp.expand(sp.diff(expr, A)*dA + sp.diff(expr, sg)*dsg + sp.diff(expr, cg)*dcg
                     + sp.diff(expr, tau)*dtau + sp.diff(expr, D)*dD)
def diff2(expr):
    e1 = sp.diff(expr, A)*dA + sp.diff(expr, sg)*dsg + sp.diff(expr, cg)*dcg + sp.diff(expr, tau)*dtau + sp.diff(expr, D)*dD
    return sp.expand(sp.diff(e1, A)*dA + sp.diff(e1, sg)*dsg + sp.diff(e1, cg)*dcg + sp.diff(e1, tau)*dtau + sp.diff(e1, D)*dD)

def evali(expr, env):
    if expr.is_Number: return pint(F(expr))
    if expr == A: return env['A']
    if expr == sg: return env['sg']
    if expr == cg: return env['cg']
    if expr == tau: return env['tau']
    if expr == D: return env['D']
    if expr.is_Symbol: raise ValueError("unknown symbol %s" % expr)
    if expr.func == sp.Add:
        r = pint(0)
        for a in expr.args: r = add(r, evali(a, env))
        return r
    if expr.func == sp.Mul:
        r = pint(1)
        for a in expr.args: r = mul(r, evali(a, env))
        return r
    if expr.func == sp.Pow:
        base = expr.args[0]; e = expr.args[1]
        if e.is_Integer and e > 0: return ipow(evali(base, env), int(e))
        if e.is_Integer and e < 0: return div(pint(1), ipow(evali(base, env), int(-e)))
        raise ValueError("pow", expr)
    if expr.func == sp.Abs:
        return iabs(evali(expr.args[0], env))
    if expr.func == sp.sign:
        v = evali(expr.args[0], env)
        if v.hi < 0: return pint(-1)
        if v.lo > 0: return pint(1)
        raise ValueError('sign of straddling interval')
    raise ValueError("func %s" % expr.func)

def f_point_interval(fname, g0):
    env = point_env(g0)
    return evali(FUNCS[fname], env)

def fprime_cell(fname, a, b):
    env = cell_env(a, b)
    return evali(diff1(FUNCS[fname]), env)

def fprime_point(fname, g0):
    env = point_env(g0)
    return evali(diff1(FUNCS[fname]), env)

def fpp_cell(fname, a, b):
    env = cell_env(a, b)
    return evali(diff2(FUNCS[fname]), env)

def sup_abs_fprime2(fname, a, b, nsub=8):
    best = F(0)
    w = (b - a)/nsub
    for i in range(nsub):
        aa = a + w*i
        bb = a + w*(i+1)
        c = (aa+bb)/2
        fp_c = fprime_point(fname, c)
        fpp = fpp_cell(fname, aa, bb)
        M2 = max(abs(fpp.lo), abs(fpp.hi))
        # f'(g) in fp_c +- M2*w/2
        lo = fp_c.lo - M2*w/2
        hi = fp_c.hi + M2*w/2
        best = max(best, abs(lo), abs(hi))
    return best

def sup_abs_fpp(fname, a, b, nsub=8):
    best = F(0)
    w = (b - a)/nsub
    for i in range(nsub):
        aa = a + w*i
        bb = a + w*(i+1)
        c = (aa+bb)/2
        fpp_c = evali(diff2(FUNCS[fname]), point_env(c))
        fppp = evali(diff2(diff1(FUNCS[fname])), cell_env(aa, bb))
        M3 = max(abs(fppp.lo), abs(fppp.hi))
        lo = fpp_c.lo - M3*w/2
        hi = fpp_c.hi + M3*w/2
        best = max(best, abs(lo), abs(hi))
    return best

print("engine v2 ready")
