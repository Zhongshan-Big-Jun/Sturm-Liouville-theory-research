from pathlib import Path
import json,hashlib,sys,re
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923');A=R/'research/artifacts/literature-absorption-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(x,msg):
    if not x:raise RuntimeError(msg)
checks=[];catalog=json.loads((R/'literature/absorption-20260923/source-catalog.json').read_text());check(len(catalog['sources'])==13,'Source cardinality')
for src in catalog['sources']:
    check(sha(R/src['note_path'])==src['note_sha256'],'Note drift '+src['id'])
    n=L.read_source(R,src['public_note_capture']['source_id'],1,1)
    check(n.get('source_id')==src['public_note_capture']['source_id'],'Source resolution '+src['id'])
    cap=src['primary_capture'];record=O/'source-cache'/cap['source'];check(sha(record)==src['primary_source_record_sha256'],'Original source record drift')
    check(sha(record.parent/'raw.bin')==cap['raw_sha256'] and sha(record.parent/'text.txt')==cap['text_sha256'],'Raw/text source drift')
    checks.append(dict(kind='source',id=src['id'],note_sha256=src['note_sha256'],status=src['reading_status']))
check(next(x for x in catalog['sources'] if x['id']=='L13')['reading_status'].startswith('METADATA_'),'L13 wrongly promoted')
check(bool(next(x for x in catalog['sources'] if x['id']=='L03').get('metadata_corrections')),'Missing L03 correction overlay')
index=json.loads((R/'index/tools.json').read_text());rows={x['location']:x for x in index['items']};new=[]
for group in ['domains','approximation','interfaces']:
    for item in json.loads((O/(group+'-cards.json')).read_text()):
        p=R/item['location'];check(sha(p)==item['sha256'],'New card drift')
        front,body,status=L.read_metadata(p.read_bytes());proposal=json.loads((R/item['proposed_card']).read_text());old=proposal['content']
        expected=old if isinstance(old,str) else '\n\n'.join('## '+k+'\n\n'+v for k,v in old.items())
        check(body.strip()==expected.strip(),'Mathematical body changed on integration '+item['location'])
        for key in ['conditions','scope','summary','title']:check(front.get(key)==proposal.get(key),'Changed reviewed '+key)
        if isinstance(old,dict):check(front['structured_content']==old,'Structured content not preserved')
        check(front['review_status']['verdict']=='APPROVED','Unapproved card')
        proof=json.loads((R/front['review_status']['report']).read_text());check(proof['verdict']=='APPROVED' and proof['packet_sha256']==front['review_status']['packet_sha256'],'Wrong approval packet')
        for key in ['sources','evidence']:
            for ref in L.reference_states(R,front[key]):
                if ref.get('path') or ref.get('source_id'):check(ref['binding_state']=='CURRENT','Bad reference '+str(ref))
        row=rows.get(item['location']);check(row and row['reuse_allowed'] and row['sha256']==sha(p),'Unavailable new tool')
        check(row['summary']==front['summary'][:500] and row['conditions']==front['conditions'] and row['scope']==front['scope'],'Incorrect query summary/scope')
        check(any(x['state']=='CURRENT' for x in row['annotations']),'Missing current annotation')
        new.append(item['location']);checks.append(dict(kind='tool',path=item['location'],sha256=sha(p),review_packet=proof['packet_sha256'],mathematics_preserved=True))
check(len(new)==11,'Expected11 new tools')
# Verify all exported input identities. Original domain rejection has permanent frozen copies.
for name in ['interfaces','approximation','domains','domains3']:
    p=A/'reviews'/name;prov=json.loads((p/'provenance.json').read_text());frozen={x['input_path']:x for x in json.loads((p/'frozen-input-map.json').read_text())['inputs']} if (p/'frozen-input-map.json').exists() else {}
    for row in prov['inputs']:
        if row['availability']=='PUBLIC_EXACT_INPUT':target=R/frozen.get(row['input_path'],row)['public_path']
        else:target=Path(row['local_path'])
        check(sha(target)==row['sha256'],'Review input identity drift '+name+'/'+row['input_path'])
    spawn=json.loads((p/'spawn.json').read_text());check(spawn['arguments']['fork_context'] is False,'Review context not isolated')
    check(spawn['result']['agent_id']==prov['reviewer_id'],'Reviewer ID mismatch')
    checks.append(dict(kind='review-export',name=name,verdict=prov['verdict'],inputs=len(prov['inputs']),native_isolation_confirmed=True))
tex=R/'docs/SL_fixed_n_supremum.tex';before=A/'before/docs/SL_fixed_n_supremum.tex';marker=b'\\begin{thebibliography}'
check(tex.read_bytes().split(marker)[0]==before.read_bytes().split(marker)[0],'Mathematical TeX body changed')
result=dict(status='PASS',source_records=13,targeted_originals=12,metadata_only_lead=1,new_scoped_tools=len(new),version_bound_annotations=len(json.loads((O/'annotations.json').read_text())),usable=len(index['items']),blocked=len(index['blocked_items']),historical_gate_warnings=len(index['issues']),checks=checks,formalization='No new Lean. These integration checks do not replace the recorded independent analytic reviews.')
(O/'integration-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
