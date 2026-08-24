import numpy as np, time
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply

def make_sparse(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1)
    n=len(ns)
    main=-nu*(k*k+ns*ns)
    data=[main]
    offsets=[0]
    # offdiag: M[i, i+N?] mapping ns[j]=ns[i]-N -> shift -N in index
    # (U*f)_n includes f_{n-N} at index i-N, so offdiag -N
    for m in [N,-N]:
        val=-1j*k*(A/2)
        # let's compute diagonal offset: output n, input j=n-m. offset = j - i = -m.
        off=-m
        if abs(off)<2*nmax+1:
            # number entries = n-|off|
            data.append(np.full(n-abs(off), val))
            offsets.append(off)
    M=diags(data,offsets,shape=(n,n),format='csr',dtype=complex)
    return M, ns

nmax=150
M,ns=make_sparse(1,10,3,0.2,nmax)
f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1.0
for tt in [0,0.5,1,2,5,10,20]:
    f=expm_multiply(M*tt, f0)
    E=np.sum(np.abs(f)**2); F=np.sum(np.abs(f)**2/(1+ns**2)); n2=np.sum(np.abs(f)**2*ns**2)
    print('t',tt,'E',E,'F',F,'Q',np.sqrt(F/E),'n2mean',n2/E)
