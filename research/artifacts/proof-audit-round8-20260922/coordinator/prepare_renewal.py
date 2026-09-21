from pathlib import Path
import sys,json,hashlib,difflib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as V
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
initial={x['release'] for x in json.loads((O/'initial-impact.json').read_text())['problems']};q=json.loads((A/'retrieval-before-renewal.json').read_text())
bad={x['release']:x for x in q['issues'] if x['release'] not in initial}
if len(bad)!=18 or any('docs/SL_spectral_topics_summary.tex' not in x['error'] for x in bad.values()):raise RuntimeError('Unexpected renewal problem set')
store=C.load_store(R);inputs={};claims={};authors={'01a06f46-dd03-7c83-9267-32048412c359'};rows=[];packets={};same=[]
for oldrelease in bad:
	r=store['requests'][oldrelease]['payload'];rid=r['revision'];rev=store['requests'][rid]['payload'];target=rev['new'];loc=target['location']
	if sha(R/loc)!=target['sha256']:raise RuntimeError('Renewal card changed '+loc)
	req=C.review_requirements(R,rid)
	for x in req['inputs']:
		if x['path'] in inputs and inputs[x['path']].get('sha256')!=x['sha256']:raise RuntimeError('Conflicting exact binding')
		inputs[x['path']]=x
	for x in req['claims']:claims[x['id']]=x
	authors.update(req['author_ids'])
	rows.append(dict(old_release=oldrelease,revision=rid,target=target,issue=rev['issue'],old_bundle=r['bundle']))
	packetpath=json.loads((R/r['bundle']/'dispatch.json').read_text())['packet'];packets[packetpath]=r['bundle']
for packetpath,bundle in packets.items():
	packet=json.loads((R/packetpath).read_text());authors.update(packet['author_ids']);changes=[]
	for name,info in packet['inputs'].items():
		current=sha(R/name);frozen=R/packetpath;frozen=frozen.parent/info['snapshot']
		if sha(frozen)!=info['sha256']:raise RuntimeError('Old frozen evidence changed '+name)
		if current!=info['sha256']:changes.append(name)
		else:same.append(dict(path=name,sha256=current,prior_packet=packetpath))
		inputs.setdefault(name,dict(path=name,role='unchanged-prior-proof-or-evidence'))
	if changes!=['docs/SL_spectral_topics_summary.tex']:raise RuntimeError('Old packet has unexpected changed inputs '+str(changes))
	for n in [packetpath,bundle+'/report.json',bundle+'/dispatch.json',bundle+'/spawn.json',bundle+'/receipt.json']:
		inputs.setdefault(n,dict(path=n,role='historical-acceptance-provenance-not-current-approval'))
old=A/'before/docs/SL_spectral_topics_summary.tex';new=R/'docs/SL_spectral_topics_summary.tex'
delta=''.join(difflib.unified_diff(old.read_text().splitlines(True),new.read_text().splitlines(True),fromfile='round8 baseline summary',tofile='current summary'))
(A/'renewal-summary.diff').write_text(delta)
identity={'cause':'Current query was 70 available /9 blocked after INF-only summary edit; eight unchanged left-definite cards need 18 exact review renewals. Old combined packet bound the whole summary, although the changed INF section is not one of their mathematical premises. No card or left-definite proof is edited in this renewal.','unchanged_bindings':same,'prior_packets':list(packets),'old_summary_sha256':sha(old),'new_summary_sha256':sha(new),'renewals':rows}
save(A/'renewal-identities.json',identity);save(O/'renewals.json',rows)
for n in [str(old.relative_to(R)),str(new.relative_to(R)),str((A/'renewal-summary.diff').relative_to(R)),str((A/'renewal-identities.json').relative_to(R))]:inputs.setdefault(n,dict(path=n,role='changed-section-and-unchanged-proof-identity-evidence'))
claims['R8-unchanged-card-renewal']=dict(id='R8-unchanged-card-renewal',verification='analytic',statement='Recheck the 18 stated existing correction obligations for eight current left-definite cards. Their card/proof/dependency bytes are unchanged from the supplied previous accepted packet. Its sole changed input is the summary INF section, shown by before/after source and diff. Independently check this change has no mathematical bearing on the retained fractional window, trace/projection/moment/stability/quotient scopes; inspect the actual corrected statements and dependency hypotheses, not just previous verdict words. Classical H2/H3 and prior unchanged derivations remain inherited dependencies; this scoped renewal does not recertify their full proofs, run old numerical scans or confer new Lean status. The original withdrawn left-definite-orthogonal-systems card stays withdrawn. Do not ask to repair unrelated inherited preview prose without a newly verified material defect; assess the current exact mathematical repair scope. Confirm no changed INF claim is a premise of these retained results and no unstated scope expansion is introduced.')
spec=dict(kind='mathematics',author_ids=sorted(authors),inputs=list(inputs.values()),claims=list(claims.values()));save(O/'renewal-review-spec.json',spec);save(O/'renewal-review-packet.json',V.create_packet(R,spec));print('Renewal packet prepared',len(inputs),'inputs',len(claims),'claims',len(rows),'releases',len({x['target']['location'] for x in rows}),'unchanged cards',flush=True)
