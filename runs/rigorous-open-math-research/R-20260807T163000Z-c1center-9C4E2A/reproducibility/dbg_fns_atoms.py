# -*- coding: utf-8 -*-
import sympy as sp, pickle
d = pickle.load(open("R1_partials_exprs.pkl","rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
for key in ("R1","R1_a","R1_b"):
    expr = sp.sympify(d[key])
    fns = sorted({f.func.__name__ for f in sp.preorder_traversal(expr) if f.is_Function})
    print(key, "functions:", fns)
    if key == "R1_a":
        # check for division by zero-width or sqrt usage
        print("  has sqrt:", any(f.func == sp.sqrt for f in sp.preorder_traversal(expr)))
