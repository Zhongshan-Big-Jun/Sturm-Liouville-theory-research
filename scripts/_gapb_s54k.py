# -*- coding: utf-8 -*-
"""Session 54k: check r_tau monotonicity on right branch with magnitudes; Psi~ shape. EVIDENCE."""
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def Psi(x,q):
    W=1+q*np.cos(x)**2
    return x/np.tan(x)+q*x*np.sin(x)*np.cos(x)/W

def check_right(R,tau):
    q=R-1
    xmid=np.pi/(tau+1)
    xs=np.linspace(xmid+1e-6, np.pi/tau-1e-6, 20001)
    d=np.array([Psi(tau*x,q)-Psi(x,q) for x in xs])
    # r_tau'(x) = (2/x) d ; monotone decreasing iff d<0
    viol=d>0
    print(f"R={R} tau={tau}: right branch x in ({xmid:.4f},{np.pi/tau:.4f}): max Psi-gap={d.max():+.3e}, min={d.min():+.3e}, violations={viol.sum()}/{len(d)}")
    if viol.sum():
        i=np.argmax(d); print(f"   worst at x={xs[i]:.4f} (tau*x={tau*xs[i]:.4f})")
    return d

# good root taus
good={1.52:None,1.6:1.8759,2.0:1.8247,3.0:1.7433,4.0:1.6941,10.0:1.5778,100.0:1.4667}
for R in [1.52,1.6,2.0,3.0,4.0,10.0,100.0]:
    if good[R] is None: continue
    check_right(R,good[R])
# tau scan for R=100 right branch
print()
print("R=100 right-branch violations vs tau:")
for tau in [1.2,1.3,1.4667,1.6,1.8,1.99]:
    d=check_right(100.0,tau)
