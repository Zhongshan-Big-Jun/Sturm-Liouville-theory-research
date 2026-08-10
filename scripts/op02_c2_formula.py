# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 40
for R in (2.0, 4.0, 10.0, 100.0):
    s = mp.sqrt(R)
    Cp = (-1 + mp.sqrt(1+4*s*s))/(2*(s+1))
    y2f = mp.acos(Cp)
    # numeric y2 from balance script (R=4: 1.0233392882277; R=2: 1.1437177404024; R=10: 0.86445002376715; R=100: 0.52610013138361)
    ynum = {2.0: mp.mpf('1.1437177404024'), 4.0: mp.mpf('1.0233392882277'),
            10.0: mp.mpf('0.86445002376715'), 100.0: mp.mpf('0.52610013138361')}[R]
    print(f"R={R}: formula y2 = {mp.nstr(y2f, 16)}  numeric y2 = {mp.nstr(ynum, 16)}  diff = {mp.nstr(y2f-ynum, 3)}")
    print(f"     ratio by formula = {mp.nstr((mp.pi/y2f - 1)**2, 12)}")
