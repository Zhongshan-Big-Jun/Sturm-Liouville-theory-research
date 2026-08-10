# -*- coding: utf-8 -*-
"""t3_nj3: print all 23 terms of NJ."""
import json
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
tm = sorted(zip(r['monoms'], r['coeffs']), key=lambda x: -int(x[1]))
print('ALL %d TERMS:' % len(tm))
for m,c in tm:
    print('  %6d * A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (int(c),m[0],m[1],m[2],m[3],m[4],m[5]))
