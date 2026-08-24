import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

def make_matrix(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1)
    n=len(ns)
    M=np.zeros((n,n),dtype=complex)
    for i,nn in enumerate(ns):
        M[i,i]=-nu*(k*k+nn*nn)
        for m in [N,-N]:
            j=np.where(ns==nn-m)[0]
            if len(j):
                M[i,j[0]] += -1j*k*(A/2)
    return M, ns

for A in [10]:
    M,ns=make_matrix(1,A,3,0.2,200)
    f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1.0
    def rhs(t,f): return M@f
    sol=solve_ivp(rhs,[0,20],f0,t_eval=np.linspace(0,20,31),method='RK45',rtol=1e-8,atol=1e-12)
    for tt in [0,0.5,1,2,5,10,20]:
        i=np.argmin(abs(sol.t-tt))
        f=sol.y[:,i]
        E=np.sum(np.abs(f)**2); F=np.sum(np.abs(f)**2/(1+ns**2)); n2=np.sum(np.abs(f)**2*ns**2)
        print('t',sol.t[i],'E',E,'F',F,'Q',np.sqrt(F/E),'n2mean',n2/E)
