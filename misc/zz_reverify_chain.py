# -*- coding: utf-8 -*-
"""Comprehensive fresh re-verification of the E1 chain claims for J2_2d < 0."""
import json, mpmath as mp
mp.mp.dps = 50
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')

def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    return dict(A=A, sg=sg, cg=cg, B1=B1, M=M, B2=B2, B4=B4, B5=B5, B7=B7, G5=G5)

def W_terms(g, q):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    B1, B2, B4, B5, B7 = f['B1'], f['B2'], f['B4'], f['B5'], f['B7']
    T1 = -2*A**3*B1*st*st*ct**4
    T2 = A*A*cg*B2*st*st*ct*ct
    T3 = -2*A**3*sg*t*st*ct**5
    T4 = A*A*sg*t*B4*st*ct**3
    T5 = -A*cg*cg*sg*t*B5*st*ct
    T6 = 4*A*A*cg*sg*sg*t*t*ct**4
    T7 = -A*cg*sg*sg*t*t*B7*ct*ct
    T8 = 6*cg**3*sg**4*t*t
    return dict(T1=T1,T2=T2,T3=T3,T4=T4,T5=T5,T6=T6,T7=T7,T8=T8, t=t, st=st, ct=ct)

# NJ2 from json
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
import sympy as sp; A_, t_, sg_, cg_, st_, ct_ = sp.symbols('A t sg cg st ct')
expr = 0
for i, m in enumerate(rj['monoms']):
    expr += mp.mpf(rj['coeffs'][i])*A_**m[0]*t_**m[1]*sg_**m[2]*cg_**m[3]*st_**m[4]*ct_**m[5]
fN = sp.lambdify((A_,t_,sg_,cg_,st_,ct_), expr, 'mpmath')

def NJ2val(g, q):
    w = W_terms(g, q); A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    return fN(A, w['t'], sg, cg, w['st'], w['ct'])

def J2_composed(g, q):
    # original composition formula J(pi-g; c2(g,q))
    x = mp.pi - g; th = mp.atan(q*mp.tan(g)); c = th/x
    s, b = mp.sin(x), -mp.cos(x)
    S, C = mp.sin(th), mp.cos(th)
    Phi = b*b + q*q*s*s
    den = q + c*Phi
    u = x*Phi/den
    A0 = mp.mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*(q*q-1)*s*(-b)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    return G*G + Gc - u*Gx

print("=== identity checks (5 sample points) ===")
worst_id = mp.mpf(0)
for (g,q) in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(0.65565,2.0),(mp.pi/3,1.0),(0.8,1.9)]:
    w = W_terms(g,q); A = mp.pi-g; sg,cg = mp.sin(g),mp.cos(g)
    Delta = A*w['st']*w['ct'] + w['t']*sg*cg
    n = NJ2val(g,q)
    Jc = J2_composed(g,q)
    Wsum = sum(w[k] for k in ['T1','T2','T3','T4','T5','T6','T7','T8'])
    Wdef = n/(32*A*A*cg)          # W = NJ2/(32 A^2 cg)  (no t?)
    d1 = abs(Jc - n/(16*Delta**4))
    d2 = abs(Wsum - Wdef)
    worst_id = max(worst_id, d1, d2)
    print('g=%.4f q=%.2f: |J2 - NJ2/(16D4)|=%.2e  |sumT - NJ2/(32A2cg)|=%.2e  Delta=%.4f' % (g,q,d1,d2,Delta))
print('worst identity gap: %.2e' % worst_id)

print()
print("=== bounds on fine grid 200x200 ===")
N = 200
worst = dict(T12m=(-mp.mpf(1e50),None), T3m=(-mp.mpf(1e50),None), T45m=(-mp.mpf(1e50),None), P2m=(-mp.mpf(1e50),None), Wmax=(-mp.mpf(1e50),None))
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    c12 = cg*abs(f['B2']) if f['B1'] >= 0 else cg*abs(f['M'])
    TA = 4*c12*A*A*sg*sg*cg**3/d**4
    TB2d = 2*A**3*sg*sg*tmax*cg**5/d**5   # uses ct>=cg? NOTE: ct<=cg! check sign later
    G5 = f['G5']
    z_lo = cg*cg/(d*d)
    Qlo = 4*A*A*z_lo*z_lo - A*f['B7']*z_lo + 6*cg*cg*sg*sg
    TD = tmax*tmax*cg*sg*sg*max(Qlo, mp.mpf(0))
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        w = W_terms(g,q)
        T12 = w['T1']+w['T2']; T3 = w['T3']; T45 = w['T4']+w['T5']
        P2 = w['T6']+w['T7']+w['T8']
        Wv = T12+T3+T45+P2
        if T12 + TA > worst['T12m'][0]: worst['T12m'] = (T12+TA, (float(g),float(q)))
        # TB2d: check T3 <= -TB2d  i.e. T3 + TB2d <= 0
        if T3 + TB2d > worst['T3m'][0]: worst['T3m'] = (T3+TB2d, (float(g),float(q)))
        # TC2d: T4+T5 <= -G5*A*sg*cg^2*t*st*ct
        TC2d = G5*A*sg*cg*cg*w['t']*w['st']*w['ct']
        if T45 + TC2d > worst['T45m'][0]: worst['T45m'] = (T45+TC2d, (float(g),float(q)))
        if P2 - TD > worst['P2m'][0]: worst['P2m'] = (P2-TD, (float(g),float(q)))
        if Wv > worst['Wmax'][0]: worst['Wmax'] = (Wv, (float(g),float(q)))
for k in ['T12m','T3m','T45m','P2m','Wmax']:
    print('%s: worst = %.6f at %s' % (k, worst[k][0], worst[k][1]))

print()
print("=== margin m2d = -(TB2d+TC2d)+P2-W  (should be >= ~1.01) ===")
mn = (mp.mpf(1e50), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    TB2d = 2*A**3*sg*sg*tmax*cg**5/d**5
    z_lo = cg*cg/(d*d)
    Qlo = 4*A*A*z_lo*z_lo - A*f['B7']*z_lo + 6*cg*cg*sg*sg
    TD = tmax*tmax*cg*sg*sg*max(Qlo, mp.mpf(0))
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        w = W_terms(g,q)
        G5 = f['G5']
        TC2d = G5*A*sg*cg*cg*w['t']*w['st']*w['ct']
        Wv = sum(w[k] for k in ['T1','T2','T3','T4','T5','T6','T7','T8'])
        P2 = w['T6']+w['T7']+w['T8']
        m = -(TB2d+TC2d) + P2 - Wv
        if m < mn[0]: mn = (m, (float(g),float(q)))
print('m2d min = %.6f at %s' % (mn[0], mn[1]))
