# -*- coding: utf-8 -*-
"""High-precision (mpmath 50-digit) spot checks of the STRICT observable
relations on the big.json last row, plus the seed-limit relations.
"""
import json
import mpmath as mp
mp.mp.dps = 50

data = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
R, uu, K, a, b = data[-1][0], data[-1][1], data[-1][2], data[-1][3], data[-1][4]
Dk_u7 = data[-1][5]
DR = data[-1][6]
Rf = mp.mpf(str(R)); uf = mp.mpf(str(uu)); Kf = mp.mpf(str(K))
Dk7 = mp.mpf(str(Dk_u7)); DRf = mp.mpf(str(DR))

# manager anchor u == R^{-1/6}
anchor = Rf**(-mp.mpf(1)/mp.mpf(6))
print('u vs R^{-1/6} diff:', mp.nstr(uf - anchor, 20))
print('abs rel err:', mp.nstr(abs(uf - anchor)/uf, 20))

# c(u) = Dk/u^5 = (Dk/u^7)*u^2
c = Dk7*uf*uf
print('c(u)=Dk/u^5 =', mp.nstr(c, 20))

# D*R = 2 K c + c^2 u^4
DR_check = 2*Kf*c + c**2*uf**4
print('2Kc + c^2 u^4 =', mp.nstr(DR_check, 20), ' vs data D*R =', mp.nstr(DRf, 20))
print('abs diff:', mp.nstr(abs(DR_check - DRf), 20))

# Dk/u^7 = c/u^2
print('(Dk/u^7) predicted = c/u^2 =', mp.nstr(c/uf**2, 20), ' vs data', mp.nstr(Dk7, 20))

# LIMIT quantities (EVIDENCE seed)
K0 = mp.mpf('3.4553'); C0 = mp.mpf('1.4741'); B0 = mp.mpf('0.2898'); a0f = mp.mpf('0.5788')
print()
print('2*K0*C0 =', mp.nstr(2*K0*C0, 20), ' (deliverable 10.18692)')
print('a0 = 2/K0 =', mp.nstr(2/K0, 20), ' vs fit a0=0.5788')
print('a0_fit*K0 =', mp.nstr(a0f*K0, 20), ' (vs 2)')
con = 1 + B0*K0/2 + 3*mp.pi/(2*K0) - K0**2/12
print('consistency C_cand (even-only) =', mp.nstr(con, 20), ' (deliverable 1.86956)')
print('hard-constant magnitude K0^3/2 =', mp.nstr(K0**3/2, 20))
print()
