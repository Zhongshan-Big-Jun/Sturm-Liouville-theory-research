# -*- coding: utf-8 -*-
"""Random algebraic verification of the n=3 four-margin identity.

Reconstructs the matrices from the tex (path incidence, P blocks, C, W) and
checks v1^2 v2^2 det H = v1 v2 [(E1+F2)(E2+F3)-s2^2 v1 v2].
"""
import numpy as np
import random

def random_spd2():
    # random 2x2 SPD matrix P (not inverse)
    a = random.uniform(1, 3)
    d = random.uniform(1, 3)
    b = random.uniform(-0.5, 0.5)
    P = np.array([[a, b], [b, d]])
    # ensure SPD
    P = P @ P.T + np.eye(2)
    return P

def check():
    for _ in range(10000):
        # m=6, three positive blocks (odd edges) -> P is block diag of three 2x2 SPD
        P = np.zeros((6,6))
        invP = np.zeros((6,6))
        for j in range(3):
            Pj = random_spd2()
            P[2*j:2*j+2, 2*j:2*j+2] = Pj
            invP[2*j:2*j+2, 2*j:2*j+2] = np.linalg.inv(Pj)
        # even edge weights W1,W2>0 (these are -K_even)
        W1 = random.uniform(0.1, 3)
        W2 = random.uniform(0.1, 3)
        W = np.diag([W1, W2])
        # C = B_e (2x6), even edges (2,3) and (4,5)
        C = np.zeros((2,6))
        C[0,1] = 1; C[0,2] = -1
        C[1,3] = 1; C[1,4] = -1
        # gamma vector: endpoints zero, internal gamma2..gamma5
        gamma = np.zeros(6)
        gamma[1] = random.uniform(-3, -0.01)  # gamma2 <0
        gamma[2] = random.uniform(0.01, 3)    # gamma3 >0
        gamma[3] = random.uniform(-3, -0.01)  # gamma4 <0
        gamma[4] = random.uniform(0.01, 3)    # gamma5 >0
        v1 = (gamma[2]-gamma[1])/W1
        v2 = (gamma[4]-gamma[3])/W2
        # M = P - C^T W^{-1} C
        M = P - C.T @ np.linalg.inv(W) @ C
        f = M @ gamma
        # P_j^{-1} f_j = (L_j,R_j)^T
        LR = []
        for j in range(3):
            fj = f[2*j:2*j+2]
            LR.append(invP[2*j:2*j+2, 2*j:2*j+2] @ fj)
        L1,R1 = LR[0]
        L2,R2 = LR[1]
        L3,R3 = LR[2]
        # H = C P^{-1} C^T - W
        H = C @ invP @ C.T - W
        detH = np.linalg.det(H)
        # s2 is off-diagonal of P_2^{-1} (the inverse block)
        s2 = invP[2,3]  # P_2^{-1} offdiag
        # E/F definitions
        E1 = gamma[1] + (invP[0,0])*v1  # r1 = invP[0,0]? Wait P_1^{-1} = [[l1,s1],[s1,r1]], so r1 = invP[1,1]? Need map: for block j, inverse [[l_j,s_j],[s_j,r_j]], so r1 = invP[1,1], l2=invP[2,2], etc.
        r1 = invP[1,1]
        l2 = invP[2,2]
        r2 = invP[3,3]
        l3 = invP[4,4]
        E1 = gamma[1] + r1*v1
        F2 = l2*v1 - gamma[2]
        E2 = gamma[3] + r2*v2
        F3 = l3*v2 - gamma[4]
        lhs = v1*v1*v2*v2*detH
        rhs = v1*v2*((E1+F2)*(E2+F3) - s2*s2*v1*v2)
        if abs(lhs - rhs) > 1e-7 * max(1.0, abs(lhs), abs(rhs)):
            print('FAIL', lhs, rhs)
            return False
    print('PASS all random four-margin checks (10000)')
    return True

check()
