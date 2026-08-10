import pickle
with open('misc/t3_symbols5.pkl','rb') as fh:
    d = pickle.load(fh)
print(type(d))
if isinstance(d, dict):
    for k in d:
        v = d[k]
        print('KEY', k, type(v), str(v)[:200])
elif isinstance(d, (list, tuple)):
    print(len(d))
    for v in d[:5]:
        print(type(v), str(v)[:300])
