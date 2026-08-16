# -*- coding: utf-8 -*-
import sys
import json
import numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data

tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
for n, R, mode in [(2, 4, 'sup'), (2, 4, 'inf'), (3, 4, 'sup'), (3, 4, 'inf')]:
    rc = Recon(n, R, mode)
    key = f'n{n}_{mode.upper()}'
    edges = np.array(tab[key]['edges'])
    w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
    z0 = rc.widths_to_z(w)
    zs = symmetric_root(rc, z0)
    sd = sector_data(rc, zs, N=200)
    print(f'\n=== n={n} {mode} R={R} ===')
    for name in ['d', 'Ko', 'Ho', 'Eo', 'Ke', 'He', 'Ee']:
        print(f'{name} =\n', np.round(np.array(sd[name]), 6))
