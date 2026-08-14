# -*- coding: utf-8 -*-
"""Update run-manifest.json: completed_at, upstream_status_verbatim, append
R-210 artifact entries, keep task_id unchanged.  Programmatic (uniform JSON)."""
import json

p = r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260812T090000Z-g1prime-g2\run-manifest.json'
d = json.load(open(p, encoding='utf-8'))

d['completed_at'] = '2026-08-14T13:30:00+08:00'
d['upstream_status_verbatim'] = (
    'RIGOROUS_PARTIAL_RESULT: (G2) CLOSED STRICT (R-204); (G1\') STRICT on '
    '(1,1+delta) for every n (R-208 anchor); open core [1+delta,infinity); '
    'n=2 (I1)/(I2) reduced to (M1) d/dR det Kp_odd, det Ko < 0 + (M2) trace '
    'signs + (M3) R->inf asymptotics; M3 NOT closed: STRICT level-by-level '
    'cascade structure established (R-210: level 0 = a0*K0=2 exact, level 1 = '
    'a1=-2K1/K0^2 exact, reduced seed E1_2/E2_2/E6_5 affine-linear in '
    '(a2,K2,c0), b0 delayed to E5_6, hard constant E5_5 = K0^3/2 + '
    'linear(K1,C1) + O(K1^3) forcing nonzero odd components, even-only ansatz '
    'structurally impossible); corrected-branch seed root and closed leading '
    'observables (m3D-m3N, C=0 value, sector-determinant coefficients) still '
    'OPEN; EVIDENCE: a0=2/K0=0.578821 matches fit, D*R -> 2K0c0 = 10.18692, '
    'Dk/u^5 -> 1.47410, consistency candidate 1.86956 != 0'
)

# append R-210 artifacts (avoid duplicating existing paths)
existing = {a['path'] for a in d['artifacts']}
new_artifacts = [
    {'path': 'run_notes_addendum_2026-08-14.md',
     'role': 'R-210: STRICT M3 cascade structure (level 0 a0*K0=2, level 1 a1=-2K1/K0^2, reduced seed, hard-constant E5_5 forcing odd components) + EVIDENCE observables + open corrected-branch root'},
    {'path': 'scripts/_gapn2_largeR_cascade.py',
     'role': 'STRICT cascade driver: pre-cleared level-0/1/2 seed equation extraction'},
    {'path': 'scripts/_gapn2_cascade_seed.py',
     'role': 'joint 12-unknown seed system (orders 0..5)'},
    {'path': 'scripts/_gapn2_cascade_reduce.py',
     'role': 'reduced seed (a0=2/K0, a1=-2K1/K0^2): E1_2/E2_2/E6_5/E5_4/E5_5/E5_6'},
    {'path': 'scripts/_gapn2_observables.py',
     'role': 'STRICT-formula leading-observable arithmetic (EVIDENCE seed values)'},
    {'path': 'scripts/_gapn2_cascade_num3.py',
     'role': 'truncated power-dict full-system precompile (builds 27 orders correctly)'},
    {'path': 'scripts/_gapn2_cascade_reducedseed.py',
     'role': 'reduced-seed root attempt (incomplete in-session; EVIDENCE)'},
]
for a in new_artifacts:
    if a['path'] not in existing:
        d['artifacts'].append(a)

# update the ledger artifact role in place (R-200..R-210)
for a in d['artifacts']:
    if a['path'] == 'research_ledger.md':
        a['role'] = 'R-200..R-210'

# notes: append R-210 summary if not present
note = ('R-210 (2026-08-14): M3 cascade structure STRICT (level 0 a0*K0=2, '
        'level 1 a1=-2K1/K0^2, reduced seed affine-linear in (a2,K2,c0), b0 '
        'delayed to E5_6, hard constant E5_5=K0^3/2+linear(K1,C1) forcing odd '
        'components -> even-only ansatz impossible); corrected-branch root and '
        'closed observables OPEN; EVIDENCE D*R -> 2K0c0 = 10.18692, Dk/u^5 -> '
        '1.47410, a0=2/K0 matches fit; scripts _gapn2_largeR_cascade.py, '
        '_gapn2_cascade_seed.py, _gapn2_cascade_reduce.py, _gapn2_observables.py')
if not any('R-210' in n for n in d['notes']):
    d['notes'].append(note)

json.dump(d, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('updated. task_id =', d['task_id'], '| artifacts =', len(d['artifacts']))
