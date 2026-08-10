import sympy as sp
from sympy import symbols, pi, cos, sin, cot, atan, simplify, diff, expand, tan, sqrt
qq, w_ = symbols('qq w_', positive=True)
Aq = pi - atan(w_/qq)
M2 = 4*Aq**2*w_*qq - 7*Aq*qq**2 - 9*Aq*w_**2 + 2*Aq*(qq**2+w_**2)/(1+w_**2) + atan(w_)*(4*Aq*w_ - 5*qq - 9*qq*w_**2)
th_ = symbols('th_', positive=True)
qth = cos(2*th_)/(2*sin(th_)**2)
wth = cot(th_)
M2b = simplify(M2.subs({qq: qth, w_: wth, atan(w_/qq): 2*th_, atan(w_): pi/2 - th_}))
dM2dth = diff(M2b, th_)
dqM2 = simplify(dM2dth / diff(qth, th_))
z = symbols('z', positive=True)
dqM2_z = dqM2.subs({tan(th_): z, sin(th_): z/sqrt(1+z**2), cos(th_): 1/sqrt(1+z**2), cot(th_): 1/z, th_: atan(z)})
dqM2_z = sp.factor(sp.together(dqM2_z))
N_true = sp.expand(sp.together(dqM2_z * 2*z**2*(z**2+1)**2))
print('N_true =', N_true)
# tex claim
b = atan(z)
Pz = 32*z*(z**2+1)**2
Qz = -10*z**6 - 32*pi*z**5 + 42*z**4 - 64*pi*z**3 + 2*z**2 - 32*pi*z + 46
Rz = 5*pi*z**6 - 10*z**5 + 8*pi**2*z**5 - 21*pi*z**4 - 40*z**3 + 16*pi**2*z**3 - pi*z**2 - 14*z + 8*pi**2*z - 23*pi
N_tex = sp.expand(b**2*Pz + b*Qz + Rz)
print('N_tex =', N_tex)
print('N_true - N_tex =', sp.factor(N_true - N_tex))
