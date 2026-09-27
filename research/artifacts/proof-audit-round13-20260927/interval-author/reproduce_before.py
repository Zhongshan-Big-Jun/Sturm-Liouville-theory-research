"""Execute the saved actual pre-edit source. Expected defects, not PASS claims."""
from fractions import Fraction as F
import hashlib
from pathlib import Path
import sys
import types

sys.dont_write_bytecode = True
path = Path(__file__).with_name('rigid1d.before.py')
data = path.read_bytes()
r = types.ModuleType('rigid1d_before')
exec(compile(data.decode('utf-8-sig'), str(path), 'exec'), r.__dict__)


def require(ok, description):
    if not ok:
        raise RuntimeError('negative-control reproduction failed: '+description)
    print('CONFIRMED_OLD_DEFECT '+description, flush=True)


print(f'PRE_EDIT optimize={sys.flags.optimize} sha256={hashlib.sha256(data).hexdigest()}', flush=True)
c = r.I_cos(r.I(F(-1, 10), F(1, 10)))
require(c.hi < F(997, 1000) < 1, 'cos([-1/10,1/10]).hi < 997/1000 < cos(0)=1')
require((r.I(F(997, 1000))-c).is_pos(), 'false strict positivity; actual value at 0 is -3/1000')
s = r.I_sin(r.I(-2, 2))
require(s.hi < F(19, 20) < 1 and r.PI.hi/2 < 2,
        'sin([-2,2]).hi < 19/20 < sin(pi/2)=1 with pi/2 in interval')
try:
    r.I_atan(r.I(F(9, 10), F(11, 10)))
except RecursionError:
    print('CONFIRMED_OLD_DEFECT atan([9/10,11/10]) RecursionError', flush=True)
else:
    raise RuntimeError('expected old recursion failure was not reproduced')
for cls in (r.I, r.D, r.D2):
    try:
        value = cls(r.I(-1, 1))**-1
    except AssertionError:
        require(not sys.flags.optimize, cls.__name__+' negative-power assert active only normally')
    else:
        require(bool(sys.flags.optimize), cls.__name__+' negative power silently accepted under -O across zero')
print('PRE_EDIT reproductions completed; author evidence only', flush=True)
