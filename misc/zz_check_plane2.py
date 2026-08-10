# -*- coding: utf-8 -*-
"""Check whether J_plane (with Dth(G), Dx(G)) equals J_comps on the curve; then compute correct dJ/dx|th."""
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
    return dict(q=q, c=c, u=u, G=G, Gx=Gx, Gc=Gc, J=J, V=V, H=H, A0=A0)

def plane_vals(x, th):
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Delta = b*s*th + C*S*x
    u = b*s*x**2/Delta
    A0 = mpf(3)/x - 2*b/s
    H = 2*th*(C*C*s*s - S*S*b*b)/Delta
    V = H - A0
    G = u*V
    # partial derivatives at fixed theta
    # Dx(f) = f_x + f_s*(-b) + f_b*s ; Dth(f) = f_th + f_S*C + f_C*(-S)
    # u = b s x^2 / Delta, Delta = b s th + C S x
    ux = (b*s*2*x*Delta - b*s*x**2*(C*S))/Delta**2
    # careful: du/dx with s,b,S,C,th fixed:
    # u = b*s*x^2 * Delta^-1 ; d/dx = b*s*2x/Delta - b*s*x^2*(C*S)/Delta^2
    uth = (b*s*x**2)*(-(b*s))/Delta**2   # dDelta/dth = b*s
    A0x = -mpf(3)/(x*x) - 2/(s*s)
    A0th = mpf(0)
    # H = 2 th (C^2 s^2 - S^2 b^2)/Delta
    Hn = 2*th*(C*C*s*s - S*S*b*b)
    Hx = (2*(C*C*s*s - S*S*b*b)*Delta - Hn*(C*S))/Delta**2
    Hth = (2*(C*C*s*s - S*S*b*b) + 2*th*0 - Hn*(b*s))/Delta**2
    Vx = Hx - A0x; Vth = Hth - A0th
    Gx_plane = ux*V + u*Vx
    Gth_plane = uth*V + u*Vth
    J_plane = G*G + Gth_plane - u*Gx_plane
    return dict(u=u, G=G, Gx_plane=Gx_plane, Gth=Gth_plane, J_plane=J_plane)

for (x, th) in [(2.2, 1.0), (2.4, 1.1), (2.1, 1.045), (2.35, 0.98)]:
    x = mpf(str(x)); th = mpf(str(th))
    r = comps(x, th); p = plane_vals(x, th)
    print('(%.3f,%.3f): J_comps=%.6f J_plane=%.6f  Gx_comps=%.6f Gx_plane=%.6f  Gc_comps=%.6f Gth_plane=%.6f'
          % (float(x), float(th), r['J'], p['J_plane'], r['Gx'], p['Gx_plane'], r['Gc'], p['Gth']))
