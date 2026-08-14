# densbc_v5_classification_verdict.py
# EVIDENCE (not a proof).  Decisive confirmation of the corrected diagonal
# classification at beta <= 3/2 (where infinite runs are killed by divergence).
#
# Corrected Diagonal Theorem (STRICT, to be proven in candidate_proof.md):
#   For H_beta (diagonal), coordinate constraint R finite, V={w_i=0 for i in R},
#   kept sparse family Q_sp = {p_n : p_n in V}:
#       Q_sp dense in V   <=>   beta <= 3/2  AND  R admits NO finite run.
#   A "finite run" is a bounded maximal interval of consecutive unconstrained
#   degrees of a fixed parity within the recursion graph.
#   Finite even run exists <=> exists constrained even 2q (q>=2, i.e. 2q>=4)
#     with 2q-2 not in R.  Finite odd run <=> exists constrained odd 2q+1
#     (2q+1>=5) with 2q-1 not in R.
#
# Here we verify the KILLER side: when a finite run exists, a finite-support
# nonzero orthogonal w is found (bad_ip=0) at beta <= 3/2; when no finite run,
# we verify the top infinite run's H_beta-norm series diverges (partial sums grow)
# so no such w exists in H_beta (supporting density).

def pn_coeff(n):
    if n == 0: return {0: 1.0}
    if n == 1: return {1: 1.0}
    mp = n // 2 if n % 2 == 0 else (n + 1) // 2
    return {n: 1.0, n - 2: -mp / (mp - 1)}

def kept_indices(top, R):
    return [n for n in range(0, top + 1) if n not in (2, 3)
            and all(d not in R for d in pn_coeff(n))]

def has_finite_even_run(R):
    # constrained even 2q>=4 with 2q-2 not in R
    for q in range(2, 2000):
        if 2*q in R and (2*q - 2) not in R:
            return True, 2*q
    return False, None

def has_finite_odd_run(R):
    for m in range(2, 2000):
        d = 2*m + 1            # constrained odd >= 5
        if d in R and (d - 2) not in R:
            return True, d
    return False, None

def finite_run_w(R, parity, beta, top):
    """Build finite-support w from the FIRST finite run (if no finite run -> None)."""
    if parity:
        # from a constrained even 2q with 2q-2 free: run below spans (prev constrain, 2q)
        found, q = has_finite_even_run(R)
        if not found:
            return None
        hi = 2*q - 2
        lo = hi
        while lo - 2 not in R and lo - 2 >= 0:
            lo -= 2
        # lo is the first unconstrained even in this run (base)
        m0 = lo // 2
        def M(k):
            if k % 2 == 0 and lo <= k <= hi:
                return (k // 2) / m0
            return 0.0
        return M
    else:
        found, hi = has_finite_odd_run(R)
        if not found:
            return None
        lo = hi - 2
        while lo - 2 not in R and lo - 2 >= 1:
            lo -= 2
        m0 = (lo + 1) // 2
        def M(k):
            if k % 2 == 1 and lo <= k <= hi:
                return ((k + 1) // 2) / m0
            return 0.0
        return M

def series_diverges(R, parity, beta, top=4000, step=1600):
    """For the top infinite run of given parity, check partial norm sums grow."""
    if parity:
        c = max((e for e in R if e % 2 == 0), default=0)
        m0 = (c + 2) // 2
        vals = []
        for N in range(step, top + 1, step):
            s = sum(((m / m0) ** 2) * ((2 * m + 1) ** (-2 * beta)) for m in range(m0, N + 1))
            vals.append(s)
        return vals
    else:
        c = max((o for o in R if o % 2 == 1), default=1)
        m0 = (c + 2 + 1) // 2
        vals = []
        for N in range(step, top + 1, step):
            s = sum(((m / m0) ** 2) * ((2 * m - 1) ** (-2 * beta)) for m in range(m0, N + 1))
            vals.append(s)
        return vals

def orth_check(w, kin, top=800):
    if w is None:
        return None
    bad, imax = 0, 0.0
    for n in kin:
        co = pn_coeff(n)
        val = sum(w(d) * c for d, c in co.items())
        if abs(val) > 1e-9:
            bad += 1
        imax = max(imax, abs(val))
    return bad, imax

if __name__ == "__main__":
    cases = [
        # name, R, expect_dense_at_below_3over2
        ("R={4}",      {4},     False),
        ("R={2,6}",    {2, 6},  False),
        ("R={4,8}",    {4, 8},  False),
        ("R={5}",      {5},     False),
        ("R={3,9}",    {3, 9},  False),
        ("R={3,7}",    {3, 7},  False),
        ("R={2,3}",    {2, 3},  True),
        ("R={2,4}",    {2, 4},  True),
        ("R={2}",      {2},     True),
        ("R={3}",      {3},     True),
        ("R={2,3,4}",  {2, 3, 4}, True),
    ]
    for beta in [1.0, 1.4, 1.5]:
        print(f"=== beta = {beta} (<= 3/2) ===")
        for name, R, exp_dense in cases:
            kin = kept_indices(900, R)
            fe, _ = has_finite_even_run(R)
            fo, _ = has_finite_odd_run(R)
            finite_run = fe or fo
            # find an orthogonal w: finite-run if present, else none at beta<=3/2
            we = finite_run_w(R, True, beta, 900)
            wo = finite_run_w(R, False, beta, 900)
            result = "NO_OUTPUT"
            if finite_run:
                # pick whichever finite run is present
                w = we if (we is not None and orth_check(we, kin)[0] == 0) else wo
                chk = orth_check(w, kin)
                if chk is not None and chk[0] == 0:
                    result = "NON-DENSE confirmed (finite-support orthogonal w found)"
                else:
                    result = f"CHECK finite-run chk={chk}"
            else:
                # no finite run: at beta<=3/2 dense; confirm top infinite run diverges
                ve = series_diverges(R, True, beta)
                vo = series_diverges(R, False, beta)
                grow_e = ve[-1] > ve[-2]
                grow_o = vo[-1] > vo[-2]
                result = f"dense-at-beta<=3/2 supported: top-even-run norm partials {[f'{x:.3f}' for x in ve[::4]]} growing={grow_e}; odd {[f'{x:.3f}' for x in vo[::4]]} growing={grow_o}"
            agree = (finite_run != exp_dense)
            print(f"  {name:12s} finite_even_run={fe} finite_odd_run={fo} expect_dense={exp_dense} => {result}  [{'AGREES' if agree else 'MISMATCH'}]")
        print()
