import sys,json,warnings
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
import numpy as np
import _gapn2_half_problem_probe as H
import mpmath as mp
mp.mp.dps=90
cases=[]
for rho,mu in [(1e-306,-np.finfo(float).max),(1e-305,-np.finfo(float).max),(1.,-np.finfo(float).max)]:
    try:
        b=[(1.,rho)]; t=H.half_spectrum(b,'D',4,return_table=True)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            val=H._spectral_full_green(b,mu,'D',.25,.25,4,spectrum=t)
        rr=mp.mpf(rho); mm=mp.mpf(mu); xx=mp.mpf('.25')
        exact=sum(2*mp.sin(k*mp.pi*xx)**2/(k*k*mp.pi**2-rr*mm) for k in range(1,5))
        cases.append(dict(rho=rho,mu=mu,eigenvalues=t.eigenvalues,computed=val,independent_finite_sum=str(exact),warnings=[str(w.message) for w in caught]))
    except Exception as e: cases.append(dict(rho=rho,error=type(e).__name__+': '+str(e)))
print(json.dumps(cases,indent=2))
