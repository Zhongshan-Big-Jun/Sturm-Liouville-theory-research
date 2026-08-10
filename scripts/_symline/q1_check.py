# -*- coding: utf-8 -*-
# Verify q=1 closed form of Fe and Fep by finite difference. EVIDENCE.
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def Fe_q1(c):
    # closed form: x = pi/(2(1+c)), Fe = x^2 sin^2 x (1-16 cos^2 x)/(1+c)
    x = pi/(2*(1+c))
    return x**2*mp.sin(x)**2*(1-16*mp.cos(x)**2)/(1+c)

def Fep_q1_num(c, h=mp.mpf('1e-6')):
    return (Fe_q1(c+h)-Fe_q1(c-h))/(2*h)

def Fep_q1_closed(c):
    x = pi/(2*(1+c))
    hb = 3*(1-16*mp.cos(x)**2) + 2*x*mp.cot(x)*(17-16*mp.cos(x)**2)
    return -x**2*mp.sin(x)**2*hb/(1+c)**2

print('c       Fe(c)         Fep_fd       Fep_closed   ratio')
for k in range(0, 11):
    c = mp.mpf(k)/20
    print('%s  %s  %s  %s' % (mp.nstr(c,4), mp.nstr(Fe_q1(c),12), mp.nstr(Fep_q1_num(c),12), mp.nstr(Fep_q1_closed(c),12)))
