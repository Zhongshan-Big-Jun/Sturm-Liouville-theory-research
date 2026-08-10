import mpmath as mp
mp.mp.dps = 50

def alpha(x, m):
    # alpha(x) = arg(cos x, sin x / m) in (0, pi), continuous, alpha(0)=0
    return mp.atan2(mp.sin(x)/m, mp.cos(x))

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

# Transfer: given s, find y(1) via middle+right propagation
def y_end(s, a, b, m):
    A = m*s*a
    psi = s*(b-a)
    B = m*s*(1-b)
    # v at a: (sy(a), y'(a)) = (sin A/m, cos A)
    sya = mp.sin(A)/m
    dya = mp.cos(A)
    # middle: rotate by -psi
    c, sn = mp.cos(psi), mp.sin(psi)
    syb = c*sya + sn*dya
    dyb = -sn*sya + c*dya
    # right: w = (ms y, y') rotates by -B; y(1) = 0  <=>  cos B * ms y(b) + sin B * y'(b) = 0
    val = mp.cos(B)*(m*syb) + mp.sin(B)*dyb
    return val

def solve_modes(a, b, m, kmax=6):
    # find eigenvalues s_k via bracketing y_end(s)=0, s>0
    roots = []
    # scan to find brackets
    s = mp.mpf('0.01')
    ds = mp.mpf('0.01')
    prev = y_end(s, a, b, m)
    brackets = []
    while len(roots) < kmax and s < 200:
        s2 = s + ds
        v2 = y_end(s2, a, b, m)
        if prev == 0 or v2*prev < 0:
            brackets.append((s, s2))
            # bisect
            lo, hi = s, s2
            flo = prev
            for _ in range(400):
                mid = (lo+hi)/2
                fm = y_end(mid, a, b, m)
                if fm*flo <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            roots.append((lo+hi)/2)
            if len(roots) >= kmax:
                break
        s, prev = s2, v2
    return roots

# Test configuration
m = mp.sqrt(4)
a = mp.mpf('0.3'); b = mp.mpf('0.7')
roots = solve_modes(a, b, m, kmax=4)
print("R=4, a=0.3,b=0.7")
print("s1,s2,s3,s4 =", [mp.nstr(r, 20) for r in roots])

for k in range(2):
    s = roots[k]
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    print(f"\n-- mode {k+1}: s={mp.nstr(s,20)}")
    print("A,psi,B =", mp.nstr(A,15), mp.nstr(psi,15), mp.nstr(B,15))
    print("alpha(A), alpha(B):", mp.nstr(alpha(A,m),15), mp.nstr(alpha(B,m),15))
    print("psi + alpha(A)+alpha(B) =", mp.nstr(psi+alpha(A,m)+alpha(B,m),15), " vs pi =", mp.nstr(mp.pi,15))
    print("2pi - alpha(A)-alpha(B) - psi =", mp.nstr(2*mp.pi-alpha(A,m)-alpha(B,m)-psi,15))
