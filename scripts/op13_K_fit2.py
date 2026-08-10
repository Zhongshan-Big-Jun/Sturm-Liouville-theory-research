# -*- coding: utf-8 -*-
"""#13(i): nonlinear fit for K(c)."""
import mpmath as mp
mp.mp.dps = 200

# K values from previous accurate run
K = {0.25: '0.73154726835733880385', 0.5: '0.71367319815073017723', 1: '0.67957045711382317795',
     2: '0.6173718425675460176', 3: '0.5622227356633425386', 4: '0.51314537669298043946',
     5: '0.46932456588215753496', 10: '0.30846328308935785349', 20: '0.1470974039275153688',
     100: '0.0025222183132672753432'}
K = {c: mp.mpf(v) for c, v in K.items()}
cs = sorted(K)

# candidate fits on log K
import numpy as np
from scipy.optimize import curve_fit
cs_arr = np.array(cs, dtype=float)
Ks_arr = np.array([float(K[c]) for c in cs], dtype=float)

# 1) K = A*(c+1)^-p * exp(-q*c)
def f1(c, A, p, q): return A*(c+1)**(-p)*np.exp(-q*c)
try:
    p0 = [1, 2, 0.05]
    popt, pcov = curve_fit(f1, cs_arr, Ks_arr, p0=p0, maxfev=100000)
    print("fit1 K=A(c+1)^-p e^-qc:", popt, "rel err:", np.max(np.abs(f1(cs_arr,*popt)/Ks_arr-1)))
except Exception as e: print("fit1 failed", e)

# 2) K = A * exp(-q c) * c^-p
def f2(c, A, p, q): return A*c**(-p)*np.exp(-q*c)
try:
    popt2, _ = curve_fit(f2, cs_arr, Ks_arr, p0=[1, 0.5, 0.05], maxfev=100000)
    print("fit2 K=A c^-p e^-qc:", popt2, "rel err:", np.max(np.abs(f2(cs_arr,*popt2)/Ks_arr-1)))
except Exception as e: print("fit2 failed", e)

# 3) K = A/(c+1)^p
def f3(c, A, p): return A*(c+1)**(-p)
try:
    popt3, _ = curve_fit(f3, cs_arr, Ks_arr, p0=[1, 2], maxfev=100000)
    print("fit3 K=A/(c+1)^p:", popt3, "rel err:", np.max(np.abs(f3(cs_arr,*popt3)/Ks_arr-1)))
except Exception as e: print("fit3 failed", e)

# 4) K = A * e^{-qc} * (c+1)^-p with A fixed by c=1
print()
print("ratio table: K(c)/K(1)")
for c in cs:
    print(f"  c={c}: {mp.nstr(K[c]/K[1],10)}")

# test K(c) = K(1)*exp(-phi(c)): compute -ln(K/K1)
print()
print("c    -ln(K(c)/K(1))     /c      /(c-1)")
for c in cs:
    if c == 1: continue
    v = -mp.log(K[c]/K[1])
    print(f"  {c:>4}: {mp.nstr(v,8)}   {mp.nstr(v/c,8)}   {mp.nstr(v/(c-1),8)}")
