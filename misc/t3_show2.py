# -*- coding: utf-8 -*-
"""t3_show2: print dNJ/dt and P05 terms."""
import json
for name, path in [('dNJ/dt','misc/t3_dNJdt.json'), ('P05','misc/t3_P05.json')]:
    with open(path) as fh: r = json.load(fh)
    tm = sorted(zip(r['monoms'], r['coeffs']), key=lambda x: -int(x[1]))
    print('===== %s (%d terms, deg %d) =====' % (name, r['nterms'], r['deg']))
    if name == 'dNJ/dt':
        for m,c in tm:
            print('  %6d * A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (int(c),m[0],m[1],m[2],m[3],m[4],m[5]))
    else:
        for m,c in tm:
            print('  %9d * u^%d su^%d cu^%d' % (int(c),m[0],m[1],m[2]))
