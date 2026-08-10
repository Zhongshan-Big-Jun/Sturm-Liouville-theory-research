# -*- coding: utf-8 -*-
"""H3 v65: verify trap self-consistency inequalities for all j in [3, 10^5].
u,v trap [1,U]; w trap even [Lw,1], odd [1,U]. Both parities, c in {1,3,10}."""
import math
def coeffs_f(c, j, par):
    lam = 4.0/c
    if par=='e':
        Pm=8.0*c*j*j-4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j-3)+4.0*c*j*(2*j-3)
        Rm=4.0*j*(j-2)*(2*j-3)*(2*j-5); Tm=4.0*j*(4*j-5)
    else:
        Pm=8.0*c*j*j+4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j+1)+4.0*c*j*(2*j-1)
        Rm=4.0*j*(j-2)*(2*j-1)*(2*j-3); Tm=4.0*j*(4*j-3)
    a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else 0.0
    return a1,a2,a3,lam,Tm

def f(L,U,a1,a2,a3,which):
    if which=='min': return a1 + a2/U + a3/(L*U)
    else: return a1 + a2/L + a3/(L*U)

for par in ('e','o'):
    for c in (1.0,3.0,10.0):
        U=1.05; Lw=0.98
        ok_u_lo=ok_u_hi=ok_v_lo=ok_v_hi=True
        ok_w_lo=ok_w_hi=True
        worst=dict()
        for j in range(3,100001):
            a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
            mu_min=f(1.0,U,a1,a2,a3,'min'); mu_max=f(1.0,U,a1,a2,a3,'max')
            if mu_min<1.0: ok_u_lo=False
            if mu_max>U: ok_u_hi=False
            # v has positive source (tiny); lower needs f>=1 (source helps), upper needs f + s/v <= U
            # w even trap [Lw,1]: min f(Lw,1)=a1+a2/1+a3/(Lw*1); max f(1,Lw)=a1+a2/Lw+a3/(Lw*1)
            if par=='e':
                wmin=f(Lw,1.0,a1,a2,a3,'min'); wmax=f(1.0,Lw,a1,a2,a3,'max')
                if wmin<Lw: ok_w_lo=False
                if wmax>1.0: ok_w_hi=False
            else:
                wmin=f(1.0,U,a1,a2,a3,'min'); wmax=f(1.0,U,a1,a2,a3,'max')
                if wmin<1.0: ok_w_lo=False
                if wmax>U: ok_w_hi=False
        print("par=%s c=%-4g: u/v trap [1,%.2f]: lo_ok=%s hi_ok=%s | w trap: lo_ok=%s hi_ok=%s"
              %(par,c,U,ok_u_lo,ok_u_hi,ok_w_lo,ok_w_hi))
