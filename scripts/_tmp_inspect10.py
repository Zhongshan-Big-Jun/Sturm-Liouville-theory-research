import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data
from _gapn2_jacobian_analytic import eigen_data
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,R,mode in [(2,4,'sup'),(3,4,'sup'),(4,4,'sup'),(2,4,'inf'),(3,4,'inf')]:
 rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0); sd=sector_data(rc,zs,N=200); ed=eigen_data(rc,zs)
 print('\n===',n,mode,'===')
 for nm in ['Ko','Ke']:
  A=np.array(sd[nm]); D=np.diag(np.diag(A)); off=A-D; rho=np.max(np.abs(np.linalg.eigvals(np.linalg.solve(D,off)))) if np.all(np.diag(D)!=0) else np.inf
  print(nm,'rho(D^-1 off)',rho,'minabsdiag',np.min(np.abs(np.diag(D))))
 # congruence by u
 u=ed['u_n'][:n]; Dinv=1/np.abs(u)
 for nm in ['Ko','Ke']:
  A=np.array(sd[nm]); B=np.diag(Dinv)@A@np.diag(Dinv); DB=np.diag(np.diag(B)); offB=B-DB; rhoB=np.max(np.abs(np.linalg.eigvals(np.linalg.solve(DB,offB)))) if np.all(np.diag(DB)!=0) else np.inf
  print(nm,'B diag',np.round(np.diag(B),3),'rho',rhoB)
