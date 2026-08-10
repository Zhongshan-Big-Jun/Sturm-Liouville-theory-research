# -*- coding: utf-8 -*-
# Scan M2 = dIN/dw for q in (0,1], w>0. EVIDENCE.
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def M2(q,w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + t*(4*A*w-5*q-9*q*w**2)

print('=== M2 over grid ===')
for q0 in ['0.01','0.05','0.1','0.2','0.3','0.5','0.7','0.8165','0.9','1.0','2.0','5.0']:
    qq = mp.mpf(q0)
    mn = mp.mpf('1e99')
    for wk in range(1, 200):
        w = mp.mpf(wk)*mp.mpf('0.05')
        v = M2(qq,w)
        mn = min(mn,v)
    print('  q=%s: min M2 over w in (0,10) = %s' % (q0, mp.nstr(mn,8)))

# find M2 = 0 boundary (if any)
print('=== M2 sign near w=0 for small q ===')
for q0 in ['0.01','0.05','0.1','0.2']:
    qq = mp.mpf(q0)
    for w0 in ['0.001','0.01','0.1']:
        ww = mp.mpf(w0)
        print('  q=%s w=%s: M2=%s' % (q0,w0,mp.nstr(M2(qq,ww),8)))
