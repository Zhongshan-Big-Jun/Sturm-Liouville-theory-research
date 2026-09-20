"""Renew four unchanged cards whose old shared review included a changing K1 card."""
from pathlib import Path
import sys
import json
import hashlib

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round4-20260921')
Art = 'research/artifacts/proof-audit-round4-20260921'
sys.path.insert(0, str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as Corrections
import research_review as Review

PriorPacketPath = Root/'research/library/reviews/packets/e35e4f9dc7e8adc5f424f0e56ac5cfe099924080195830a6a720e787c4e2736a/packet.json'
PriorPacket = json.loads(PriorPacketPath.read_text())
OldIds = [
	'71ea16c297d01a1b00edca68d76aa185b9ec99c1e3f5fdb9bfb6788760f5106f',
	'bcc4813b874b820d47f9fb47dfa5ac38b70267e87c464d74d6d01175f2170916',
	'a201d2e5ce0fce506c398a7a053274d6ef1883dedc6c6cef0d31fe75ee86dd90',
	'0daeec119317eb414580f207f6afc723883e0899b80bf08b589c42719de119ed'
]
Author = '01a06f46-dd03-7c83-9267-32048412c359'
Inputs = {}
Claims = []
Authors = {Author}
Rows = []
for OldId in OldIds:
	OldRevision = json.loads((Root/'research/library/corrections/requests'/(OldId+'.json')).read_text())['payload']
	assert hashlib.sha256((Root/OldRevision['new']['location']).read_bytes()).hexdigest() == OldRevision['new']['sha256']
	Saved = Out/('renew-'+Path(OldRevision['new']['location']).stem+'.json')
	if Saved.exists():
		Previous=json.loads(Saved.read_text()); assert Previous['old_revision']==OldId
		Result,Req=Previous['revision'],Previous['requirements']
	else:
		Result = Corrections.propose_revision(Root, OldRevision['issue'], OldRevision['old'], OldRevision['new'], Author,
			'Fourth-round review coherence renewal: this current card and its mathematical proof dependencies are byte-identical to the prior accepted version. Its previous shared review also included the K1 card, whose general-c status is being updated. Recheck this exact existing repair in a separate scoped packet; no new theorem or card edit is asserted here.')
		Req = Corrections.review_requirements(Root, Result['revision_id'])
	for Item in Req['inputs']:
		if Item['path'] in Inputs:
			assert Inputs[Item['path']]['sha256'] == Item['sha256']
		Inputs[Item['path']] = Item
	Claims += Req['claims']
	Authors.update(Req['author_ids'])
	Row = {'old_revision': OldId, 'revision': Result, 'requirements': Req}
	Rows.append(Row)
	(Out/('renew-'+Path(OldRevision['new']['location']).stem+'.json')).write_text(json.dumps(Row,ensure_ascii=False,indent=2)+'\n')
	print('Renewal proposed', OldRevision['new']['location'], flush=True)

StableSources = ['docs/SL_denseness_criteria.tex','docs/SL_fractional_left_definite.tex','docs/SL_h2_completeness_proof.tex','docs/SL_h3_completeness_proof.tex','tools/spectral-domain-checks.md']
Evidence = []
for Name in StableSources + [Row['requirements']['targets'][0]['location'] for Row in Rows]:
	Raw = (Root/Name).read_bytes()
	Hash = hashlib.sha256(Raw).hexdigest()
	assert Hash == PriorPacket['inputs'][Name]['sha256'], Name
	assert Raw == (PriorPacketPath.parent/PriorPacket['inputs'][Name]['snapshot']).read_bytes(), Name
	Evidence.append({'path':Name,'sha256':Hash,'matches_prior_frozen_input':True})
	Inputs.setdefault(Name, {'path':Name,'role':'unchanged-source-for-current-scoped-recheck'})
IdentityPath = Root/Art/'unchanged-card-inputs.json'
IdentityPath.write_text(json.dumps({'prior_packet':str(PriorPacketPath.relative_to(Root)),'checked':Evidence,'scope':'Four cards remain byte-identical; repair reacceptance is separately reviewed. This identity comparison is not a new proof.'},indent=2)+'\n')
Inputs[str(IdentityPath.relative_to(Root))] = {'path':str(IdentityPath.relative_to(Root)),'role':'exact-input-identity-evidence'}
Claims.append({'id':'R4-unchanged-card-scope','verification':'analytic','statement':'Recheck only the four existing card repairs and their precise mathematical scope, using the supplied unchanged proof dependencies. The H2/H3 results are inherited dependencies for the domain/spectral-transfer claims, not a request to recertify their entire derivations. The exact x2 and p4 thresholds and the open 3<s<7/2 interval must remain correctly distinguished. These cards and their supplied proof files match the prior frozen input hashes; the previous combined review also covered a separate K1 card now being revised. No new spectral theorem or numerical re-execution is claimed by this receipt renewal. Check that none of the four retained cards depends mathematically on the changed general-c K1 status.'})
for Row in json.loads((Out/'stability-revisions.json').read_text()):
	Req=Row['requirements']
	for Item in Req['inputs']:
		if Item['path'] in Inputs: assert Inputs[Item['path']]['sha256']==Item['sha256']
		Inputs[Item['path']]=Item
	Claims+=Req['claims']; Authors.update(Req['author_ids']); Rows.append(Row)
Name='docs/SL_stability_moment_jump.tex'
Inputs.setdefault(Name,{'path':Name,'role':'unchanged-stability-proof'})
Claims.append({'id':'R4-stability-binding-renewal','verification':'analytic','statement':'Independently verify the exact retained stability-card repair against its unchanged proof. Distinguish general recurrence lower bound from the B=0 exact model, require both perturbed coefficients at all indices, and preserve the bounded-basis-perturbation counterexample. The new footer/source binding renews evidence after an unrelated quotient document changed; it is not a new mathematical result or newly discovered flaw in this stability proof.'})
Packet = Review.create_packet(Root, {'kind':'mathematics','author_ids':sorted(Authors),'inputs':list(Inputs.values()),'claims':Claims})
(Out/'unchanged-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
(Out/'unchanged-renewals.json').write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(Packet,ensure_ascii=False))
