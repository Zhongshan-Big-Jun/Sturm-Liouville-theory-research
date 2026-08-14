# -*- coding: utf-8 -*-
"""Audit inspect: dump P dict structure and the last rows of big.json."""
import pickle, json, sys

P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
print('P keys:')
for (name, m) in sorted(P.keys()):
    print('  (%s,%d) %s' % (name, m, str(P[(name, m)])))

print()
print('big.json structure:')
data = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
if isinstance(data, list):
    print('list of', len(data), 'rows')
    print('row[0]:', data[0])
    print('last row:', data[-1])
else:
    print(type(data), list(data.keys())[:20])
    r0 = data[list(data.keys())[0]]
    print('first value:', r0)
