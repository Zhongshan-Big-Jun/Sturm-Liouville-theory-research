# -*- coding: utf-8 -*-
import mpmath as mp, random
mp.mp.dps = 60
iv = mp.iv
iv.dps = 50
random.seed(7)

def mk(a, b):
    return iv.mpf((str(a), str(b)))

fns = [
    ('sin', lambda x: iv.sin(x), lambda x: mp.sin(x)),
    ('cos', lambda x: iv.cos(x), lambda x: mp.cos(x)),
    ('tan', lambda x: iv.tan(x), lambda x: mp.tan(x)),
    ('atan2', lambda x: iv.atan2(x, iv.mpf(1)), lambda x: mp.atan(x)),
]
bad = 0; total = 0
for name, f, tf in fns:
    for _ in range(300):
        a = random.random()*1.3
        b = a + random.random()*0.05
        R = f(mk(a, b))
        for pt in (a, (a+b)/2, b, a+0.37*(b-a)):
            tv = tf(mp.mpf(str(pt)))
            total += 1
            if not (float(R.a) <= float(tv) <= float(R.b)):
                bad += 1
                print('VIOLATION', name, a, b, pt, R, tv)
    for _ in range(200):
        a = -1.2 + random.random()*2.4
        b = a + 0.03
        R = f(mk(a, b))
        for pt in (a, (a+b)/2, b):
            tv = tf(mp.mpf(str(pt)))
            total += 1
            if not (float(R.a) <= float(tv) <= float(R.b)):
                bad += 1
                print('NEG VIOLATION', name, a, b, pt, R, tv)
print('total %d, violations %d' % (total, bad))
# also check wide-interval enclosure of monotone fns
for name, f, tf in fns:
    R = f(mk(0.655, 1.0472))
    lo, hi = float(R.a), float(R.b)
    # sample true min/max at many points
    vals = [float(tf(mp.mpf(str(0.655 + i*0.3922/5000)))) for i in range(5001)]
    if min(vals) < lo - 1e-6 or max(vals) > hi + 1e-6:
        print('WIDE VIOLATION', name, lo, hi, min(vals), max(vals))
print('wide-interval monotone containment check done')
