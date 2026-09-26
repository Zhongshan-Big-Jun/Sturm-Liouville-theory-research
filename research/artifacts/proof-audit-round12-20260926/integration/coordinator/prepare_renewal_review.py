from pathlib import Path
import hashlib
import json
import sys
Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections
import research_review as Review

def save(Path, Data):
	Path.write_text(json.dumps(Data, ensure_ascii=False, indent=2)+'\n')

Cards = json.loads((Out/'cards.json').read_text())
Changed = {Card['location'] for Card in Cards.values()}
Invalid = json.loads((Out/'renewal-inspection.json').read_text())['new_invalid_releases']
Rows = list({Row['revision']: Row for Row in Invalid if Row['target']['location'] not in Changed and hashlib.sha256((Root/Row['target']['location']).read_bytes()).hexdigest() == Row['target']['sha256']}.values())
save(Out/'renewals.json', Rows)
if not Rows:
	print('No unchanged exact-version renewal required', flush=True)
	raise SystemExit(0)
Inputs, Claims = {}, {}
Authors = {'01a06f46-dd03-7c83-9267-32048412c359','01a0dce3-b8a0-7d83-b359-03a8073d76d4'}
Identities = []
for Row in Rows:
	Requirements = Corrections.review_requirements(Root, Row['revision'])
	for Input in Requirements['inputs']:
		if Input['path'] in Inputs and Inputs[Input['path']].get('sha256') != Input['sha256']:
			raise RuntimeError('Conflicting renewal binding')
		Inputs[Input['path']] = Input
	for Claim in Requirements['claims']:
		Claims[Claim['id']] = Claim
	Authors.update(Requirements['author_ids'])
	Identities.append(dict(target=Row['target'], issue=Row['issue'], revision=Row['revision'], reason=Row['problem']['error']))
Extras = ['research/artifacts/proof-audit-round9-20260923/analytic-repair.md', 'research/artifacts/proof-audit-round10-20260925/analytic-repair.md', 'research/artifacts/proof-audit-round11-20260926/jacobian-repair.md', 'docs/SL_gap_nge2_symmetry_local_proof.tex', 'docs/SL_fixed_n_supremum.tex', 'literature/absorption-20260923/interfaces/derivations/P3-interface-chain-rule.md', 'research/artifacts/proof-audit-round12-20260926/analytic-repair.md']
Extras += [Card['location'] for Card in Cards.values()]
Extras += ['research/artifacts/proof-audit-round12-20260926/before/tools/'+Name+'.md' for Name in Cards]
Identity = dict(scope='Unchanged exact versions whose prior whole-packet inputs changed; old verdicts are not premises.', unchanged=Identities, changed_card_paths=sorted(Changed))
save(Artifact/'renewal-identities.json', Identity)
Extras.append('research/artifacts/proof-audit-round12-20260926/renewal-identities.json')
for Name in Extras:
	Inputs.setdefault(Name, dict(path=Name, role='current-proof-or-exact-changed-source-comparison'))
Claims['R12-unchanged-version-renewal'] = dict(id='R12-unchanged-version-renewal', verification='analytic', statement='Independently reassess each exact unchanged correction obligation in renewal-identities. Read the actual prior mathematical repair sources and the changed three card scopes; do not rely on previous verdict labels. The corrected half-spectrum, K versus SKS labels and negative-rank-one criterion must not be used as an invalid premise for retained variational/FH, local reflection or balanced-candidate root/limit results. If any real dependency is affected, reject with its location rather than treating byte stability as proof. No global G1/uniqueness, complete historical Green/M3/KP or whole-program formalization is certified.')
Spec = dict(kind='mathematics', author_ids=sorted(Authors), inputs=list(Inputs.values()), claims=list(Claims.values()))
save(Out/'renewal-review-spec.json', Spec)
save(Out/'renewal-review-packet.json', Review.create_packet(Root, Spec))
print('Renewal packet',len(Rows),'obligations;',len({Row['target']['location'] for Row in Rows}),'unchanged cards;',len(Inputs),'inputs',flush=True)
