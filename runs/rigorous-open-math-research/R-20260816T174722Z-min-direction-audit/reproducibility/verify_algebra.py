# -*- coding: utf-8 -*-
"""Algebraic verification of key identities in min_direction_progress.tex.

Run: py -m pip install sympy numpy (if needed); then py verify_algebra.py
Output: PASS/FAIL lines for each identity.
"""
import sympy as sp

x, y, r = sp.symbols('x y r', positive=True)
mu = sp.Integer(2)

def half_angle(theta):
    return sp.tan(theta/2)

def trig(theta):
    c = sp.cos(theta)
    s = sp.sin(theta)
    C = sp.cos(mu*theta)
    S = sp.sin(mu*theta)
    return c, s, C, S

# theta = 2 atan(x), eta = 2 atan(y)
theta = 2*sp.atan(x)
eta = 2*sp.atan(y)
c, s, C, S = trig(theta)
d, t, D, T = trig(eta)

# --- n=2 mu=2 a,b formulas from the tex ---
D_a = 3*r*x**3*y**2 - r*x**3 - 3*r*x*y**2 + r*x + x**4*y + 2*x**2*y**3 - 4*x**2*y + y
N_b = 2*r*x**3*y**2 + r*x*y**4 - 4*r*x*y**2 + r*x + 3*x**2*y**3 - 3*x**2*y - y**3 + y
a_tex = - y*(x-y)*(x+y)*(1+x**2) / D_a
b_tex = N_b / (r*x*(x-y)*(x+y)*(1+y**2))

# General interface momentum equations (mu=2):
# (c - 1/a)/s = r*(b - d)/t
# -(1/a + C)/S = r*(b + D)/T
eq1 = sp.simplify((c - 1/a_tex)/s - r*(b_tex - d)/t)
eq2 = sp.simplify(-(1/a_tex + C)/S - r*(b_tex + D)/T)
print('mu=2 interface eq1 simplified numerator:', sp.factor(sp.together(eq1)))
print('mu=2 interface eq2 simplified numerator:', sp.factor(sp.together(eq2)))
print('mu=2 interface eq1 zero:', sp.simplify(eq1) == 0)
print('mu=2 interface eq2 zero:', sp.simplify(eq2) == 0)

# --- General mu interface mapping formulas (chapter n=3) ---
mu_g = sp.symbols('mu', positive=True)
theta_g = sp.symbols('theta', positive=True)
eta_g = sp.symbols('eta', positive=True)
cg, sg, Cg, Sg = sp.cos(theta_g), sp.sin(theta_g), sp.cos(mu_g*theta_g), sp.sin(mu_g*theta_g)
dg, tg, Dg, Tg = sp.cos(eta_g), sp.sin(eta_g), sp.cos(mu_g*eta_g), sp.sin(mu_g*eta_g)
Delta = tg*Sg - sg*Tg
A0 = tg*Sg*cg + sg*Tg*Cg
A1 = sg*Sg*(dg + Dg)
B0 = tg*Tg*(cg + Cg)
B1 = tg*Sg*Dg + sg*Tg*dg
a_gen = Delta/(A0 + r*A1)
b_gen = -(B0 + r*B1)/(r*Delta)
eqg1 = sp.simplify((cg - 1/a_gen)/sg - r*(b_gen - dg)/tg)
eqg2 = sp.simplify(-(1/a_gen + Cg)/Sg - r*(b_gen + Dg)/Tg)
print('general interface eq1 zero:', sp.simplify(eqg1) == 0)
print('general interface eq2 zero:', sp.simplify(eqg2) == 0)

# --- Identity A1 B0 - B1 (A0 - Delta) = s t Delta (1+C)(-D) Xi ---
# Xi = -(d T)/(D t) - (S/s)*(1-c)/(1+C)
Xi = -(dg*Tg)/(Dg*tg) - (Sg/sg)*(1-cg)/(1+Cg)
lhs = sp.simplify(A1*B0 - B1*(A0 - Delta))
rhs = sp.simplify(sg*tg*Delta*(1+Cg)*(-Dg)*Xi)
print('Xi identity lhs-rhs:', sp.simplify(lhs - rhs))
print('Xi identity holds:', sp.simplify(lhs - rhs) == 0)

# --- Determinant parity random numeric check (symbolic matrices with random values) ---
import random
random.seed(0)
def random_pos_matrix(n):
    # diagonal dominant random SPD
    M = [[0.0]*n for _ in range(n)]
    for i in range(n):
        M[i][i] = random.uniform(2, 5)
        for j in range(n):
            if i != j:
                v = random.uniform(-0.3, 0.3)
                M[i][j] = v
                M[j][i] = v
    # make SPD via M*M^T + I
    import numpy as np
    A = np.array(M)
    A = A @ A.T + np.eye(n)
    return A

def det_sign(vals):
    import numpy as np
    det = np.linalg.det(vals)
    return 1 if det > 0 else (-1 if det < 0 else 0)

for n in [2,3,4,5]:
    ok = True
    for _ in range(20):
        import numpy as np
        m = 2*(n-1)+1  # odd edges count? actually m=2n events, K has m-1=2n-1 edges; odd count n, even count n-1
        # We'll directly test the Sylvester identity with random matrices of matching dimensions.
        # Let K_o (n x n), W (n-1 x n-1), B_o (n x (n-1)?) Need dimensions from doc: P=D+B_o^T K_o^-1 B_o, C=B_e.
        # We can construct any dimensions: D (n x n), B_o (n x n?), K_o (n x n), B_e ((n-1) x n?), W ((n-1)x(n-1)).
        # For random test, choose n_d = n (odd block count), n_e = n-1 (even count).
        nd, ne = n, n-1
        Dm = np.diag(np.random.uniform(1,3,nd))
        Ko = random_pos_matrix(nd)
        Wm = random_pos_matrix(ne)
        Bo = np.random.uniform(-1,1,(nd,nd))
        Be = np.random.uniform(-1,1,(ne,nd))
        P = Dm + Bo.T @ np.linalg.inv(Ko) @ Bo
        C = Be
        M = P - C.T @ np.linalg.inv(Wm) @ C
        H = C @ np.linalg.inv(P) @ C.T - Wm
        # Build full L_-? Not needed; test det M relation sign to det H.
        # sgn det M = (-1)^{n-1} sgn det H since P,W positive.
        detM = np.linalg.det(M)
        detH = np.linalg.det(H)
        if detM == 0 or detH == 0:
            continue
        sgnM = 1 if detM > 0 else -1
        sgnH = 1 if detH > 0 else -1
        if sgnM != ((-1)**(n-1))*sgnH:
            ok = False
            break
    print(f'det parity random n={n}:', 'PASS' if ok else 'FAIL')

# --- n=3 four-margin identity (symbolic matrix) ---
# Build H for N=2 with positive block inverse entries and v.
# H = [[r1+l2-W1, -s2],[-s2, r2+l3-W2]] (from tex: H_ii = r_i + l_{i+1} - W_i, H_{i,i+1}=-s_{i+1})
# The four-margin identity is in terms of E/F/gamma. Let's verify the algebraic expansion
# using definitions from tex:
l1,l2,l3,r1,r2,s2,v1,v2,g2,g3,g4,g5 = sp.symbols('l1 l2 l3 r1 r2 s2 v1 v2 g2 g3 g4 g5')
E1 = g2 + r1*v1
F2 = l2*v1 - g3
E2 = g4 + r2*v2
F3 = l3*v2 - g5
# From charge_compensation: v1^2 v2^2 det H = v1 v2 [(E1+F2)(E2+F3)-s2^2 v1 v2]
# This should correspond to H with W_i? Let's compute det H and compare after substituting W? Hard without W.
# We'll just check the algebraic identity as a formal consequence if we define H entries via E/F?
# Skip for now; print placeholder.
print('n=3 four-margin identity: manual check deferred to subagent')
