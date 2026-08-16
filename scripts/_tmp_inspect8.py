import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,R,mode in [(2,4,'sup'),(3,4,'sup'),(4,4,'sup'),(2,4,'inf'),(3,4,'inf')]:
 rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0); sd=sector_data(rc,zs,N=200)
 print('\n===',n,mode,'===')
 for nm in ['Ko','Ke']:
  A=np.array(sd[nm]); inv=np.linalg.inv(A)
  # print max off-band magnitude >2 bands
  print(nm,'bandwidth(offdiag>1e-8):')
  for d in range(1,n):
   vals=A[np.abs(np.arange(n)[:,None]-np.arange(n)[None,:])==d]
   if np.max(np.abs(vals))>1e-8: print('  dist',d,'max',np.max(np.abs(vals)))
  print(' inv')
  print(np.round(inv,5))
