import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data
from _gapn2_jacobian_analytic import eigen_data
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,R,mode in [(2,4,'sup'),(3,4,'sup'),(2,100,'sup'),(3,10,'sup')]:
 rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; edges=np.array(tab[key]['edges']); w=np.diff(np.concatenate([[0],edges,[1]])); z0=rc.widths_to_z(w); zs=symmetric_root(rc,z0); sd=sector_data(rc,zs,N=200); ed=eigen_data(rc,zs)
 print('\n===',n,mode,'R',R,'===')
 for nm in ['Ko','Ke']:
  A=np.array(sd[nm]); d=np.array(sd['d']); print(nm,'mineig',np.linalg.eigvalsh(A)[0],'dmin',d.min(),'dmax',d.max())
 # reconstruct u and M? use d/u^2 maybe
 u=ed['u_n'][:n]; print('u',np.round(u,6)); print('d/u2',np.round(d/u**2,6))
