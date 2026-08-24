import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply

def make_sparse(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1); n=len(ns)
    main=-nu*(k*k+ns*ns)
    data=[main]; offsets=[0]
    for m in [N,-N]:
        off=-m
        if abs(off)<2*nmax+1:
            data.append(np.full(n-abs(off), -1j*k*(A/2)))
            offsets.append(off)
    return diags(data,offsets,shape=(n,n),format='csr',dtype=complex),ns

for (A,N,nu) in [(10,3,0.2),(10,10,0.2),(10,30,0.2),(100,30,0.2),(100,100,0.2),(10,100,0.2),(1,100,0.01)]:
    nmax=min(500,max(2*N+50, 300))
    M,ns=make_sparse(1,A,N,nu,nmax)
    f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1.0
    bestG=-1; bestT=0; bestQ=10
    for tt in np.linspace(0,5,101):
        f=expm_multiply(M*tt,f0)
        E=np.sum(np.abs(f)**2)
        G=np.sum((1+ns**2)*np.abs(f)**2) # include k=1? use n2
        n2=np.sum(ns**2*np.abs(f)**2)
        F=np.sum(np.abs(f)**2/(1+ns**2))
        Q=np.sqrt(F/E) if E>0 else 1
        if n2/E>bestG: bestG=n2/E; bestT=tt
        if Q<bestQ: bestQ=Q
    print((A,N,nu), 'best n2/E',bestG,'at',bestT,'minQ',bestQ)
