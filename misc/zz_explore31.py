import mpmath as mp
mp.mp.dps = 30
# f(w) = 25 w^2/(4-3w)^2 - 13.8 w/(4-3w) + 6w(1-w), w in [0.25, 0.63]
def f(w):
    return 25*w*w/(4-3*w)**2 - 13.8*w/(4-3*w) + 6*w*(1-w)
mn = mp.mpf('1e30'); mx = mp.mpf('-1e30')
for i in range(2001):
    w = mp.mpf('0.25') + mp.mpf(i)*(mp.mpf('0.63')-mp.mpf('0.25'))/2000
    v = f(w)
    mn = min(mn, v); mx = max(mx, v)
print('f(w) on [0.25, 0.63]: [%.5f, %.5f]' % (mn, mx))
# better constants: 4A^2 <= 4*6.187=24.75, AB7 >= 13.8
def f2(w):
    return 24.75*w*w/(4-3*w)**2 - 13.8*w/(4-3*w) + 6*w*(1-w)
mn = mp.mpf('1e30'); mx = mp.mpf('-1e30')
for i in range(2001):
    w = mp.mpf('0.25') + mp.mpf(i)*(mp.mpf('0.63')-mp.mpf('0.25'))/2000
    v = f2(w)
    mn = min(mn, v); mx = max(mx, v)
print('f2(w): [%.5f, %.5f]' % (mn, mx))
# where does f2 peak?
best = (mp.mpf('-1e30'), None)
for i in range(20001):
    w = mp.mpf('0.25') + mp.mpf(i)*(mp.mpf('0.63')-mp.mpf('0.25'))/20000
    v = f2(w)
    if v > best[0]: best = (v, float(w))
print('f2 max %.5f at w=%.5f' % (best[0], best[1]))
