from pathlib import Path
import hashlib
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections
import research_review as Review

def save(Path, Data):
	Path.write_text(json.dumps(Data, ensure_ascii=False, indent=2)+'\n')

Baseline = json.loads((Out/'baseline.json').read_text())
Cards = json.loads((Out/'cards.json').read_text())
Coordinator = '01a06f46-dd03-7c83-9267-32048412c359'
Store = Corrections.load_store(Root)
States, Problems = Corrections.impact_states(Root, Store)
Initial = {Row['release'] for Row in json.loads((Root/Artifact/'initial-impact.json').read_text())['review_problems']}
Invalid = []
for Problem in Problems:
	if Problem['release'] in Initial:
		continue
	Payload = Store['requests'][Problem['release']]['payload']
	Revision = Store['requests'][Payload['revision']]['payload']
	Invalid.append(dict(old_release=Problem['release'], revision=Payload['revision'], target=Revision['new'], issue=Revision['issue'], old_bundle=Payload['bundle'], problem=Problem))
save(Out/'renewal-inspection.json', dict(new_invalid_releases=Invalid, all_review_problems=Problems))
Done = json.loads((Out/'revisions.json').read_text()) if (Out/'revisions.json').exists() else []
for Name, New in Cards.items():
	for Issue in States[Corrections.key(New)]['issues']:
		if any(Row['name']==Name and Row['issue']==Issue and Row['target']['sha256']==New['sha256'] for Row in Done):
			continue
		Old = dict(location=New['location'], sha256=Baseline['tracked'][New['location']])
		Result = Corrections.propose_revision(Root, Issue, Old, dict(location=New['location'], sha256=New['sha256']), Coordinator, 'Round12 repairs indexed DD/DN half spectra and bound pole identity, separates raw K from SKS parity blocks, and corrects propagated sector_data and rank-one criterion labels. Retain the exact scopes of previous determinant, normalization, phase/reflection and Jacobian/FD repairs. New n2 Green derivation is conditional on fixed finite R>1 symmetric stationary geometry; no global signs, full historical scans or complete formalization.')
		Done.append(dict(name=Name, issue=Issue, revision=Result['revision_id'], target=dict(location=New['location'], sha256=New['sha256']), result=Result))
		save(Out/'revisions.json', Done)
		print('Revision', Name, Issue[:8], flush=True)
save(Out/'current-revisions.json', Done)
Inputs, Claims = {}, {}
Authors = {Coordinator, '01a0dce3-b8a0-7d83-b359-03a8073d76d4'}
for Row in Done:
	Requirements = Corrections.review_requirements(Root, Row['revision'])
	save(Out/(Row['revision']+'-requirements.json'), Requirements)
	for Input in Requirements['inputs']:
		if Input['path'] in Inputs and Inputs[Input['path']].get('sha256') != Input['sha256']:
			raise RuntimeError('Conflicting review binding')
		Inputs[Input['path']] = Input
	for Claim in Requirements['claims']:
		Claims[Claim['id']] = Claim
	Authors.update(Requirements['author_ids'])
Extras = [Artifact+'/analytic-repair.md', Artifact+'/submitted/proof_audit_round12_20260926.md', Artifact+'/intake-verification.json', 'research/artifacts/proof-audit-round11-20260926/jacobian-repair.md', 'research/artifacts/proof-audit-round10-20260925/analytic-repair.md', 'research/artifacts/proof-audit-round9-20260923/analytic-repair.md', 'docs/SL_gap_nge2_symmetry_local_proof.tex', 'literature/absorption-20260923/interfaces/derivations/P3-interface-chain-rule.md']
Extras += [Artifact+'/before/tools/'+Name+'.md' for Name in Cards]
# Freeze program copies already submitted for separate actual execution review.
Extras += [Artifact+'/software-review2/inputs/scripts/'+Name for Name in ['_sl_prufer.py','_gapn2_half_problem_probe.py','_gapn2_sector_decomposition.py','_gapn2_green_inertia_probe.py']]
for Name in Extras:
	Inputs.setdefault(Name, dict(path=Name, role='proof-or-explicit-before-after-scope'))
NewClaims = [dict(id='R12-phase-identity', verification='analytic', statement='Independently verify the exact DD/DN phase lift, positive coordinate-change fixed integer AND half-integer targets, strict frequency monotonicity, all-index ordering/comparison brackets, physical zero counts and half/full interleaving. Assess the independent proof rather than assuming the supplied audit is correct. Numerical tables/guards remain finite diagnostics, not interval certification.'), dict(id='R12-normalized-Green-sectors', verification='analytic', statement='Independently check generic finite mirror compression/conjugacy without symmetry assumptions, versus the separate commuting condition for block decomposition. In fixed finite R>1 n2 symmetric five-layer stationary configurations, verify differentiability, FH sign and normalization kernel component, exact K/Kp formulas, half-normalization factors, interface alternation/diagonal sign, cross-parity KpOdd=E Ke E and raw Ko own-pole reduced kernels plus surviving rank one. Inspect spectral/Green source, projection and boundary obligations, not only matrix algebra.'), dict(id='R12-propagation-and-scope', verification='analytic', statement='Verify the three current card bodies and actual summaries consistently correct raw versus conjugated sector labels, sector_data H/E summands and the negative rank-one criterion. The n2 analytic derivation, generic finite algebra, n2/n3 finite execution and unchanged historical scopes must stay distinct. Prior cofinite theorem, global G1/uniqueness and all historical scans are outside this repair. Reassess each exact retained correction obligation without using prior verdicts as a premise.')]
for Claim in NewClaims:
	Claims[Claim['id']] = Claim
Spec = dict(kind='mathematics', author_ids=sorted(Authors), inputs=list(Inputs.values()), claims=list(Claims.values()))
save(Out/'math-review-spec.json', Spec)
save(Out/'math-review-packet.json', Review.create_packet(Root, Spec))
print('Math packet ready', len(Inputs), 'inputs;', len(Claims), 'claims;', len(Invalid), 'new stale releases', flush=True)
