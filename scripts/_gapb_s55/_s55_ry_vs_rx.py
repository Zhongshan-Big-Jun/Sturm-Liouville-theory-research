import math
def Wf(x, m): return math.sin(x)**2 + m*m*math.cos(x)**2
def Jf(x, m): return math.sin(x)**2/Wf(x, m)
def rf(x, m, tau): return Jf(tau*x, m)/Jf(x, m)

# test: x in (xmid, pi/2), y in (pi/2, pi-x): is r(y) > r(x) always?
print("test r(y) > r(x) for x in (xmid,pi/2), y in (pi/2, pi-x]")
viol = 0; worst = None
for R in [1.05, 1.5, 2, 4, 10, 50, 100, 1000, 1e4, 1e6]:
    m = math.sqrt(R)
    for tau in [1.05, 1.1, 1.22, 1.3, 1.5, 1.7, 1.9, 2.5, 3.0]:
        xmid = math.pi/(1+tau)
        if xmid >= math.pi/2: continue
        n = 400
        for i in range(1, n):
            x = xmid + (math.pi/2 - xmid)*i/n
            # y in (pi/2, pi-x)
            m2 = 200
            for j in range(1, m2):
                y = math.pi/2 + (math.pi-x-math.pi/2)*j/m2
                if y <= math.pi/2: continue
                d = rf(y,m,tau) - rf(x,m,tau)
                if d <= 0:
                    viol += 1
                    if worst is None or d < worst[0]:
                        worst = (d, R, tau, x, y)
print("violations:", viol)
if worst: print("worst:", worst)
