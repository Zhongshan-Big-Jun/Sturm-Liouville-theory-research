# -*- coding: utf-8 -*-
"""Session 54 (gap b): structural identities + exhaustive good-root search.
EVIDENCE only - no theorem claims.
"""
import numpy as np
from scipy.optimize import brentq, least_squares
from _well_rigid_verify import well_secular_vec

def eigs_fast(a,b,R,k=2,N=900):
    m=np.sqrt(R); smax=2+k*np.pi*m+4
    sp_=np.linspace(1e-9,smax,N)
    d=well_secular_vec(sp_,a,b,R)
    sg=np.signbit(d[1:])!=np.signbit(d[:-1])
    idx=np.nonzero(sg)[0]
    out=[]
    for i in idx[:k]:
        lo,hi=sp_[i],sp_[i+1]
        out.append(brentq(lambda z: well_secular_vec(z,a,b,R),lo,hi,xtol=1e-13,rtol=1e-13)**2)
    return np.sort(out)[:k]

def norm_closed(a,b,R,s):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    W=lambda t: np.sin(t)**2 + m*m*np.cos(t)**2
    X0=np.sin(A)/m; Y0=np.cos(A)
    nL=a/(2*s*s) - np.sin(2*A)/(4*m*s**3)
    nM=(1/s**3)*(W(A)*psi/(2*m*m) + (X0**2-Y0**2)*np.sin(2*psi)/4 + X0*Y0*np.sin(psi)**2)
    C2=W(A)/W(B)
    nR=C2*((1-b)/(2*s*s) - np.sin(2*B)/(4*m*s**3))
    return nL+nM+nR

def phases(a,b,R):
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=np.sqrt(R)
    A=m*s1*a; psi=s1*(b-a); B=m*s1*(1-b)
    return dict(lam1=lam1,lam2=lam2,s1=s1,s2=s2,tau=tau,A=A,B=B,psi=psi,m=m)

def Xb(A,psi,m):
    return np.cos(psi)*np.sin(A)/m + np.sin(psi)*np.cos(A)

def well_data(a,b,R):
    p=phases(a,b,R)
    A,psi,B,m,tau=p['A'],p['psi'],p['B'],p['m'],p['tau']
    n1=norm_closed(a,b,R,p['s1']); n2=norm_closed(a,b,R,p['s2'])
    W=lambda t: np.sin(t)**2 + m*m*np.cos(t)**2
    # residuals: R1 = f(a) = [sin^2(tau A)/n2 - sin^2 A/n1]/m^2 ; R2 = f(b)
    R1=(np.sin(tau*A)**2/n2 - np.sin(A)**2/n1)/m**2
    C1sq=W(A)/W(B); C2sq=W(tau*A)/W(tau*B)
    R2=(C2sq*np.sin(tau*B)**2/n2 - C1sq*np.sin(B)**2/n1)/m**2
    Xb1=Xb(A,psi,m); Xb2=Xb(tau*A,tau*psi,m)
    h_a=np.sin(tau*A)/(tau*np.sin(A))
    h_b=Xb2/(tau*Xb1)
    E=np.log((np.sin(tau*A)**2/W(tau*A))/(np.sin(A)**2/W(A))) - np.log((np.sin(tau*B)**2/W(tau*B))/(np.sin(B)**2/W(B)))
    N1=n2/n1 - np.sin(tau*A)**2/np.sin(A)**2
    return dict(p=p,n1=n1,n2=n2,R1=R1,R2=R2,h_a=h_a,h_b=h_b,E=E,N1=N1,
                Xb1=Xb1,Xb2=Xb2,sg_cons=(h_a>0 and h_b<0))

# ---------- (I1)/(I2) verification on interior samples ----------
print("== identity checks (interior points, R=4) ==")
for (a,b) in [(0.2,0.8),(0.3,0.7),(0.3826,0.6174),(0.35,0.65),(0.25,0.62),(0.4,0.55)]:
    d=well_data(a,b,4.0)
    p=d['p']
    lhs1=(p['lam2']*np.sin(p['tau']*p['A'])**2/(p['m']**2*d['n2'])) - (p['lam1']*np.sin(p['A'])**2/(p['m']**2*d['n1']))
    print(f"  (a,b)=({a},{b}): R1={d['R1']:+.4e} R2={d['R2']:+.4e} N1={d['N1']:+.4e} E={d['E']:+.4e}")
    print(f"      h(a)+h(b)={d['h_a']+d['h_b']:+.4e}  Xb2/Xb1+sin(tA)/sinA={d['Xb2']/d['Xb1']+np.sin(p['tau']*p['A'])/np.sin(p['A']):+.4e}")
    print(f"      sign-consistent={d['sg_cons']} h_a={d['h_a']:+.4f} h_b={d['h_b']:+.4f}")

# ---------- exhaustive critical-point search ----------
print()
print("== good-root search (R1=R2=0, least_squares multi-seed) ==")
def crit_pts(R, seeds):
    def res(ab):
        aa,bb=ab
        d=well_data(aa,bb,R)
        return [d['R1'],d['R2']]
    found=[]
    for (a0,b0) in seeds:
        try:
            sol=least_squares(res,[a0,b0],bounds=([2e-3,2e-3],[0.998,0.998]),xtol=1e-12,ftol=1e-12,max_nfev=400)
            a,b=sol.x
            if not (0.002<a<b<0.998): continue
            d=well_data(a,b,R)
            cost=max(abs(d['R1']),abs(d['R2']))
            if cost>1e-8: continue
            key=(round(a,4),round(b,4))
            if not any(abs(key[0]-f[0])<2e-3 and abs(key[1]-f[1])<2e-3 for f in found):
                found.append((a,b))
        except Exception:
            pass
    return found

seeds=[(v,w) for v in np.linspace(0.05,0.7,14) for w in np.linspace(v+0.05,0.95,14)]
for R in [1.6,2.0,2.5,3.0,4.0]:
    pts=crit_pts(R,seeds)
    print(f"R={R}: {len(pts)} critical points (interior, |R1|,|R2|<1e-8):")
    for (a,b) in pts:
        d=well_data(a,b,R)
        p=d['p']
        print(f"    (a,b)=({a:.6f},{b:.6f}) a+b={a+b:.6f} sg={d['sg_cons']} D={p['lam2']-p['lam1']:.6f} |A-B|={abs(p['A']-p['B']):.2e} N1={d['N1']:+.3e} tau={p['tau']:.4f}")
