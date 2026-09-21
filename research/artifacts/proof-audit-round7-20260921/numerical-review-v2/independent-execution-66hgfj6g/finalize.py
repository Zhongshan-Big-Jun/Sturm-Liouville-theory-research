import datetime
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
PREFIX=str(OUT.relative_to(ROOT))

def load(rel):
    return json.loads((ROOT/rel).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

preparation_errors={
    'scope':'Verifier-owned report preparation only; neither command executed or changed a frozen checker/input. These are retained tooling errors, not failed mathematical or integrity checks.',
    'attempts':[
        {'command':'/usr/bin/python3 -B - with an inline Python generator intended to write independent-execution-66hgfj6g/finalize.py','returncode':1,'stdout':'','stderr':'  File "<stdin>", line 93\n    Read scope was PACKET.json, its 39 listed frozen files, installed Python/SymPy/mpmath runtime, and this execution\'s own outputs. All 39 packet-file SHA-256 values matched; PACKET.json itself was separately hashed. All inputs remained byte-identical after execution and at finalization. `inputs/manifest.json` is supplied, and all four of its snapshot entries are supplied, packet-listed, and match both their declared SHA-256 and byte counts. Original source paths, report claims, and historical commit labels were not treated as instructions or verified by accessing their external locations.\n                                                                                                                     ^\nSyntaxError: unterminated string literal (detected at line 93)\n','cause':'Nested triple-single-quoted source and report strings terminated the generator literal early.'},
        {'argv':['/usr/bin/python3','-B','independent-execution-66hgfj6g/finalize.py'],'returncode':2,'stdout':'','stderr':"/usr/bin/python3: can't open file '/mnt/f/tools/math-audit-round7-20260921/numerical-review-v2/independent-execution-66hgfj6g/finalize.py': [Errno 2] No such file or directory\n",'cause':'Previous generator had failed before creating the report script.'}
    ],
    'recovery':'Wrote only the verifier-owned report generator using a literal shell heredoc and reran report assembly. Frozen run_checks.py and checks.py were not rerun or modified.'
}
write(OUT/'report_preparation_errors.json',preparation_errors)
before=load(PREFIX+'/input_hashes.before.json')
after=load(PREFIX+'/input_hashes.after.json')
preflight=load(PREFIX+'/preflight.json')
outer=load(PREFIX+'/outer.execution.json')
verify=load(PREFIX+'/verification.json')
verification_process=load(PREFIX+'/verification.execution.json')
runtime=load(PREFIX+'/runtime.json')
notes=[
'Product-to-sum symbolic identity for the constant-density Wronskian; no variable-density theorem certified.',
'Symbolic recurrence and n=0 base checked; no audit of the referenced derivation notes.',
'Two exact polynomial identities at n=1,2,3,4,5,8,12 (14 identities).',
'Direct n=2, x=1/2 value is -4*pi; the old -6*pi value differs.',
'Fixed-n x^2 coefficient is 2*pi^4*(n^4-(n+1)^4); independent n=2 sample is -130*pi^4. No uniform remainder bound.',
'Both roots (11 +/- 2*sqrt(10))/36 satisfy the quadratic, lie in (0,1), and are simple.',
'Four-interface normalized determinant is 7030400000*pi^4/4782969 > 0; independently recomputed by a resultant. No Hessian definiteness implication.',
'Four roots ordered in (0,1), residuals <=1e-80, slope signs +,-,+,-; determinant product checked at 1e-75.',
'Segment mass primitive checked by differentiation and zero initial value.',
'rho=(1,4,1), a=1/4: two ordered shooting roots with residuals <=1e-75 and abs(f(a))>1.',
'Both weighted segment norms compared with quadrature at 1e-80; reflected squared eigenfunction values compared at 1e-75.',
'Both interfaces move: new roots at h=1e-5,1e-8,1e-11; O(h^2) convergence; final error 9.23088812046e-20 <=1e-18. Individual eigenvalue derivatives also checked.',
'Old mirrored formula is half the correct derivative; ratio approximately 2 and absolute discrepancy exceeds 20.',
'Only left interface moves: derivative 26.940486080120... agrees with one-interface FH within 1e-18.',
'One-sided second derivatives have jump -4.383575835224...; u and u-prime continuous in this example, u-second not continuous.',
'Exact plateau mass 2*R*d+(h-2*d)/3 and energy 4/(h-2*d); integral identities only.',
'20 exact cases with n=1,2,3,5,8 and R=8,10^3,10^6,10^9; Rayleigh bound and support geometry tested.',
'12 exact cases, 45 cells; positive leading minors for two-polynomial cell spaces (dimensions 4,6,8,12), not all of H_0^1.',
'Four real spectral samples: (1,1000),(2,1000),(3,1000),(2,1000000); reported inequalities independently rechecked.',
'Symbolic limits of scalar bounds for R=q^3 and d=q^-2; spectral theorem remains conditional on analytic bounds.',
'rho=1 gives gap (2*n+1)*pi^2; n=2 gives 5*pi^2, excluding a universal 4*pi^2 supremum limit for all n. No arbitrary branch limit certified.',
'Fixed-L2 potential model rho=2: weighted norm 1, ordinary squared norm 1/2; old derivative 1 versus exact derivative 2.',
'Generalized FH instantiated in two elementary models; no general operator differentiability proof.',
'Finite counterexamples: determinant/definiteness, missing eigenvalue scaling (8 versus 8/9), n=3 determinant sign, and matrix versus elementwise products. No historical NumPy scripts run.',
'Bookkeeping only: zero assert AST nodes, intentional RuntimeError caught, four manifest snapshots hash-checked.'
]
if len(notes)!=25:
    raise RuntimeError('Group assessment cardinality')
group_inventory=[]
for i,(g,source,note) in enumerate(zip(verify['groups'],preflight['static_inspection']['checks.py']['groups'],notes),1):
    category='bookkeeping' if g['kind']=='execution_integrity' else ('real numerical' if g['kind'].startswith('high_precision') else 'symbolic/exact')
    group_inventory.append(dict(g,index=i,category=category,source_function=source['function'],source_lines=[source['line'],source['end_line']],independent_assessment=note,normal_status=g['status'],optimized_status=g['status']))
input_bindings=[]
final_failures=[]
for b,a in zip(before['records'],after['records']):
    final=sha(ROOT/b['path'])
    row={'path':b['path'],'size_bytes':b['size_bytes'],'packet_expected_sha256':b['expected_sha256'],'before_sha256':b['sha256'],'after_sha256':a['sha256'],'final_sha256':final,'unchanged':b['sha256']==a['sha256']==final,'matches_packet':b.get('matches_packet')}
    input_bindings.append(row)
    if not row['unchanged'] or row['matches_packet'] is False:
        final_failures.append({'path':b['path'],'cause':'Input identity changed or failed'})
failures=verify['failed_verification_gates']+final_failures
if outer['returncode']!=0 or verification_process['returncode']!=0:
    failures.append({'cause':'A required actual process did not succeed'})
verdict='PASS' if not failures else 'INCOMPLETE'
status='COMPLETE' if verdict=='PASS' else 'CHANGES_REQUIRED'
limits=[
'This verdict covers only this packet\'s explicit symbolic identities, finite exact cases, real high-precision samples, and execution/input integrity.',
'No whole analytic theorem certification: no Volterra, full variational/min-max argument, full H_0^1 bound, arbitrary spectral branch, global extremality, or general operator differentiability certification.',
'mpmath results use floating-point working precision, not rigorous interval arithmetic. Residuals and tolerances are numerical evidence, not certified error enclosures.',
'General symbolic checks establish the displayed algebraic identities or scalar limits only, subject to their parameter domains. They do not validate untested analytic hypotheses or uniform Taylor remainders.',
'Matrix counterexamples and the normalized determinant are finite algebra; they do not certify G2 or refute a specific spectral branch.',
'Frozen source-scan files were hashed as data. No historical scripts, missing appendices, referenced derivations.md, repository originals, old certificates, Lean, or mathlib were run or consulted.',
'No memory, authors\' conversations or prior execution results, other agents\' directories, or main project working tree were read. Source paths appearing inside documents were not followed.',
'Manifest commit/provenance labels and matches_report_base claims were not verified against Git or original locations. SHA bindings establish identity to the supplied packet, not authenticity or current working-tree identity.',
'Runtime versions, interpreter hash, and SymPy/mpmath entrypoint hashes were recorded; the entire installed runtime dependency closure was not hashed.',
'Outer process capture and rechecked child receipts provide execution evidence; no separate kernel-level process or filesystem trace was collected.'
]
table='\n'.join('| '+str(r['index'])+' | `'+r['name']+'` | '+r['category']+' | '+r['normal_status']+' / '+r['optimized_status']+' | '+r['independent_assessment']+' |' for r in group_inventory)
process_table='\n'.join('| '+p['name']+' | '+str(p['returncode'])+' | '+str(p['expected_exitcode'])+' | '+str(p['elapsed_seconds'])+' |' for p in verify['child_processes'])
readme=f'''# Independent finite-check verification: {verdict}

Execution role: **fresh independent finite-check verifier**. Disposition: **{status}**. No required check failed. This is a bounded finite-check verdict, not a whole analytic theorem certification.

Read scope was PACKET.json, its 39 listed frozen files, installed Python/SymPy/mpmath runtime, and this execution's own outputs. All 39 packet-file SHA-256 values matched; PACKET.json itself was separately hashed. All frozen inputs remained byte-identical after execution and at finalization. `inputs/manifest.json` and all four of its snapshot entries are supplied, packet-listed, and match their SHA-256 and byte counts. Original source paths and historical commit labels were not followed.

The unchanged runner uses the labels `author execution evidence, not independent final review` and `independent executable-check author, not final reviewer`. These describe the provenance of the frozen code. **The execution documented here was performed and checked independently in this directory.**

## Actual process evidence

Executed argv exactly:

```json
["/usr/bin/python3", "-B", "run_checks.py"]
```

Working directory: `{ROOT}`. Started `{outer['started_at_utc']}`; ended `{outer['ended_at_utc']}`. Actual outer exit: **{outer['returncode']}**; timeout: false; stderr: empty. Actual captured outer stdout:

```text
{outer['stdout'].rstrip()}
```

| Child process | Actual exit | Expected exit | Elapsed seconds |
| --- | ---: | ---: | ---: |
{process_table}

Every child argv, raw stdout/stderr, source/output hash, timestamp and exit code is preserved in EXECUTION.json and the receipts. All 15 expected runner output files were observed as newly written during this run; none of those files existed before it. The receipts directory already existed and needed no repair.

Both old-FH controls failed at the intended formula comparison, ending with:

```text
RuntimeError: intentional old FH formula rejection: error=26.9404860801202857619399303749492449801291945661366696096904176100696272189699061222717259
```

Both have empty stdout and identical stderr. The expected formula rejection is distinguished from an unrelated crash. No required check failure was suppressed or relabeled. The optional `old-schrodinger` CLI control was not run; its exact counterexample is exercised in group 22.

Runtime: Python `{runtime['python']}`; SymPy `{runtime['sympy']}`; mpmath `{runtime['mpmath']}`. Frozen checks use 90 decimal digits; supplemental calculations use 100. Both frozen Python files were inspected and contain zero `assert` AST nodes. The checker imports standard-library modules, mpmath and SymPy and reads itself, the manifest and its four snapshots. It does not import or execute frozen historical scripts.

Two verifier-owned report-preparation commands initially failed: a nested-quote SyntaxError and the resulting missing report-generator file. Their actual exit codes and errors are retained in `{PREFIX}/report_preparation_errors.json` and EXECUTION.json. Only this verifier's report generator was corrected; no frozen program or input was modified, and the required runner was executed once. These report-preparation failures are separate from the successful required checks.

## Completeness and normal/-O equality

The source registers **25 distinct named groups**. Each output contains precisely those names in source order, nonempty details, and all PASS statuses. Each actual stdout contains the corresponding 25 PASS lines and a mode-specific summary. Counts and names were independently recomputed, not inferred from returncode.

There are **16 symbolic/exact mathematical groups, 8 high-precision real numerical groups, and 1 bookkeeping group**. These are groups, not independent theorems; several share eigenpairs or helpers. The separate verification script passed {verify['passed_verification_gates']} integrity and finite-computation gates, also not theorem counts.

For all groups, `name`, `kind`, `status`, and complete `details` are exactly equal between normal and -O. Their canonical detail digest is:

```text
{verify['normal_optimized_equality']['normal_sha256']}
```

Canonicalization: UTF-8 JSON, sorted keys, compact separators, ensure_ascii=False, no final newline. Raw output hashes differ because mode flags and elapsed times differ. Normal has optimize=0 and __debug__=true; optimized has optimize=1 and __debug__=false.

| # | Named group | Evidence type | Normal / -O | Inspected evidence and scope |
| ---: | --- | --- | --- | --- |
{table}

## Substantive mirror-derivative comparison

For `-u''=lambda*rho*u` on [0,1] with Dirichlet endpoints, use rho=(1,4,1), interfaces a=1/4 and 1-a=3/4, and integral(rho*u^2)=1. The eigenvalues are approximately 2.829586034443622 and 14.602077453837592. Here f(a)=-8.980162026706762, so the sample is substantially nonstationary.

Moving a to a+h moves the mirror to 1-a-h. The corrected gap derivative is 2*(1-4)*f(a):

```text
FH               = 53.880972160240571523695242987489219318052973256092167942806432826
FD at h=1e-11    = 53.880972160240571523787551868693854639155681194182753581093634023
absolute error  = 9.23088812046353211027079380905856e-20
old half formula= 26.940486080120285761847621493744609659026486628046083971403216413
```

Errors for h=1e-5,1e-8,1e-11 are approximately 9.23088812327e-8, 9.23088812046e-14, 9.23088812046e-20. Roots are recomputed at both perturbed geometries. Moving only the left interface gives 26.940486080120... and correctly uses no extra mirror factor.

The separate verifier calculation did not import `checks.py`. It used characteristic equations on [0,1/2], with a Neumann center condition for the first mode and Dirichlet condition for the second. At a=1/4, sqrt(lambda) is 4*acos(sqrt(5/6)) and 4*acos(1/sqrt(3)), respectively. It normalized by weighted quadrature, differentiated characteristic equations implicitly, and resolved roots at h=1e-12. Implicit and FH derivatives agree within 1e-90; the independent finite-difference error is approximately **9.23088812046e-22**. The old half formula still misses by approximately **26.94048608012**. These are numerical tolerances, not certified enclosures.

## Exact samples independently recomputed

For sqrt(2)*sin(2*pi*x) and sqrt(2)*sin(3*pi*x), direct differentiation gives W(1/2)=-4*pi; the old value is -6*pi. A separate series expansion gives coefficient -130*pi^4 for n=2, matching 2*pi^4*(n^4-(n+1)^4).

For F=f/(9*pi^2), the four-interface determinant is exactly **7030400000*pi^4/4782969**, approximately 143179.8687395738. A separate resultant computation with P(t)=144*t^2-88*t+9 and t*(1-t)^3*P'(t)^2 takes the product over both algebraic roots; it does not merely copy radical substitutions. This verifies only the stated normalization and determinant sample.

## SHA-256 bindings and evidence

EXECUTION.json contains all packet/input hashes before, after and at finalization; all produced payload, receipt, log and verifier-script hashes; actual outer and child process results; every group with details and scope; supplemental computations; and explicit limits. README.md is also bound there. **SHA256SUMS** additionally binds EXECUTION.json. SHA256SUMS excludes its own bytes, avoiding a recursive self-hash. Runtime identities do not hash the full dependency closure.

Evidence directory: `{PREFIX}`. Raw runner outputs are `outputs.json`, `outputs.optimized.json` and the 13 receipt files listed in EXECUTION.json. The independent implementation is `{PREFIX}/verify_evidence.py`; its actual process receipt, stdout, stderr and detailed results are retained.

## Limits

'''+'\n\n'.join('- '+limit for limit in limits)+'\n'
if failures:
    readme=readme.replace('No required check failed.','Required checks failed; see failures in EXECUTION.json. No PASS is claimed.')
(ROOT/'README.md').write_text(readme)
own_names=['input_hashes.before.json','preflight.json','launch.py','outer.stdout.log','outer.stderr.log','outer.started.json','outer.execution.json','verify_evidence.py','input_hashes.after.json','runtime.json','verification.json','verification.stdout.log','verification.stderr.log','verification.execution.json','finalize.py','report_preparation_errors.json']
output_paths=[r['path'] for r in outer['generated_outputs']]+[PREFIX+'/'+n for n in own_names]+['README.md']
output_bindings=[{'path':rel,'size_bytes':(ROOT/rel).stat().st_size,'sha256':sha(ROOT/rel)} for rel in sorted(output_paths)]
report={
    'schema_version':1,
    'verdict':verdict,
    'disposition':status,
    'execution_role':'fresh stateless independent finite-check verifier',
    'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Frozen packet finite/symbolic/real-numeric verification and execution integrity only',
    'scope_complete':verdict=='PASS',
    'failures':failures,
    'requested_outer_command':'/usr/bin/python3 -B run_checks.py',
    'outer_process':outer,
    'child_processes':verify['child_processes'],
    'supplemental_verification_process':verification_process,
    'report_preparation_errors_and_recovery':preparation_errors,
    'frozen_input_summary':{'packet_file_count':39,'packet_itself_also_hashed':True,'all_packet_hashes_matched':all(r['matches_packet'] is not False for r in input_bindings),'all_unchanged':all(r['unchanged'] for r in input_bindings),'manifest_and_all_four_snapshots_supplied':preflight['all_snapshots_supplied_and_bound'],'snapshot_byte_counts_checked':True,'snapshot_records':preflight['snapshots'],'external_original_paths_followed':False},
    'input_sha256_bindings':input_bindings,
    'output_sha256_bindings':output_bindings,
    'report_hash_binding':{'manifest':'SHA256SUMS','description':'SHA256SUMS covers all packet/input files and all produced outputs including EXECUTION.json; it excludes its own bytes. EXECUTION.json binds all other outputs except the checksum manifest, avoiding circular hashes.'},
    'source_inspection':{'checks_assert_nodes':0,'runner_assert_nodes':0,'checks_group_count':25,'unique_group_names':25,'failure_mechanism':'explicit conditional RuntimeError, active under -O','runner_behavior':'Four sequential subprocesses; unexpected exit stops runner. Here all four ran. Complete count/detail equality independently rechecked.','static_inspection':preflight['static_inspection'],'frozen_files_modified':False,'historical_scripts_executed':False},
    'runtime':runtime,
    'normal_optimized_comparison':verify['normal_optimized_equality'],
    'kind_counts':verify['kind_counts'],
    'category_counts':verify['category_counts'],
    'group_count_independently_recomputed':len(group_inventory),
    'group_inventory':group_inventory,
    'independent_verification_gates':{'passed':verify['passed_verification_gates'],'failed':verify['failed_verification_gates'],'evidence_file':PREFIX+'/verification.json'},
    'independent_exact_samples':verify['independent_exact_samples'],
    'independent_nonstationary_mirror_sample':verify['independent_nonstationary_mirror_sample'],
    'provenance_label_interpretation':verify['provenance_labels'],
    'frozen_source_notes':{'inputs/gap-band-extremals.md':'Lines 24-27 evidence the mirror convention and old gap formula missing its factor; historical numerical claims were not adopted as independent evidence.','inputs/feynman-hellmann.md':'Lines 12-18 evidence the weighted-normalization wording; group 22 checks a fixed-L2 counterexample.'},
    'limits':limits
}
write(ROOT/'EXECUTION.json',report)
all_paths=[r['path'] for r in input_bindings]+output_paths+['EXECUTION.json']
if len(set(all_paths))!=len(all_paths):
    raise RuntimeError('Duplicate binding path')
checksum_rows=[(sha(ROOT/rel),rel) for rel in sorted(all_paths)]
(ROOT/'SHA256SUMS').write_text(''.join(digest+'  '+rel+'\n' for digest,rel in checksum_rows))
loaded=load('EXECUTION.json')
for row in loaded['output_sha256_bindings']:
    if sha(ROOT/row['path'])!=row['sha256']:
        raise RuntimeError('Output binding failed: '+row['path'])
for digest,rel in checksum_rows:
    if sha(ROOT/rel)!=digest:
        raise RuntimeError('Final checksum failed: '+rel)
if loaded['group_count_independently_recomputed']!=25 or len(loaded['group_inventory'])!=25:
    raise RuntimeError('Saved group inventory mismatch')
print(json.dumps({'verdict':verdict,'disposition':status,'input_files_bound':len(input_bindings),'produced_files_bound_in_execution':len(output_bindings),'checksum_manifest_entries':len(checksum_rows),'checksum_entries_verified':True,'EXECUTION.json_sha256':sha(ROOT/'EXECUTION.json'),'README.md_sha256':sha(ROOT/'README.md'),'SHA256SUMS_sha256':sha(ROOT/'SHA256SUMS'),'files':['EXECUTION.json','README.md','SHA256SUMS']},indent=2))
