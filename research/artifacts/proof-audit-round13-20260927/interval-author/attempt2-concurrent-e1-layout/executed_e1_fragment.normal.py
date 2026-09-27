GLO, GHI = (F(131, 200), F(1309, 1250))
mconst = F(791, 2500)

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
