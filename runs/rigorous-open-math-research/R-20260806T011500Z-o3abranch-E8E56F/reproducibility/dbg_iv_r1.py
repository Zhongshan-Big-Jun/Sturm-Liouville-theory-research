import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0])

a, R = 0.57364, 1500.0
b = 0.5830
# float value
def R1f(b):
    rs = roots2_robust(a, b, R)
    s1, s2 = rs[0], rs[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*(np.sin(s1*a)/s1)**2/n1 - s2*s2*(np.sin(s2*a)/s2)**2/n2
print("float R1:", R1f(b))
# interval: replicate R1_iv
s1f_, s2f_ = roots2_robust(a, b, R)
print("float roots:", s1f_, s2f_)
s1l, s1h = sec_root_bracket(s1f_ - 1e-6, s1f_ + 1e-6, mpf(repr(a)), mpf(repr(b)), mpf(repr(R)))
s2l, s2h = sec_root_bracket(s2f_ - 1e-6, s2f_ + 1e-6, mpf(repr(a)), mpf(repr(b)), mpf(repr(R)))
print("s1 enclosure:", s1l, s1h)
print("s2 enclosure:", s2l, s2h)
s1 = iv.mpf([s1l, s1h]); s2 = iv.mpf([s2l, s2h])
v = ir1(pt(mpf(repr(a))), pt(mpf(repr(b))), pt(mpf(repr(R))), s1, s2)
print("interval R1:", v)
# inspect components
n1 = inorm(s1, pt(mpf(repr(a))), pt(mpf(repr(b))), pt(mpf(repr(R))))
n2 = inorm(s2, pt(mpf(repr(a))), pt(mpf(repr(b))), pt(mpf(repr(R))))
print("n1:", n1)
print("n2:", n2)
y1a = iy1a(s1, pt(mpf(repr(a))), pt(mpf(repr(b))), pt(mpf(repr(R))))
y2a = iy1a(s2, pt(mpf(repr(a))), pt(mpf(repr(b))), pt(mpf(repr(R))))
print("y1a^2/n1:", y1a**2/n1)
print("y2a^2/n2:", y2a**2/n2)
