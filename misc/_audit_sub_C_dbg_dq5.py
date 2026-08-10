import sympy as sp
from sympy import symbols, pi, cos, sin, cot, atan, simplify, diff, expand, tan, sqrt, Rational
qq, w_ = symbols('qq w_', positive=True)
Aq = pi - atan(w_/qq)
M2 = 4*Aq**2*w_*qq - 7*Aq*qq**2 - 9*Aq*w_**2 + 2*Aq*(qq**2+w_**2)/(1+w_**2) + atan(w_)*(4*Aq*w_ - 5*qq - 9*qq*w_**2)
th_ = symbols('th_', positive=True)
qth = cos(2*th_)/(2*sin(th_)**2)
wth = cot(th_)
# partial derivative dM2/dq at fixed w, then w = w_b(theta)
dM2dq_partial = diff(M2, qq)
dM2dq_oncurve = simplify(dM2dq_partial.subs({qq: qth, w_: wth, atan(w_/qq): 2*th_, atan(w_): pi/2 - th_}))
z = symbols('z', positive=True)
dM2dq_oncurve_z = dM2dq_oncurve.subs({tan(th_): z, sin(th_): z/sqrt(1+z**2), cos(th_): 1/sqrt(1+z**2), cot(th_): 1/z, th_: atan(z)})
N_partial = sp.expand(sp.together(dM2dq_oncurve_z * 2*z**2*(z**2+1)**2))
print('N_partial (for partial dM2/dq at w=w_b):')
print(' ', N_partial)
# tex N
b = atan(z)
Pz = 32*z*(z**2+1)**2
Qz = -10*z**6 - 32*pi*z**5 + 42*z**4 - 64*pi*z**3 + 2*z**2 - 32*pi*z + 46
Rz = 5*pi*z**6 - 10*z**5 + 8*pi**2*z**5 - 21*pi*z**4 - 40*z**3 + 16*pi**2*z**3 - pi*z**2 - 14*z + 8*pi**2*z - 23*pi
N_tex = sp.expand(b**2*Pz + b*Qz + Rz)
print('N_tex == N_partial ?', sp.simplify(N_tex - N_partial) == 0)
