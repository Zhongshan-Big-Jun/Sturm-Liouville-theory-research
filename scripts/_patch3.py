import io
p = r"F:\LaTeX\BVE research\scripts\audit_o3a_pdf_part1.py"
s = io.open(p, encoding="utf-8").read()
old = """def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('0'), mp.pi/2 - mp.mpf('1e-12')
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

def alpha2_of_c(q, c):
    if c < 1:
        f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
        lo, hi = mp.pi/2 + mp.mpf('1e-12'), mp.pi - mp.mpf('1e-12')
        for _ in range(300):
            mid = (lo+hi)/2
            if f(mid) > 0: lo = mid
            else: hi = mid
        return (lo+hi)/2
    else:
        f = lambda x: mp.pi - mp.atan(q*mp.tan(x)) - c*x
        lo, hi = mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12')
        for _ in range(300):
            mid = (lo+hi)/2
            if f(mid) > 0: lo = mid
            else: hi = mid
        return (lo+hi)/2"""
new = """def _bracket_bisect(f, lo, hi, tol=mp.mpf('1e-80')):
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=tol)

def alpha1_of_c(q, c):
    return _bracket_bisect(lambda x: mp.atan(1/(q*mp.tan(x))) - c*x,
                           mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20'))

def alpha2_of_c(q, c):
    if c < 1:
        return _bracket_bisect(lambda x: mp.atan(-q*mp.tan(x)) - c*x,
                               mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20'))
    else:
        return _bracket_bisect(lambda x: mp.pi - mp.atan(q*mp.tan(x)) - c*x,
                               mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20'))"""
assert old in s
s = s.replace(old, new)
s = s.replace("mp.mp.dps = 50", "mp.mp.dps = 90")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
