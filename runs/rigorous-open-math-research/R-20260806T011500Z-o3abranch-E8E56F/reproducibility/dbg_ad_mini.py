import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220
ns = {}
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0], ns)
IAD = ns['IAD']; pt = ns['pt']

a = pt(mpf('0.57364')); s = pt(mpf('0.528586829'))
# AD with vars (a, s)
a_ = IAD(a, [iv.mpf(1), iv.mpf(0)])
s_ = IAD(s, [iv.mpf(0), iv.mpf(1)])
p = s_ * a_
print("p = s*a : v=%s g=[%s, %s]" % (p.v, p.g[0], p.g[1]))
print("expected da: s=%s, ds: a=%s" % (s, a))
q = p.sin()
import mpmath as mpm
print("sin(sa) : v=%s g=[%s, %s]" % (q.v, q.g[0], q.g[1]))
print("expected: v=%s, da=%s, ds=%s" % (mpm.sin(s*a), s*mpm.cos(s*a), a*mpm.cos(s*a)))
# test a plain product with a float constant on the left
c = iv.mpf('2.5')
r = c * s_
print("c*s: v=%s g=%s" % (r.v, r.g))
r2 = s_ * c
print("s*c: v=%s g=%s" % (r2.v, r2.g))
