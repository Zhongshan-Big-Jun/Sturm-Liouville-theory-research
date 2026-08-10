import mpmath as mp
mp.mp.dps = 50

def fprime(x):
    return (8*x/mp.pi**2)*(3 + 3*x/mp.tan(x) - x**2/mp.sin(x)**2)
mn = None
for i in range(5001):
    x = mp.pi/3 + (mp.mpf('1.1220') - mp.pi/3)*mp.mpf(i)/5000
    v = fprime(x)
    mn = v if mn is None else min(mn, v)
print("min f'(x) on [pi/3, 1.1220]:", mn)

# alpha1 max over Q
def alpha1(q, c):
    f = lambda x: c*x - mp.atan(1/(q*mp.tan(x)))
    return mp.findroot(f, mp.mpf('1.0'))
mx_a = None
for qv in [mp.mpf(1), mp.mpf(1.2), mp.mpf(1.5), mp.mpf(2)]:
    for cv in [mp.mpf('0.4'), mp.mpf('0.42'), mp.mpf('0.45'), mp.mpf('0.48'), mp.mpf('0.5')]:
        a = alpha1(qv, cv)
        mx_a = a if mx_a is None else max(mx_a, a)
print("max alpha1 on Q grid:", mx_a)
print("5pi/14 =", 5*mp.pi/14)
print("diff:", abs(mx_a - 5*mp.pi/14) < mp.mpf('1e-40'))
