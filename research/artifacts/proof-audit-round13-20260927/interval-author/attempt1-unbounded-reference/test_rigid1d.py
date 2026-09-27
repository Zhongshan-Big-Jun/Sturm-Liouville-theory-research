"""R13-03/04 author selfchecks. Exact Fraction tests, no numerical oracle.

Run with python3 -B and python3 -B -O. unittest assertions remain active in -O.
The E1 function is read from the actual current source, with only named AST
definitions/constants executed; the generator's output-producing body is not run.
"""
import ast
from fractions import Fraction as F
import hashlib
import math
from pathlib import Path
import sys
import types
import unittest

sys.dont_write_bytecode = True
REPO = Path('/mnt/f/LaTeX/BVE research')
HERE = Path(__file__).resolve().parent


def load_source(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    data = path.read_bytes()
    exec(compile(data.decode('utf-8-sig'), str(path), 'exec'), module.__dict__)
    print(f'SOURCE {path} sha256={hashlib.sha256(data).hexdigest()}', flush=True)
    return module


R = load_source(REPO / 'misc/rigid1d.py', 'r13_actual_rigid1d')
I, D, D2 = R.I, R.D, R.D2


def atan_series_reference(v, n=96):
    """One-sided geometric-integral remainder for 0 <= v <= 1/2."""
    if not 0 <= v <= F(1, 2):
        raise ValueError('reference series domain')
    s = sum(((-1)**k * v**(2*k+1) / (2*k+1) for k in range(n)), F(0))
    next_term = (-1)**n * v**(2*n+1) / (2*n+1)
    return min(s, s+next_term), max(s, s+next_term)


def pi_reference():
    a, b = atan_series_reference(F(1, 5)), atan_series_reference(F(1, 239))
    return 16*a[0]-4*b[1], 16*a[1]-4*b[0]


PREF = pi_reference()


def atan_reference(v):
    v = F(v)
    if v < 0:
        a, b = atan_reference(-v)
        return -b, -a
    if v > 1:
        a, b = atan_reference(1/v)
        return PREF[0]/2-b, PREF[1]/2-a
    if v > F(1, 2):
        # Different inner reduction from production: addition at 1/2.
        a, b = atan_series_reference(F(1, 2))
        c, d = atan_series_reference((v-F(1, 2))/(1+v/2))
        return a+c, b+d
    return atan_series_reference(v)


def trig_reference(v, n=48):
    v = F(v)
    s = sum(((-1)**k * v**(2*k+1)/math.factorial(2*k+1)
             for k in range(n)), F(0))
    c = sum(((-1)**k * v**(2*k)/math.factorial(2*k)
             for k in range(n)), F(0))
    rs = abs(v)**(2*n+1)/math.factorial(2*n+1)
    rc = abs(v)**(2*n)/math.factorial(2*n)
    return (s-rs, s+rs), (c-rc, c+rc)


def load_e1_definitions():
    path = REPO / 'misc/e1_certgen.py'
    data = path.read_bytes()
    tree = ast.parse(data.decode('utf-8-sig'), filename=str(path))
    names = {'GLO', 'GHI', 'mconst', 'PRIM_PTS', 'deriv_facts', 'point_facts'}
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'comps2':
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            assigned = {sub.id for target in node.targets for sub in ast.walk(target)
                        if isinstance(sub, ast.Name)}
            if assigned and assigned <= names:
                nodes.append(node)
    found = {node.name for node in nodes if isinstance(node, ast.FunctionDef)}
    if found != {'comps2'}:
        raise RuntimeError('actual comps2 definition missing')
    namespace = {name: getattr(R, name) for name in
                 ('I', 'D2', 'd2_sin', 'd2_cos', 'd2_atan', 'PI')}
    namespace['F'] = F
    fragment = ast.Module(body=nodes, type_ignores=[])
    exec(compile(fragment, str(path), 'exec'), namespace)
    mode = 'optimized' if sys.flags.optimize else 'normal'
    (HERE / f'executed_e1_fragment.{mode}.py').write_text(ast.unparse(fragment)+'\n')
    print(f'E1_SOURCE {path} sha256={hashlib.sha256(data).hexdigest()}', flush=True)
    print('E1_EXECUTION named definitions/constants only; no generator output body', flush=True)
    return namespace


E1 = load_e1_definitions()


class ExactChecks(unittest.TestCase):
    def enclosure(self, outer, inner):
        self.assertIsInstance(outer.lo, F)
        self.assertIsInstance(outer.hi, F)
        self.assertLessEqual(outer.lo, inner[0])
        self.assertGreaterEqual(outer.hi, inner[1])

    def same(self, a, b):
        self.assertEqual((a.lo, a.hi), (b.lo, b.hi))

    def test_cosine_exact_false_positive_witness_is_rejected(self):
        x = I(F(-1, 10), F(1, 10))
        self.enclosure(R.I_cos(x), (F(1), F(1)))
        self.assertFalse((I(F(997, 1000))-R.I_cos(x)).is_pos())
        self.assertEqual(F(997, 1000)-1, F(-3, 1000))

    def test_wide_sine_exact_false_positive_witness_is_rejected(self):
        self.assertLess(PREF[1]/2, 2)
        self.enclosure(R.I_sin(I(-2, 2)), (F(1), F(1)))
        self.assertFalse((I(F(19, 20))-R.I_sin(I(-2, 2))).is_pos())
        self.assertEqual(F(19, 20)-1, F(-1, 20))

    def test_internal_critical_points(self):
        for k in range(-8, 9):
            # cos(k*pi)=(-1)^k, sin((k+1/2)*pi)=(-1)^k.
            p = I(*PREF)*k
            self.enclosure(R.I_cos(p+I(F(-1, 1000), F(1, 1000))),
                           (F((-1)**k), F((-1)**k)))
            q = I(*PREF)*F(2*k+1, 2)
            self.enclosure(R.I_sin(q+I(F(-1, 1000), F(1, 1000))),
                           (F((-1)**k), F((-1)**k)))
        self.enclosure(R.I_cos(I(-4, 4)), (F(-1), F(1)))

    def test_offset_domain_and_zero(self):
        self.same(R._sc_u(0)[0], I(0))
        self.same(R._sc_u(0)[1], I(1))
        with self.assertRaises(ValueError):
            R._sc_u(F(-1, 10**20))
        for w in (F(1, 10**6), F(1, 10), F(999, 1000), F(1),
                  F(1001, 1000), F(2), F(100)):
            s, c = R._sc_u(w)
            self.enclosure(c, (F(1), F(1)))
            self.enclosure(s, (F(0), F(0)))
            if w > 1:
                self.same(s, I(-1, 1))
                self.same(c, I(-1, 1))
            else:
                sr, cr = trig_reference(w)
                self.enclosure(s, sr)
                self.enclosure(c, cr)

    def test_point_lagrange_envelopes_beyond_alternating_term_domain(self):
        for x in (F(-32), F(-10), F(-7, 2), F(0), F(1, 10),
                  F(13, 10), F(7, 2), F(10), F(32)):
            s, c = R._sc_series(x)
            sr, cr = trig_reference(x, n=96)
            self.enclosure(s, sr)
            self.enclosure(c, cr)
        for x in (10**6, -10**6):
            self.same(R.I_sin(I(x)), I(-1, 1))
            self.same(R.I_cos(I(x)), I(-1, 1))

    def test_structured_interval_envelopes_and_fraction_endpoints(self):
        count = 0
        for c in map(F, (-8, -4, -2, -1, 0, 1, 2, 4, 8)):
            for w in (F(0), F(1, 1000), F(1, 10), F(1), F(1001, 1000), F(2)):
                x = I(c-w, c+w)
                s, co = R.I_sin(x), R.I_cos(x)
                self.assertGreaterEqual(s.lo, -1)
                self.assertLessEqual(s.hi, 1)
                self.assertGreaterEqual(co.lo, -1)
                self.assertLessEqual(co.hi, 1)
                for t in (c-w, c-w/2, c, c+w/2, c+w):
                    sr, cr = trig_reference(t)
                    self.enclosure(s, sr)
                    self.enclosure(co, cr)
                    count += 2
        print(f'EXACT_STRUCTURED_TRIG_PROBES {count}; finite regression, not the proof', flush=True)

    def test_sine_oddness_cosine_evenness(self):
        for x in (I(-4, 2), I(F(1, 10), F(11, 10)), I(7), I(-2, 2)):
            self.same(R.I_sin(-x), -R.I_sin(x))
            self.same(R.I_cos(-x), R.I_cos(x))

    def test_atan_crossing_one_zero_and_negative_one(self):
        for lo, hi in ((F(9, 10), F(11, 10)), (F(0), F(2)),
                       (F(-11, 10), F(-9, 10)), (F(-2), F(2)),
                       (F(-100), F(-2)), (F(-1, 10), F(1, 10)),
                       (F(1), F(1)), (F(0), F(0))):
            x = I(lo, hi)
            result = R.I_atan(x)
            self.enclosure(result, (atan_reference(lo)[0], atan_reference(hi)[1]))
            self.same(R.I_atan(-x), -result)
        self.same(R.I_atan(I(1)), R.PI/4)
        self.same(R.I_atan(I(0)), I(0))

    def test_atan_reduction_boundaries_and_accuracy(self):
        eps = F(1, 10**8)
        for x in (F(1, 10**6), F(1, 2)-eps, F(1, 2), F(1, 2)+eps,
                  F(1)-eps, F(1), F(1)+eps, F(2), F(10**6)):
            self.enclosure(I(*R._atan_point(x)), atan_reference(x))
            self.assertLess(I(*R._atan_point(x)).width(), F(1, 10**12))
        self.assertLess(R.I_atan(I(1)).width(), F(1, 10**25))

    def test_atan_series_explicit_domain_and_length_guards(self):
        for v in (F(-1, 10), F(11, 10)):
            with self.assertRaises(ValueError):
                R._atan1_series(v)
        for n in (0, -1):
            with self.assertRaises(ValueError):
                R._atan1_series(F(1, 5), n)
        for n in (F(2), 2.0, '2'):
            with self.assertRaises(TypeError):
                R._atan1_series(F(1, 5), n)
        for n in (1, 2, 3, 22):
            self.enclosure(I(*R._atan1_series(F(1, 5), n)), atan_reference(F(1, 5)))
        self.enclosure(I(*R._atan1_series(F(1), 22)), (PREF[0]/4, PREF[1]/4))

    def test_pi_enclosure(self):
        self.enclosure(R.PI, PREF)
        self.assertLess(R.PI.width(), F(1, 10**30))

    def test_power_rejections_survive_optimization(self):
        for cls in (I, D, D2):
            for n in (-1, -2):
                with self.subTest(cls=cls.__name__, exponent=n):
                    with self.assertRaises(ValueError):
                        cls(I(-1, 1))**n
            for n in (F(1, 2), F(2), 0.5, 2.0, '2', None):
                with self.subTest(cls=cls.__name__, exponent=n):
                    with self.assertRaises(TypeError):
                        cls(I(1, 4))**n

    def test_valid_power_endpoints_and_dual_derivatives(self):
        for n in range(7):
            for x in (I(-2, -1), I(-2, 3), I(0, 3), I(1, 2)):
                for v in (x.lo, (x.lo+x.hi)/2, x.hi):
                    self.enclosure(x**n, (v**n, v**n))
            d = D(F(-2), F(3))**n
            z = D2(F(-2), F(3), F(5))**n
            first = F(0) if n == 0 else n*F(-2)**(n-1)*3
            second = F(0) if n == 0 else n*F(-2)**(n-1)*5
            if n >= 2:
                second += n*(n-1)*F(-2)**(n-2)*9
            self.same(d.v, I(F(-2)**n))
            self.same(d.d, I(first))
            self.same(z.d1, I(first))
            self.same(z.d2, I(second))
        # bool was already an int under the original API.
        self.same(I(2)**True, I(2))
        self.same(I(2)**False, I(1))

    def test_sqrt_domains_and_exact_rational_inequalities(self):
        for x in (I(-1), I(-1, 0), I(-1, 2)):
            with self.assertRaises(ValueError):
                x.sqrt()
        for cls in (D, D2):
            for x in (I(-1), I(-1, 2), I(0), I(0, 1)):
                with self.assertRaises(ValueError):
                    cls(x).sqrt()
        for x in (I(0), I(0, 1), I(2), I(F(1, 10**12), F(3, 10**8)),
                  I(F(4, 9), F(25, 16))):
            y = x.sqrt()
            self.assertGreaterEqual(y.lo, 0)
            self.assertLessEqual(y.lo**2, x.lo)
            self.assertGreaterEqual(y.hi**2, x.hi)
        d = D(4, 3).sqrt()
        z = D2(4, 3, 5).sqrt()
        self.enclosure(d.v, (F(2), F(2)))
        self.enclosure(d.d, (F(3, 4), F(3, 4)))
        self.enclosure(z.d1, (F(3, 4), F(3, 4)))
        self.enclosure(z.d2, (F(31, 32), F(31, 32)))

    def test_division_by_zero_interval_still_rejected(self):
        for cls in (I, D, D2):
            for denominator in (I(0), I(-1, 1), I(0, 1)):
                with self.assertRaises(ZeroDivisionError):
                    cls(1)/cls(denominator)

    def test_nonfinite_scalar_inputs_rejected(self):
        for x in (float('nan'), float('inf'), float('-inf')):
            with self.assertRaises((ValueError, OverflowError)):
                I(x)
        self.same(I(0.5), I(F(1, 2)))
        self.same(I(2, -1), I(-1, 2))
        a, b = R._sc_series(0.1)
        c, d = R._sc_series(F.from_float(0.1))
        self.same(a, c)
        self.same(b, d)

    def test_dual_atan_across_zero_has_positive_denominator(self):
        x = I(-2, 2)
        d = R.d_atan(D(x, 1))
        z = R.d2_atan(D2(x, 1, 0))
        self.enclosure(d.d, (F(1, 5), F(1)))
        self.enclosure(z.d1, (F(1, 5), F(1)))
        for t in (F(-2), F(-1, 2), F(0), F(1, 2), F(2)):
            second = -2*t/(1+t*t)**2
            self.enclosure(z.d2, (second, second))
            self.enclosure(z.v, atan_reference(t))

    def test_dual_sine_cosine_critical_values_and_chain_rule(self):
        x = D2(I(F(-1, 10), F(1, 10)), 3, 5)
        s, c = R.d2_sin(x), R.d2_cos(x)
        for interval, point in ((s.v, 0), (s.d1, 3), (s.d2, 5),
                                (c.v, 1), (c.d1, 0), (c.d2, -9)):
            self.enclosure(interval, (F(point), F(point)))
        y = D(I(-2, 2), 1)
        self.enclosure(R.d_sin(y).d, (F(1), F(1)))
        self.enclosure(R.d_cos(y).d, (F(-1), F(1)))

    def test_derivative_sign_helpers_do_not_accept_known_counterexample(self):
        # f(x)=x^3/3-x/2: f'(0)=-1/2 while f'(+-1)=1/2.
        fn = lambda x: x**3/3-x/2
        self.assertFalse(R.der_sign2(fn, F(-1), F(1), True, base_n=1, max_n=4)[0])
        self.assertFalse(R.der_sign_adaptive(fn, F(-1), F(1), True,
                                            min_w=F(1, 4), max_boxes=16)[0])
        self.assertTrue(R.der_sign2(lambda x: R.d2_atan(x), F(-2), F(2), True,
                                   base_n=16, max_n=64)[0])

    def test_actual_e1_primitive_points_and_tau(self):
        worst_s = worst_c = worst_tau = F(0)
        for x in E1['PRIM_PTS']+[F(13, 10)]:
            sg, cg = R.I_sin(I(x)), R.I_cos(I(x))
            sr, cr = trig_reference(x)
            self.enclosure(sg, sr)
            self.enclosure(cg, cr)
            self.assertGreater(cg.lo, 0)
            argument = 2*sg/cg
            self.assertGreater(argument.lo, 1)
            tau = R.I_atan(argument)
            argref = 2*I(*sr)/I(*cr)
            self.enclosure(tau, (atan_reference(argref.lo)[0], atan_reference(argref.hi)[1]))
            self.assertLess(sg.width(), F(1, 10**20))
            self.assertLess(cg.width(), F(1, 10**20))
            self.assertLess(tau.width(), F(1, 10**12))
            if x <= E1['GHI']:
                self.assertGreater(tau.lo, R.PI.hi/4)
                self.assertLess(tau.hi, F(13, 10))
            worst_s = max(worst_s, sg.width())
            worst_c = max(worst_c, cg.width())
            worst_tau = max(worst_tau, tau.width())
        print('E1_POINT_WIDTHS exact comparisons: sin,cos < 1/10^20; tau < 1/10^12; '
              '11 primary points plus h endpoint 13/10', flush=True)

    def test_actual_e1_derivative_cells_gamma_and_tau(self):
        cells = set()
        for _, _, a, b, _, n in E1['deriv_facts']:
            for k in range(n):
                cells.add((a+(b-a)*F(k, n), a+(b-a)*F(k+1, n)))
        for a, b in sorted(cells):
            g = D2(I(a, b), 1, 0)
            s, c = R.d2_sin(g), R.d2_cos(g)
            tau = R.d2_atan(2*s/c)
            self.assertGreater(c.v.lo, 0)
            self.assertGreater((2*s.v/c.v).lo, 1)
            self.assertLess(s.v.width(), 2*(b-a)+F(1, 10**18))
            self.assertLess(c.v.width(), 2*(b-a)+F(1, 10**18))
            self.assertLess(tau.v.width(), 4*(b-a)+F(1, 10**12))
            for t in (a, (a+b)/2, b):
                sr, cr = trig_reference(t)
                si, co = I(*sr), I(*cr)
                argument = 2*si/co
                self.enclosure(tau.v, (atan_reference(argument.lo)[0],
                                       atan_reference(argument.hi)[1]))
                # Closed formulas, independent of production AD assembly.
                den = 1+3*si**2
                first = I(2)/den
                second = -12*si*co/den**2
                self.enclosure(tau.d1, (first.lo, first.hi))
                self.enclosure(tau.d2, (second.lo, second.hi))
        print(f'E1_ACTUAL_UNIQUE_DERIVATIVE_CELLS {len(cells)}; endpoints and midpoints; '
              'universal enclosure supplied by analytic proof', flush=True)

    def test_actual_e1_comps2_selected_certificate_margins(self):
        # Actual current function, not a retyped approximation or generator run.
        checks = [(F(17, 20), 'B1', 'ge', F(1, 200)),
                  (F(43, 50), 'B1', 'le', F(-1, 50)),
                  (E1['GHI'], 'tmax', 'le', F(13, 10)),
                  (E1['GHI'], 'TB', 'ge', F(1, 40))]
        cache = {}
        for x, key, cmp, target in checks:
            if x not in cache:
                cache[x] = E1['comps2'](D2(I(x), 1, 0))
            value = cache[x][key].v
            if cmp == 'ge':
                self.assertGreaterEqual(value.lo, target)
            else:
                self.assertLessEqual(value.hi, target)
        for x in cache:
            actual = cache[x]['tmax']
            sr, cr = trig_reference(x)
            argument = 2*I(*sr)/I(*cr)
            self.enclosure(actual.v, (atan_reference(argument.lo)[0],
                                       atan_reference(argument.hi)[1]))
        print('E1_COMPS2 3 actual point evaluations; B1(17/20), B1(43/50), '
              'tau(GHI), TB(GHI) exact target margins checked', flush=True)


if __name__ == '__main__':
    print(f'R13 AUTHOR SELFCHECK optimize={sys.flags.optimize} python={sys.version}', flush=True)
    unittest.main(verbosity=2)
