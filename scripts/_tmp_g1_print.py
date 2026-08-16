import sys, json, numpy as np
sys.path.insert(0,'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
for n in [2,3]:
  rc=Recon(n,4,'sup')
  tab=json.load(open('scripts/op03_gap_table.json'))
  e0=np.array(tab['n%d_SUP'%n]['edges'])
  w0=np.diff(np.concatenate([[0],e0,[1]]))
  z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0)
  sd=sector_data(rc,zs,N=200)
  print('\n=== n',n,'SUP R4 ===')
  for name in ['d','Ke','Ko','He','Ho','Ee','Eo']:
    A=np.array(sd[name]); print(name,'\n',np.array2string(A,precision=6))
    if name in ['Ke','Ko','He','Ho','Ee','Eo']:
      print(' ev',np.linalg.eigvalsh(A))
