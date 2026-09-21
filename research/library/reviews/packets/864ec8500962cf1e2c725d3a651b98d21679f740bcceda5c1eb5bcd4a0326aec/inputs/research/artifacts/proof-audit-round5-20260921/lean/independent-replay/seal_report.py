from pathlib import Path
import datetime, hashlib, json, os, sys, traceback
from audit_runner import OUT, PACKET, SOURCE_HASH, ROOT_NAME, sha, now, write_json, packet

def load(rel): return json.loads((OUT/rel).read_bytes())

def seal():
    assert load('checks/RESULT.json')['status']=='PASS'
    pkt=packet()
    rows=[]
    for name,item in pkt['inputs'].items():
        p=PACKET.parent/item['snapshot']
        actual=sha(p)
        rows.append({'input':name,'snapshot':item['snapshot'],'expected_sha256':item['sha256'],
                     'actual_sha256':actual,'match':actual==item['sha256']})
    assert all(r['match'] for r in rows)
    write_json(OUT/'packet-verification-after.json',{'packet_sha256':sha(PACKET),'all_match':True,
               'snapshot_count':len(rows),'checked_at':now(),'snapshots':rows})
    result=load('checks/RESULT.json')
    imports=load('checks/import-identity.json')
    declarations=load('checks/declaration-comparison.json')
    root=load('checks/root-identity.json')
    commands=load('checks/command-summary.json')
    environment=load('frozen/environment.json')
    rootobj=imports['root_object']
    authorroot=next(m for m in load('frozen/final/module-artifact-hashes.json')['modules']
                    if m['module']=='SL.AuditRound5')
    authorrootobj=next(a for a in authorroot['artifacts'] if a['path']==authorroot['resolved_olean'])
    assert sha(rootobj['path'])==rootobj['sha256']
    assert sha(OUT/'SL/AuditRound5.lean')==SOURCE_HASH
    identity={'native_agent_id':os.environ['CODEX_THREAD_ID'],'identity_source':'CODEX_THREAD_ID',
              'role':'independent execution verifier; not an author',
              'distinct_from_frozen_authors':os.environ['CODEX_THREAD_ID'] not in pkt['author_ids'],
              'spawned_agents':False,'read_memory_or_author_conversations':False}
    limitations=[
      'The maintained verifier implementation is absent from the frozen packet and was not replayed or read outside the allowed inputs.',
      'This verdict covers independent execution, exact local target identity, imported artifact identity and axiom closure. It does not replace the separate semantic comparison or analytic mathematics review.',
      'Formal carrier is Polynomial Real. No complex or Sobolev theory, topological closure/density, cutoff approximation, Green integration, leading-term tail equality or full cofinite classification was formalized here.',
      'Installed pinned imports were byte-verified before and after execution, not rebuilt. No package installation, download or full Lake build was run.',
      'This is an installed Windows PE Lean runtime invoked through WSL, not a native Linux runtime or offline self-contained toolchain distribution.',
      'The first two bootstrap tool outputs were displayed with transport truncation. Their command text and deterministic reconstructed stdout are saved with explicit provenance; every Lean command has raw, separate stdout/stderr and exit-code receipts.'
    ]
    report={
      'schema':'independent-lean-execution-review/v1','verdict':'PASS',
      'completed_at':now(),'agent':identity,
      'packet':{'path':str(PACKET),'sha256':sha(PACKET),'snapshot_count':len(rows),
                'all_snapshot_hashes_verified_before_and_after':True},
      'target':{'declaration':ROOT_NAME,'source_sha256':SOURCE_HASH,'source_copy':str(OUT/'SL/AuditRound5.lean'),
                'fresh_root_object':rootobj,'expected_type_source':str(OUT/'ContractCheck.lean'),
                'expected_contract_json':str(OUT/'frozen/positive-contract.json'),
                'typed_contract_byte_identity_verified':True,'typed_contract_compiler_exit_code':0,
                'conjunct_count':8,'no_outer_assumptions':True,
                'type_expression_sha256':root['type_expression_sha256'],
                'fully_explicit_type_sha256_utf8':root['fully_explicit_type_sha256_utf8'],
                'conjuncts':[{'index':x['index'],'description':x['description']} for x in root['conjuncts']]},
      'execution':{'performed_by_this_agent':True,'checks_passed':result['checks'],
                   'compiler':environment['compiler'],
                   'compiler_sha256':next(r['sha256'] for r in environment['runtime_files']
                                          if r['path']==environment['compiler']),
                   'actual_version':(OUT/'logs/01-version.stdout.txt').read_text().strip(),
                   'format':'Windows PE; MZ signature checked after declared SHA-256 identity',
                   'fresh_root_compilation_exit_code':0,'exporter_exit_code':0,
                   'commands':commands,'compiler_commands_count':len(commands),
                   'raw_stdout_stderr_and_exit_codes_preserved':True,
                   'original_source_pins_controls_unchanged':True,
                   'warning':'One linter.unnecessarySeqFocus warning at source line 119; retained, not repaired.'},
      'runtime_and_import_identity':{
                   'runtime_files_rehashed':11,'manifest_modules':3712,'manifest_artifacts_rehashed':14845,
                   'manifest_module_artifact_bytes':3028880240,
                   'before_and_after_all_declared_hashes_match':True,
                   'all_nonlocal_imports_resolve_to_manifest_paths':True,
                   'local_root_resolution':rootobj,
                   'root_path_and_hash_confirmed_before_after_all_probes':True,
                   'only_resolved_module_path_change':'SL.AuditRound5',
                   'frozen_author_root_hashed_but_not_imported':authorrootobj,
                   'fresh_object_equals_frozen_object_bytes':rootobj['sha256']==authorrootobj['sha256'],
                   'binary_identity_note':'The fresh object has its own recorded hash. Physical source/root path changed; exact elaborated exports match byte for byte. Binary equality with the author object is not asserted.',
                   'LEAN_PATH':load('logs/04-export.json')['LEAN_PATH'],
                   'WSLENV':load('logs/04-export.json')['WSLENV'],
                   'existing_project_SL_olean_lookup_excluded':True,
                   'receipt_files':['artifact-rehash-before.json','artifact-rehash-after.json','checks/import-identity.json']},
      'declaration_identity':{'count':59,'theorems':37,'definitions':22,
                   'all_export_bytes_equal_to_both_frozen_author_and_coordinator_exports':True,
                   'exports':declarations['exports_byte_equality'],
                   'fully_explicit_types_and_definition_bodies_equal':True,
                   'union_dependency_nodes':12604,'root_dependency_nodes':12601,
                   'union_semantic_nodes':2347,
                   'independent_graph_recomputation_matches_lean_axiom_and_dependency_exports_for_all59':True,
                   'axiom_union':['Classical.choice','Quot.sound','propext'],
                   'root_axioms':root['transitive_axioms'],'sorryAx':False,
                   'unknown_dependencies':[],'unsafe_dependencies':[],
                   'comparison_policy':'Strict byte equality of union-of-all-59 exports; no root-only versus union field relaxation used in this replay.',
                   'scope_of_unsafe_check':'All 12604 nodes in the mathematical declaration dependency union; the Lean runtime and exporter are execution infrastructure.'},
      'controls':{'positive':{'exit_code':0,'object_emitted':True,
                   'explicit_1_plus_X_witness':True,'explicit_all_index_false_equality_negation':True,
                   'other_checks':'m=2 even/odd polynomials, concrete correction coefficients, matrix inverse, general trace formulas'},
                  'negative':{'exit_code':1,'expected':True,'failure_reason':'Strict inclusion versus equality type mismatch',
                   'actual_type':'high_span 2 < oblique ⊓ krein_polynomials',
                   'requested_false_type':'high_span 2 = oblique ⊓ krein_polynomials',
                   'not_a_failed_proof_of_False':True},
                  'typed_eight_conjunct_root_contract':{'exit_code':0,'object_emitted':True}},
      'export_helper':load('input-bindings.json')['exporter_change'],
      'semantic':{'status':'not_reviewed_by_this_execution_verifier',
                   'relationship':'Complements the separately approved semantic comparison described by the user; no new analytic certification.'},
      'optional_maintained_verifier':{'status':'not_replayed','blocking':False,
                   'reason':'Implementation not included in the frozen packet; no permission to read the installed verifier implementation.',
                   'historical_author_and_coordinator_verdicts_not_substituted_for_current_execution':True},
      'read_write_scope':{'sole_write_area':str(OUT),'project_source_or_dependency_modified':False,
                   'source_read_from_frozen_snapshot_only':True,
                   'live_module_runtime_reads_limited_to_declared_manifest_paths':True,
                   'no_library_dependency_integration_attempted':True,
                   'frozen_snapshots_and_declared_runtime_import_bytes_unchanged_after_execution':True,
                   'changed_path_inventory':'changed-paths.json',
                   'scope_verification_note':'Audit-owned write destinations and unchanged allowed input bytes were checked; unrelated working-tree files and history were not read or scanned.'},
      'limitations':limitations,
      'artifacts':{'report_markdown':'REPORT.md','hash_inventory':'hash-inventory.json',
                   'sha256_sums':'SHA256SUMS','changed_paths':'changed-paths.json',
                   'raw_compiler_receipts':'logs/','shell_and_bootstrap_receipts':'receipts/',
                   'declaration_comparison':'checks/declaration-comparison.json',
                   'root_contract':'checks/root-identity.json','import_identity':'checks/import-identity.json'}
    }
    write_json(OUT/'REPORT.json',report)
    md=f"""# Independent Lean execution review — PASS

Agent: {identity['native_agent_id']} (native CODEX_THREAD_ID; independent of the frozen authors).

Target: {ROOT_NAME}. The exact frozen source was compiled by this agent into a fresh object with Windows PE Lean 4.31.0 through WSL. All 196 checks passed.

- Packet and all 104 snapshots matched their hashes before and after the audit.
- All 11 runtime files and 14,845 declared artifacts (3,712 modules; 3,028,880,240 module-artifact bytes) matched current-byte hashes before and after execution.
- All 59 declarations (37 theorems, 22 definitions), exported types, definition bodies and dependency identities matched both frozen exports byte for byte.
- Independent graph traversal reproduced every declaration's Lean axiom closure. The 12,604-node union and 12,601-node root closure contain only propext, Classical.choice and Quot.sound as axioms; no sorryAx, unknown or unsafe dependency.
- The explicitly typed eight-conjunct root contract compiled with exit 0. It is local real-polynomial algebra, with explicit parameter and kernel-inclusion hypotheses inside the relevant conjuncts.
- Positive controls compiled with exit 0, including the 1+X witness and explicit negation of high-span equality.
- The false-equality control exited 1 with the expected strict-inclusion/equality type mismatch. This was not a failed proof of False.
- Import resolution before and after the probes selected only the new SL.AuditRound5 object. Every probe retained its path/hash. All other module paths matched the pinned manifest.
- Source, pins and controls were copied unchanged. Only the exporter's literal output directory was adapted; both hashes and the one-line diff are retained.
- One source-line-119 style warning was retained. No mathematical source was authored or repaired.

Source SHA-256: {SOURCE_HASH}

Fresh root SHA-256: {rootobj['sha256']}

The fresh root has a different physical-source/output provenance and its own binary hash; binary equality with the author's object is not claimed. Export equality is exact.

The root's eight components are low traces, low residues, the all-index high-family trace/residue conclusions, high-span inclusion/strictness, the oblique 1+X witness, positive-L determinant/inverse, positive-even-L endpoint correction/divisibility, and trace-lift membership under the explicit kernel-inclusion hypothesis.

All eight compiler invocations have exact argument vectors, effective LEAN_PATH/WSLENV, separate raw stdout/stderr, exit codes and source/object hashes in logs/. REPORT.json, checks/, the exporter diff, hash inventory and changed-path list give the structured evidence.

The optional maintained-verifier replay was not performed because its implementation is absent from the frozen packet. This execution review complements the separate semantic comparison; it does not certify complex/Sobolev analysis, topological closure, cutoff approximation, Green integration, leading-term tail equality or full cofinite classification. No installation, download or full Lake build was performed, and no offline self-contained toolchain distribution is claimed.

Receipt qualification: the initial two bootstrap display outputs were truncated by the tool transport; their deterministic reconstructed streams are explicitly labelled in receipts/. All actual Lean compiler streams were captured raw without this limitation.

All audit writes are under this new directory. The project, library, toolchain and packages were not modified.
"""
    (OUT/'REPORT.md').write_text(md)
    summary={'verdict':'PASS','checks':196,'report':str(OUT/'REPORT.json'),
             'root_object_sha256':rootobj['sha256']}
    stdout=(json.dumps(summary,ensure_ascii=False,indent=2)+'\n').encode()
    (OUT/'receipts/seal.stdout.txt').write_bytes(stdout)
    (OUT/'receipts/seal.stderr.txt').write_bytes(b'')
    write_json(OUT/'receipts/seal.json',{
       'argv':[sys.executable,str(OUT/'seal_report.py')],
       'shell_command':'PYTHONDONTWRITEBYTECODE=1 python3 seal_report.py',
       'cwd':str(OUT),'native_agent_id':identity['native_agent_id'],
       'script_sha256':sha(__file__),'exit_code':0,
       'stdout_sha256':sha(OUT/'receipts/seal.stdout.txt'),
       'stderr_sha256':sha(OUT/'receipts/seal.stderr.txt'),
       'note':'Self-recorded deterministic finalizer output, also emitted to the command stdout.',
       'recorded_at':now()})
    planned={'changed-paths.json','hash-inventory.json','SHA256SUMS'}
    names={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}|planned
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
    write_json(OUT/'changed-paths.json',{
       'write_area_initial_state':'Directory did not exist; creation guarded by assertion.',
       'write_area':str(OUT),'outside_write_area_paths':[],
       'files':[{'relative_path':n,'absolute_path':str(OUT/n),'change':'created'} for n in sorted(names)],
       'scope_note':'Audit write inventory only; unrelated working tree not scanned.'})
    entries=[{'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)}
             for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in {'hash-inventory.json','SHA256SUMS'}]
    write_json(OUT/'hash-inventory.json',{
       'algorithm':'SHA-256','root':str(OUT),'files':entries,
       'exclusions':['hash-inventory.json','SHA256SUMS'],
       'self_reference_policy':'Inventory omits itself and SHA256SUMS; SHA256SUMS includes the inventory digest and omits only itself.'})
    sums=[e['sha256']+'  '+e['path'] for e in entries]
    sums.append(sha(OUT/'hash-inventory.json')+'  hash-inventory.json')
    (OUT/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    for e in entries:
        assert sha(OUT/e['path'])==e['sha256']
    current={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}
    assert current==names
    assert len(current)==len(entries)+2
    sys.stdout.buffer.write(stdout)

if __name__=='__main__':
    try:seal()
    except BaseException:
        traceback.print_exc()
        sys.exit(1)

