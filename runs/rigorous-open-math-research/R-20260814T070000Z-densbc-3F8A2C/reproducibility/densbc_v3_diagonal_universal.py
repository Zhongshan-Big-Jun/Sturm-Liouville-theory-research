# densbc_v3_diagonal_universal.py
# EVIDENCE script (not a proof).
# Universal check of the diagonal classification:
#   H_beta, V = {w_i = 0 for i in R} (coordinate constraints, R finite),
#   kept sparse family = {p_n : p_n in V}.
#
# Sparse family (CORRECTED odd support!): 
#   p_0 = 1, p_1 = x
#   p_{2m}      = x^{2m}     - (m/(m-1)) x^{2m-2}   (m >= 2, support {2m, 2m-2})
#   p_{2m+1}    = x^{2m+1}   - (m/(m-1)) x^{2m-1}   (m >= 2, support {2m+1, 2m-1})
# So p_n has SUPPORT {n, n-2} for n >= 4 (both parities); p_0,p_1 singletons.
#
# Claim C2: for beta > 3/2 and finite R, the kept sparse family is NOT dense in V.
# Proof sketch (STRICT): even degrees form a graph with edge (2m-2,2m) iff p_{2m}
# kept.  Maximal runs of consecutive unconstrained evens are components, each one
# free parameter y = M/(index).  The TOP run (above max constrained even) is
# infinite and unconstrained; setting its free param to a nonzero value yields
# M_{2m} = m*y (tail) with sum_m (my)^2 (2m+1)^{-2b} converging iff b > 3/2, so a
# nonzero w in V orthogonal to every kept p_n exists.  (Even side alone suffices.)
#
# Here we VERIFY by constructing the even-only and odd-only orthogonal w's with
# the CORRECT family and checking inner products = 0 with every kept p_n.

def pn_coeff(n):
    if n == 0: return {0: 1.0}
    if n == 1: return {1: 1.0}
    if n % 2 == 0:
        mp = n // 2
        return {n: 1.0, n - 2: -mp/(mp - 1)}
    else:
        mp = (n + 1) // 2
        return {n: 1.0, n - 2: -mp/(mp - 1)}

def kept_indices(top, R):
    return [n for n in range(0, top+1) if n not in (2, 3)
            and all(d not in R for d in pn_coeff(n))]

def even_base(R):
    c = max((e for e in R if e % 2 == 0), default=0)
    return c + 2            # lowest even degree of the top infinite even run

def odd_base(R):
    c = max((o for o in R if o % 2 == 1), default=1)
    return c + 2            # lowest odd degree of the top infinite odd run

def build_even_w(R):
    low = even_base(R)      # even degree; index m0 = low/2
    m0 = low // 2
    def M(k):
        if k % 2 == 0:
            m = k // 2
            if m >= m0:
                return m / m0       # M_{2m} = (m/m0) * (base M_{low} = 1)
        return 0.0
    return M

def build_odd_w(R):
    low = odd_base(R)       # odd degree 2m0-1 ; m0 = (low+1)/2
    m0 = (low + 1) // 2
    def M(k):
        if k % 2 == 1:
            m = (k + 1) // 2
            if m >= m0:
                return m / m0
        return 0.0
    return M

def check_orth(R, build, kin):
    M = build(R)
    bad = 0; imax = 0.0
    for n in kin:
        co = pn_coeff(n)
        val = sum(M(d) * c for d, c in co.items())
        if abs(val) > 1e-9:
            bad += 1
        imax = max(imax, abs(val))
    return bad, imax

def norm2(R, build, beta, top=4000):
    M = build(R)
    return sum(M(k) ** 2 * (k + 1) ** (-2 * beta) for k in range(0, top + 1))

if __name__ == "__main__":
    cases = [
        ("R={2,3} packet example", {2, 3}),
        ("R={2}", {2}),
        ("R={3}", {3}),
        ("R={2,4}", {2, 4}),
        ("R={3,5}", {3, 5}),
        ("R={0,1,2,3}", {0, 1, 2, 3}),
        ("R={1,2}", {1, 2}),
        ("R={2,3,11}", {2, 3, 11}),
        ("R=even up to 20", {2 * i for i in range(1, 11)}),
        ("R=all of 0..5", {0, 1, 2, 3, 4, 5}),
        ("R={2,3,100,101}", {2, 3, 100, 101}),
        ("R={7}", {7}),
    ]
    print("For each finite R and beta > 3/2, we exhibit a nonzero w in V, orthogonal to every kept p_n.")
    print("(bad_ev/bad_od = number of kept p_n with |(w,p_n)|>1e-9 for the even-only / odd-only w)\n")
    for beta in [1.6, 2.0, 3.0]:
        print(f"=== beta = {beta} ===")
        for name, R in cases:
            kin = kept_indices(1500, R)
            eb, ei = check_orth(R, build_even_w, kin)
            ob, oi = check_orth(R, build_odd_w, kin)
            # combined w
            Me = build_even_w(R); Mo = build_odd_w(R)
            def Mc(k): return Me(k) + Mo(k)
            cbad, cimax = 0, 0.0
            for n in kin:
                co = pn_coeff(n)
                val = sum(Mc(d) * c for d, c in co.items())
                if abs(val) > 1e-9: cbad += 1
                cimax = max(cimax, abs(val))
            ne = norm2(R, build_even_w, beta)
            no = norm2(R, build_odd_w, beta)
            status = "CONFIRMED" if (eb == 0 and ob == 0 and cbad == 0) else "CHECK"
            print(f"  {name:26s}: even(bad={eb:3d},||w||^2={ne:.5f}) odd(bad={ob:3d},||w||^2={no:.5f}) combined(bad={cbad:3d},max={cimax:.1e}) [{status}]")
        print()
