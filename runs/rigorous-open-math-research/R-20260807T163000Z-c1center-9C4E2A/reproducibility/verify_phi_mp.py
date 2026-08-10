# -*- coding: utf-8 -*-
"""verify_phi_mp.py: mpmath 60-digit check of Phi-1 at select points for R=1e6."""
import mpmath as mp, json
mp.mp.dps = 60
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from c1trace_lib import a_fp, partials, R1R2

def sec_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR)
    return (mp.cos(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.sin(sv*aa)
            - mm*mp.sin(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))*mp.sin(sv*aa)
            + (mp.cos(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))/mm)*mp.cos(sv*aa)
            + mp.sin(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.cos(sv*aa))
def roots2_mp(aa, bb, RR):
    # get numpy roots for start
    s = np.linspace(1e-9, 7.0, 4001)
    mm = np.sqrt(float(RR)); fa=float(aa); fb=float(bb)
    M = (np.cos(s*(1-fb))*np.cos(s*mm*(fb-fa))*np.sin(s*fa)
         - mm*np.sin(s*(1-fb))*np.sin(s*mm*(fb-fa))*np.sin(s*fa)
         + (np.cos(s*(1-fb))*np.sin(s*mm*(fb-fa))/mm)*np.cos(s*fa)
         + np.sin(s*(1-fb))*np.cos(s*mm*(fb-fa))*np.cos(s*fa))
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]
        for _ in range(60):
            md = 0.5*(lo+hi)
            mmm = np.sqrt(float(RR))
            fm = (np.cos(md*(1-fb))*np.cos(md*mmm*(fb-fa))*np.sin(md*fa)
                  - mmm*np.sin(md*(1-fb))*np.sin(md*mmm*(fb-fa))*np.sin(md*fa)
                  + (np.cos(md*(1-fb))*np.sin(md*mmm*(fb-fa))/mmm)*np.cos(md*fa)
                  + np.sin(md*(1-fb))*np.cos(md*mmm*(fb-fa))*np.cos(md*fa))
            f0 = (np.cos(lo*(1-fb))*np.cos(lo*mmm*(fb-fa))*np.sin(lo*fa)
                  - mmm*np.sin(lo*(1-fb))*np.sin(lo*mmm*(fb-fa))*np.sin(lo*fa)
                  + (np.cos(lo*(1-fb))*np.sin(lo*mmm*(fb-fa))/mmm)*np.cos(lo*fa)
                  + np.sin(lo*(1-fb))*np.cos(lo*mmm*(fb-fa))*np.cos(lo*fa))
            if np.signbit(fm) == np.signbit(f0): lo = md
            else: hi = md
        x0 = mp.mpf(float(0.5*(lo+hi)))
        for _ in range(10):
            fx = sec_mp(x0, aa, bb, RR)
            h = mp.mpf('1e-12')
            fpx = (sec_mp(x0+h, aa, bb, RR)-sec_mp(x0-h, aa, bb, RR))/(2*h)
            x0 = x0 - fx/fpx
        out.append(x0)
    return out
def n_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR); LL = bb-aa; be = 1-bb
    al = sv*aa; th = sv*mm*LL
    I1 = aa/2 - mp.sin(2*al)/(4*sv)
    Icc = LL/2 + mp.sin(2*th)/(4*sv*mm)
    Iss = LL/2 - mp.sin(2*th)/(4*sv*mm)
    Ics = mp.sin(th)**2/(2*sv*mm)
    sa, ca = mp.sin(al), mp.cos(al)
    I2 = sa*sa*Icc + (ca/mm)**2*Iss + 2*sa*(ca/mm)*Ics
    yb = sa*mp.cos(th) + (ca/mm)*mp.sin(th)
    ypb = -mm*mp.sin(th)*mp.sin(al) + mp.cos(th)*mp.cos(al)
    Icc3 = be/2 + mp.sin(2*sv*be)/(4*sv)
    Iss3 = be/2 - mp.sin(2*sv*be)/(4*sv)
    Ics3 = mp.sin(sv*be)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + RR*I2)/sv**2 + I3

R = mp.mpf('1e6')
# load trace2 data to get the branch points (a,b) on S3
d = json.load(open(os.path.join(HERE, "trace2_1e+06.json"), encoding="utf-8"))
rows = [r for r in d["rows"] if np.isfinite(r[7])]
# for selected a values, find (a,b) from rows by interpolation, then refine with mpmath Newton
def R1_mp(aa, bb):
    s1, s2 = roots2_mp(aa, bb, R)
    n1 = n_mp(s1, aa, bb, R); n2 = n_mp(s2, aa, bb, R)
    return mp.sin(s1*aa)**2/n1 - mp.sin(s2*aa)**2/n2
def partial_mp(aa, bb):
    h = mp.mpf('1e-9')
    s1, s2 = roots2_mp(aa, bb, R)
    def r1(xa, xb, ss1, ss2):
        nn1 = n_mp(ss1, xa, xb, R); nn2 = n_mp(ss2, xa, xb, R)
        return ss1**2*(mp.sin(ss1*xa)/ss1)**2/nn1 - ss2**2*(mp.sin(ss2*xa)/ss2)**2/nn2
    ds1a = -((sec_mp(s1, aa+h, bb, R)-sec_mp(s1, aa-h, bb, R))/(2*h)) / ((sec_mp(s1+h, aa, bb, R)-sec_mp(s1-h, aa, bb, R))/(2*h))
    ds2a = -((sec_mp(s2, aa+h, bb, R)-sec_mp(s2, aa-h, bb, R))/(2*h)) / ((sec_mp(s2+h, aa, bb, R)-sec_mp(s2-h, aa, bb, R))/(2*h))
    dr1a = (r1(aa+h, bb, s1, s2)-r1(aa-h, bb, s1, s2))/(2*h) + (r1(aa, bb, s1+h, s2)-r1(aa, bb, s1-h, s2))/(2*h)*ds1a + (r1(aa, bb, s1, s2+h)-r1(aa, bb, s1, s2-h))/(2*h)*ds2a
    dr1b = (r1(aa, bb+h, s1, s2)-r1(aa, bb, s1, s2-h))/(2*h)*0 + (r1(aa, bb, s1, s2+h)-r1(aa, bb, s1, s2-h))/(2*h)*ds2a  # wrong; fix below
    # proper dr1b
    ds1b = -((sec_mp(s1, aa, bb+h, R)-sec_mp(s1, aa, bb-h, R))/(2*h)) / ((sec_mp(s1+h, aa, bb, R)-sec_mp(s1-h, aa, bb, R))/(2*h))
    ds2b = -((sec_mp(s2, aa, bb+h, R)-sec_mp(s2, aa, bb-h, R))/(2*h)) / ((sec_mp(s2+h, aa, bb, R)-sec_mp(s2-h, aa, bb, R))/(2*h))
    dr1b = (r1(aa, bb+h, s1, s2)-r1(aa, bb-h, s1, s2))/(2*h) + (r1(aa, bb, s1+h, s2)-r1(aa, bb, s1-h, s2))/(2*h)*ds1b + (r1(aa, bb, s1, s2+h)-r1(aa, bb, s1, s2-h))/(2*h)*ds2b
    return dr1a, dr1b

import json
for at in [0.48, 0.49, 0.492, 0.494, 0.496, 0.497, 0.498, 0.499, 0.5, 0.501, 0.502, 0.503, 0.505, 0.51, 0.52]:
    aa = mp.mpf(repr(at))
    # initial b from trace rows
    idx = int(np.argmin(np.abs(np.array([r[0] for r in rows]) - at)))
    bb = mp.mpf(repr(rows[idx][1]))
    # Newton refine in b
    for _ in range(20):
        f = R1_mp(aa, bb)
        d1a, d1b = partial_mp(aa, bb)
        bb = bb - f/d1b
        if abs(f) < mp.mpf('1e-45'): break
    d1a, d1b = partial_mp(aa, bb)
    G = -d1a/d1b
    print("a=%s b=%s G=%s" % (mp.nstr(aa,6), mp.nstr(bb,10), mp.nstr(G,10)))


