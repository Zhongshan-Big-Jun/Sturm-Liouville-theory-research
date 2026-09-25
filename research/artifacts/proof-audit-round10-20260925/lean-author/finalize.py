from run import *
import re

MANIFEST_PATH = BASE / 'evidence/exact-root-02/run-manifest.json'
MANIFEST = json.loads(MANIFEST_PATH.read_text())
DECLARATION_PATH = next((BASE / 'evidence/exact-root-02/lean-verification-runs').glob('*/declaration.json'))
DECLARATION = json.loads(DECLARATION_PATH.read_text())
assert MANIFEST['machine_verification_passed'] is True
assert MANIFEST['exact_root_passed'] is True
assert DECLARATION['declaration'] == 'AuditRound10.root'
assert DECLARATION['comparison']['status'] == 'matched'
assert DECLARATION['comparison']['definitionally_equal'] is True
assert set(DECLARATION['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}

EXPECTED = {
	'runtime-version':0, 'development-01':1, 'development-02':0, 'development-03':1,
	'final-source-01':0, 'positive-refutations-01':1, 'positive-refutations-02':0,
	'negative-flip-01':1, 'negative-reflection-01':1, 'negative-index-01':1,
	'print-main-01':0, 'print-controls-01':0, 'explicit-export-01':0,
	'explicit-export-full-01':0, 'blind-source-01':0, 'exact-root-01':1, 'exact-root-02':0}
COMMANDS = []
for Label, Expected in EXPECTED.items():
	PathArg = BASE / 'commands' / Label / 'command.json'
	Record = json.loads(PathArg.read_text())
	assert Record['exit_code'] == Expected, (Label, Record['exit_code'])
	assert Record['inputs_unchanged'] is True, Label
	assert digest(PathArg.parent / 'stdout.log') == Record['stdout_sha256']
	assert digest(PathArg.parent / 'stderr.log') == Record['stderr_sha256']
	COMMANDS.append({'label':Label,'exit_code':Record['exit_code'],'seconds':Record['seconds'],
		'command_record':str(PathArg.relative_to(BASE)),'record_sha256':digest(PathArg)})
write_json(BASE / 'execution-summary.json', COMMANDS)

NAMES = json.loads((BASE / 'declaration-names.json').read_text())
PRINTED = {}
for Label in ['print-main-01', 'print-controls-01']:
	Log = (BASE / 'commands' / Label / 'stdout.log').read_text()
	for Match in re.finditer(r"^'([^']+)' depends on axioms: (\[[^\n]*\])$", Log, re.M):
		Axioms = [A.strip().split('.{')[0] for A in Match[2][1:-1].split(',') if A.strip()]
		assert set(Axioms) <= {'propext','Classical.choice','Quot.sound'}
		PRINTED[Match[1]] = {'axioms':Axioms,'raw':Match[0],'log':'commands/'+Label+'/stdout.log'}
assert set(PRINTED) == set(NAMES['main'] + NAMES['controls'])
write_json(BASE / 'per-declaration-axioms.json', PRINTED)
EXPORT = json.loads((BASE / 'formal-declarations-full.json').read_text())
EXPORTED = {E['name']:E for E in EXPORT}
for Name in NAMES['main']:
	assert Name in EXPORTED
	assert '⋯' not in EXPORTED[Name]['type_explicit']
	assert '...' not in EXPORTED[Name]['type_explicit']
	if 'value_explicit' in EXPORTED[Name]:
		assert '⋯' not in EXPORTED[Name]['value_explicit']
write_json(BASE / 'export-coverage.json', {'main_declarations':NAMES['main'], 'controls':NAMES['controls'],
	'full_explicit_types_have_no_ellipsis':True, 'named_print_and_axiom_coverage_complete':True,
	'full_export_sha256':digest(BASE / 'formal-declarations-full.json'),
	'ordinary_readable_types':'May suppress proof terms; type_explicit is the complete type.'})

SOURCE = (PROJECT / 'AuditRound10.lean').read_text()
assert not re.search(r'\b(sorry|admit|axiom|unsafe)\b', SOURCE)
FINAL_SOURCE_RECORD = json.loads((BASE / 'commands/final-source-01/command.json').read_text())
assert digest(PROJECT / 'AuditRound10.lean') == FINAL_SOURCE_RECORD['inputs_after'][str(PROJECT / 'AuditRound10.lean')]
FROZEN_INPUTS = json.loads((BASE / 'frozen-root-inputs.json').read_text())
for Name, Data in FROZEN_INPUTS.items():
	assert digest(BASE / 'root-project' / Name) == Data['sha256']
assert (BASE / 'root-project/AuditRound10.lean').read_bytes() == (PROJECT / 'AuditRound10.lean').read_bytes()
PACKET = json.loads((BASE / 'formal-only/packet.json').read_text())
for Rel, Data in PACKET['files'].items():
	assert digest(BASE / 'formal-only' / Rel) == Data['sha256']

BEFORE = json.loads((BASE / 'external-input-identities.json').read_text())
AFTER = {P:{'before':D['sha256'],'after':digest(P),'unchanged':digest(P)==D['sha256']} for P,D in BEFORE.items()}
write_json(BASE / 'external-input-postcheck.json', AFTER)
for P,D in AFTER.items():
	if 'plugins/cache/' in P or 'round9-' in P or '/DevCache/' in P:
		assert D['unchanged'], P

JOB = json.loads((BASE / '.research-state/jobs/exact-root-02-durable.json').read_text())
assert JOB['state'] not in ['RUNNING','DISPATCHED'], JOB['state']
COMPACT = {'role':'mathematics-and-Lean-author','final_source':str(PROJECT / 'AuditRound10.lean'),
	'final_source_sha256':digest(PROJECT / 'AuditRound10.lean'),
	'root':'AuditRound10.root','root_contract_sha256':digest(BASE / 'root-contract.json'),
	'machine_verification_passed':MANIFEST['machine_verification_passed'],
	'exact_root_passed':MANIFEST['exact_root_passed'],
	'axioms':DECLARATION['axioms'], 'comparison_status':DECLARATION['comparison']['status'],
	'loaded_module_count':DECLARATION['loaded_module_count'],
	'independent_readback':'pending coordinator dispatch', 'independent_semantic_verification':'pending coordinator dispatch',
	'full_project_build':'not run', 'core_source_contains_open_placeholders':False,
	'negative_controls':{L:1 for L in ['negative-flip-01','negative-reflection-01','negative-index-01']},
	'positive_counterexample_proofs':'positive-refutations-02',
	'durable_job':{'job_id':JOB['job_id'],'state':JOB['state']},
	'verifier_manifest':str(MANIFEST_PATH),'verifier_manifest_sha256':digest(MANIFEST_PATH),
	'blind_packet':'formal-only/packet.json','blind_packet_sha256':digest(BASE / 'formal-only/packet.json'),
	'contract':'HUMAN-CONTRACT.md','contract_sha256':digest(BASE / 'HUMAN-CONTRACT.md')}
write_json(BASE / 'author-result.json', COMPACT)

ROWS = '\n'.join('| '+C['label']+' | '+str(C['exit_code'])+' | '+f"{C['seconds']:.3f}"+' |' for C in COMMANDS)
REPORT = f'''# Round10 local Lean author handoff

作者侧局部形式化完成. 指定最终源码与合取根已由实际 Lean 编译, 原版 lean-verify 2.0.1 返回 machine_verification_passed=true 和 exact_root_passed=true. 这不是独立语义验收, 也不是完整 Lean 工程通过.

## Mathematical content

`project/AuditRound10.lean` 从 `Fin (2*n)` 上真实 `Fin.rev` 定义实线性 J, 坐标定理明确其值为 `2*n-1-i`. 两个线性投影严格定义为 `(I-J)/2` 与 `(I+J)/2`. 证明包括线性性, 对合, 两种特征关系, 分解, 幂等, 双向消去, 固定点/特征空间等价, 反转保持 Euclidean 点积及两个投影范围正交. 还证明 `R(x)=1-Jx` 的对合与精确扰动公式, 并识别对称基点处的保持/破缺方向.

相位部分使用实函数在 `[0,∞)` 上的连续性和严格递增性. `phase_root Phi k x` 精确定义为 `0≤x ∧ Phi x=kπ`. IVT 给出有效闭括区中的唯一解; 已知相位根满足 `x<y ↔ j<k`; 严格递增的指标及逐指标有效括区给出位于括区内的严格递增根序列. 存在性使用 classical choice, 不是数值算法.

`AuditRound10.root` 是全部 21 项局部接口的显式合取. 投影定理从实际定义推出, 未将投影性质当作假设; 相位连续性, 严格单调性和有效括区则按任务要求保留为显式前提. `root-contract.json` 与 `root-exact-type.lean.txt` 保存完整预期 Lean 类型; `root-clauses.json` 逐项列出组成声明. 机械匹配也检查 binder kinds 和 universe parameters; informal 合同性仍须后续独立检验.

## Execution and identity

- Lean: {(BASE / 'commands/runtime-version/stdout.log').read_text().strip()}.
- Final source SHA-256: `{COMPACT['final_source_sha256']}`.
- Root contract SHA-256: `{COMPACT['root_contract_sha256']}`.
- Exact-root durable job: `{JOB['job_id']}`, actual terminal state `{JOB['state']}`.
- Root dependency axioms: `{', '.join(DECLARATION['axioms'])}`. No sorryAx or additional axioms were found in the actual selected root closure.
- Full imported-module inventory, dependency closure, expected-type comparison, source/tool/runtime/environment hashes and Lean job logs: `evidence/exact-root-02/run-manifest.json` and its immutable per-run directory. The verifier checks the minimal frozen `root-project/`, whose core source is byte-identical to `project/AuditRound10.lean`. Loaded environment inventory contains {DECLARATION['loaded_module_count']} modules; this is an evidence inventory count, not a count of new mathematical results.
- `commands/*/command.json` saves actual argv, cwd, relevant environment, process ID, start/end, exit code, input hashes and log hashes. Each command directory contains full stdout/stderr and input snapshots. `REPLAY.md` gives non-overwriting replay commands.

| Command label | Actual exit | Seconds |
| --- | --- | --- |
{ROWS}

## Preserved failures and negative controls

- development-01: true exit 1. Fin.rev subtraction was propositionally but not definitionally equal; a distributive coordinate identity needed ring; an ordered-multiplication lemma requested an unsuitable generic instance. Corrected with Fin.ext/omega, ring, and real arithmetic.
- development-03: true exit 1. A style cleanup ran ring after simp had already closed one constructor branch. Split branches explicitly.
- positive-refutations-01: true exit 1. norm_num had already closed the off-by-one contradiction before later tactics. Removed only those unreachable tactics; positive-refutations-02 returned 0.
- exact-root-01: true exit 1, evidence status stale. All Lean jobs returned 0 and the exact type matched, but the verifier's project-wide source snapshot detected the repaired Counterexamples.lean and newly added ReadbackExportFull.lean. This first root run is not a pass. The successful successor checks a separate minimal frozen root-project and leaves the first result intact.
- NegativeFlip: F=-J on v=(1,1) was falsely asserted idempotent. Lean rejected the false equality with an unresolved False goal.
- NegativeReflection: a plus sign was falsely used in the reflection perturbation, for x=0,v=(1,1). Lean rejected it with an unresolved False goal.
- NegativeIndex: Phi(x)=x at x=2π was falsely assigned level 1π. Lean rejected it, with False remaining under the true premise 0<π.
- `Counterexamples.lean` proves all three exact negations. `PrintCounterexamples.lean` and corresponding logs export their statements/proofs and axioms. Negative compiler failures therefore have mathematical witnesses, not just failed tactics.
- The first structured export had pretty-print truncation in large explicit types. It remains saved. `formal-declarations-full.json` and its exporter were regenerated under higher printing limits; all named `type_explicit` and definition bodies have no ellipses. Ordinary readable types may suppress proof terms.

## Files for the coordinator

1. `formal-only/packet.json`: hashed blind packet with comment-free real source, actual declarations, explicit types/definitions, #print/#print axioms output, toolchain, package pinning and runtime search paths. It contains no author-intent prose or audit verdict. The transformed source itself compiled as blind-source-01. `blind-transform.json` records the sole removed comment and both hashes.
2. `HUMAN-CONTRACT.md`: separate per-target intended statements, domains, assumptions, boundary cases and exclusions. Do not give it to the first blind reader. Give it to the separate semantic comparison reviewer afterward.
3. `per-declaration-axioms.json`, `export-coverage.json`: coverage and axiom extraction for every named main declaration and positive counterexample.
4. `author-result.json`, `execution-summary.json`: compact author-side results. These do not manufacture an independent review.

## Exact remaining scope

Fresh isolated blind readback and a separate intended-versus-formal semantic check remain for the coordinator. No Sturm-Liouville theory, infinite-dimensional operator, Prüfer phase differential equation or lift, spectral/phase index identification, comparison bound, floating-point/interval enclosure, executable root enumerator or its termination is formalized here. Strictly increasing indices may skip levels; full coverage requires choosing the desired consecutive indices. Unboundedness is not assumed or derived, so all-level root existence remains conditional on the supplied brackets. Vector algebra does not certify feasible ordered interfaces, clipping, normalization, Hessian sectors or global extremizers.

All task-created files are under the authorized formal-author directory. No project, old evidence, plugin or Git write was performed. `external-input-postcheck.json` covers only the explicitly recorded read inputs, not a full-project protection audit; concurrent project maintenance by the coordinator is outside this author's evidence scope. AGENTS.md records the method and actual dialogue/task constraints.
'''
(BASE / 'REPORT.md').write_text(REPORT)
with (BASE / 'AGENTS.md').open('a') as File:
	File.write('\n- 2026-09-25. Final handoff: complete core and blind source compiled; all three mathematical negative controls rejected with accepted opposite proofs; all named print/axiom outputs and fully explicit types saved. Original verifier exact root completed with only the allowed foundational axioms. Frozen formal-only packet and separate per-target human contract delivered. Independent readback/semantic review, complete Sturm theory and executable solver correctness remain unclaimed. No commit or project/plugin/old-evidence write.\n')

FILES = {}
for P in sorted(BASE.rglob('*')):
	if P.is_file() and P.name not in ['handoff-manifest.json', 'finalization.log'] and '/tmp/' not in str(P):
		FILES[str(P.relative_to(BASE))] = {'sha256':digest(P),'bytes':P.stat().st_size}
write_json(BASE / 'handoff-manifest.json', {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'role':'author','root_declaration':'AuditRound10.root',
	'exclusions':['tmp/','handoff-manifest.json','finalization.log (still open during manifest creation)'], 'files':FILES})
print(json.dumps(COMPACT,ensure_ascii=False,indent=2))
