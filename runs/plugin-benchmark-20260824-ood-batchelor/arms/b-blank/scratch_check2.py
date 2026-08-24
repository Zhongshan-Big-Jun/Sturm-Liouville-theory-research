import numpy as np
from scipy.linalg import eig

M,ns=np.ones((1,1)), np.array([0])  # placeholder
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
Amat=v
B=np.linalg.inv(v)
f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1
c=B@f0
for tt in [1,5,10,20]:
    f=Amat@(np.exp(w*tt)*c)
    E=np.sum(np.abs(f)**2); F=np.sum(np.abs(f)**2/(1+ns**2)); n2=np.sum(np.abs(f)**2*ns**2)
    print('tt',tt,'E',E,'Q',np.sqrt(F/E),'n2',n2/E)
# Also dominate terms contributions
tt=20
ind=np.argsort(-w.real)
print('index top real')
for q in range(5):
    i=ind[q]; print(q,w[i], 'c',abs(c[i]),'F/E eigen',np.sqrt(np.sum(np.abs(v[:,i])**2/(1+ns**2))/np.sum(np.abs(v[:,i])**2)))
