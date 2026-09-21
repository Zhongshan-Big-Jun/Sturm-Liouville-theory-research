from pathlib import Path
import collections, hashlib, json, ntpath, os, re, sys, traceback
from audit_runner import OUT, PACKET, BASE, SOURCE_HASH, ROOT_NAME, sha, win, write_json, packet, now

results = []
def check(name, ok, detail=None):
    item = {'check': name, 'passed': bool(ok)}
    if detail is not None: item['detail'] = detail
    results.append(item)
    write_json(OUT / 'checks/check-progress.json', results)
    if not ok:
        raise AssertionError(name)
def load(name):
    return json.loads((OUT/name).read_bytes())
def norm(s):
    return ntpath.normcase(ntpath.normpath(s))
def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()
def decompose_application(e):
    args = []
    while e[0] == 'app':
        args.append(e[2])
        e = e[1]
    return e, list(reversed(args))
def split_outer_and(e):
    head, args = decompose_application(e)
    if head == ['const', ['And', []]] and len(args) == 2:
        return [args[0]] + split_outer_and(args[1])
    return [e]
def constants(e):
    names=set()
    todo=[e]
    while todo:
        x=todo.pop()
        if isinstance(x,list):
            if len(x)==2 and x[0]=='const':
                names.add(x[1][0])
            else:
                todo.extend(x)
    return names

def compare():
    pkt=packet()
    check('native_independent_identity',
          os.environ.get('CODEX_THREAD_ID') not in pkt['author_ids'],
          {'native_agent_id':os.environ.get('CODEX_THREAD_ID'),'frozen_author_ids':pkt['author_ids']})
    for stage in ['before','after']:
        r=load('artifact-rehash-'+stage+'.json')
        check('runtime_and_modules_'+stage, r['all_match'] and len(r['runtime'])==11
              and r['artifact_count']==14845 and r['module_count']==3712,
              {'artifacts':r['artifact_count'],'runtime_files':len(r['runtime']),'modules':r['module_count'],'bytes':r['bytes']})
    before=load('artifact-rehash-before.json'); after=load('artifact-rehash-after.json')
    bypath=lambda r:{x['path']:x['actual_sha256'] for x in r['artifacts']+r['runtime']}
    check('current_runtime_and_module_bytes_unchanged',bypath(before)==bypath(after))
    check('compiler_pe',Path(load('frozen/environment.json')['compiler']).read_bytes()[:2]==b'MZ')
    copies=load('input-bindings.json')
    for r in copies['copies']:
        check('unchanged_copy:'+r['input'],sha(r['copy'])==r['sha256'])
    exporter=(OUT/'InspectAuditRound5.lean').read_bytes()
    frozen_exporter=(OUT/'frozen/InspectAuditRound5.lean').read_bytes()
    change=copies['exporter_change']
    check('exporter_only_literal_output_folder_changed',
          exporter.replace(change['new_literal'].encode(),change['old_literal'].encode())==frozen_exporter
          and sha(OUT/'InspectAuditRound5.lean')==change['new_sha256'],
          change)
    check('exact_source_identity',sha(OUT/'SL/AuditRound5.lean')==SOURCE_HASH, SOURCE_HASH)
    source=(OUT/'SL/AuditRound5.lean').read_text()
    declared=[('SL.AuditRound5.'+n, k) for k,n in re.findall(r'^(def|theorem)\s+(\w+)',source,re.M)]
    check('source_public_declarations_count',len(declared)==59)
    check('source_no_holes_or_axiom_commands',
          re.search(r'\b(sorry|admit|sorryAx)\b|^\s*(axiom|unsafe)\s',source,re.M) is None)
    data=load('final/declarations.json')
    declarations=data['declarations']
    check('all59_exported_once',len(declarations)==59 and len({x['declaration'] for x in declarations})==59)
    check('all_source_public_names_exported',set(n for n,k in declared)==set(d['declaration'] for d in declarations))
    check('37_theorems_22_definitions',collections.Counter(x['kind'] for x in declarations)=={'theorem':37,'definition':22})
    equality=[]
    for old in ['frozen/final/declarations.json','frozen/coordinator-replay/final/declarations.json']:
        equal=(OUT/'final/declarations.json').read_bytes()==(OUT/old).read_bytes()
        equality.append({'baseline':old,'actual_sha256':sha(OUT/'final/declarations.json'),
                         'baseline_sha256':sha(OUT/old),'byte_equal':equal})
        check('all_export_fields_byte_equal:'+old,equal)
    for name in ['formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt']:
        check('readable_export_byte_equal:'+name,
              (OUT/'final'/name).read_bytes()==(OUT/'frozen/final'/name).read_bytes())
    nodes={x['name']:x for x in data['dependencies']}
    check('dependency_nodes_unique',len(nodes)==len(data['dependencies'])==12604)
    unknown=[n for n,x in nodes.items() if x.get('missing') or x.get('kind') not in
             {'axiom','theorem','definition','opaque','inductive','constructor','recursor','quotient_primitive'}]
    unsafe=[n for n,x in nodes.items() if x.get('unsafe') is not False]
    check('no_unknown_dependency_nodes',not unknown,unknown)
    check('no_unsafe_dependency_nodes',not unsafe,unsafe)
    check('no_sorryAx_dependency','sorryAx' not in nodes)
    def closure(seeds,semantic=False):
        seen=set()
        pending=list(seeds)
        while pending:
            n=pending.pop()
            if n in seen:continue
            seen.add(n)
            if n not in nodes: raise AssertionError('Missing dependency '+n)
            node=nodes[n]
            pending.extend(node['type_dependencies'])
            if not semantic or node['kind']!='theorem':
                pending.extend(node['body_dependencies'])
        return seen
    per_declaration=[]
    combined=set()
    semantic_union=set()
    allowed={'propext','Classical.choice','Quot.sound'}
    root=None
    for d in declarations:
        n=d['declaration']
        reached=closure([n])
        combined |= reached
        axioms={m for m in reached if nodes[m]['kind']=='axiom'}
        semantic=closure(d['type_dependencies'],semantic=True)
        semantic_union |= closure(d['type_dependencies'] if d['kind']=='theorem' else [n],semantic=True)
        row={'declaration':n,'kind':d['kind'],'type_expression_sha256':canonical_hash(d['type_expression']),
             'fully_explicit_type_sha256_utf8':hashlib.sha256(d['fully_explicit_type'].encode()).hexdigest(),
             'value_expression_sha256':canonical_hash(d['value_expression']) if 'value_expression' in d else None,
             'transitive_dependency_count':len(reached),'transitive_axioms':sorted(axioms),
             'dependency_closure_matches':reached==set(d['transitive_dependencies']),
             'axioms_match_lean_collectAxioms':axioms==set(d['transitive_axioms']),
             'only_standard_axioms':axioms<=allowed,
             'semantic_dependency_closure_matches':semantic==set(d['semantic_dependencies'])}
        per_declaration.append(row)
        check('closure:'+n,all(row[k] for k in ['dependency_closure_matches',
              'axioms_match_lean_collectAxioms','only_standard_axioms','semantic_dependency_closure_matches']))
        if n==ROOT_NAME:root=d
    check('union_graph_exactly_closed',combined==set(nodes))
    check('semantic_union_matches',semantic_union==set(data['semantic_dependencies']))
    check('axiom_union',set(n for n,d in nodes.items() if d['kind']=='axiom')==allowed)
    for old in load('frozen/final/public-theorem-axioms.json')['theorems']:
        current=next(d for d in declarations if d['declaration']==old['declaration'])
        check('frozen_public_axioms:'+old['declaration'],
              all(current[k]==v for k,v in old.items()))
    check('root_present_theorem',root is not None and root['kind']=='theorem')
    check('root_closed_no_binders',root['binder_kinds']==[] and root['universes']==[])
    conjuncts=split_outer_and(root['type_expression'])
    labels=['low value/derivative traces','low endpoint residues',
            'all m >= 2 high polynomial traces and residues','all-index high-span inclusion and strictness',
            '1+X witness with 1 and X exclusions','positive-L determinant and two-sided inverse',
            'positive-even-L correction and preserved divisibility','trace-lift membership with explicit kernel inclusion']
    check('root_exact_eight_conjuncts',len(conjuncts)==8)
    contract=load('frozen/positive-contract.json')
    expected_source='import SL.AuditRound5\nexample : '+contract['expected_type']+' := '+ROOT_NAME+'\n'
    check('typed_contract_exact_frozen_expected_type',
          (OUT/'ContractCheck.lean').read_text()==expected_source)
    root_details={'name':ROOT_NAME,'actual_type':root['actual_type'],
                  'type_expression_sha256':canonical_hash(root['type_expression']),
                  'fully_explicit_type_sha256_utf8':hashlib.sha256(root['fully_explicit_type'].encode()).hexdigest(),
                  'binder_kinds':root['binder_kinds'],'universes':root['universes'],
                  'conjunct_count':len(conjuncts),
                  'conjuncts':[{'index':i+1,'description':labels[i],'expression_sha256':canonical_hash(c),
                                'constants':sorted(constants(c))} for i,c in enumerate(conjuncts)],
                  'root_dependency_count':len(root['transitive_dependencies']),
                  'transitive_axioms':root['transitive_axioms'],
                  'semantic_scope':'local algebra over Polynomial Real; semantic comparison is a separate review'}
    expected_logs={'01-version':0,'02-root-compile':0,'03-import-resolution-before':0,'04-export':0,
                   '05-positive-controls':0,'06-false-high-span-equality':1,
                   '07-exact-root-contract':0,'08-import-resolution-after':0}
    receipts={}
    ownroot=OUT/'build/SL/AuditRound5.olean'
    root_hash=sha(ownroot)
    for log,code in expected_logs.items():
        r=load('logs/'+log+'.json')
        receipts[log]=r
        check('executed:'+log,r['exit_code']==code and r['all_inputs_unchanged'])
        for k in ['stdout','stderr']:
            check('exact_stream_hash:'+log+':'+k,sha(OUT/'logs'/(log+'.'+k+'.txt'))==r[k+'_sha256'])
        if log!='01-version':
            check('fresh_root_hash_binding:'+log,r['root_object']['path']==str(ownroot)
                  and r['root_object']['sha256']==root_hash)
        if log not in ['01-version','02-root-compile']:
            check('fresh_root_before_after:'+log,
                  r['source_sha256_before'][str(ownroot)]==r['source_sha256_after'][str(ownroot)]==root_hash)
    check('root_was_fresh',not receipts['02-root-compile']['root_preexists'])
    for n in ['02-root-compile','05-positive-controls','07-exact-root-contract']:
        obj=receipts[n]['output_artifact']
        check('object_emitted:'+n,sha(obj['path'])==obj['sha256'] and obj['bytes']>0)
    for n in ['03-import-resolution-before','08-import-resolution-after']:
        lines=(OUT/'logs'/(n+'.stdout.txt')).read_text().splitlines()
        roots=[x for x in lines if norm(x).endswith('\\sl\\auditround5.olean')]
        check('actual_root_resolution:'+n,len(roots)==1 and norm(roots[0])==norm(win(ownroot)),roots)
    check('import_resolution_before_after_equal',
          (OUT/'logs/03-import-resolution-before.stdout.txt').read_bytes()==
          (OUT/'logs/08-import-resolution-after.stdout.txt').read_bytes())
    modules=load('final/loaded-modules.json')['modules']
    manifest=load('frozen/final/module-artifact-hashes.json')
    declared_modules={m['module']:m for m in manifest['modules']}
    check('exact_imported_module_set',len(modules)==3712 and
          {m['module'] for m in modules}==set(declared_modules))
    root_module='SL.AuditRound5'
    resolved=[]
    for m in modules:
        original=declared_modules[m['module']]
        want=ownroot if m['module']==root_module else Path(original['resolved_olean'])
        if norm(m['olean']) != norm(win(want)):
            raise AssertionError('Unexpected module resolution: '+str(m))
        resolved.append({'module':m['module'],'actual_resolved_olean':m['olean'],
                         'original_resolved_olean':original['resolved_olean'],
                         'independent_root_override':m['module']==root_module})
    check('every_import_resolves_to_verified_object',True)
    path_changes=[]
    for baseline in ['frozen/final/loaded-modules.json','frozen/coordinator-replay/final/loaded-modules.json']:
        old={m['module']:m['olean'] for m in load(baseline)['modules']}
        delta=[{'module':m['module'],'frozen':old[m['module']],'actual':m['olean']}
               for m in modules if norm(old[m['module']])!=norm(m['olean'])]
        check('only_local_root_path_changed:'+baseline,
              len(delta)==1 and delta[0]['module']==root_module,delta)
        path_changes.append({'baseline':baseline,'changes':delta})
    actual_paths=receipts['04-export']['LEAN_PATH'].split(';')
    check('own_output_first_and_packages_only',norm(actual_paths[0])==norm(win(OUT/'build')) and
          all('\\.lake\\packages\\' in p for p in actual_paths[1:]) and len(actual_paths)==10)
    negative=(OUT/'logs/06-false-high-span-equality.stdout.txt').read_text()
    check('negative_is_strictness_equality_type_mismatch',
          all(s in negative for s in ['error: Type mismatch','high_span_lt_krein_oblique 2',
                'high_span 2 < oblique ⊓ krein_polynomials','high_span 2 = oblique ⊓ krein_polynomials'])
          and negative.count('error:')==1 and 'sorry' not in negative)
    positive=(OUT/'PositiveControls.lean').read_text()
    check('positive_explicit_negation_and_witness_in_compiled_source',
          '(m₀ : ℕ) : high_span m₀ ≠ oblique ⊓ krein_polynomials' in positive
          and '(1 + X : Polynomial ℝ) ∉ high_span m₀' in positive
          and '(1 + X : Polynomial ℝ) ∈ oblique ⊓ krein_polynomials' in positive)
    check('supplied_maintained_verifier_implementation_absent',
          not any(Path(k).name in {'verify_contract.py','verify.py','verify_lean.py'}
                  for k in pkt['inputs']))
    source_warnings=(OUT/'logs/02-root-compile.stdout.txt').read_text()
    check('only_known_root_linter_warning',source_warnings.count('warning:')==1 and
          '119:30: warning: Used ' in source_warnings and 'error:' not in source_warnings)
    write_json(OUT/'checks/declaration-comparison.json',
               {'exports_byte_equality':equality,'declarations':per_declaration,
                'graph_nodes':len(nodes),'semantic_graph_nodes':len(semantic_union),
                'unknown_dependencies':unknown,'unsafe_dependencies':unsafe,
                'axiom_union':sorted(allowed),'all_passed':True})
    write_json(OUT/'checks/root-identity.json',root_details)
    write_json(OUT/'checks/import-identity.json',
               {'root_object':{'path':str(ownroot),'sha256':root_hash,'bytes':ownroot.stat().st_size},
                'module_count':len(modules),'path_changes':path_changes,'modules':resolved,
                'all_nonlocal_objects_byte_verified_before_after':True})
    write_json(OUT/'checks/command-summary.json',
               [{'receipt':'logs/'+name+'.json','argv':r['argv'],'exit_code':r['exit_code'],
                 'expected_exit_code':r['expected_exit_code'],'duration_seconds':r['duration_seconds']}
                for name,r in receipts.items()])
    write_json(OUT/'checks/RESULT.json',{'status':'PASS','checks':len(results),'completed_at':now(),
               'root_object_sha256':root_hash,'all59_export_bytes_identical':True,
               'axiom_union':sorted(allowed),'negative_control_exit':1,'root_conjuncts':len(conjuncts)})
    print(json.dumps(load('checks/RESULT.json'),ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    try: compare()
    except BaseException as e:
        write_json(OUT/'checks/RESULT.json',{'status':'FAIL','error':str(e),'checks':results,'at':now()})
        traceback.print_exc()
        sys.exit(1)

