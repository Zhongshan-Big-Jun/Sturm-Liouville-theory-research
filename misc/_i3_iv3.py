# -*- coding: utf-8 -*-
"""Corrected iv evaluators (Gx fixed via sp.diff chain). Recount boxes for J1_2d>0, J2_2d<0."""
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 50

X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
Gx_s = sp.simplify(sp.diff(G, X))
Gc_s = sp.simplify(sp.diff(G, C))
xp_s = -X*Ph/D
Gp_s = sp.simplify(Gx_s*xp_s + Gc_s)
J_s = sp.simplify(G**2 + Gp_s)

# Generate Python code strings for G, Gx, Gc, J with mpmath.iv-friendly ops.
# Use sympy codegen printing with 'mpmath' via lambdify source? Simpler: use lambdify with
# a wrapper module that maps functions to iv versions.
import inspect
def iv_sin(x): return iv.sin(x)
def iv_cos(x): return iv.cos(x)
def iv_tan(x): return iv.tan(x)
def iv_pow(a,b): return a**b
mod = {'sin': iv_sin, 'cos': iv_cos, 'tan': iv_tan, 'atan': None, 'pi': iv.pi, 'sqrt': iv.sqrt}
# Build evaluators by evaluating the sympy expression tree symbolically on interval objects!
# Trick: use sp.lambdify with modules={'sin':..., ...} won't do atan; but J1_2d needs atan (in c).
# Approach: compose: c = iv_atan(...)/x is computed outside; then J_iv(x,c,q) with c an interval.
# For J_iv we need G, Gx, Gc evaluated with interval c. Use lambdify with mpmath module but
# ensure all ops are interval-safe by testing.
try:
    Jf = sp.lambdify((X,C,Q), J_s, modules='mpmath')
    x = iv.mpf([mp.mpf('0.9'), mp.mpf('1.0')]); c = iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')]); q = iv.mpf([mp.mpf(1), mp.mpf(2)])
    r = Jf(x,c,q)
    print("J iv works:", r)
except Exception as e:
    print("J iv fails:", e)
