import numpy as np
from scipy.integrate import quad

# first roots of tan mu = mu
def roots(N=5):
    out=[]
    for k in range(1,N+1):
        lo,hi=(k-0.5)*np.pi+0.1,(k+0.5)*np.pi-0.1
        for _ in range(80):
            mid=0.5*(lo+hi)
            if np.tan(mid)-mid>0: hi=mid
            else: lo=mid
        out.append(0.5*(lo+hi))
    return out

for mu in roots(4):
    v, err = quad(lambda x: x*np.sin(mu*x), -1, 1, limit=300)
    print(f"mu={mu:.6f}: (x, sin mu x) = {v:.3e}  (err {err:.1e})")
    v1, _ = quad(lambda x: x*np.sin(mu*x), 0, 1, limit=300)
    print(f"    int_0^1 x sin(mu x) = {v1:.6f},  sin(mu)={np.sin(mu):.6f}, cos(mu)={np.cos(mu):.6f}")
