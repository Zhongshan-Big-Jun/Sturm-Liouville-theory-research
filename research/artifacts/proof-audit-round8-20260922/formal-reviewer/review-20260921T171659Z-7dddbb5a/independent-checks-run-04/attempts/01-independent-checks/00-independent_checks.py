from pathlib import Path
from fractions import Fraction as F
import collections, hashlib, json, re, sys, zipfile
sys.setrecursionlimit(100000)
ROOT=Path(__file__).resolve().parent
PACKET=Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/02bb73b7d317455bfe1b191b4a0a4b66bae141336c65815df537fe1ba273347f/packet.json')
pkt=json.loads(PACKET.read_text())
PACKAGE=ROOT/'package';REPLAY=ROOT/'replay-01'
def read(p): return json.loads(Path(p).read_text())
def digest(p):
 with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def stable(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def supplied(suffix):
 return PACKET.parent/next(v['snapshot'] for k,v in pkt['inputs'].items() if k.endswith(suffix))
checks={}
def verify(name,condition,details=None):
 checks[name]={'passed':bool(condition),'details':details}
 if not condition: raise AssertionError(name+': '+str(details))

def scan(e,depth=0):
 tag=e[0];constants=set()
 if tag=='bvar':
  if not (0<=e[1]<depth): raise ValueError(('unbound',e,depth))
 elif tag in ('fvar','mvar'): raise ValueError(('free_or_meta',e))
 elif tag=='const': constants.add(e[1][0])
 elif tag in ('forall','lam'):
  constants |= scan(e[2],depth);constants |= scan(e[3],depth+1)
 elif tag=='let':
  constants |= scan(e[1],depth);constants |= scan(e[2],depth);constants |= scan(e[3],depth+1)
 elif tag=='app': constants |= scan(e[1],depth)|scan(e[2],depth)
 elif tag=='projection': constants.add(e[1]);constants |= scan(e[3],depth)
 elif tag not in ('sort','literal'): raise ValueError(('unrecognized',tag))
 return constants

def scan_used(e,depth=0):
 tag=e[0];constants=set()
 if tag=='bvar':
  if not (0<=e[1]<depth): raise ValueError(('unbound',e,depth))
 elif tag in ('fvar','mvar'): raise ValueError(('free_or_meta',e))
 elif tag=='const': constants.add(e[1][0])
 elif tag in ('forall','lam'):
  constants |= scan_used(e[2],depth);constants |= scan_used(e[3],depth+1)
 elif tag=='let':
  constants |= scan_used(e[1],depth);constants |= scan_used(e[2],depth);constants |= scan_used(e[3],depth+1)
 elif tag=='app': constants |= scan_used(e[1],depth)|scan_used(e[2],depth)
 elif tag=='projection': constants |= scan_used(e[3],depth)
 elif tag not in ('sort','literal'): raise ValueError(('unrecognized',tag))
 return constants

def split_and(e):
 if e[0]=='app' and e[1][0]=='app' and e[1][1][0]=='const' and e[1][1][1][0]=='And':return e[1][2],e[2]
 raise ValueError('not an And')

inventory={k:digest(PACKET.parent/v['snapshot']) for k,v in pkt['inputs'].items()}
verify('all_ten_input_hashes',all(inventory[k]==v['sha256'] for k,v in pkt['inputs'].items()),inventory)
handoff=read(supplied('handoff-manifest.json'))
verify('all_archive_member_hashes',all(digest(PACKAGE/n)==h for n,h in handoff['package_files'].items()),{'members':len(handoff['package_files'])})
verify('archive_identity',digest(ROOT/'round8-lean-frozen-inputs.zip')==handoff['archive']['sha256'])
verify('standalone_package_compiled_source_equal',supplied('lean-proof/SL/AuditRound8.lean').read_bytes()==(PACKAGE/'AuditRound8.lean').read_bytes()==(REPLAY/'src/AuditRound8.lean').read_bytes())
verify('copied_package_contains_no_proof_object',not any(p.suffix in ('.olean','.ir') for p in PACKAGE.rglob('*')))

d=read(REPLAY/'declarations.json');author=read(supplied('author-replay-03/declarations.json'));contract=read(PACKAGE/'public-declaration-contract.json')
public={p['declaration']:p for p in d['public_declarations']}
deps={p['name']:p for p in d['dependencies']}
verify('complete_public_inventory',len(public)==47 and set(public)=={p['declaration'] for p in contract['entries']})
verify('all_public_types_bodies_match_author_export',d['public_declarations']==author['public_declarations'])
verify('all_dependency_records_match_author_export',d['dependencies']==author['dependencies'])
verify('public_kind_inventory',collections.Counter(p['kind'] for p in public.values())=={'theorem':36,'definition':11})
verify('source_inventory',set('AuditRound8.'+n for n in re.findall(r'^(?:def|theorem|lemma) (\w+)',(PACKAGE/'AuditRound8.lean').read_text(),re.M))=={p['declaration'] for p in contract['entries'] if p['origin']=='source'})
allowed={'propext','Classical.choice','Quot.sound'}
for name,p in public.items():
 refs=scan(p['type_expression'])
 term=p['type_expression'];binders=[]
 while term[0]=='forall':binders.append(term[1]);term=term[3]
 verify('binders:'+name,binders==p['binder_kinds'])
 if p['kind']=='definition':refs |= scan(p['value_expression'])
 verify('closed_type_and_definition:'+name,refs<=set(deps))
 verify('axioms:'+name,set(p['axioms'])<=allowed and not p['unsafe'])
verify('closed_dependency_edges',all(set(p['type_dependencies']+p['body_dependencies'])<=set(deps) for p in deps.values()))
verify('safe_known_dependencies',all(not p.get('missing') and not p.get('unsafe') for p in deps.values()))
verify('only_standard_axioms',{p['name'] for p in deps.values() if p['kind']=='axiom'}==allowed)
seen=set();pending=list(public)+list(scan(d['expected_type_expression']))
while pending:
 name=pending.pop()
 if name in seen:continue
 seen.add(name);pending += deps[name]['type_dependencies']+deps[name]['body_dependencies']
verify('exact_dependency_reachability',seen==set(deps),{'declarations':len(seen)})
component_names=['phase_bound','integral_reduction','S_reduction','coefficient_identity','stationary_coefficient','scalar_ratio_bound','B_curved_counterexample','D_gap_signs','D_curved_counterexample']
root_type=public['AuditRound8.local_root']['type_expression'];remainder=root_type
for name in component_names[:-1]:
 first,remainder=split_and(remainder)
 verify('root_conjunct:'+name,first==public['AuditRound8.'+name]['type_expression'])
verify('root_conjunct:'+component_names[-1],remainder==public['AuditRound8.'+component_names[-1]]['type_expression'])
verify('literal_complete_expected_type',root_type==d['expected_type_expression'])
blind=read(supplied('/report.json'));dispatch=read(supplied('/dispatch.json'));spawn=read(supplied('/spawn.json'))
verify('blind_inventory_matches_actual',len(blind['claim_results'])==47 and {v['id'] for v in blind['claim_results']}==set(public))
verify('blind_provenance_binding',dispatch['spawn_sha256']==digest(supplied('/spawn.json')) and dispatch['packet_sha256']==blind['packet_sha256'] and dispatch['reviewer_id']==spawn['result']['agent_id'] and not spawn['arguments']['fork_context'] and dispatch['reviewer_id'] not in pkt['author_ids'])
verify('source_definitions_count',len([p for p in public.values() if p['kind']=='definition'])==11)

ratio=F(4)*F(337,1000)*9*F(100046,100000)/(3*F(333,106)*F(156,100)*F(99996,100000))
wB=F(48743,100000);wD=F(4995815,10000000);r=F(3015,2)
threshold=(2*wB/(1-2*wB))**2
B_left=threshold-1500;B_right=r-threshold
fac=1/(4*wD*wD)-1
D_left=25-F(31416,10000)**2*r*fac
D_right=F(31415,10000)**2*1515*fac-25
verify('independent_exact_rational_scalar',ratio==F(893460803,1082206710) and F(4,5)<ratio<F(8256,10000),{'value':str(ratio),'upper_margin':str(F(8256,10000)-ratio),'false_bound_margin':str(ratio-F(4,5))})
verify('independent_exact_B_witness',1500<r<1515 and F(19,100)<wB<F(1,2) and B_left>0 and B_right>0,{'threshold':str(threshold),'left_squared_margin':str(B_left),'right_squared_margin':str(B_right)})
verify('independent_exact_D_witness',0<wD<F(1,2) and fac>0 and D_left>0 and D_right>0,{'pi_lower':'31415/10000','pi_upper':'31416/10000','left_gap_upper_margin':str(D_left),'right_gap_lower_margin':str(D_right)})

receipts=[]
for p in sorted((REPLAY/'logs').glob('*.json')):
 rec=read(p);label=rec['label']
 verify('receipt_stream_hashes:'+label,all(digest(p.with_suffix('.'+s+'.txt'))==rec[s+'_sha256'] for s in ['stdout','stderr']))
 verify('receipt_input_stability:'+label,rec['inputs_before']==rec['inputs_after'] and rec['inputs_unchanged'])
 verify('receipt_source_snapshots:'+label,all(digest(REPLAY/'attempts'/label/(str(i).zfill(2)+'-'+Path(n).name))==h for i,(n,h) in enumerate(rec['inputs_before'].items())))
 so=p.with_suffix('.stdout.txt').read_text();se=p.with_suffix('.stderr.txt').read_text()
 expected=1 if label.split('-')[0] in ['08','09','10'] else 0
 verify('command_exit:'+label,rec['exit_code']==expected,{'argv':rec['argv'],'exit':rec['exit_code'],'stdout':so,'stderr':se})
 receipts.append({'label':label,'argv':rec['argv'],'exit_code':rec['exit_code'],'receipt_sha256':digest(p),'stdout_sha256':rec['stdout_sha256'],'stderr_sha256':rec['stderr_sha256']})
verify('ten_replay_commands',len(receipts)==10)
for stem in ['imports','runtime']:
 before=read(REPLAY/(stem+'-before.json'));after=read(REPLAY/(stem+'-after.json'))
 verify(stem+'_before_after_equal',before==after,{'count':len(before)})
 binding=read(PACKAGE/'external-environment.json')[('import' if stem=='imports' else stem)+'_hashes']
 verify(stem+'_equals_frozen_binding',{k:v['sha256'] for k,v in before.items()}==binding)
root_entries=[v for v in d['modules'] if v['module']=='AuditRound8']
expected_windows=str(REPLAY/'lib/AuditRound8.olean').replace('/mnt/f/','F:\\\\').replace('/','\\\\')
actual_root=root_entries[0]['olean'].replace('\\\\','/').replace('\\','/') if len(root_entries)==1 else ''
verify('fresh_root_module_resolution',actual_root.lower()==('F:'+str(REPLAY/'lib/AuditRound8.olean')[6:]).lower(),{'resolved':root_entries,'expected':str(REPLAY/'lib/AuditRound8.olean')})
verify('no_imported_project_proof',all(not v['module'].startswith('SL.') for v in d['modules']))
manifest=read(REPLAY/'receipt-manifest.json')
verify('replay_receipt_manifest_hashes',all(digest(REPLAY/n)==h for n,h in manifest['files'].items()),{'files':len(manifest['files'])})
index=read(PACKAGE/'command-index.json');ev=read(PACKAGE/'author-evidence.json')
verify('supplied_author_history_counts',len(index['commands'])==32 and sum(bool(r['exit_code']) for r in index['commands'])==10 and sum(r['executable'].endswith('/lean.exe') for r in index['commands'])==25)
verify('author_history_manifest_identities',all(handoff['raw_evidence_files'].get(r['path'])==r['sha256'] for r in index['commands']))
verify('author_evidence_bound_to_supplied_export',ev['final_replay']==read(supplied('author-replay-03/evidence.json')) and ev['final_replay']['declarations_sha256']==digest(supplied('author-replay-03/declarations.json')))

semantic=read(ROOT/'supplemental-01/semantic-definitions.json')
all_sem={v['name']:v for v in semantic['semantic_nodes']}
semantic_reachable=set();semantic_pending=list(public)
while semantic_pending:
 name=semantic_pending.pop()
 if name in semantic_reachable:continue
 semantic_reachable.add(name);node=all_sem[name]
 semantic_pending+=node['type_dependencies']
 if node['kind']!='theorem':semantic_pending+=node['body_dependencies']
supplemental_auxiliaries=sorted(set(all_sem)-semantic_reachable)
verify('supplemental_generated_auxiliaries_identified',set(supplemental_auxiliaries)=={'AuditRound8.I2.eq_1','AuditRound8.phase.eq_1','AuditRound8.wCap.eq_1','AuditRound8.wCritical.eq_1'},supplemental_auxiliaries)
verify('supplemental_auxiliaries_only_define_existing_functions',all(all_sem[n]['kind']=='theorem' and scan(all_sem[n]['type_expression'])<=semantic_reachable for n in supplemental_auxiliaries))
sem={n:all_sem[n] for n in sorted(semantic_reachable)}
verify('requested_semantic_scope',len(sem)==1794 and set(sem)<=set(deps),{'reviewed_semantic_nodes':len(sem),'supplemental_generated_auxiliaries':supplemental_auxiliaries})
(ROOT/'semantic-definitions-reviewed.json').write_text(json.dumps({'source_export_sha256':digest(ROOT/'supplemental-01/semantic-definitions.json'),'roots':sorted(public),'semantic_nodes':list(sem.values()),'separate_supplemental_auxiliaries':supplemental_auxiliaries},ensure_ascii=False)+'\n')
for name,node in sem.items():
 verify('semantic_type_constants:'+name,scan_used(node['type_expression'])==set(node['type_dependencies']))
 verify('semantic_node_matches_replay:'+name,all(node[k]==deps[name][k] for k in ['kind','universes','unsafe','type_dependencies','body_dependencies']))
 if 'value_expression' in node:
  verify('semantic_body_constants:'+name,scan_used(node['value_expression'])==set(node['body_dependencies']))
 verify('semantic_projected_types_closed:'+name,scan(node['type_expression'])<=set(sem) and ('value_expression' not in node or scan(node['value_expression'])<=set(sem)))
 refs=set(node['type_dependencies'])
 if node['kind']!='theorem':refs.update(node['body_dependencies'])
 verify('semantic_closure:'+name,refs<=set(sem))
 if node['kind'] in ['definition','opaque']:
  verify('semantic_actual_body_present:'+name,'value_expression' in node)
 if name in public:
  verify('public_type_same_as_semantic:'+name,node['type_expression']==public[name]['type_expression'])
  if node['kind']=='definition':verify('public_body_same_as_semantic:'+name,node['value_expression']==public[name]['value_expression'])
verify('semantic_root_set_complete',set(public)<=set(sem))
verify('supplemental_proofs_allowed_axioms',len(semantic['controls'])==4 and all(set(v['axioms'])<=allowed for v in semantic['controls']))
verify('supplemental_same_loaded_modules',semantic['modules']==d['modules'])
verify('supplemental_stability',read(ROOT/'supplemental-01/stability.json')=={'imports_unchanged':True,'runtime_unchanged':True,'root_unchanged':True,'exit_code':0})
verify('supplemental_hashes_match_replay',all(read(ROOT/'supplemental-01'/f'{stem}-{when}.json')==read(REPLAY/f'{stem}-after.json') for stem in ['imports','runtime'] for when in ['before','after']))

result={'packet_sha256':digest(PACKET),'checks':checks,'public_semantic_sha256':stable(d['public_declarations']),'command_receipts':receipts,'author_nonzero_summaries':[r for r in index['commands'] if r['exit_code']],
'limitations':['Historical author raw stdout/stderr and seven non-control failure receipts are only indexed, not included; those failures were inspected as supplied summaries, not independently replayed.','This checks the supplied current snapshots, not an unsupplied live source tree.']}
(ROOT/'independent-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'all_passed':True,'check_count':len(checks),'public_semantic_sha256':result['public_semantic_sha256'],'exact_scalar':checks['independent_exact_rational_scalar'],'exact_B':checks['independent_exact_B_witness'],'exact_D':checks['independent_exact_D_witness']},indent=2))
