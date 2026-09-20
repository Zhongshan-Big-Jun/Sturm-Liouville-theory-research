from pathlib import Path
import json,sys
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round4-20260921')
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as R
Intake=json.loads((Out/'card-intake.json').read_text());Old=next(X['old'] for X in Intake if X['issue_id']=='round4-k1-status');New=json.loads((Out/'k1-card-result.json').read_text())
Revision=C.propose_revision(Root,'round4-recurrence',Old,New,'01a06f46-dd03-7c83-9267-32048412c359','The revised K1 status card explicitly depends on the repaired third-order card. Its old round2 and new round4 K1 issues have independent approvals and release events, but the new exact dependency propagates the upstream round4-recurrence issue as a distinct review obligation. No further card or proof bytes changed. Review the exact dependency link and downstream scope before releasing this inherited obligation.')
Req=C.review_requirements(Root,Revision['revision_id']);Row={'issue_id':'round4-recurrence','revision':Revision,'requirements':Req};(Out/'k1-dependency-revisions.json').write_text(json.dumps([Row],indent=2)+'\n')
Inputs={I['path']:I for I in Req['inputs']}
Prior=json.loads((Out/'recurrence-review-dispatch.json').read_text())['bundle']
for Name in ['docs/SL_third_order_K1_proof.tex','docs/SL_third_order_recurrence_theory.tex',Prior+'/report.json']:
	Inputs.setdefault(Name,{'path':Name,'role':'proof-and-prior-scoped-review-provenance'})
Claims=Req['claims']+[{'id':'R4-K1-inherited-obligation','verification':'analytic','statement':'Review the previously unreleased dependency-propagated round4-recurrence obligation for the exact current K1 card. No new card/proof bytes are proposed: check its hash-bound upstream tool, explicit coefficient/parameter scope, terminal-convention distinction, normalization and specialization K0(1)=e/4. The current recurrence proof and actual prior review are supplied; the earlier review is provenance, not a substitute for checking this downstream inference. No wider-family conclusion, new numerical run or new full-project audit is asserted. A prior same-card approval for another issue does not waive this inherited obligation.'}]
Packet=R.create_packet(Root,{'kind':'mathematics','author_ids':Req['author_ids'],'inputs':list(Inputs.values()),'claims':Claims})
(Out/'k1-dependency-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n');print(Packet['packet_sha256'])
