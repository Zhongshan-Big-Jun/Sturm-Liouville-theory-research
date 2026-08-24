import numpy as np
from scipy.linalg import eig

def make_dense(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1); n=len(ns)
    M=np.zeros((n,n),dtype=complex)
    for i,nn in enumerate(ns):
        M[i,i]=-nu*(k*k+nn*nn)
        for m in [N,-N]:
            j=np.where(ns==nn-m)[0]
            if len(j): M[i,j[0]] += -1j*k*(A/2)
    return M,ns
M,ns=make_dense(1,10,3,0.2,100)
w,v=np.linalg.eig(M)
B=np.linalg.inv(v)
f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1
c=B@f0
# sort by c magnitude
for i in np.argsort(-np.abs(c))[:20]:
    f=v[:,i]; Q=np.sqrt(np.sum(np.abs(f)**2/(1+ns**2))/np.sum(np.abs(f)**2))
    print('real',w[i].real,'imag',w[i].imag,'c',abs(c[i]),'Q',Q)
