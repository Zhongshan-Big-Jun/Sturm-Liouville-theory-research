import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220
ns = {}
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0], ns)
IAD = ns['IAD']; pt = ns['pt']

sa, sb_, ss, sR = mpf('0.57364'), mpf('0.5832744756851049'), mpf('0.528586829'), mpf('1500')
m = mp.sqrt(sR)
A = pt(sa); B = pt(sb_); Rm = pt(sR); S = pt(ss)
a3 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0)])
b3 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0)])
s3 = IAD(S, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])

# term-by-term
t1 = s3 * a3          # alpha
t2 = s3 * (1 - b3)  # beta
t3 = s3 * (b3 - a3) * Rm    # theta
ca, cta = t1.cos(), t1.sin()
cb, stb = t2.cos(), t2.sin()
ct, stt = t3.cos(), t3.sin()
print("alpha g:", t1.g)
print("beta  g:", t2.g)
print("theta g:", t3.g)
term1 = cb * ct * cta
term2 = stb * stt * cta * Rm
term3 = (cb * stt * ca) / Rm
term4 = stb * ct * ca
print("term1 v:", term1.v, "g:", term1.g)
print("term2 v:", term2.v, "g:", term2.g)
print("term3 v:", term3.v, "g:", term3.g)
print("term4 v:", term4.v, "g:", term4.g)
sec = term1 - term2 + term3 + term4
print("sec v:", sec.v, "g:", sec.g)
# hand chain rule (scalar, mp): d/ds
alpha = ss*sa; beta = ss*(1-sb_); theta = ss*m*(sb_-sa)
d_alpha = sa; d_beta = 1-sb_; d_theta = m*(sb_-sa)
sin_a, cos_a = mp.sin(alpha), mp.cos(alpha)
sin_b, cos_b = mp.sin(beta), mp.cos(beta)
sin_t, cos_t = mp.sin(theta), mp.cos(theta)
# sec = cos_b cos_t sin_a - m sin_b sin_t sin_a + (cos_b sin_t/m) cos_a + sin_b cos_t cos_a
dsec_ds = (cos_b*cos_t*cos_a*d_alpha - cos_b*sin_t*sin_a*d_theta
           - m*(cos_b*d_beta*sin_t*sin_a + sin_b*cos_t*d_theta*sin_a + sin_b*sin_t*cos_a*d_alpha)
           + (1/m)*((-sin_b*d_beta)*sin_t*cos_a + cos_b*cos_t*d_theta*cos_a - cos_b*sin_t*sin_a*d_alpha)
           + (cos_b*d_beta*cos_t*cos_a - sin_b*sin_t*d_theta*cos_a - sin_b*cos_t*sin_a*d_alpha))
print("hand d sec/ds:", dsec_ds)
print("hand d sec/da:")
d_alpha = ss; d_beta = 0; d_theta = -ss*m
dsec_da = (cos_b*cos_t*cos_a*d_alpha - cos_b*sin_t*sin_a*d_theta
           - m*(sin_b*sin_t*cos_a*d_alpha)
           + (1/m)*((-sin_b*d_beta)*sin_t*cos_a + cos_b*cos_t*d_theta*cos_a - cos_b*sin_t*sin_a*d_alpha)
           + (cos_b*d_beta*cos_t*cos_a - sin_b*sin_t*d_theta*cos_a - sin_b*cos_t*sin_a*d_alpha))
print(dsec_da)
