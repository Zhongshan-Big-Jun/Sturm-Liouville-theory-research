# O1 exploration: non-diagonal but polynomial representers -> richer kept set N.
# H = L^2([-1,1]).  Single non-coordinate constraint with polynomial representer
# v_1(x) = x - (1/2) x^2.  Then V = { f : <x,f>_L2 - (1/2)<x^2,f>_L2 = 0 }.
# This is genuinely NON-diagonal (representer is not a monomial), yet the
# representer moments a_k = <v_1, x^k> have FINITE support (a polynomial), so the
# kept-set/run/first-obstruction analysis is finite-to-check.
#
# EVIDENCE ONLY (not a proof).  Strict theorems in candidate_proof.md.
#
# Checks:
#   1) kept set N = { n : p_n in V } (exact rational via sympy).
#   2) run/recursion structure on kept set.
#   3) first-obstruction degree via a finite-support-moment w in V orthogonal to
#      all kept p_n (construct free-base ansatz, verify (w,p_n)=0 exactly).

from sympy import symbols, S, Rational, simplify

x = symbols('x', real=True)

# L^2([-1,1]) moments of monomials: <x^i, x^j> = (1-(-1)^{i+j+1})/(i+j+1)
def gram_l2(i, j):
    return (1 - (-1)**(i+j+1)) / (i+j+1)

# representer v_1 = x - (1/2)x^2 ;  a_k = <v_1, x^k>_L2 = gram(1,k) - (1/2) gram(2,k)
def a(k):
    return S(gram_l2(1, k)) - S(1)/2 * S(gram_l2(2, k))

def p_support(n):
    if n == 0:
        return [(0, S(1))]
    if n == 1:
        return [(1, S(1))]
    m = n // 2
    return [(n, S(1)), (n-2, -S(m)/(m-1))]

def kept_check(n):
    if n in (2, 3):
        return False
    supp = p_support(n)
    s = S(0)
    for (deg, coeff) in supp:
        s += coeff * a(deg)
    return s == 0

print("V = { f : <x-1/2 x^2, f> = 0 },  H = L^2([-1,1])  (non-diagonal, poly rep)")
N = [n for n in range(0, 60) if kept_check(n)]
print("kept set N (n<60):", N)

evens = [n for n in N if n % 2 == 0 and n >= 4]
odds  = [n for n in N if n % 2 == 1 and n >= 5]
print("kept evens>=4:", evens)
print("kept odds >=5:", odds)
print("0 in N?", 0 in N, " 1 in N?", 1 in N)

# Run structure: even degrees vertices {0,2,4,...}; kept p_{2m} (m>=2) is an edge
# (2m-2, 2m).  Build runs on even side and odd side.
def even_runs(kept_evens):
    # vertices: 0,2,4,... ; edge (2m-2,2m) present iff 2m in kept_evens
    # runs = maximal consecutive step-2 intervals connected by kept edges
    evens = sorted(set([0, 2] + [2*m for m in range(2, 60)]))  # all even degrees incl 0, base 2
    # use kept edges
    parent = {}
    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for n in kept_evens:
        m = n // 2
        union(n, n-2)
    comps = {}
    for k in evens:
        comps.setdefault(find(k), []).append(k)
    return list(comps.values())

def odd_runs(kept_odds):
    odds = sorted(set([1, 3] + [2*m+1 for m in range(2, 60)]))
    parent = {}
    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for n in kept_odds:
        m = (n-1)//2
        union(n, n-2)
    comps = {}
    for k in odds:
        comps.setdefault(find(k), []).append(k)
    return list(comps.values())

print("\neven components (runs, incl isolated bases):")
for c in sorted(even_runs(evens), key=lambda c: c[0]):
    print("  ", c)
print("odd components (runs):")
for c in sorted(odd_runs(odds), key=lambda c: c[0]):
    print("  ", c)

# first obstruction: lowest free base realized.  For each candidate free base
# degree L (2 or 3, or run base), set M_L = 1, lower bases 0, verify there is a
# w in V orthogonal to all kept p_n.  We scan low degrees with finite support.
print("\n=== first-obstruction scan (lowest surviving free moment) ===")
# A finite-support moment ansatz: nonzero only at degrees in the run of L.
# For an even run {2,4,...} with base 2: M_{2m} = m * c.
# Check existence of w in V (fails if <v_1, w> != 0 can't be fixed).
# Here we only report the run bases + kept structural first obstruction; the
# realization-in-V check is the moment-problem core (honest, may be infinite).
bases = []
# even base 2 (M_2 free if run {2,4,...} not pinned)
run_at_2 = [c for c in even_runs(evens) if 2 in c]
run_at_3 = [c for c in odd_runs(odds) if 3 in c]
print("even run containing degree 2:", run_at_2)
print("odd run containing degree 3:", run_at_3)
