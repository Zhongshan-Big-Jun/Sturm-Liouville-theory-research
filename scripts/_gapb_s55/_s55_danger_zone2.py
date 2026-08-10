import math
def Wf(x, m): return math.sin(x)**2 + m*m*math.cos(x)**2
def Jf(x, m): return math.sin(x)**2/Wf(x, m)
def rf(x, m, tau): return Jf(tau*x, m)/Jf(x, m)

print("test r(y) < r(x) on D = {x in (xmid,pi/2), y in (pi/2, min(pi-x, pi/tau))}?")
viol = 0; worst = None; total = 0; worst_pos = None
for R in [1.05, 1.5, 2, 4, 10, 50, 100, 1000, 1e4, 1e6]:
    m = math.sqrt(R)
    for tau in [1.05, 1.1, 1.22, 1.3, 1.5, 1.7, 1.9]:
        xmid = math.pi/(1+tau); xmax = math.pi/tau
        if xmid >= math.pi/2: continue
        if xmax <= math.pi/2: continue
        n = 300
        for i in range(1, n):
            x = xmid + (math.pi/2 - xmid)*i/n
            ymax = min(math.pi-x, xmax)
            if ymax <= math.pi/2: continue
            m2 = 300
            for j in range(1, m2):
                y = math.pi/2 + (ymax-math.pi/2)*j/m2
                total += 1
                d = rf(y,m,tau)-rf(x,m,tau)
                if not (d < 0):
                    viol += 1
                    if worst is None or d > worst[0]:
                        worst = (d, R, tau, x, y, rf(x,m,tau), rf(y,m,tau))
print("total samples:", total, "violations:", viol)
if worst:
    print("worst excess:", worst[0], "at R=%s tau=%s x=%s y=%s r(x)=%s r(y)=%s" % (worst[1], worst[2], round(worst[3],6), round(worst[4],6), worst[5], worst[6]))
