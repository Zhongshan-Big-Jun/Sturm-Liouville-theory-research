import mpmath as mp
mp.mp.dps = 40
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def bracket(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    B1 = A*cg - 2*sg
    return dict(M=M, B2=B2, B4=B4, B5=B5, B7=B7, G5=G5, B1=B1)
N = 4000
h = mp.mpf('1e-9')
for name in ['M','B2','B4','B5','B7','G5']:
    vals = [bracket(glo+mp.mpf(i)*(ghi-glo)/N)[name] for i in range(N+1)]
    mn = min(vals); mx = max(vals)
    # derivative sign changes
    ds = []
    for i in range(1, N):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        d = (bracket(g+h)[name]-bracket(g-h)[name])/(2*h)
        ds.append(float(d))
    signch = 0
    for i in range(1, len(ds)):
        if ds[i-1]*ds[i] < 0: signch += 1
    print('%s: [%.5f, %.5f]  deriv: [%.2f, %.2f]  sign changes: %d' % (name, mn, mx, min(ds), max(ds), signch))
# locate extrema
for name in ['M','B2','B4','B5','B7','G5']:
    vals = [(bracket(glo+mp.mpf(i)*(ghi-glo)/N)[name], float(glo+mp.mpf(i)*(ghi-glo)/N)) for i in range(N+1)]
    mn = min(vals); mx = max(vals)
    print('%s: min %.5f at g=%.4f ; max %.5f at g=%.4f' % (name, mn[0], mn[1], mx[0], mx[1]))
