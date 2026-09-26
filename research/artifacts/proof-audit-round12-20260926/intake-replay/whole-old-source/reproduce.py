import sys, json, warnings
import numpy as np
sys.path.insert(0, 'scripts')
import _gapn2_half_problem_probe as H
hb = [(0.5, 100.0)]
cases = {bc + str(n): H.half_spectrum(hb, bc, N=n) for bc in ('D','N') for n in (4,80,160)}
mu = cases['N160'][1]
with warnings.catch_warnings(record=True) as ws:
 warnings.simplefilter('always')
 value = H._spectral_green(hb, mu, 1, 'N', 0.1, 0.1, N=80)
if not (np.isposinf(value) and np.where(cases['N80'] == mu)[0].tolist() == [3]):
 raise RuntimeError('Whole source counterexample did not reproduce')
result = dict(source_module=H.__file__, roots={k:v[:6].tolist() for k,v in cases.items()}, target=float(mu), actual_index=np.where(cases['N80'] == mu)[0].tolist(), removed_index=1, result=str(value), warnings=[str(w.message) for w in ws], scope='Whole original module execution; finite counterexample')
print(json.dumps(result, indent=2))
