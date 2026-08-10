# -*- coding: utf-8 -*-
import sympy as sp, pickle, time
d = pickle.load(open("s3_bounds.pkl","rb"))
expr = sp.sympify(d["sp3"])
print("orig size:", len(str(expr)))
t0 = time.time()
e2 = sp.trigsimp(expr)
print("trigsimp: %.1fs size %d" % (time.time()-t0, len(str(e2))))
t0 = time.time()
e3 = sp.factor(e2)
print("factor: %.1fs size %d" % (time.time()-t0, len(str(e3))))
t0 = time.time()
e4 = sp.cancel(e3)
print("cancel: %.1fs size %d" % (time.time()-t0, len(str(e4))))
import pickle
with open("sp3_simplified.pkl","wb") as fh:
    pickle.dump(str(e4), fh)
print("saved sp3_simplified.pkl")
