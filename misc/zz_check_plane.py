# -*- coding: utf-8 -*-
"""Independent check: plane-formula J vs NJ2; correct dJ/dx|th sign on T2."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40

def comps(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    J = G*G + Gc - u*Gx
    return dict(q=q, c=c, u=u, G=G, Gx=Gx, Gc=Gc, J=J, Phi=Phi, den=den, V=V, H=H, A0=A0)

# plane formulas from re_dJdx (theta fixed derivatives)
def plane(x, th):
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Delta = b*s*th + C*S*x
    u = b*s*x**2/Delta
    A0 = mpf(3)/x - 2*b/s
    H = 2*th*(C*C*s*s - S*S*b*b)/Delta
    V = H - A0
    # Dx at fixed theta: df/dx + df/ds*(-b) + df/db*s
    # u
    ux = 2*b*s*x/Delta - b*s*x**2*(C*S + b*s*(-b)/1 + 0)/Delta**2  # placeholder, compute below properly
    return None

# Verify H plane formula equals H comps at sample points
print('check H plane formula:')
for (x, th) in [(2.2, 1.0), (2.4, 1.1), (2.1, 1.045), (2.35, 0.98)]:
    x = mpf(str(x)); th = mpf(str(th))
    r = comps(x, th)
    s, b = sin(x), -cos(x); S, C = sin(th), cos(th)
    Delta = b*s*th + C*S*x
    Hp = 2*th*(C*C*s*s - S*S*b*b)/Delta
    up = b*s*x**2/Delta
    A0p = mpf(3)/x - 2*b/s
    Vp = Hp - A0p
    Gp = up*Vp
    print('  (%.3f,%.3f): H comps=%.8f plane=%.8f ; u comps=%.8f plane=%.8f ; G comps=%.8f plane=%.8f'
          % (float(x), float(th), r['H'], Hp, r['u'], up, r['G'], Gp))
