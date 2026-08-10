# -*- coding: utf-8 -*-
# Structure of G2 >= 0 region for q<1: monotonicity, IN machinery. EVIDENCE.
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def alpha1(c,q):
    return mp.findroot(lambda A: mp.atan(1/(q*mp.tan(A))) - c*A, (mp.mpf('1e-30'), pi/2-mp.mpf('1e-30')), solver='bisect')
def alpha2(c,q):
    def O(x):
        if x < pi/2: return pi - mp.atan(q*mp.tan(x))
        elif x == pi/2: return pi/2
        else: return mp.atan(-q*mp.tan(x))
    return mp.findroot(lambda A: O(A) - c*A, (mp.mpf('1e-30'), pi-mp.mpf('1e-30')), solver='bisect')
def Phi(x,q): return mp.cos(x)**2 + q**2*mp.sin(x)**2
def Gval(x,c,q):
    Ph = Phi(x,q); D = q + c*Ph
    return -Ph*(3+2*x*mp.cot(x))/D + 2*c*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def G2(c,q): return Gval(alpha2(c,q),c,q)

q0 = mp.sqrt(mp.mpf(2)/3)
h = mp.mpf('1e-4')

print('=== dG2/dc on (0,0.40] (want < 0 => G2 decreasing, min at c=0.40) ===')
for c0 in ['0.05','0.1','0.2','0.3','0.35','0.38','0.40']:
    cc = mp.mpf(c0)
    d = (G2(cc+h,q0)-G2(cc-h,q0))/(2*h)
    print('  q=q0 c=%s: dG2/dc=%s' % (c0, mp.nstr(d,8)))

print('=== G2(c,q) at c=0.40 for q grid ===')
for qs in ['0.8165','0.85','0.9','0.95','1.0']:
    print('  q=%s: G2(0.40)=%s' % (qs, mp.nstr(G2(mp.mpf('0.40'),mp.mpf(qs)),8)))

print('=== IN machinery: M2 = dIN/dw for q<1 (want <0 => IN decreasing in w) ===')
# w = q tan gamma, c = arctan(w)/A, A = pi - arctan(w/q); IN = (q^2+w^2)A(2Aq-3w+2 arctan w) - 3wq(1+w^2) arctan w
def IN(q,w):
    A = pi - mp.atan(w/q)
    t = mp.atan(w)
    return (q**2+w**2)*A*(2*A*q-3*w+2*t) - 3*w*q*(1+w**2)*t
def M2(q,w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + t*(4*A*w-5*q-9*q*w**2)
# w range for c in (0,0.5], q in [q0,1]: w = q tan gamma, gamma in (0, ~1.105); w = tan(cA) <= tan(0.5*pi)~inf? At c=1/2: w = q tan(gamma), gamma=arccos(q/(q+1))... 
# c=0.5: w = tan(c*alpha2)=tan(alpha2/2) = tan((pi-x)/2) = cot(x/2), x=arccos(q/(q+1)) -> w = cot(x/2)
# at q=q0: x=1.1046, w=cot(0.5523)=1.599; at q=1: x=pi/3, w=cot(pi/6)=sqrt3=1.732
# c=0.40: w smaller
print('  M2 at (q,w) samples:')
for qs in ['0.8165','0.9','1.0']:
    qq = mp.mpf(qs)
    for w0 in ['0.5','1.0','1.5','1.7']:
        ww = mp.mpf(w0)
        print('    q=%s w=%s: M2=%s' % (qs,w0,mp.nstr(M2(qq,ww),8)))
