# _audit_sub_C_final.py — edge checks: f' positivity, containment, E1/E3 usage scan
import mpmath as mp
mp.mp.dps = 40
import io, re

# 1) f'(x) = (8x/pi^2)(3+3x cotx - x^2 csc^2x) on [pi/3, 1.1220]
def fprime(x):
    return (8*x/mp.pi**2)*(3 + 3*x/mp.tan(x) - x**2/mp.sin(x)**2)
mn = mp.mpf(0)
for i in range(2001):
    x = mp.pi/3 + (mp.mpf('1.1220') - mp.pi/3)*mp.mpf(i)/2000
    mn = min(mn, fprime(x))
print("min f'(x) on [pi/3, 1.1220]:", mn, " > 0:", mn > 0)

# 2) alpha1 max over Q is alpha1(1,2/5) = 5pi/14; check alpha1(1,2/5)=5pi/14 and c1 range
x1 = 5*mp.pi/14
c1_at = mp.atan(1/mp.tan(x1))/x1
print("c1(5pi/14, 1) =", c1_at, " (should be 0.4)")
# c1(x,q) for q in [1,2], x in [0.841, 1.1220]: range check
def c1(x, q): return mp.atan(1/(q*mp.tan(x)))/x
lo = mp.mpf(10); hi = mp.mpf(-10)
for qv in [mp.mpf(1), mp.mpf(1.5), mp.mpf(2)]:
    for i in range(201):
        x = mp.mpf('0.841') + (mp.mpf('1.1220')-mp.mpf('0.841'))*mp.mpf(i)/200
        v = c1(x, qv)
        lo = min(lo, v); hi = max(hi, v)
print("c1 range on [0.841,1.1220]x[1,2]:", (lo, hi))
# alpha1(q,c) for (q,c) in Q
def alpha1(q, c):
    f = lambda x: c*x - mp.atan(1/(q*mp.tan(x)))
    return mp.findroot(f, mp.mpf('1.0'))
mn_a = mp.mpf(10); mx_a = mp.mpf(-10)
for qv in [mp.mpf(1), mp.mpf(1.5), mp.mpf(2)]:
    for cv in [mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.5')]:
        a = alpha1(qv, cv)
        mn_a = min(mn_a, a); mx_a = max(mx_a, a)
print("alpha1 over Q grid:", (mn_a, mx_a), " max <= 5pi/14:", mx_a <= 5*mp.pi/14)

# 3) E1/E3 scan of back half (lines 559-end): find E3/numeric-scan mentions and check they are not premises
lines = io.open(r'F:\LaTeX\BVE research\docs\SL_gap_n1_O3a_phase_rigidity_proof.tex', encoding='utf-8').read().split('\n')
for i, ln in enumerate(lines[558:], 559):
    if 'E3' in ln or '扫描' in ln or '侦察' in ln or '交叉检验' in ln or 'mpmath' in ln:
        print(i, ':', ln.strip()[:200])
