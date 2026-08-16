import sys,json,numpy as np
sys.path.insert(0,'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data
for n in [2,3,4]:
 rc=Recon(n,4,'sup')
 tab=json.load(open('scripts/op03_gap_table.json'))
 e0=np.array(tab['n%d_SUP'%n]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0)
 sd=sector_data(rc,zs,N=200)
 for sect in ['e','o']:
  d=np.diag(np.array(sd['d'])); H=np.array(sd['H'+sect]); E=np.array(sd['E'+sect]); A=d+H
  print(n,sect,'ev(d+H)',np.linalg.eigvalsh(A),'min',np.linalg.eigvalsh(A)[0],'ev(H)',np.linalg.eigvalsh(H))
