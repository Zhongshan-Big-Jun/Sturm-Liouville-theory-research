import numpy as np

def fd_all(rho, N=2000, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    w, V = np.linalg.eigh(B)
    U = V[:, :k] / s[:, None]
    return w[:k], U

def build(c1,c2,R,N):
    rho = np.ones(N)
    rho[int(round(c1*N)):int(round(c2*N))] = R
    rho[int(round((1-c2)*N)):int(round((1-c1)*N))] = R
    return rho

N=2000; R=4.0
x = np.linspace(0,1,N)
# config A: fixed-point-like A on [0.249,0.374]U[0.626,0.751]
rhoA = build(0.249,0.374,R,N)
wA, UA = fd_all(rhoA, N, 4)
print("configA ratio lam3/lam2:", wA[2]/wA[1])
# config B: scan max A on [0.3974,0.48]U[0.52,0.6026]
rhoB = build(0.3974,0.48,R,N)
wB, UB = fd_all(rhoB, N, 4)
print("configB ratio lam3/lam2:", wB[2]/wB[1])
u2, u3 = UB[:,1], UB[:,2]
d = u2**2 - u3**2
# sign of d on A-regions of config B
m1 = (x>0.3974)&(x<0.48); m2=(x>0.52)&(x<0.6026)
print("sign(u2^2-u3^2) on A-region1:", np.sign(d[m1][:5]), "... mean d:", np.mean(d[m1]))
print("sign(u2^2-u3^2) on A-region2:", np.sign(d[m2][:5]), "... mean d:", np.mean(d[m2]))
# and on the a-regions
ma = (x>0.48)&(x<0.52); me = (x<0.3974)|(x>0.6026)
print("mean d on middle a-region:", np.mean(d[ma]), " on end a-regions:", np.mean(d[me]))
# crossings
cross = np.where(np.diff(np.sign(d))!=0)[0]
print("crossings of u2^2-u3^2:", np.round(x[cross],4))
