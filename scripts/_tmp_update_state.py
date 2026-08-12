# -*- coding: utf-8 -*-
# One-off maintenance: update state/current.json and state/RESUME.md for
# session 58 continuation 4b (n>=2 reflection symmetry).
import io
import json

# ---------- current.json ----------
pj = r'F:\LaTeX\BVE research\state\current.json'
with io.open(pj, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

data['last_updated'] = '2026-08-12T08:10:00Z'
data['gap_nge2_symmetry_status'] = 'LOCAL_THEOREM_PROVED (STRICT, R->1 unique symmetric branch, 2026-08-12 cont 4b); GLOBAL_OPEN_((G1\')(G2))'

notes = data.get('note', '')
add_note = (
    ' | 2026-08-12 continuation 4b (n>=2): reflection symmetry LOCAL theorem STRICT closed - '
    'docs/SL_gap_nge2_symmetry_local_proof.pdf (9 pp zero warnings: R=1 general-n analysis via '
    'Wronskian W=-2(n+1)pi sin(pi x)<0, exactly 2n simple symmetric zeros, sgn detJ=(-1)^n; '
    'R->1 uniqueness with boundary-exclusion lemmas 4.2/4.3; equivariance F(R,xbar)=PF(R,x) + '
    'unique branch => symmetric); global uniqueness via topological-degree homotopy framework '
    'conditional on OPEN (G1\') (detJ nonzero, sign (-1)^n on solution set) and (G2) (block widths '
    'uniformly positive on compact R). Recon doc 5 pp zero warnings. Numerics EVIDENCE only '
    '(R=1 zeros n=2..8, detJ=143179.8687, equivariance 1e-16, symmetrization non-monotone '
    '118/116 of 200, old 33/200 57/200 not reproducible). NOT claimed: global reflection '
    'symmetry theorem.'
)
data['note'] = notes + add_note

na = data.get('next_actions', [])
new_na = []
for item in na:
    if item.startswith('3.'):
        item = ('3. n>=2 reflection symmetry: LOCAL theorem STRICT (2026-08-12 cont 4b, '
                'unique symmetric R->1 branch); GLOBAL uniqueness open pending (G1\') sgn detJ '
                '= (-1)^n on solution set and (G2) block-width compactness; then closed-form '
                'max/min D_n and switch positions/block lengths')
    new_na.append(item)
data['next_actions'] = new_na

with io.open(pj, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('current.json updated')

# ---------- RESUME.md ----------
rp = r'F:\LaTeX\BVE research\state\RESUME.md'
raw = open(rp, 'rb').read()
bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig') if bom else raw.decode('utf-8')
nl = '\r\n' if '\r\n' in text else '\n'

anchor = '## Last completed action'
assert text.count(anchor) >= 1, 'anchor missing'

new_entry = (
    '## Last completed action\n'
    '2026-08-12 (session 58 continuation 4b): n>=2 reflection symmetry -- LOCAL theorem STRICT closed.\n'
    'Deliverables: docs/SL_gap_nge2_symmetry_local_proof.pdf (9 pp zero warnings, rewritten: '
    'section 2 structure theorem with corrected level-set counting at first/last cells '
    '(|Q(0+)|=q0=|q1| finite, still 2n level-set solutions); section 3 R=1 general-n analysis: '
    'f_1 has exactly 2n simple symmetric zeros, interval signs (-,+,-,...,-), '
    'sgn f_1\'(x_j*)=(-1)^{j+1}, sgn det D_xF(1,x*)=(-1)^n via Wronskian W=-2(n+1)pi sin(pi x)<0; '
    'n=2 closed form t=(11+-2sqrt10)/36, detJ=143179.8687; section 4 R->1 local theorem: '
    'uniqueness boundary-exclusion lemmas 4.2/4.3 airtight (zeros uniformly away from endpoints, '
    'C^1 convergence + simple-zero isolation), equivariance F(R,xbar)=PF(R,x) (palindromic pattern '
    'sigma_i=sigma_{2n+2-i}) + unique branch => symmetric; section 5 global classification: '
    'topological-degree homotopy framework, conditional on OPEN (G1\') (detJ nonzero with sign '
    '(-1)^n on the solution set) and (G2) (block widths uniformly positive on compact R), '
    'framework-level proof hole in the draft fixed; section 6 EVIDENCE incl. symmetrization '
    'failure route).  Recon: docs/SL_gap_nge2_symmetry_recon.pdf (5 pp zero warnings; recon '
    'methods, 6 failed routes registered incl. the draft boundary-exclusion hole, lessons, '
    'open conditions, math-knowledge section).  EVIDENCE: scripts/_gapn2_symmetry_recon.py, '
    '_gapn2_jacobian_probe.py, _gapn2_antigrid_search.py; R=1 zeros n=2..8 all pass; '
    'equivariance D(xbar)=D(x) to 1e-16; detJ>0 along n=2 R-branch (SUP 1.38e5->330, '
    'INF 1.22e5->0.123, R in [1.05,100]); ~2000 solves no asymmetric internal solution and no '
    'boundary accumulation; density-averaging symmetrization NON-monotone (SUP 118/200, '
    'INF 116/200 violations; old 33/200, 57/200 numbers not reproducible - corrected).  Tools: '
    'tools/band-selfconsistency-equivariance.md added (equivariance identity + anticommutation '
    'J=-PJP + detJ=(-1)^n detA detB + degree framework, STRICT parts marked), README synced; '
    'AGENTS.md session 58 continuation 4b; state/current.json updated.  Honest: (G1\')/(G2) '
    'OPEN, global closure is sufficiency framework only; section-3 spectral sign conventions are '
    'classical self-referential (noted in doc); numerics EVIDENCE only.\n'
)
text = text.replace(anchor, new_entry + anchor, 1)

# extend read-first list
last_item = '16. `misc/_well_explore_log.md` (well-family EVIDENCE log, 2026-08-10; section 16 = all-R work)'
assert last_item in text, 'read-first anchor missing'
add_items = (
    '\n17. `docs/SL_gap_nge2_symmetry_local_proof.pdf` (n>=2 reflection symmetry LOCAL theorem, 9 pp, STRICT, 2026-08-12 cont 4b; R=1 general-n analysis, R->1 uniqueness, equivariance; global via OPEN (G1\')/(G2))'
    '\n18. `docs/SL_gap_nge2_symmetry_recon.pdf` (5 pp: recon methods, failed routes, lessons, open conditions)'
)
text = text.replace(last_item, last_item + add_items, 1)

# update exact next action item 3
old3 = ('3. Open problems remaining (per summary section 5.5): switch positions/block lengths,\n'
        '   reflection symmetry, uniqueness/classification, closed-form optimal values max/min D_n,\n'
        '   n=1 certificate kernel formalization, MDE unified theory, H^s density criteria,\n'
        '   p-Laplacian, etc.')
new3 = ('3. Open problems remaining (per summary section 5.5): n>=2 reflection symmetry GLOBAL\n'
        '   (LOCAL theorem STRICT since 2026-08-12 cont 4b; needs (G1\') detJ sign (-1)^n and (G2)\n'
        '   block-width compactness), switch positions/block lengths, closed-form optimal values\n'
        '   max/min D_n, n=1 certificate kernel formalization, MDE unified theory, H^s density\n'
        '   criteria, p-Laplacian, etc.')
if old3 in text:
    text = text.replace(old3, new3, 1)
else:
    print('WARN: next-action item 3 not replaced')

with io.open(rp, 'wb') as f:
    data = text.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    f.write(data)
print('RESUME.md updated')
