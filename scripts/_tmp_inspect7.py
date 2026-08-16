import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
rng=np.random.default_rng(0)
for n,R,mode in [(2,4,'sup'),(3,4,'sup'),(2,4,'inf'),(3,4,'inf')]:
 rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0); blocks=rc.blocks_from_z(zs); ed=eigen_data(rc,zs); lam_n=ed['lam_n']; lam_np1=ed['lam_np1']; x=ed['edges']; u=ed['u_n']; u2=ed['u_np1']; eps=ed['eps']; s=np.array([rc.pat[i+1]-rc.pat[i] for i in range(2*n)]); N=80; ss=roots_of(blocks,N+1); lam=ss**2
 y=rng.normal(size=2*n)
 print('\n===',n,mode,'===')
 for l in range(N+1):
  if l in (n-1,n): continue
  ul=eigfun(blocks,ss[l],x)
  U=np.sum(u*ul*y); Nl=np.sum(eps*u*ul*y); r=Nl/U if abs(U)>1e-12 else None
  # M = -sigma(R-1)c*U, N_l=-sigma(R-1)*Nl
  off_l=2*lam_np1**2*( -np.sum(s*u2*ul*y))**2/(lam[l]-lam_np1) - 2*lam_n**2*( -np.sum(s*u*ul*y))**2/(lam[l]-lam_n)
  # print only extreme r and off signs maybe
  if l<20: print(l,'r',None if r is None else round(r,3),'off',round(off_l,6))
