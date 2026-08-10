import mpmath as mp
mp.mp.dps = 30

def alpha(x, m):
    return mp.atan2(mp.sin(x)/m, mp.cos(x))

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def y_end(s, a, b, m):
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    sya = mp.sin(A)/m; dya = mp.cos(A)
    c, sn = mp.cos(psi), mp.sin(psi)
    syb = c*sya + sn*dya
    dyb = -sn*sya + c*dya
    return mp.cos(B)*(m*syb) + mp.sin(B)*dyb

def solve_modes(a, b, m, kmax=4):
    roots = []
    s = mp.mpf('0.01'); ds = mp.mpf('0.01')
    prev = y_end(s, a, b, m)
    while len(roots) < kmax and s < 100:
        s2 = s + ds
        v2 = y_end(s2, a, b, m)
        if prev == 0 or v2*prev < 0:
            lo, hi = s, s2; flo = prev
            for _ in range(300):
                mid = (lo+hi)/2
                fm = y_end(mid, a, b, m)
                if fm*flo <= 0: hi = mid
                else: lo, flo = mid, fm
            roots.append((lo+hi)/2)
            if len(roots) >= kmax: break
        s, prev = s2, v2
    return roots

print("=== 1. Mode identities on grid of (a,b) with sign-consistent mode2 ===")
m = mp.sqrt(4)
bad1 = bad2 = 0
for ia in range(1, 19):
    for ib in range(ia+1, 20):
        a = mp.mpf(ia)/20; b = mp.mpf(ib)/20
        roots = solve_modes(a, b, m, kmax=3)
        if len(roots) < 2: continue
        s1, s2 = roots[0], roots[1]
        A1 = m*s1*a; p1 = s1*(b-a); B1 = m*s1*(1-b)
        A2 = m*s2*a; p2 = s2*(b-a); B2 = m*s2*(1-b)
        # sign consistency of mode 2: y2(a)>0, y2(b)<0, exactly one zero in (a,b)
        if not (A2 < mp.pi and B2 < mp.pi): continue
        if not (mp.sin(A2)/m > 0): continue
        # y2(b): sy2(b) via transfer
        c,sn = mp.cos(p2), mp.sin(p2)
        sy2b = c*mp.sin(A2)/m + sn*mp.cos(A2)
        if not (sy2b < 0): continue
        # mode1 identity
        e1 = p1 + alpha(A1,m) + alpha(B1,m) - mp.pi
        # mode2 identity
        e2 = alpha(A2,m) + alpha(B2,m) + p2 - 2*mp.pi
        if abs(e1) > mp.mpf('1e-20'): bad1 += 1
        if abs(e2) > mp.mpf('1e-20'): bad2 += 1
print("grid 171 configs; mode1 identity failures:", bad1, "; mode2 identity failures:", bad2)

print("\n=== 2. P-sum for good roots (R=4) ===")
# symmetric good root approx
a = mp.mpf('0.3826'); b = 1-a
roots = solve_modes(a, b, m, kmax=2)
s1, s2 = roots
tau = s2/s1
A = m*s1*a; B = m*s1*(1-b); psi = s1*(b-a)
P = (alpha(tau*A,m)-tau*alpha(A,m)) + (alpha(tau*B,m)-tau*alpha(B,m))
print("tau =", mp.nstr(tau,15))
print("Psum =", mp.nstr(P,15), " (2-tau)pi =", mp.nstr((2-tau)*mp.pi,15))
print("Psum-(2-tau)pi =", mp.nstr(P-(2-tau)*mp.pi,15))

print("\n=== 3. r_tau monotone on (0, x_mid)? across R ===")
for R in [2, 4, 10, 100, 1000]:
    mR = mp.sqrt(R)
    tau = mp.mpf('1.5')
    xmid = mp.pi/(1+tau)
    # sample
    xs = [xmid*i/200 for i in range(1,200)]
    vals = [rtau(x, mR, tau) for x in xs]
    dec = all(vals[i] > vals[i+1] for i in range(len(vals)-1))
    print(f"R={R}: r_tau decreasing on (0,x_mid): {dec}")

print("\n=== 4. L0: tau^2 r_tau(x) > 1 on (0,x_mid) ===")
for R in [2,4,100]:
    mR = mp.sqrt(R)
    for tau in [mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('2')]:
        xmid = mp.pi/(1+tau)
        mn = min(rtau(x,mR,tau)*tau**2 for x in [xmid*i/500 for i in range(1,500)])
        print(f"R={R}, tau={tau}: min tau^2 r = {mp.nstr(mn,12)}")
