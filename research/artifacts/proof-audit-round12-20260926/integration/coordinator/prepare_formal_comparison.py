from pathlib import Path
import gzip
import json
import sys

Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round12-20260926')
Root = Artifact / 'formal-comparison'
Source = Out / 'formal-author'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as Review

Readback = json.loads((Out / 'formal-readback2-verified.json').read_text())
if Readback['verdict'] != 'APPROVED':
	raise RuntimeError('Blind readback incomplete')
Manifest = json.loads((Source / 'evidence/exact-root/run-manifest.json').read_text())
if not (Manifest['machine_verification_passed'] and Manifest['exact_root_passed'] and Manifest['evidence']['status'] == 'current'):
	raise RuntimeError('Author exact-root evidence incomplete')
Root.mkdir(parents=True, exist_ok=True)
(Root / 'AGENTS.md').write_text('# Independent formal comparison\n\nUse only frozen inputs and recorded read-only runtime/package dependencies. Execute in a new private workspace. Compare the intended contract with actual definitions and blind readback independently. Do not consult conversation, memory, unrelated sources or past verdicts.\n')
Inputs = []

def put(Name, Data, Role):
	Path = Root / 'inputs' / Name
	Path.parent.mkdir(parents=True, exist_ok=True)
	if Path.exists() and Path.read_bytes() != Data:
		raise RuntimeError('Frozen input drift: ' + Name)
	Path.write_bytes(Data)
	Inputs.append(dict(path=Path.relative_to(Root).as_posix(), role=Role))

for Name in ['contract.md', 'contract.json', 'negative-contract.json', 'summary.json', 'environment.json', 'run.py', 'README.md']:
	put(Name, (Source / Name).read_bytes(), 'intended-contract-or-author-execution')
for Name in ['declarations.json', 'declarations.txt']:
	put(Name, (Out / 'formal-export2' / Name).read_bytes(), 'actual-full-export-after-elision-repair')
put('complete-export/ExportRound12.lean', (Out / 'formal-export2/project/ExportRound12.lean').read_bytes(), 'complete-export-generator-record-output-path-must-be-adapted')
put('complete-export/coordinator-note.json', (Out / 'formal-export2/coordinator-note.json').read_bytes(), 'export-repair-provenance-not-independent-acceptance')
for Path in sorted((Source / 'project').iterdir()):
	if Path.is_file() and (Path.suffix in ['.lean', '.toml'] or Path.name == 'lean-toolchain'):
		put('project/' + Path.name, Path.read_bytes(), 'formal-source-and-pinned-environment')
put('lake-manifest.json', (Source / 'inputs/07-lake-manifest.json').read_bytes(), 'read-only-dependency-identity')
put('analytic-repair.md', (Artifact / 'analytic-repair.md').read_bytes(), 'informal-mathematical-intent-not-certified-by-Lean')
put('submitted/analytic_repairs.md', (Artifact / 'submitted/analytic_repairs.md').read_bytes(), 'unverified-external-audit-intent')
put('blind/AuditRound12.lean', (Source / 'blind/AuditRound12.lean').read_bytes(), 'blind-source-identity')
put('blind/readback-completion.json', (Out / 'formal-readback2-completion.json').read_bytes(), 'actual-independent-blind-translation')
put('blind/verified-receipt.json', (Out / 'formal-readback2-verified.json').read_bytes(), 'blind-readback-provenance-only')
for Label in ['exact-root', 'negative-contract']:
	put(Label + '/run-manifest.json.gz', gzip.compress((Source / 'evidence' / Label / 'run-manifest.json').read_bytes(), mtime=0), 'author-manifest-lossless-gzip')
for Label in ['final-source', 'export-03', 'positive-controls', 'positive-contract-type', 'blind-source', 'negative-wrong-sector', 'negative-mirror-sign', 'negative-normalization', 'exact-root', 'negative-contract']:
	for Name in ['command.json', 'stdout.log', 'stderr.log']:
		put('commands/' + Label + '/' + Name, (Source / 'commands' / Label / Name).read_bytes(), 'actual-author-command-and-log')
Scope = '''# Independent formal comparison and actual execution

Personally compare all 59 exported declarations, definition bodies, implicit binders and the complete literal root against the intended contract, informal Sections 1 and 5, and the separate blind readback. The main source has 22 authored definitions/abbreviations and 10 principal theorems including the nine-clause root. Inspect all n including zero, arbitrary real matrices without symmetry/commutation premises, the actual Equiv from Fin n sum Fin n to increasing Fin(n+n), mirrored right-half order, alternating signs starting +1, Gram matrices, normalization by sqrt(2), generic sector exchange, odd rank-one survival and the n=1 distinct-sector counterexample. Do not confuse the optional global-sign conversion with a necessary source correction. Distinguish compression from invariant-subspace decomposition.

Create a NEW private execution workspace under /mnt/f/tools/math-audit-round12-20260926/formal-reviewer/. Copy only frozen inputs. Do not write author or source project files. Adapt supplied run.py only for your own paths and reviewer role, recording its new hash and all path changes. Use Lean 4.31.0 at /mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe and lake.exe; package artifacts under /mnt/f/LaTeX/BVE research/lean-proof/.lake/packages are read-only. The unchanged installed lean-verify 2.0.1 verifier may be read and executed. No installation, downloads or full lake build are necessary.

Actually compile the frozen AuditRound12.lean, use complete-export/ExportRound12.lean (adapt its output file into your own directory, retaining the full pretty-printer options) to export and compare all 59 declarations/definition bodies and transitive axioms, and invoke the unchanged installed verify_lean_project.py using --direct --strict-exit, explicit compiler paths, exact contract and a fresh output directory. Check actual import resolution, local object/source identity, runtime/environment binding, exact root and full axiom closure. Personally execute positive controls and all three deliberate mathematical negatives; confirm negatives fail for the false sector/mirror-sign/normalization assertions rather than syntax/import failures. Supply any missing complementary positive witnesses. Also run the wrong-type contract against the original verifier and require target_mismatch. Current source should use only propext, Classical.choice and Quot.sound; report any extra, unknown or unsafe dependency.

Preserve actual argv, cwd, selected environment, source hashes, all exits/stdout/stderr, unsuccessful attempts, module origins and a SHA-bound execution manifest. Report exact evidence paths in final JSON. Author machine flags are not independent acceptance. This target is finite matrix algebra with a coordinate/normalization bridge; it does not formalize Green functions, phase monotonicity, Sturm-Liouville differentiability, a formal inertia index/Sylvester law or numerical Python correctness. Do not upgrade any of those from local Lean success.
'''
put('execution-scope.md', Scope.encode(), 'independent-execution-and-scope-contract')
Spec = dict(kind='mathematics', author_ids=['01a06f46-dd03-7c83-9267-32048412c359', '01a0dce9-5748-7710-9a4e-adff48f38f61', '01a0dce3-b8a0-7d83-b359-03a8073d76d4'], inputs=Inputs, claims=[
	dict(id='R12-formal-coordinate-fidelity', verification='formal', statement='Compare all quantifiers, actual coordinate Equiv, signs, normalized/un-normalized bases and compression/scaling bridges with intended mathematics and independent blind readback. Check arbitrary n including zero and absence of unnecessary symmetry/commutation assumptions.'),
	dict(id='R12-formal-sector-rankone-fidelity', verification='formal', statement='Verify generic sector exchange, odd rank-one survival, optional global-sign convention and explicit distinct-sector counterexample faithfully address the stated local repair. Inspect actual definitions and all binders; state absent ODE/Green/inertia/software bridges.'),
	dict(id='R12-independent-formal-execution', verification='formal', statement='Personally execute the fresh compiler, original exact-root verifier, 59 declaration/definition/axiom comparisons, meaningful positive and three mathematical negatives, and wrong-contract negative in execution-scope.md. Preserve actual failures, source/environment bindings and paths.')])
(Out / 'formal-comparison-spec.json').write_text(json.dumps(Spec, ensure_ascii=False, indent=2) + '\n')
(Out / 'formal-comparison-root.json').write_text(json.dumps(dict(project=str(Root))) + '\n')
(Out / 'formal-comparison-packet.json').write_text(json.dumps(Review.create_packet(Root, Spec), ensure_ascii=False, indent=2) + '\n')
print('Prepared formal comparison', len(Inputs), 'inputs', flush=True)
