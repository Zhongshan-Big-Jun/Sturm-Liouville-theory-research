"""Assemble review from independently checked, completed evidence; preserve inputs."""
import datetime
import hashlib
import json
from pathlib import Path

OWN=Path(__file__).resolve().parent
ROOT=OWN.parent
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def write_new(p,obj):
    with p.open('x',encoding='utf-8') as f:
        f.write(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

packet=read(ROOT/'PACKET.json')
initial=read(OWN/'initial-hashes.json')
audit=read(OWN/'execution-audit.json')
if not audit['passed'] or audit['errors'] or len(audit['results'])!=4:
    raise RuntimeError('independent audit not complete and clean')
final={}
for p,v in initial['files'].items():
    actual=sha(ROOT/p)
    final[p]=dict(expected_sha256=v['expected_sha256'],before_sha256=v['actual_sha256'],after_sha256=actual,matches=actual==v['expected_sha256'],unchanged=actual==v['actual_sha256'])
if not all(v['matches'] and v['unchanged'] for v in final.values()):
    raise RuntimeError('frozen packet changed')
write_new(OWN/'final-hashes.json',dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),packet_sha256=sha(ROOT/'PACKET.json'),listed_files_checked=52,packet_checked_separately=True,all_match=True,all_unchanged=True,files=final))

clean=[r for r in audit['results'] if not r['mutant']]
mutants=[r for r in audit['results'] if r['mutant']]
first_run=Path(clean[0]['run'])
candidate=read(first_run/'results/candidates-normal.json')
original=read(first_run/'results/originals-normal.json')
by_name={r['name']:r for r in original['checks']}
executions=[]
for name in ['verify-normal','replay-normal','verify-optimized','replay-optimized','mutant-verify-normal','mutant-replay-normal','mutant-verify-optimized','mutant-replay-optimized','independent-output-audit']:
    out=OWN/'executions'/name
    r=read(out/'receipt.json')
    executions.append(dict(name=name,argv=r['argv'],cwd=r['cwd'],pid=r['pid'],started_utc=r['started_utc'],seconds=r['seconds'],exit_code=r['exit_code'],expected_exit=r['expected_exit'],receipt=rel(out/'receipt.json'),receipt_sha256=sha(out/'receipt.json'),stdout=rel(out/'stdout.txt'),stdout_sha256=r['stdout_sha256'],stderr=rel(out/'stderr.txt'),stderr_sha256=r['stderr_sha256'],frozen_unchanged=r['frozen_unchanged']))

patch_notes={
 'op03_gap_fh.py':('backend switch and paired factor',[5,23],'Actual Df_at/backend functions, source-formatted expression, and complete instrumented CLI.'),
 'gap_n1_grad.py':('INF width-gradient signs',[44],'Actual spectral/gradient functions and exact gFH AST; original outer loop omitted.'),
 '_tmp_fh_paradox.py':('paired sum and SUP/INF signs',[27,28],'Actual D_and_f and exact fh/fh2 AST; original outer loops omitted.'),
 'tmp_fh_test.py':('INF eigenvalue and gap signs',[26,27,30],'Actual lam_of and exact fh1/fh2/formatted-gap AST; original outer loop omitted.'),
 'tmp_verify_endpoints.py':('paired derivative signs',[30],'Actual D_and_f and exact fh AST; endpoint scan and brentq search omitted.'),
 '_gapn2_hess_verify.py':('lower eigenvalue, gradient and stationary Hessian signs',[40,46,47,60,61],'Actual D_edges, f/printed-gradient/H1/H2 AST; J supplied by jac_fd; main and analytic_jacobian_hp not exercised.'),
 '_gapn2_hess_sign_and_bigR.py':('matrix product preserving off-diagonal entries',[61],'Actual hess_fd and H AST with both signs, jac_fd input; main and large-R scan not exercised.'),
 '_gapn2_jacobian_analytic.py':('stationary Hessian matrix product',[289],'Actual eigen_data and H AST with Jfd; old analytic Jacobian and continuation not certified.'),
 '_gapn2_o3_scan.py':('stationary Hessian spectrum matrix product',[74],'evH AST only with jac_fd input; module/main/spectral Jacobian scan not executed.'),
 '_gapn2_second_variation_probe.py':('stationary Hessian matrix product',[213],'Hess AST only; module/main and P1/P2/P3 density-path probes not executed.')
}
patches=[]
for name,(topic,lines,scope) in patch_notes.items():
    orig='originals/scripts/'+name; cand='candidates/scripts/'+name
    patches.append(dict(path=cand,original_path=orig,original_sha256=packet['files'][orig],candidate_sha256=packet['files'][cand],changed_lines=lines,assessment='PASS within stated local contract',change=topic,executed_scope=scope))
if sum(packet['files'][p]!=packet['files'][p.replace('candidates/','originals/',1)] for p in packet['files'] if p.startswith('candidates/'))!=10:
    raise RuntimeError('wrong delta count')

children=[]
for replay in audit['results']:
    run=Path(replay['run'])
    for r in replay['runs']:
        name=r['name']
        children.append(dict(replay=rel(run),mutant=replay['mutant'],outer_optimize=replay['optimize'],name=name,pid=r['pid'],exit_code=r['exit_code'],module_count=r['module_count'],module_categories=r['categories'],required_bindings=r['required_count'],provenance_problems=r['problems'],numerical=None if 'numerical' not in r else dict(tests=r['numerical']['tests'],passed=r['numerical']['passed'],failed=len(r['numerical']['failed_names'])),cli_cases=r.get('cli_cases'),result=rel(run/'results'/(name+'.json')),receipt=rel(run/'receipts'/name/'receipt.json'),stdout=rel(run/'receipts'/name/'stdout.txt'),stderr=rel(run/'receipts'/name/'stderr.txt')))

math_limits=[
 'Local interface formulas assume positive ordered block densities, simple Dirichlet eigenvalues, weighted eigenfunctions normalized by integral rho*u_k^2=1, and the stated edge orientation.',
 'Finite floating-point checks at R=4, nonstationary n=1 fixtures, and stationary n=1,2 SUP/INF fixtures; no interval enclosure or exact-zero certificate.',
 'The simplified Hessian requires F=f/lambda_{n+1}=0. Away from stationarity the outer(F,grad lambda) term is necessary; finite residuals do not prove exact stationarity.',
 'Sixteen distinct recorded source AST expressions span all ten patches. AST substitution with jac_fd verifies those local expressions, not the original callers using analytic_jacobian_hp or analytic_jacobian_spectral.',
 'No full old analytic/Green/resolvent/spectral-summation Jacobian audit, infinite-tail estimate, all-R/all-n continuation or global scan is claimed.',
 'No global extremum, branch uniqueness, root simplicity theorem, historical certificate/proof audit, Lean verification, or P1/P2/P3 density-path derivation is certified.',
 'Only op03_gap_fh receives a complete actual four-point instrumented CLI execution; other changed scripts have the precisely documented function/AST scope.',
 'The unchanged op03_gap_precise normalization defect remains excluded; the selected candidate op03_gap_fh imports op03_gap_fixed. No eleventh source was repaired.'
]
runtime_limits=[
 'This is acceptance of the observed end-of-execution file-backed sys.modules snapshot, not OS/process isolation or import prevention. The benign outside module executes before refusal.',
 'No continuous import trace, transient/unloaded-module guarantee, malicious sys.modules metadata/evasion resistance, arbitrary-file-read trace, or shared-library provenance certification.',
 'File hashes establish recorded source identity at observation and before/after execution; they do not prove execution of every line or exclude transient mid-run changes.',
 'Built-in/namespace modules with no __file__ are excluded by the explicitly stated file-backed contract. The instrumented CLI changes launch machinery while executing the complete unchanged target source.',
 'Executed only installed Linux/WSL Python 3.14.4, NumPy 2.5.2, SciPy 1.18.1. No native Windows or other-platform claim.',
 'Installed runtime roots are discovered and documented, not supply-chain certified. Allowed roots are exact NumPy/SciPy directories plus stdlib excluding site/dist-packages; their search-directory parents are not blanket provenance allowances.',
 'PACKET is the sole frozen identity boundary. No live/main-tree or author/sibling-directory comparison was performed. Matching historical hashes means matching supplied records only.',
 'The initial python command failed before per-stream capture existed; the exact tool-combined output, command, status and hashes are preserved. All substantive test subprocesses have separate raw stdout/stderr receipts.'
]

review=dict(
 schema='independent-software-review-round7-v2',
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 verdict='APPROVED',
 verdict_reason='No substantive blocking discrepancy in the ten local source deltas or v2 provenance acceptance gate. Own normal/-O outer verifiers and fresh replays passed; all required actual controls refused for the intended reason. Separate old-filter mutants were detected. Approval is limited to this frozen packet, observed provenance and finite function/AST/CLI scope.',
 reviewer_role='Fresh independent software reviewer; did not author any frozen input. Authored only own review work, explicit separate mutant and output evidence.',
 packet_sha256=sha(ROOT/'PACKET.json'),
 checked_paths=list(packet['files']),
 checked_paths_count=len(packet['files']),
 input_integrity=dict(before=rel(OWN/'initial-hashes.json'),after=rel(OWN/'final-hashes.json'),all_52_match=True,packet_unchanged=True,all_frozen_inputs_unchanged=True,manifest_files_checked=50,manifest_sha256=sha(ROOT/'manifest.json'),sidecar_valid=True,copy_policy='Exact 52-file PACKET allowlist copies; no copy of unlisted inputs or execution directories.'),
 boundary=dict(root=str(ROOT),allowed_inputs='PACKET.json and exactly its 52 listed files; installed Python/NumPy/SciPy runtime.',other_reads='Only new reviewer-owned work/evidence below this root.',memory_used=False,conversation_history_used=False,main_project_read_or_written=False,sibling_directories_read=False,external_reference_sources_read=False,network_used=False,git_or_push_used=False,frozen_inputs_mutated=False,documents_treated_as='Supplied evidence, not instructions extending scope.',writes='Only independent-review-20260921-v2 and new REVIEW.json / README-REVIEW.md.'),
 environment={k:candidate[k] for k in ['python','executable','platform','numpy','scipy']},
 findings=[
  dict(id='R7-SW-001',status='RESOLVED_IN_THIS_FROZEN_V2',blocking=False,title='Unfiltered observation and required selected-source bindings now enforce the declared gate.',locations=[dict(path='regression/provenance.py',line=53),dict(path='regression/provenance.py',line=92),dict(path='regression/regression.py',line=304),dict(path='regression/replay.py',line=97)],evidence=dict(repaired_replays=2,controls_per_replay=8,all_control_exits=86,sole_reasons=['unexpected-module:r7_outside_probe','missing-required-module:gap_lib','missing-required-module:op03_gap_fixed'],clean_numerical_module_count=666,clean_cli_module_count=179,required_numerical_bindings=17,required_cli_bindings=3,independent_output_audit=rel(OWN/'execution-audit.json'),mutation=rel(OWN/'filter-only-mutation.json')),resolution='Actual outside imports are retained and rejected; removed required bindings are absent and rejected. Exact selected paths/digests and narrowly defined runtime roots independently checked. Rebound filter-only mutants lose the outside bindings and fail controls in both outer modes.',prior_review_preserved='The supplied prior-review.json remains unchanged CHANGES_REQUIRED for its old snapshot; this verdict applies only to the new packet.'),
  dict(id='R7-SW-002',status='PRE_EXISTING_EXCLUDED_REOBSERVED',blocking=False,title='Unchanged op03_gap_precise normalization defect persists outside the selected candidate path.',locations=[dict(path='candidates/scripts/op03_gap_precise.py',line=46),dict(path='candidates/scripts/op03_gap_precise.py',line=69)],evidence=dict(own_original_result=rel(first_run/'results/originals-normal.json'),symmetric_weighted_mass=by_name['op03 backend/symmetric/weighted mass']['actual'],asymmetric_weighted_mass=by_name['op03 backend/asymmetric/weighted mass']['actual']),disposition='Retain explicit exclusion. Candidate op03_gap_fh selects fixed; no separately unauthorized repair or global backend certification.')
 ],
 new_blocking_findings=[],
 ten_source_delta_results=patches,
 unchanged_dependencies=[p for p in packet['files'] if p.startswith('candidates/') and packet['files'][p]==packet['files'][p.replace('candidates/','originals/',1)]],
 source_review=rel(OWN/'source-review.md'),
 complete_source_diff=rel(OWN/'ten-deltas.diff'),
 all_36_source_data_copies_match_supplied_prior_hash_record=True,
 own_execution_evidence=dict(author_results_counted_as_own=False,executions=executions,child_executions=children,independent_audit=rel(OWN/'execution-audit.json'),independent_audit_source=rel(OWN/'audit_evidence.py'),repaired_replay_count=2,repaired_child_count=28,repaired_controls=16,all_repaired_controls_refuse_intended_reason=True,numerical=dict(per_process_tests=117,clean_candidate_passed=117,original_passed=38,original_failed=79,normal_optimized_names_and_statuses_agree=True,independently_recomputed_from_saved_values=True),actual_cli=dict(points=[.4,.43,.45,.458],four_clean_processes_across_outer_and_inner_modes=True,all_control_cli_processes_also_execute_four_points=True),mutation=dict(separate_rebound=True,changed_files=['regression/provenance.py','manifest.json','manifest.sha256'],outer_modes=['normal','optimized'],each_replay_exit=1,each_four_outside_controls_incorrectly_exit=0,each_four_missing_controls_exit=86,record=rel(OWN/'filter-only-mutation.json'),diff=rel(OWN/'filter-only-mutation.diff')),bootstrap_failure=rel(OWN/'bootstrap-failure.json'),all_new_failures_retained=True),
 historical_context=dict(private_missing_file='inputs/tools-AGENTS.md',not_supplied=True,not_read=True,not_executable_dependency=True,not_permission_to_follow_references=True,unchanged_context_manifest='inputs/snapshot-manifest.json',historical_failures='Prior missing-NumPy/backend/selector failures and author v2 startup-hook/mutant failures are supplied documentary evidence only; their unsupplied raw historical directories were not read or counted as own runs.'),
 mathematical_limitations=math_limits,
 runtime_limitations=runtime_limits,
 artifact_hash_inventory=rel(OWN/'artifact-index.json'),
 artifact_hash_inventory_note='Created after the review; lists all reviewer-owned files and the two final reports, excluding itself to avoid self-hashing.'
)
write_new(ROOT/'REVIEW.json',review)

readme=f'''# Round7 independent software review v2 — APPROVED

The ten local source deltas and repaired R7-SW-001 provenance gate have no substantive blocking discrepancy within the frozen packet and the executed scope.

Packet SHA-256: `{review['packet_sha256']}`. All 52 listed input files matched before and after review; PACKET.json was also unchanged. No frozen file, main source, external referenced source, private context or sibling directory was edited/read beyond the stated boundary; no Git operation or push was used.

| Own execution | Normal outer | -O outer |
| --- | --- | --- |
| Actual package verifier, 50 entries plus manifest sidecar | exit 0 | exit 0 |
| Complete fresh replay, both inner modes, 14 cases | exit 0 | exit 0 |
| Candidate numerical checks per process | 117/117 | 117/117 |
| Original negative checks per process | 38 pass, 79 fail; exit 1 | 38 pass, 79 fail; exit 1 |
| Actual candidate CLI | all four points pass in each inner mode | all four points pass in each inner mode |
| Eight real provenance controls per replay | all exit 86 for intended sole reason | all exit 86 for intended sole reason |
| Separate rebound old-filter mutant, eight controls | replay exit 1 as expected | replay exit 1 as expected |

The four CLI points are u=0.400, 0.430, 0.450, 0.458. Clean numerical snapshots contain 666 file-backed modules (17 required project/harness, 147 stdlib, 502 installed package); clean CLI snapshots contain 179 (3 required, 92 stdlib, 84 installed package). Outside controls add a real imported module and refuse; missing controls remove a real required binding and refuse. Exact selected paths and frozen digests were checked independently. NumPy/SciPy package directories and stdlib excluding site/dist-packages are the runtime allowances; their parent directories receive no blanket acceptance.

Restoring only the old collector filter in a **separate, explicitly rebound mutant** makes each of the four outside controls incorrectly exit 0, while the four missing controls still exit 86. Each mutant replay therefore exits 1. This is own sensitivity evidence, not an author result or a candidate modification.

The reviewer-written output audit passed across all 44 repaired/mutant children. It independently recomputed the 117 numerical truth checks, checked the 16 distinct recorded AST expressions across all ten patches, checked required and observed source hashes/paths, and verified raw stream hashes, statuses and exact refusal reasons. All original failures, mutant failures and the initial `python`-not-found bootstrap failure are retained. Actual commands and per-process evidence paths are in REVIEW.json and the receipts.

Approval covers finite tests, the documented source functions/AST nodes, the complete instrumented op03 CLI, and the observed file-backed provenance gate. It does **not** certify OS isolation, import prevention, transient/malicious module behavior, full old analytic/spectral Jacobians, global scans, historical proofs, or density-path P1/P2/P3 calculations. The simplified Hessian requires stationarity; the general product-rule term remains necessary. The unchanged legacy op03_gap_precise normalization defect (R7-SW-002) is reobserved and explicitly excluded from approval.

The historical `inputs/tools-AGENTS.md` reference is disclosed in unchanged supplied manifests. The file was not supplied or read, is not an executable dependency, and gives no permission to follow that reference. The old prior-review.json remains CHANGES_REQUIRED for its old snapshot.

- [Structured verdict, checks, limitations and actual commands](REVIEW.json)
- [Independent derivation and ten-source review]({rel(OWN/'source-review.md')})
- [Independently audited execution evidence]({rel(OWN/'execution-audit.json')})
- [Before hashes]({rel(OWN/'initial-hashes.json')}) and [after hashes]({rel(OWN/'final-hashes.json')})
- [Separate mutant description]({rel(OWN/'filter-only-mutation.json')})
- [All own artifact hashes]({rel(OWN/'artifact-index.json')})

Only supplied inputs and installed Python/NumPy/SciPy were used, together with this reviewer's new own work. The reviewer-owned AGENTS.md records the method and this request; frozen AGENTS.md was preserved.
'''
with (ROOT/'README-REVIEW.md').open('x',encoding='utf-8') as f: f.write(readme)
with (OWN/'AGENTS.md').open('a',encoding='utf-8') as f:
    f.write('\nMaintenance 3: issued REVIEW.json and README-REVIEW.md with bounded APPROVED verdict, resolved R7-SW-001, retained excluded R7-SW-002, exact execution references and mathematical/runtime limitations. Final packet and all 52 listed hashes match the initial inventory. Sealed the own artifact index after report creation. Frozen AGENTS.md and every other input remain unchanged.\n')
index={rel(p):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name!='artifact-index.json'}
for p in (ROOT/'REVIEW.json',ROOT/'README-REVIEW.md'):
    index[rel(p)]=dict(sha256=sha(p),bytes=p.stat().st_size)
write_new(OWN/'artifact-index.json',dict(schema='independent-review-artifacts-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),excludes_self=True,files=index))
for p,info in index.items():
    if sha(ROOT/p)!=info['sha256']:
        raise RuntimeError('output hash mismatch '+p)
for p,v in initial['files'].items():
    if sha(ROOT/p)!=v['actual_sha256']:
        raise RuntimeError('final frozen mismatch '+p)
print(json.dumps(dict(verdict=review['verdict'],packet_sha256=review['packet_sha256'],checked_input_files=52,own_artifacts_indexed=len(index),review_path=str(ROOT/'REVIEW.json'),readme_path=str(ROOT/'README-REVIEW.md'),artifact_index_sha256=sha(OWN/'artifact-index.json')),indent=2))
