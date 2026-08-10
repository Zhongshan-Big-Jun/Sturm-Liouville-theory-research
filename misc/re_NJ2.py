# -*- coding: utf-8 -*-
import json
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
print('num terms:', len(monoms))
for c, m in sorted(zip(coeffs, monoms), key=lambda t: -t[0]):
    # m = (A_pow, t_pow, sg_pow, cg_pow, st_pow, ct_pow)
    print('%+d * A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c, m[0], m[1], m[2], m[3], m[4], m[5]))
