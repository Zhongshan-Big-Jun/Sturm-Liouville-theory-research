# -*- coding: utf-8 -*-
import sympy as sp, pickle
d = pickle.load(open("R1_partials_exprs.pkl","rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
for key in ("R1","R1_a","R1_b"):
    expr = sp.sympify(d[key])
    pows = set()
    for f in sp.preorder_traversal(expr):
        if f.is_Pow and not f.exp.is_Integer:
            pows.add((str(f.base), str(f.exp)))
    print(key, "non-integer powers:", pows)
