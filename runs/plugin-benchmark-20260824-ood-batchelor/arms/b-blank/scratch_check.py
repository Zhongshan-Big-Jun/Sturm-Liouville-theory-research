import numpy as np
from scipy.linalg import eig
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply

def make_dense(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1); n=len(ns)
    M=np.zeros((n,n),dtype=complex)
    for i,nn in enumerate(ns):
        M[i,i]=-nu*(k*k+nn*nn)
        for m in [N,-N]:
            j=np.where(ns==nn-m)[0]
            if len(j): M[i,j[0]] += -1j*k*(A/2)
    return M,ns
def make_sparse(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1); n=len(ns)
    main=-nu*(k*k+ns*ns); data=[main]; offsets=[0]
    for m in [N,-N]:
        off=-m
        data.append(np.full(n-abs(off), -1j*k*(A/2)))
        offsets.append(off)
    return diags(data,offsets,shape=(n,n),format='csr',dtype=complex),ns

# Compare M dense and sparse for small
Md,ns=make_dense(1,10,3,0.2,10)
Ms,ns2=make_sparse(1,10,3,0.2,10)
print('mismatch', np.abs(Md-Ms.toarray()).max())
# spectral nmax=100
M,ns=make_dense(1,10,3,0.2,100)
w,v=np.linalg.eig(M)
idx=np.argsort(-w.real)
for q in range(2):
    e=w[idx[q]]; f=v[:,idx[q]]; f=f/np.linalg.norm(f)
    print('dense eig',q,'real',e.real,'imag',e.imag,'Q',np.sqrt(np.sum(np.abs(f)**2/(1+ns**2))))
# sparse expm
Msp,ns=make_sparse(1,10,3,0.2,100)
f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1.
for tt in [5,10,20]:
    f=expm_multiply(Msp*tt,f0)
    E=np.sum(np.abs(f)**2); F=np.sum(np.abs(f)**2/(1+ns**2))
    print('expm',tt,'E',E,'Q',np.sqrt(F/E),'n2',np.sum(np.abs(f)**2*ns**2)/E)
