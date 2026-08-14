# densbc_v1_verify_free_params.py
# EVIDENCE script (not a proof).
# Verifies the packet claim that V = span{x^2,x^3}^\perp in H_beta (diagonal
# space, inner product (x^j,x^k)=delta_jk (k+1)^{2 beta}) makes the sparse
# family {p_n} dense for EVERY beta.
#
# STRICT-theory prediction tested here:
#   For beta > 3/2 density FAILS.  The recursion M_{2m} = m*M_2 does NOT hold
#   for all m because p_4 = x^4 - (4/3)x^2 involves degree 2 in R so p_4 is
#   NOT in V; hence M_4 becomes a FREE parameter.  A nonzero
#   w with even moments M_{2m} = (m/2) M_4 (m>=2), odd M_{2m+1} = (m/2) M_5
#   (m>=3), M_0=M_1=M_2=M_3=0 lies in H_beta for beta>3/2 and is orthogonal to
#   every KEPT p_n.
#
# Checks:
#   (1) ||w||_beta^2 = sum_m [(m/2)^2 (M4^2+M5^2) * (2m+1)^{-2b}] < inf for b>3/2
#   (2) (w,p_n)_beta = 0 for every KEPT p_n (those avoiding degrees 2,3).
#   (3) partial sums saturate -> w genuinely in H_beta.

def pn_coeff(n):
    """coeff dict degree->coeff of sparse p_n. leading coeff 1.
    p_0=1, p_1=x, p_{2m'}=x^{2m'}-(m'/(m'-1))x^{2m'-2}, odd similar."""
    if n == 0:
        return {0: 1.0}
    if n == 1:
        return {1: 1.0}
    if n % 2 == 0:
        mp = n // 2
        return {n: 1.0, n - 2: -(mp / (mp - 1))}
    else:
        mp = (n + 1) // 2
        return {n: 1.0, n - 2: -(mp / (mp - 1))}

def kept_indices(top, R):
    inds = []
    for n in range(0, top + 1):
        if n == 2 or n == 3:
            continue
        co = pn_coeff(n)
        if all(d not in R for d in co):
            inds.append(n)
    return inds

def Mk(k, M4, M5):
    if k == 0 or k == 1:
        return 0.0
    if k % 2 == 0:
        m = k // 2
        return (m / 2) * M4 if m >= 2 else 0.0
    else:
        m = (k + 1) // 2          # k=2m-1 odd>=5 -> m>=3
        return (m / 2) * M5 if m >= 3 else 0.0

def check(beta, R, M4, M5, top):
    # (w,p_n)_beta = sum_k M_k * c_k  (as derived in the script header comment)
    bad, imax, nind = 0, 0.0, 0
    for n in kept_indices(top, R):
        co = pn_coeff(n)
        val = sum(Mk(d, M4, M5) * c for d, c in co.items())
        if abs(val) > 1e-9:
            bad += 1
        imax = max(imax, abs(val))
        nind += 1
    return bad, imax, nind

if __name__ == "__main__":
    print("=== V = span{x^2,x^3}^\\perp in H_beta ; R = {2,3} ===")
    for beta in [1.5, 1.6, 2.0, 3.0]:
        # verify orthogonality to every kept p_n for the two free-param w's
        for (tag, M4, M5) in [("even-only w (M4 free)", 1.0, 0.0),
                              ("odd-only w (M5 free)", 0.0, 1.0),
                              ("both free", 1.0, 1.0)]:
            bad, imax, nind = check(beta, {2, 3}, M4, M5, 200)
            print(f"  beta={beta}  {tag:28s}: bad_ip={bad} max|ip|={imax:.2e} kept_count={nind}")
    print()
    print("=== h_beta norm of free-param w: ||w||^2 = sum_m (m/2)^2(M4^2+M5^2)(2m+1)^{-2b} ===")
    for beta in [1.5, 1.6, 2.0]:
        s = 0.0
        for N in [50, 100, 200, 400, 800, 1600]:
            s = sum(((m / 2) ** 2) * ((2 * m + 1) ** (-2 * beta)) for m in range(2, N + 1))
            print(f"  beta={beta} partial_sum at m<= {N}: {s:.6f}")
        print()
    print("conclusion (EVIDENCE): for beta > 3/2 a nonzero orthogonal w exists =>")
    print("  density of KEPT sparse family in V = span{x^2,x^3}^perp FAILS.")
    print("  This contradicts the packet's claim that M_{2m}=m M_2 forces w=0 for every beta.")
