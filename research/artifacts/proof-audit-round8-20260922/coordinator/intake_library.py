from pathlib import Path
import hashlib
import json
import shutil
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round8-20260922')
Artifacts = Root/'research/artifacts/proof-audit-round8-20260922'
Plugin = Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'
sys.path.insert(0, str(Plugin))
import research_corrections as Corrections

def save(Path, Data):
	Path.write_text(json.dumps(Data,ensure_ascii=False,indent=2)+'\n')

def sha(Path):
	return hashlib.sha256(Path.read_bytes()).hexdigest()

Verification = json.loads((Out/'source-verification.json').read_text())
if Verification['status'] != 'PASS':
	raise RuntimeError('Intake identities not verified')
for Name, Digest in Verification['plugin_sources'].items():
	if sha(Plugin/Name) != Digest:
		raise RuntimeError('Plugin source changed')
Baseline = json.loads((Out/'baseline.json').read_text())
Artifacts.mkdir(parents=True, exist_ok=True)
Attribute = Artifacts/'.gitattributes'
if not Attribute.exists():
	Attribute.write_text('* -text\n')
for File in (Out/'submitted').iterdir():
	Target = Artifacts/'submitted'/File.name
	Target.parent.mkdir(exist_ok=True)
	if Target.exists() and Target.read_bytes() != File.read_bytes():
		raise RuntimeError('Existing supplied evidence changed')
	if not Target.exists():
		shutil.copyfile(File,Target)
for Name in ['intake.json','source-verification.json']:
	Target = Artifacts/Name
	if not Target.exists():
		shutil.copyfile(Out/Name,Target)
Targets = ['tools/inf-limit-comparison.md','tools/lemma-A-doubleprime.md','tools/cot-series-certificate.md','tools/delta-bracketing.md']
for Name in Targets+['AGENTS.md','docs/SL_gap_n1_inf_limit_proof.tex','docs/SL_gap_n1_inf_limit_proof.pdf']:
	Target = Artifacts/'before'/Name
	Target.parent.mkdir(parents=True,exist_ok=True)
	if not Target.exists():
		if sha(Root/Name) != Baseline['tracked'][Name]:
			raise RuntimeError('Original bytes changed before preservation: '+Name)
		shutil.copyfile(Root/Name,Target)
Finding = Artifacts/'direct-propagation-findings.md'
if not Finding.exists():
	Finding.write_text('''# Round 8 direct propagation findings (author observations)

R8-P01: tools/cot-series-certificate.md writes cot z = 1/z - sum(k>=1) c_k z^(2k+1), with c_k=2^(2k)|B_(2k)|/(2k)!. For k=1 this incorrectly starts at z^3/3; the actual first term is z/3. Correct powers are z^(2k-1), and R(z)/z has powers z^(2k-2). The series is locally uniformly convergent on compact subsets of |z|<pi, not uniformly convergent throughout (0,pi). The main INF limit source repeats the wrong exponent/index.

R8-P02: tools/delta-bracketing.md says delta_2^+=arctan(2u/(pi ell)) diverges as u->1/2. The argument diverges, but delta_2^+ tends to pi/2 and is bounded. Its opening phase equations also require an explicitly justified branch. Restrict the stated bracket to R>=1500, w>=2 and derive mode identity before dividing by trigonometric factors.

R8-P03: INF summary references inherit the unsound 05/16/19 certification. Replace current evidence pointers and fixed-u rate claims; retain historical scripts and reviews by exact bytes. The displayed u*=0.3299225081196866 in the main and summary text conflicts with the narrower T3 interval and must be updated from the new exact enclosure.

These are coordinator source observations awaiting fresh mathematical review, not final approvals.
''')
Issue = dict(issue_id='round8-inf-limit-certificates',origin='external',reporter='sl_audit_round8 supplied audit plus direct propagation inspection',summary='R8-F01 through F05: incorrect root image endpoint, unsound transcendental interval expansion, missing continuous sliver coverage, unqualified phase branches and wrong fixed-u rate. Directly related cot-series exponent/local-uniform scope, bounded phase bracket and stale summaries are included.',disposition='quarantine',targets=[dict(location=Name,sha256=Baseline['tracked'][Name]) for Name in Targets],evidence=[dict(path=str((Artifacts/'submitted/proof_audit_round8_20260922.md').relative_to(Root)),locator='R8-F01 through R8-F05'),dict(path=str(Finding.relative_to(Root)),locator='R8-P01 through R8-P03')])
if not (Out/'issue-result.json').exists():
	save(Out/'issue-input.json',Issue)
	print('Registering round 8 exact-version issue.',flush=True)
	Result=Corrections.register_issue(Root,Issue)
	save(Out/'issue-result.json',Result)
	for Name in ['issue-input.json','issue-result.json']:
		shutil.copyfile(Out/Name,Artifacts/Name)
Store=Corrections.load_store(Root)
States,Problems=Corrections.impact_states(Root,Store)
Affected=[dict(key=Key,state=State) for Key,State in States.items() if not State['reuse_allowed']]
save(Out/'initial-impact.json',dict(affected=Affected,problems=Problems))
save(Artifacts/'initial-impact.json',dict(affected=Affected,problems=Problems))
print(json.dumps(dict(status='INTAKE_COMMITTED',affected_versions=len(Affected),historical_problem_occurrences=len(Problems))),flush=True)
