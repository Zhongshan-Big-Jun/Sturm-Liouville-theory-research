# densbc_v4_finite_run_phenomenon.py
# EVIDENCE (not a proof).
# Tests the (surprising) finite-run phenomenon in the diagonal H_beta:
#   A FINITE maximal run of unconstrained same-parity degrees carries a free
#   parameter that is never killed by H_beta convergence (finite support => in
#   H_beta for every beta).  Hence a coordinate constraint R that creates a
#   FINITE run destroys density even at beta <= 3/2.
#
# Prediction (STRICT theory):
#   density of kept sparse family in V (beta <= 3/2) fails iff both:
#     * there is a finite even run, OR a finite odd run.
#   A finite even run exists iff exists constrained even 2q (q>=2 i.e. >=4) with
#   2q-2 not in R.  (e.g. R={4}: run [2,2] singleton; R={2,6}: run [4,4].)
#   If no finite run (e.g. R={2,3},{2},{2,3,4},{2,4}), density holds at b<=3/2.
#
# We construct the finite-run orthogonal w explicitly and verify orthogonality
# to every kept p_n, and membership in H_beta (finite support), at beta <= 3/2.

def pn_coeff(n):
    if n == 0: return {0: 1.0}
    if n == 1: return {1: 1.0}
    mp = n // 2 if n % 2 == 0 else (n + 1) // 2
    return {n: 1.0, n - 2: -mp / (mp - 1)}

def kept_indices(top, R):
    return [n for n in range(0, top + 1) if n not in (2, 3)
            and all(d not in R for d in pn_coeff(n))]

def find_finite_runs(R, parity):
    """Maximal runs of unconstrained degrees of given parity (even True/odd False)
    among degrees >= (2 if even else 1).  Return list of (low, high) finite runs."""
    if parity:
        ds = [d for d in range(2, 2000, 2) if d not in R]
    else:
        ds = [d for d in range(1, 2000, 2) if d not in R]
    runs = []
    if not ds:
        return runs
    lo = hi = ds[0]
    for d in ds[1:]:
        if d == hi + 2:
            hi = d
        else:
            runs.append((lo, hi)); lo = hi = d
    runs.append((lo, hi))          # top run may be infinite-looking up to 1998
    infinite = [r for r in runs if r[1] >= 1999]
    finite = [r for r in runs if r[1] < 1999]
    return finite

def parity_has_finite_even(R):
    return len(find_finite_runs(R, True)) > 0

def parity_has_finite_odd(R):
    return len(find_finite_runs(R, False)) > 0

def build_finite_run_w(low, step, base_degree):
    # moments on the run [low, high] with M_{low}=1 free; for even low, M_{2m}=(m/m0)
    # Actually simpler: put M = 1 at base_degree only (this is orthogonal if the
    # base is an isolated/finite-run base and all kept p_n touching it are excluded).
    # But to be safe we place moments satisfying all kept recursions within the run.
    pass

def test_finite_run(R, beta, top=600):
    """For a constraint R with a finite run, find the lowest finite run, build w
    supported there, verify orthogonality to all kept p_n and finite norm."""
    # find lowest finite even run or odd run
    kin = kept_indices(top, R)
    res = []
    for parity, step in [(True, 2), (False, 2)]:
        fr = find_finite_runs(R, parity)
        for (lo, hi) in fr:
            # base_degree = lo ; build moments M on the run so all kept recursions hold
            # For even run: degrees lo, lo+2, ..., hi. base m0 = lo//2.
            if parity:
                m0 = lo // 2
                def M(k):
                    if k % 2 == 0:
                        m = k // 2
                        if lo <= k <= hi and m >= m0:
                            return m / m0
                    return 0.0
            else:
                m0 = (lo + 1) // 2
                def M(k):
                    if k % 2 == 1:
                        m = (k + 1) // 2
                        if lo <= k <= hi and m >= m0:
                            return m / m0
                    return 0.0
            bad, imax = 0, 0.0
            for n in kin:
                co = pn_coeff(n)
                val = sum(M(d) * c for d, c in co.items())
                if abs(val) > 1e-9:
                    bad += 1
                imax = max(imax, abs(val))
            nrm = sum(M(k) ** 2 * (k + 1) ** (-2 * beta) for k in range(0, top + 1))
            res.append((parity, lo, hi, bad, imax, nrm))
            break  # only need one finite run
        # also only need one parity
    return kin, res

if __name__ == "__main__":
    cases = [
        ("R={4}   (finite singleton run at 2)", {4}, "expect NON-dense at beta<=3/2"),
        ("R={2,6} (finite run [4,4])",         {2, 6}, "expect NON-dense at beta<=3/2"),
        ("R={5}   (finite singleton odd run at 1?)", {5}, "expect NON-dense at beta<=3/2"),
        ("R={4,8} (finite run [2,2])",         {4, 8}, "expect NON-dense at beta<=3/2"),
        ("R={2,3} (no finite run)",            {2, 3}, "expect dense at beta<=3/2 (no finite run)"),
        ("R={2,4} (no finite even run)",       {2, 4}, "expect dense at beta<=3/2"),
        ("R={2}   (no finite run)",            {2},    "expect dense at beta<=3/2"),
    ]
    for beta in [1.0, 1.4, 1.5]:
        print(f"=== beta = {beta} (<= 3/2) ===")
        for name, R, pred in cases:
            kin, res = test_finite_run(R, beta)
            if res:
                p, lo, hi, bad, imax, nrm = res[0]
                tag = "NON-DENSE(found finite-run w)" if bad == 0 else "CHECK"
                print(f"  {name:36s} pred='{pred}'")
                print(f"      finite run parity={'even' if p else 'odd'} deg[{lo}..{hi}] bad_ip={bad} max={imax:.1e} ||w||^2={nrm:.5f} -> {tag}")
            else:
                print(f"  {name:36s} pred='{pred}'      (no finite run found -> density not obstructed by finite run)")
        print()
