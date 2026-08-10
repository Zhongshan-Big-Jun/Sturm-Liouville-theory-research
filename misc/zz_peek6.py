import pickle, sympy as sp
with open('misc/t3_symbols5.pkl','rb') as fh:
    d = pickle.load(fh)
for k in ['G','Gc','Gx','u','P']:
    e = d[k]
    e = sp.cancel(e)
    print('==== %s ====' % k)
    print(e)
    print()
