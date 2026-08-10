from mpmath import mp, mpf, sin, cos, tan, atan, cot, sqrt, pi, asin, acos
mp.dps = 60
def Phi(qq, xx): return cos(xx)**2 + qq**2*sin(xx)**2
def Mf_mp(xx, qq, cc): return xx**2*sin(xx)**2/(qq+cc*Phi(qq,xx))
def alpha1_mp(qq, cc):
    lo, hi = mpf('1e-15'), pi/2
    for _ in range(300):
        mid = (lo+hi)/2
        if cc*mid > atan(1/(qq*tan(mid))):
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2
def alpha2_mp(qq, cc):
    # gamma = pi - alpha2 solves c*(pi-gamma) = atan(q tan gamma), gamma in (0,pi/2)
    lo, hi = mpf('1e-15'), pi/2
    for _ in range(300):
        mid = (lo+hi)/2
        if cc*(pi-mid) > atan(qq*tan(mid)):
            lo = mid
        else:
            hi = mid
    return pi - (lo+hi)/2
def Fe_mp(qq, cc):
    a1 = alpha1_mp(qq, cc); a2 = alpha2_mp(qq, cc)
    return Mf_mp(a1, qq, cc) - Mf_mp(a2, qq, cc)
for qq in [mpf('1.1'), mpf('1.5'), mpf('2')]:
    h = mpf('1e-9')
    num = (Fe_mp(qq, mpf('0.5')+h) - Fe_mp(qq, mpf('0.5')-h))/(2*h)
    xq = 2*asin(1/sqrt(2*(qq+1)))
    Pq = 3*xq**2 + 6*xq*sin(xq) - 3*pi*xq - 3*pi*sin(xq) + pi**2
    cf = 2*pi*(cos(xq)-1)**3/sin(xq)**3*Pq
    print("q=", qq, "num=", num, "closed=", cf, "rel err", abs(num-cf)/abs(cf))
    # also direct derivative using alpha' formula
    a1 = alpha1_mp(qq, mpf('0.5'))
    D1 = qq + mpf('0.5')*Phi(qq, a1)
    a1p = -a1*Phi(qq, a1)/D1
    # Mf_x
    Mf_x = lambda xx: 2*xx*sin(xx)**2/(qq+mpf('0.5')*Phi(qq,xx)) - xx**2*sin(xx)**2*Phi(qq,xx)*0 + (xx**2*2*sin(xx)*cos(xx)*(qq+mpf('0.5')*Phi(qq,xx)) - xx**2*sin(xx)**2*mpf('0.5')*(2*(qq**2-1)*sin(xx)*cos(xx)))/(qq+mpf('0.5')*Phi(qq,xx))**2
    Mf_c = lambda xx: -xx**2*sin(xx)**2*Phi(qq,xx)/(qq+mpf('0.5')*Phi(qq,xx))**2
    a2 = pi - a1
    D2 = qq + mpf('0.5')*Phi(qq, a2)
    a2p = -a2*Phi(qq, a2)/D2
    direct = (Mf_x(a1)*a1p + Mf_c(a1)) - (Mf_x(a2)*a2p + Mf_c(a2))
    print("   direct:", direct)
