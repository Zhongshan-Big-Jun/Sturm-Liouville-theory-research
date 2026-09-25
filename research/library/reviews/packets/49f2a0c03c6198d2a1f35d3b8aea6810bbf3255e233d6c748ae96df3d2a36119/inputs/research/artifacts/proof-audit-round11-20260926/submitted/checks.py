"""Independent, scoped checks for SL audit round 11.

Runs the byte-verified current Pruefer module, and AST-extracted unchanged
jac_fd/sym_antisym_decomp functions from a byte-verified repository module.
The R=1 adapter uses the exact analytic residual and the repository's two
coordinate conversion formulas. It is NOT a rerun of the entire repository CLI.
Finite checks do not certify infinite-dimensional closure theorems.
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'source'))
RECORDS = []


def require(condition, name, details=None):
    if not bool(condition):
        raise RuntimeError('FAILED: ' + name)
    RECORDS.append({'name': name, 'confirmed': True, 'details': details})


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


require(git_blob(ROOT/'source/_sl_prufer.py') == '3800e210282cd1bf19f1523609b75b9498135754',
        'Current Pruefer source has exact repository Git blob identity')
require(git_blob(ROOT/'source/_gapn2_jacobian_probe.py') == '442f8e52572ccd80ecc6ddcfe648b9358c45bb6c',
        'Current Jacobian probe source has exact repository Git blob identity')
from _sl_prufer import indexed_roots, mp_lifted_phase

# Execute the two exact function bodies, without unrelated module imports/main.
path = ROOT/'source/_gapn2_jacobian_probe.py'
tree = ast.parse(path.read_text(encoding='utf-8'))
selected = [node for node in tree.body if isinstance(node, ast.FunctionDef)
            and node.name in {'jac_fd', 'sym_antisym_decomp'}]
namespace = {'np': np}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), namespace)
jac_fd = namespace['jac_fd']
old_decomp = namespace['sym_antisym_decomp']

blocks = [(0.02, 10000.0), (0.96, 1.0), (0.02, 10000.0)]
roots, root_records = indexed_roots(blocks, 6)
expected_brackets = [(F('0.783424012239'), F('0.783424012240')),
                     (F('0.797807654414'), F('0.797807654415')),
                     (F('2.345707847544'), F('2.345707847545')),
                     (F('2.358540421082'), F('2.358540421083'))]
require(all(a < F(float(x)) < b for x, (a, b) in zip(roots, expected_brackets)),
        'New engine recovers all four previously missed low roots',
        {'roots': roots.tolist(), 'certified': False})
long_roots, _ = indexed_roots(blocks, 61)
short_roots, _ = indexed_roots(blocks, 3)
require(np.max(np.abs(long_roots[:6]-roots)) < 1e-13 and
        np.max(np.abs(short_roots-roots[:3])) < 1e-13,
        'High-contrast root prefixes agree for requests of 3, 6 and 61 modes')

mp.mp.dps = 70
# Independent physical zeros: not a Pruefer-angle implementation.
def physical_zero_count(omega, data):
    y, yp, count = mp.mpf(0), mp.mpf(1), 0
    for length, density in data:
        length, density = mp.mpf(length), mp.mpf(density)
        w = omega * mp.sqrt(density)
        A, B = y, yp/w
        delta = mp.atan2(A, B)
        left = int(mp.floor(delta/mp.pi))-2
        right = int(mp.ceil((w*length+delta)/mp.pi))+2
        for k in range(left, right+1):
            t = (k*mp.pi-delta)/w
            if mp.mpf('1e-55') < t < length-mp.mpf('1e-55'):
                count += 1
        phase = w*length
        y = A*mp.cos(phase)+B*mp.sin(phase)
        yp = w*(-A*mp.sin(phase)+B*mp.cos(phase))
    return count

probes = [mp.mpf(float(roots[0]))/2] + [(mp.mpf(float(a))+mp.mpf(float(b)))/2
                                     for a,b in zip(roots[:-1],roots[1:])]
counts = [physical_zero_count(w, blocks) for w in probes]
require(counts == list(range(6)),
        'Independent 70-digit physical nodal counts agree with first six root indices',
        {'counts': counts, 'status': 'finite high-precision check, not interval certification'})

constant_tests = []
for length, density in [(1.,1.),(.3,.2),(5.,1e6),(2.,3.)]:
    rr,_ = indexed_roots([(length,density)], 32)
    exact = np.arange(1,33)*np.pi/(length*np.sqrt(density))
    error = float(np.max(np.abs(rr/exact-1)))
    constant_tests.append(error)
require(max(constant_tests) < 5e-14,
        'Current root engine obeys constant-density and interval scaling cases', constant_tests)

phase_errors = [abs(mp_lifted_phase([(mp.mpf(l),mp.mpf(c)) for l,c in blocks],mp.mpf(float(w)))
                    -(i+1)*mp.pi) for i,w in enumerate(roots)]
require(max(phase_errors) < mp.mpf('1e-10'),
        'Returned roots retain their labels under higher-precision phase evaluation',
        {'max_error': mp.nstr(max(phase_errors),20),
         'limitation': 'same phase mathematics; independent count is recorded separately'})

# Exact anti-commutation and exact determinant at the R=1, n=2 root.
a,b = sp.symbols('a b', nonzero=True, real=True)
P = sp.zeros(4)
for i in range(4): P[i,3-i]=1
J = sp.diag(a,b,-b,-a)
S = sp.Matrix([[1,0,0,1],[0,1,1,0],[1,0,0,-1],[0,1,-1,0]])
M = S*J*S.inv()
require(J*P+P*J == sp.zeros(4) and M[:2,:2] == sp.zeros(2) and M[2:,2:] == sp.zeros(2),
        'Symbolic reflection law forces a cross-block, not block-diagonal, Jacobian',
        {'matrix': str(M), 'determinant': str(J.det())})

tplus=(11+2*sp.sqrt(10))/36
tminus=(11-2*sp.sqrt(10))/36
# d(x)/pi with t=cos(pi*x)^2 on the left half.
def dsquared(t):
    C=2*t-1
    return sp.simplify(4*t*(1-t)*(-24*C**2+sp.Rational(32,9)*C+6)**2)
coefficient=sp.simplify(dsquared(tplus)*dsquared(tminus))
require(coefficient == sp.Rational(7030400000,4782969),
        'Exact normalized R=1 Jacobian determinant is nonzero',
        {'det': '7030400000*pi**4/4782969'})
left=np.arccos(np.sqrt(np.array([float(tplus),float(tminus)])))/np.pi
xstar=np.r_[left,1-left[::-1]]
dleft=(16*np.pi/9)*np.sin(4*np.pi*left)-6*np.pi*np.sin(6*np.pi*left)
Jexact=np.diag(np.r_[dleft,-dleft[::-1]])
old_A,old_B=old_decomp(Jexact,2)
Snp=np.array(S,dtype=float)
Mnp=Snp@Jexact@np.linalg.inv(Snp)
C,D=Mnp[:2,2:],Mnp[2:,:2]
require(np.array_equal(old_A,np.zeros((2,2))) and np.array_equal(old_B,np.zeros((2,2)))
        and abs(np.linalg.det(Jexact)) > 1e5,
        'Actual repository decomposition returns two zero blocks for a nondegenerate SL Jacobian',
        {'xstar':xstar.tolist(), 'diag':np.diag(Jexact).tolist(),
         'det_J':float(np.linalg.det(Jexact)), 'old_det_A':float(np.linalg.det(old_A)),
         'old_det_B':float(np.linalg.det(old_B))})
require(abs(np.linalg.det(C)*np.linalg.det(D)-np.linalg.det(Jexact)) < 1e-8,
        'Extracting the cross blocks restores the correct determinant relation',
        {'det_C':float(np.linalg.det(C)), 'det_D':float(np.linalg.det(D))})

class AnalyticR1Recon:
    """Exact R=1 residual; conversion bodies are the current Recon formulas."""
    n=2
    nb=5
    def z_to_widths(self,z):
        z=np.asarray(z,dtype=float)
        ez=np.exp(z-np.max(z))
        sm=ez/np.sum(ez)
        return (1.0-self.nb*1e-7)*sm+1e-7
    def widths_to_z(self,widths):
        w=np.asarray(widths,dtype=float)
        w=np.clip(w,2e-7,1.0-2e-7)
        w=w/np.sum(w)
        return np.log(w-1e-7)
    def residual(self,z):
        xx=np.cumsum(self.z_to_widths(z))[:-1]
        return 2*((4/9)*np.sin(2*np.pi*xx)**2-np.sin(3*np.pi*xx)**2)

def exact_R1_jac(xx):
    return np.diag((16*np.pi/9)*np.sin(4*np.pi*xx)-6*np.pi*np.sin(6*np.pi*xx))

rc=AnalyticR1Recon()
zstar=rc.widths_to_z(np.diff(np.r_[0.,xstar,1.]))
require(np.max(np.abs(jac_fd(rc,zstar)-exact_R1_jac(xstar))) < 1e-7,
        'The finite-difference helper works on the well-separated R=1 configuration')
xnarrow=np.array([.25,.2500003,.7499997,.75])
wnarrow=np.diff(np.r_[0.,xnarrow,1.])
znarrow=rc.widths_to_z(wnarrow)
base_roundtrip=rc.z_to_widths(znarrow)
require(np.max(np.abs(base_roundtrip-wnarrow)) < 1e-15 and np.min(wnarrow)>2e-7,
        'Narrow-block counterexample base is strictly feasible and initially unclipped')
actual=jac_fd(rc,znarrow)
exact=exact_R1_jac(xnarrow)
err=float(np.max(np.abs(actual-exact)))
require(err > 6,
        'Default finite difference silently changes paths after clipping a narrow block',
        {'default_h':1e-6,'widths':wnarrow.tolist(), 'max_entry_error':err,
         'returned':actual.tolist(), 'correct':exact.tolist()})
safe=jac_fd(rc,znarrow,1e-8)
require(np.max(np.abs(safe-exact)) < 1e-5,
        'A feasible smaller step removes the large clipping error in this finite example',
        {'h':1e-8,'max_entry_error':float(np.max(np.abs(safe-exact))),
         'limitation':'finite numerical diagnostic, not a universal step rule'})
# Exact rational change of an unrelated edge caused by normalization.
x1=F(1,4); old_width=F(3,10_000_000); h=F(1,1_000_000); floor=F(2,10_000_000)
extra=floor-(old_width-h)
changed_x1=x1/(1+extra)
require(extra==F(9,10_000_000) and changed_x1<x1,
        'Exact arithmetic proves that clipping moves an edge meant to stay fixed',
        {'intended_edge':str(x1), 'actual_after_clipping':str(changed_x1),
         'unintended_displacement':str(changed_x1-x1)})

# Algebra supporting the NEW all-order cofinite theorem; not the functional proof.
L=sp.symbols('L', positive=True, integer=True)
E=sp.Matrix([[L,L+2],[L*(L-1)*(L-2),(L+2)*(L+1)*L]])
O=sp.Matrix([[L,L+2],[(L+1)*L*(L-2),(L+3)*(L+2)*L]])
require(sp.factor(E.det())==2*L*(L+2)*(2*L-1) and
        sp.factor(O.det())==2*L*(L+2)*(2*L+1),
        'All-degree even/odd endpoint correction determinants are nonzero for even L>=4',
        {'even_det':str(sp.factor(E.det())),'odd_det':str(sp.factor(O.det()))})

x=sp.symbols('x')
def B(poly):
    delta=poly.subs(x,1)-poly.subs(x,-1)
    return sp.Matrix([sp.diff(poly,x).subs(x,1)-delta/2,
                      sp.diff(poly,x).subs(x,-1)-delta/2])
for ell in [4,6,8,10]:
    matrix=sp.Matrix.hstack(*[B(x**k).col_join(B(sp.diff(x**k,x,2)))
                              for k in range(ell,ell+4)])
    if matrix.det()==0:
        raise RuntimeError('finite boundary matrix singular')
require(True,'Finite direct differentiation checks the four-row boundary correction matrices')
polys={0:sp.Integer(1),1:x}
for m in range(2,11):
    polys[2*m]=x**(2*m)-sp.Rational(m,m-1)*x**(2*m-2)
    polys[2*m+1]=x**(2*m+1)-sp.Rational(m,m-1)*x**(2*m-1)
jetdict={str(n):[int(sp.diff(p,x,r).subs(x,0)) for r in range(4)] for n,p in polys.items()}
require(jetdict['0']==[1,0,0,0] and jetdict['1']==[0,1,0,0]
        and jetdict['4']==[0,0,-4,0] and jetdict['5']==[0,0,0,-12]
        and all(jetdict[str(n)]==[0,0,0,0] for n in polys if n>=6),
        'Centre-jet algebra isolates the four possible low-order directions',jetdict)
# Exact threshold tests include equality, where the new trace is not continuous.
threshold_samples=[(F(0),[]),(F(1,2),[]),(F(1),[0]),(F(3,2),[0]),
                   (F(2),[0,1]),(F(5,2),[0,1]),(F(3),[0,1,4]),(F(17,5),[0,1,4])]
for s,wanted in threshold_samples:
    selected=[idx for r,idx in enumerate([0,1,4]) if F(2*r+1,2)<s]
    if selected!=wanted:
        raise RuntimeError('critical threshold inequality mismatch')
require(True,'Critical threshold table uses strict interior trace inequalities')

result={'commit':'4f6b35cbdc433d2d319cd3e483b6dbf0af3f9d87',
        'python_optimized':not __debug__, 'group_count':len(RECORDS),
        'scope':'Finite checks plus exact finite/all-index algebra; no Lean or complete repository suite',
        'checks':RECORDS}
out=ROOT/'evidence'/('checks_optimized.json' if not __debug__ else 'checks_normal.json')
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'confirmed_groups':len(RECORDS),'python_optimized':not __debug__,
                  'output':str(out),'root_prefix':roots[:4].tolist(),
                  'clipping_max_error':err},ensure_ascii=False,indent=2))
