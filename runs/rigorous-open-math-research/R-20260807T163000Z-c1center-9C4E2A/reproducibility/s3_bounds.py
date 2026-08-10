# -*- coding: utf-8 -*-
"""s3_bounds.py - closed form of s_k'''(a,b,eps) via implicit differentiation of
F(s_k(eps), a, b, 1+eps) = 0 (NO trigsimp/expand - kept factored for speed).
Dumps to s3_bounds.pkl for interval certification of the Taylor remainder."""
import sympy as sp
import pickle, time
pi = sp.pi
s, a, b, R = sp.symbols("s a b R", positive=True)
t0 = time.time()
m = sp.sqrt(R); w = b - a
ca, sa = sp.cos(s*a), sp.sin(s*a)
cb, sb = sp.cos(s*(1-b)), sp.sin(s*(1-b))
ct, st = sp.cos(s*m*w), sp.sin(s*m*w)
F = cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
print("F built %.1fs" % (time.time()-t0), flush=True)
Fs = sp.diff(F, s); Fss = sp.diff(Fs, s); Fsss = sp.diff(Fss, s)
FR = sp.diff(F, R); FRR = sp.diff(FR, R); FRRR = sp.diff(FRR, R)
FsR = sp.diff(Fs, R); FsRR = sp.diff(FsR, R); FssR = sp.diff(Fss, R)
print("partials built %.1fs" % (time.time()-t0), flush=True)
# chain: s' = -FR/Fs ; s'' ; s'''
sp1 = -FR/Fs
sp2 = -(Fss*sp1**2 + 2*FsR*sp1 + FRR)/Fs
sp3 = -(Fsss*sp1**3 + 3*Fss*sp1*sp2 + 3*FssR*sp1**2 + 3*FsR*sp2 + 3*FsRR*sp1 + FRRR)/Fs
print("sp3 built %.1fs" % (time.time()-t0), flush=True)
out = {"Fs": str(Fs), "sp1": str(sp1), "sp2": str(sp2), "sp3": str(sp3),
       "Fss": str(Fss), "Fsss": str(Fsss), "FR": str(FR), "FRR": str(FRR), "FRRR": str(FRRR),
       "FsR": str(FsR), "FsRR": str(FsRR), "FssR": str(FssR)}
with open("s3_bounds.pkl", "wb") as fh:
    pickle.dump(out, fh)
print("saved s3_bounds.pkl", {k: len(v) for k, v in out.items()}, "%.1fs" % (time.time()-t0))
