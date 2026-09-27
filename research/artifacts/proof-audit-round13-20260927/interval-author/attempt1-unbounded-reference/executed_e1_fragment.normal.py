GLO, GHI = (F(655, 1000), F(10472, 10000))
mconst = F(3164, 10000)

def comps2(g):
    """D2-valued quantities (g : D2)."""
    A = PI - g
    sg = d2_sin(g)
    cg = d2_cos(g)
    D2v = I(1) + 3 * sg * sg
    B1 = A * cg - 2 * sg
    B2 = 4 * A * A * cg * cg - A * A - 12 * A * cg * sg + 6 * sg * sg
    M = 2 * A * A * cg * cg - A * A - 8 * A * cg * sg + 6 * sg * sg
    B4 = 7 * A * cg * cg - A * sg * sg - 4 * cg * sg
    B5 = A * A * cg * cg - A * A * sg * sg + 2 * A * A + 12 * A * cg * sg - 12 * sg * sg
    B7 = 3 * A * cg * cg + A * sg * sg + 8 * cg * sg
    G5 = B5 - A * B4
    tan = sg / cg
    tmax = d2_atan(2 * tan)
    TA_B2 = 4 * -B2 * A * A * sg * sg * cg ** 4 / (D2v * D2v)
    TA_M = 4 * -M * A * A * sg * sg * cg ** 4 / (D2v * D2v)
    TC = mconst * G5 * A * sg * cg * cg
    TB = 2 * A ** 3 * sg * sg * tmax * cg ** 5 / (D2v * D2v * D2v.sqrt())
    z = cg * cg / D2v
    Qlo = 4 * A * A * z * z - A * B7 * z + 6 * cg * cg * sg * sg
    Qhi = 4 * A * A * cg ** 4 - A * B7 * cg * cg + 6 * cg * cg * sg * sg
    Fv = tmax * tmax * cg * sg * sg
    return dict(A=A, sg=sg, cg=cg, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7, G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TC=TC, TB=TB, Qlo=Qlo, Qhi=Qhi, Fv=Fv)
deriv_facts = [('Qlo increasing', 'Qlo', GLO, GHI, True, 4), ('F increasing [1.0014,1.0472]', 'Fv', F(10014, 10000), GHI, True, 2), ('TA_B2 inc [0.655,0.72]', 'TA_B2', GLO, F(72, 100), True, 8), ('TA_B2 inc [0.72,0.723]', 'TA_B2', F(72, 100), F(723, 1000), True, 2), ('TA_B2 dec [0.724,0.73]', 'TA_B2', F(724, 1000), F(73, 100), False, 2), ('TA_B2 dec [0.73,0.85]', 'TA_B2', F(73, 100), F(85, 100), False, 8), ('TA_B2 dec [0.85,0.86]', 'TA_B2', F(85, 100), F(86, 100), False, 2), ('TA_M dec [0.85,0.86]', 'TA_M', F(85, 100), F(86, 100), False, 2), ('TA_M dec [0.86,1.0472]', 'TA_M', F(86, 100), GHI, False, 4), ('TB decreasing', 'TB', GLO, GHI, False, 8), ('TC inc [0.655,0.82]', 'TC', GLO, F(82, 100), True, 16), ('TC dec [0.83,1.0472]', 'TC', F(83, 100), GHI, False, 8)]
point_facts = [('TA_B2(0.655) >= 11/5', 'TA_B2', F(655, 1000), 'ge', F(11, 5)), ('TA_B2(0.72) >= 13/5', 'TA_B2', F(72, 100), 'ge', F(13, 5)), ('TA_B2(0.73) >= 13/5', 'TA_B2', F(73, 100), 'ge', F(13, 5)), ('TA_B2(0.82) >= 2', 'TA_B2', F(82, 100), 'ge', F(2)), ('TA_B2(0.83) >= 2', 'TA_B2', F(83, 100), 'ge', F(2)), ('TA_B2(0.85) >= 19/10', 'TA_B2', F(85, 100), 'ge', F(19, 10)), ('TA_B2(0.86) >= 47/25', 'TA_B2', F(86, 100), 'ge', F(47, 25)), ('TA_M(0.86) >= 9/5', 'TA_M', F(86, 100), 'ge', F(9, 5)), ('TA_M(1.0014) >= 3/5', 'TA_M', F(10014, 10000), 'ge', F(3, 5)), ('TA_M(1.0472) >= 3/8', 'TA_M', GHI, 'ge', F(3, 8)), ('TB(0.72) >= 3/10', 'TB', F(72, 100), 'ge', F(3, 10)), ('TB(0.73) >= 3/10', 'TB', F(73, 100), 'ge', F(3, 10)), ('TB(0.82) >= 3/20', 'TB', F(82, 100), 'ge', F(3, 20)), ('TB(0.83) >= 3/20', 'TB', F(83, 100), 'ge', F(3, 20)), ('TB(0.85) >= 1/10', 'TB', F(85, 100), 'ge', F(1, 10)), ('TB(0.86) >= 1/10', 'TB', F(86, 100), 'ge', F(1, 10)), ('TB(1.0014) >= 1/25', 'TB', F(10014, 10000), 'ge', F(1, 25)), ('TB(1.0472) >= 1/40', 'TB', GHI, 'ge', F(1, 40)), ('TC(0.655) >= 57/50', 'TC', F(655, 1000), 'ge', F(57, 50)), ('TC(0.72) >= 3/2', 'TC', F(72, 100), 'ge', F(3, 2)), ('TC(0.73) >= 3/2', 'TC', F(73, 100), 'ge', F(3, 2)), ('TC(0.85) >= 19/10', 'TC', F(85, 100), 'ge', F(19, 10)), ('TC(0.86) >= 19/10', 'TC', F(86, 100), 'ge', F(19, 10)), ('TC(1.0014) >= 4/3', 'TC', F(10014, 10000), 'ge', F(4, 3)), ('TC(1.0472) >= 11/10', 'TC', GHI, 'ge', F(11, 10)), ('B4(1.0472) >= 9/25', 'B4', GHI, 'ge', F(9, 25)), ('Qlo(1.0014) <= -1/10000', 'Qlo', F(10014, 10000), 'le', F(-1, 10000)), ('Qlo(1.0472) <= 33/200', 'Qlo', GHI, 'le', F(33, 200)), ('F(1.0472) <= 63/100', 'Fv', GHI, 'le', F(63, 100)), ('tau(1.0472) < 13/10', 'tmax', GHI, 'le', F(13, 10)), ('h(gamma) >= m at 0.655', 'h', F(655, 1000), 'ge', mconst), ('h(13/10) >= m', 'h', F(13, 10), 'ge', mconst)]
PRIM_PTS = [F(655, 1000), F(72, 100), F(723, 1000), F(724, 1000), F(73, 100), F(82, 100), F(83, 100), F(85, 100), F(86, 100), F(10014, 10000), GHI]
