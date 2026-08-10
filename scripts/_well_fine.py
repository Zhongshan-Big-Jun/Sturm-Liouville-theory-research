# -*- coding: utf-8 -*-
"""Fine D(v) scan near v~0.361 for R=10 (E3)."""
import numpy as np
from _well_landscape2 import eigs_well

R = 10.0
vs = np.linspace(0.3590, 0.3630, 801)
Ds = np.array([eigs_well(v, 1-v, R)[1]-eigs_well(v, 1-v, R)[0] for v in vs])
# find all local minima/maxima
lm = [i for i in range(1, len(vs)-1) if Ds[i] < Ds[i-1] and Ds[i] < Ds[i+1]]
lx = [i for i in range(1, len(vs)-1) if Ds[i] > Ds[i-1] and Ds[i] > Ds[i+1]]
print(f"R={R}: local minima at v = {[round(vs[i],6) for i in lm]} with D = {[round(Ds[i],8) for i in lm]}")
print(f"        local maxima at v = {[round(vs[i],6) for i in lx]} with D = {[round(Ds[i],8) for i in lx]}")
# wider check
vs2 = np.linspace(0.001, 0.499, 4000)
Ds2 = np.array([eigs_well(v, 1-v, R)[1]-eigs_well(v, 1-v, R)[0] for v in vs2])
lm2 = [i for i in range(1, len(vs2)-1) if Ds2[i] < Ds2[i-1] and Ds2[i] < Ds2[i+1]]
print("  all local minima on (0,1/2):", [(round(vs2[i],5), round(Ds2[i],7)) for i in lm2])
# same for R=100 and R=25
for RR in [25.0, 100.0]:
    vs3 = np.linspace(0.001, 0.499, 4000)
    Ds3 = np.array([eigs_well(v, 1-v, RR)[1]-eigs_well(v, 1-v, RR)[0] for v in vs3])
    lm3 = [i for i in range(1, len(vs3)-1) if Ds3[i] < Ds3[i-1] and Ds3[i] < Ds3[i+1]]
    print(f"R={RR}: local minima:", [(round(vs3[i],5), round(Ds3[i],8)) for i in lm3])
