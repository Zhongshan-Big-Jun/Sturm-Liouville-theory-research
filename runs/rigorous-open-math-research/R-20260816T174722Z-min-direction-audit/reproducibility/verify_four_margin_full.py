# -*- coding: utf-8 -*-
"""Four-margin identity with arbitrary gamma_1,gamma_6 (no endpoint zero assumption)."""
import numpy as np
import random

def random_spd2():
    a = random.uniform(1, 3); d = random.uniform(1, 3); b = random.uniform(-0.5, 0.5)
    P = np.array([[a, b], [b, d]])
    return P @ P.T + np.eye(2)

def check():
    for _ in range(10000):
        P = np.zeros((6,6)); invP = np.zeros((6,6))
        for j in range(3):
            Pj = random_spd2()
            P[2*j:2*j+2, 2*j:2*j+2] = Pj
            invP[2*j:2*j+2, 2*j:2*j+2] = np.linalg.inv(Pj)
        W1 = random.uniform(0.1, 3); W2 = random.uniform(0.1, 3)
        W = np.diag([W1, W2])
        C = np.zeros((2,6))
        C[0,1] = 1; C[0,2] = -1
        C[1,3] = 1; C[1,4] = -1
        gamma = np.zeros(6)
        for i in range(6):
            gamma[i] = random.uniform(-3, 3)
        # but keep v1,v2 positive as defined
        v1 = (gamma[2]-gamma[1])/W1
        v2 = (gamma[4]-gamma[3])/W2
        if v1 <= 0 or v2 <= 0:
            continue
        M = P - C.T @ np.linalg.inv(W) @ C
        f = M @ gamma
        LR = []
        for j in range(3):
            fj = f[2*j:2*j+2]
            LR.append(invP[2*j:2*j+2, 2*j:2*j+2] @ fj)
        L1,R1 = LR[0]; L2,R2 = LR[1]; L3,R3 = LR[2]
        H = C @ invP @ C.T - W
        detH = np.linalg.det(H)
        s2 = invP[2,3]
        r1 = invP[1,1]; l2 = invP[2,2]; r2 = invP[3,3]; l3 = invP[4,4]
        E1 = gamma[1] + r1*v1
        F2 = l2*v1 - gamma[2]
        E2 = gamma[3] + r2*v2
        F3 = l3*v2 - gamma[4]
        lhs = v1*v1*v2*v2*detH
        rhs = v1*v2*((E1+F2)*(E2+F3) - s2*s2*v1*v2)
        if abs(lhs - rhs) > 1e-7 * max(1.0, abs(lhs), abs(rhs)):
            print('FAIL', lhs, rhs, 'gamma', gamma)
            return False
    print('PASS all random four-margin checks with arbitrary gamma endpoints (10000)')
    return True

check()
