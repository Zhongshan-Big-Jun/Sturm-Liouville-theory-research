from pathlib import Path
import json,sys,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923');Group=sys.argv[1];ReviewName=sys.argv[2] if len(sys.argv)>2 else Group;Q=O/'verification'/ReviewName;Root=R/'literature/absorption-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_review as V
D=json.loads((O/(ReviewName+'-review-dispatch.json')).read_text());Verdict=V.verify_review_bundle(Q,D['bundle'])
if Verdict['verdict']!='APPROVED':raise RuntimeError('Acceptance unavailable')
Packet=json.loads((Q/json.loads((O/(ReviewName+'-review-packet.json')).read_text())['packet']).read_text());Catalog=json.loads((Root/'source-catalog.json').read_text());ByURL={x['primary_capture']['url']:x for x in Catalog['sources']}
ProposalDir={'domains':'proposed-tool-cards','approximation':'tool-cards','interfaces':'cards'}[Group]
Names={'01-finite-tsvd':'finite-synthesis-tsvd','02-krein-integrated-legendre':'krein-integrated-legendre-riesz','03-full-muntz-moment-interface':'full-muntz-krein-moment-interface','04-infinite-deletion-subclasses':'krein-infinite-deletion-subclasses','L10-fixed-operator-bridge':'fixed-operator-boundary-extension-check','L11-measures-and-concentration':'measure-weight-atoms-and-concentration','P3-bounded-interface-chain-rule':'finite-interface-second-derivative'}
Author=json.loads((O/(Group+'-spawn.json')).read_text())['result']['agent_id'];Report='research/artifacts/literature-absorption-20260923/reviews/'+ReviewName+'/runtime/report.json';Provenance='research/artifacts/literature-absorption-20260923/reviews/'+ReviewName+'/provenance.json'
Done=json.loads((O/(Group+'-cards.json')).read_text()) if (O/(Group+'-cards.json')).exists() else []
for p in sorted((Root/Group/ProposalDir).glob('*.json')):
    proposal=ProposalDir+'/'+p.name;Raw=p.read_bytes();h=L.digest(Raw)
    if Packet['inputs'].get(proposal,{}).get('sha256')!=h:raise RuntimeError('Unreviewed proposed card '+proposal)
    name=Names.get(p.stem,p.stem);loc='tools/'+name+'.md'
    if any(x['location']==loc for x in Done):
        old=next(x for x in Done if x['location']==loc)
        if L.digest((R/loc).read_bytes())!=old['sha256']:raise RuntimeError('Imported card drift')
        continue
    if (R/loc).exists():raise RuntimeError('New tool path collides '+loc)
    Data=json.loads(Raw);Refs=[];NoteIDs=set()
    for ref in Data.get('sources',[]):
        ref=dict(ref)
        if ref.get('path'):
            old=Path(ref['path']);dest=old if old.is_absolute() else Root/Group/old
            if not dest.is_relative_to(R):raise RuntimeError('External file reference '+str(dest))
            ref['path']=dest.relative_to(R).as_posix()
            if ref.get('sha256',L.digest(dest.read_bytes()))!=L.digest(dest.read_bytes()):raise RuntimeError('Source hash drift '+ref['path'])
        elif ref.get('url'):
            original_id=ref.pop('source_id',None)
            if original_id:ref['author_source_id']=original_id
            ref.pop('source_id_scope',None)
            if ref['url'] in ByURL:
                row=ByURL[ref['url']];ref['primary_source_namespace']='private source-cache';ref['primary_source_id']=row['primary_capture']['source_id'];ref['raw_sha256']=row['primary_capture']['raw_sha256'];ref['text_sha256']=row['primary_capture']['text_sha256'];NoteIDs.add(row['public_note_capture']['source_id'])
        else:raise RuntimeError('Unsupported source pointer '+str(ref))
        Refs.append(ref)
    Refs.extend(dict(source_id=x,locator='Original project reading/assumption note; SECONDARY source, primary body separately identified') for x in sorted(NoteIDs))
    OldContent=Data['content'];OldStatus=Data.get('evidence_status')
    if isinstance(OldContent,str):Body=OldContent
    elif isinstance(OldContent,dict) and all(isinstance(v,str) for v in OldContent.values()):
        Body='\n\n'.join('## '+k+'\n\n'+v for k,v in OldContent.items())
        Data['structured_content']=OldContent
    else:raise RuntimeError('Unsupported structured mathematical content')
    Data['content']=Body
    Data.update(tool_id=name,author_ids=[Author,'01a06f46-dd03-7c83-9267-32048412c359'],sources=Refs,evidence_status='INDEPENDENT_ANALYTIC_REVIEW_APPROVED_WITH_DECLARED_LIMITS',review_status=dict(verdict='APPROVED',reviewer_id=D['reviewer_id'],packet_sha256=Verdict['packet_sha256'],report=Report,scope='Exact original mathematical content and source mapping; no complete Lean formalization or canonical acceptance'),integration_status='ACTIVE_SCOPED_REVIEW; REVALIDATE_EACH_APPLICATION',evidence=[dict(path=Report,locator='Per-claim scope and limitations'),dict(path=Provenance,locator='Native call and exact input identities; private primary-source availability'),dict(path=p.relative_to(R).as_posix(),locator='Exact proposed card reviewed independently')],created='2026-09-23',updated='2026-09-23')
    # Mathematical content and explicit assumptions stay exactly as independently reviewed.
    # Author-era provenance sentences remain attributable to the frozen proposed card;
    # current review evidence is recorded in separate fields rather than rewriting prose.
    if Data['content']!=Body:raise RuntimeError('Unexpected body edit')
    Result=L.save_card(R,Data,loc)
    Done.append(dict(Result,group=Group,proposed_card=p.relative_to(R).as_posix(),proposed_sha256=h,mathematical_content_sha256=L.digest(Body.encode()),rendering='verbatim string' if isinstance(OldContent,str) else 'original string-valued dictionary rendered as same-key Markdown sections; structured_content retained verbatim',author_evidence_status=OldStatus,review_bundle_private=D['bundle'],public_report=Report))
    (O/(Group+'-cards.json')).write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n')
    print('Saved approved scope',loc,Result['sha256'],flush=True)
