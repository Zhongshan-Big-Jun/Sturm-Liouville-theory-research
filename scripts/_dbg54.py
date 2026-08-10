import numpy as np
from _gapb_s54b import eigs_cont, norm_closed, res_ab
for R,ab in [(1.6,(0.407075,0.592925)),(2.0,(0.401037,0.598963)),(4.0,(0.382598,0.617402))]:
    a,b=ab
    lam=eigs_cont(a,b,R,(None,None))
    print("R",R,"lam",lam)
    print("res",res_ab(np.array([a,b]),R))
# probe grid residuals near symmetric line for R=1.6
a,b=0.407075,0.592925
for da in [-0.03,-0.015,0,0.015,0.03]:
    for db in [-0.03,-0.015,0,0.015,0.03]:
        r=res_ab(np.array([a+da,b+db]),1.6)
        if max(abs(r))<0.3: print("  near",da,db,r)
