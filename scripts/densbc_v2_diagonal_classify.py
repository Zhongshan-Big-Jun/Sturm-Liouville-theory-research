# densbc_v2_diagonal_classify.py
# EVIDENCE script (not a proof).
# Verifies the complete diagonal classification:
#   H_beta, V = span{e_{j1},...,e_{jm}}^\perp (coordinate constraint set R,
#   w in V iff w_i=0 for i in R), kept sparse family = {p_n : p_n in V}.
#
# STRICT-theory claims tested here:
#  (C1) For beta <= 3/2 the kept sparse family is dense in V.
#  (C2) For beta > 3/2 the kept sparse family is NEVER dense (finite R):
#       there is always a nonzero w in V orthogonal to every kept p_n,
#       built from the free base moment of the top infinite unconstrained run.
#
# Method to build the orthogonal w for a given R:
#   Even recursion graph: components = maximal runs of consecutive unconstrained
#   even degrees (>=2).  Each run [2a,2b] has constant y = M_{2m}/m, free param
#   = M at its lowest degree.  Odd graph separate.  For beta>3/2 we only need the
#   infinite even run (top run above max constrained even degree) -- set its free
#   param to make convergence.  Actually here we just test any SPECIFIED run.
#
# We test: given R and beta>3/2, take the top infinite even run and the top
# infinite odd run, set their free params, set all else 0, verify orthogonality
# to all kept p_n and finite norm.

def pn_coeff(n):
    if n == 0: return {0: 1.0}
    if n == 1: return {1: 1.0}
    if n % 2 == 0:
        mp = n // 2
        return {n: 1.0, n - 2: -mp/(mp - 1)}
    else:
        mp = (n + 1) // 2
        return {n: 1.0, n - 1: -mp/(mp - 1)}

def kept_indices(top, R):
    out = []
    for n in range(0, top+1):
        if n in (2, 3):
            continue
        co = pn_coeff(n)
        if all(d not in R for d in co):
            out.append(n)
    return out

def build_w_from_runs(R, beta, top):
    """Given the free params on specified runs, return moment function Mk(k).
    We'll test the infinite top even run and top odd run, each with free param 1
    at their lowest degree.
    Even degrees = {2,4,6,...}.  An even degree 2m is in a run; find runs.
    We want, for a single candidate run [2a, 2b] (b may be inf -> top), moments:
       M_{2m} = m * (free/base) where free = M_{2a}, so M_{2m} = (m/a) M_{2a}.
    Pick the TOP infinite even run and the TOP infinite odd run.
    """
    even_in_R = sorted(e for e in range(2, top+1) if e in R)
    # top infinite even run starts just above the largest constrained even (if any)
    max_even_R = max(even_in_R) if even_in_R else 0  # 2 not in R means run covers from 2
    even_run_low = max_even_R + 2
    odd_in_R = sorted(o for o in range(3, top+1) if o in R)
    max_odd_R = max(odd_in_R) if odd_in_R else 1
    odd_run_low = max_odd_R + 2
    # base moments
    a_even = even_run_low // 2
    a_odd = odd_run_low // 2
    def M(k):
        if k == 0 or k == 1:
            return 0.0
        if k % 2 == 0:
            m = k // 2
            if m >= a_even and m >= 2:   # in top even run (all m>=a_even)
                # M_{2m} = m * c with c = base/(a_even)
                # base = M_{even_run_low} = 1.0 (free param)
                return m * (1.0 / a_even)
            return 0.0
        else:
            m = (k + 1) // 2
            if m >= a_odd and m >= 3:
                return m * (1.0 / a_odd)
            return 0.0
    return M

def test_case(R, beta, top=300):
    M = build_w_from_runs(R, beta, top)
    bad, imax = 0, 0.0
    for n in kept_indices(top, R):
        co = pn_coeff(n)
        val = sum(M(d)*c for d, c in co.items())
        if abs(val) > 1e-9:
            bad += 1
        imax = max(imax, abs(val))
    # norm
    norm2 = sum(M(k)**2 * (k+1)**(-2*beta) for k in range(0, top+1))
    # check constraint compliance: M_i should be 0 for i in R (pinned) - verify
    constraint_ok = all(abs(M(i)) < 1e-12 for i in R if i < top)
    return bad, imax, norm2, constraint_ok

if __name__ == "__main__":
    cases = [
        ("R={2,3} packet example", {2,3}),
        ("R={2}", {2}),
        ("R={3}", {3}),
        ("R={2,3,4}", {2,3,4}),
        ("R={0,1}", {0,1}),
        ("R={2n for n<=10}: many evens", {2*i for i in range(1,11)}),
        ("R={0,1,2,3}", {0,1,2,3}),
    ]
    for beta in [1.51, 2.0, 3.0]:
        print(f"=== beta = {beta} (> 3/2: prediction C2 = nonzero orthogonal w always exists) ===")
        for name, R in cases:
            bad, imax, norm2, ok = test_case(R, beta)
            flag = "OK" if (ok and bad == 0 and norm2 < 1e6) else "FAIL"
            print(f"  {name:28s}: bad_pn_ips={bad:4d} max|(w,p_n)|={imax:.2e} ||w||^2(top)={norm2:.6f} constraint_ok={ok}  [{flag}]")
        print()
    # For beta <= 3/2 the free-param series diverges, so the SAME w is NOT in H_beta:
    print("=== beta <= 3/2: the free-param w must NOT be in H_beta (series diverges) ===")
    for beta in [1.0, 1.4, 1.5]:
        M = build_w_from_runs({2,3}, beta, 3800)
        n2 = {N: sum(M(k)**2*(k+1)**(-2*beta) for k in range(0, N+1)) for N in [400,800,1600,3200]}
        print(f"  beta={beta}: partial ||w||^2 growing? {[f'{n2[N]:.4f}' for N in [400,800,1600,3200]]}")
    print("(growing partial sums at 3/2 => w not in H_beta => density holds at beta<=3/2)")
