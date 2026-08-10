# -*- coding: utf-8 -*-
"""H3 v45: search for explicit rational moment sequences solving the homogeneous
even recurrence.  Try nu_n = 1/((n+a)...) families."""
from fractions import Fraction as F

C = F(3)

def P_e(j,c): return F(8)*c*j*j - F(4)*c*j + c*c*F(j,j-1)
def Q_e(j,c): return F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
def R_e(j,c): return F(4)*j*(j-2)*(2*j-3)*(2*j-5)

def resid(seq):
    c=C; N=len(seq)
    mx=F(0)
    for j in range(3,N):
        d = c*c*seq[j] - (P_e(j,c)*seq[j-1] - Q_e(j,c)*seq[j-2] + R_e(j,c)*seq[j-3])
        mx = max(mx, abs(d))
    return mx

print("=== single-pole ansatz nu_n = 1/(n+a), exact search a in [-6,7] ===")
hits=0
for den in range(1,13):
    for num in range(-6*den, 7*den+1):
        a=F(num,den)
        if a<=0: continue
        seq=[F(1)/F(n+a) for n in range(30)]
        r=resid(seq)
        if r==0:
            print("  EXACT: a=%s" % a); hits+=1
        elif r < F(1,10**6):
            print("  small resid %.2e at a=%s" % (float(r), a))
print("exact hits:", hits)

print()
print("=== two-pole ansatz nu_n = 1/((n+a)(n+b)) ===")
hits=0
for den in range(1,9):
    for na in range(-4*den, 5*den+1):
        for nb in range(-4*den, 5*den+1):
            a=F(na,den); b=F(nb,den)
            if a<=0 or b<=0: continue
            seq=[F(1)/(F(n+a)*F(n+b)) for n in range(30)]
            r=resid(seq)
            if r==0:
                print("  EXACT: a=%s b=%s" % (a,b)); hits+=1
            elif r < F(1,10**6):
                print("  small resid %.2e at a=%s b=%s" % (float(r), a, b))
print("exact hits:", hits)

print()
print("=== three-pole ansatz nu_n = 1/((n+a)(n+b)(n+c)) ===")
hits=0
for a in (1,2,3):
    for b in (1,2,3):
        for c in (1,2,3):
            seq=[F(1)/(F(n+a)*F(n+b)*F(n+c)) for n in range(30)]
            r=resid(seq)
            if r==0:
                print("  EXACT: a=%s b=%s c=%s" % (a,b,c)); hits+=1
            elif r < F(1,10**6):
                print("  small resid %.2e at a=%s b=%s c=%s" % (float(r), a, b, c))
print("exact hits:", hits)
