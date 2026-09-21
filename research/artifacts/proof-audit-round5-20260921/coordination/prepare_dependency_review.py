from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round5-20260921')
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as V
New=json.loads((O/'card-result.json').read_text());Old={'location':New['location'],'sha256':'1e8977c0137179a8a5009e8de9e5c3055a0596e1454d4e3ee3f9a6c0ec80f0d5'}
print('Preparing inherited round2-spectrum obligation for unchanged current card',flush=True)
Revision=C.propose_revision(R,'round2-spectrum',Old,New,'01a06f46-dd03-7c83-9267-32048412c359','The fifth-round cofinite card now explicitly depends on the exact left-definite-theory card, whose spectral-domain dependency propagates round2-spectrum. The original fifth-round issue is already independently approved and has a release event, but does not waive this distinct inherited obligation. No card or proof bytes change. Review the operator domain, positive shift, norm/isometry, two low modes and scope boundaries before releasing the inherited spectral obligation.')
(O/'dependency-revision-result.json').write_text(json.dumps(Revision,ensure_ascii=False,indent=2)+'\n');print('Committed inherited revision',Revision['revision_id'],flush=True)
Req=C.review_requirements(R,Revision['revision_id']);(O/'dependency-review-requirements.json').write_text(json.dumps(Req,ensure_ascii=False,indent=2)+'\n')
Inputs={I['path']:I for I in Req['inputs']};Prior=json.loads((O/'mathematics-review-dispatch.json').read_text())['bundle']
for Name in ['docs/SL_cofinite_left_definite.tex','docs/SL_h2_completeness_proof.tex','docs/SL_fractional_left_definite.tex','tools/spectral-domain-checks.md',Prior+'/report.json']:
 Inputs.setdefault(Name,{'path':Name,'role':'proof-transitive-dependency-or-prior-scoped-review'})
Claims=Req['claims']+[{'id':'R5-inherited-spectrum-obligation','verification':'analytic','statement':'Independently review the inherited round2-spectrum issue for this exact unchanged fifth-round card. Check the explicit dependency chain to left-definite-theory and spectral-domain-checks, their actual hashes, the precise Krein operator domain Hc2=D(Kc), c>0, the graph norm, positive self-adjoint onto isometry, and inclusion of both1 andx low modes. Check that the complex cofinite classification and Green/moment formulas do not rely on discarded all-order density, missing norms, ordinary-Sobolev/domain confusion, invalid negative-order completion or unproved s=3/non-cofinite claims. The new analytic proof supplies its own operator and topology argument; the prior fifth-round review is provenance, not a substitute for checking this dependency application. No card/proof bytes changed and no new full historical certificate or Lean certification is asserted. A previous approval under round5-o1pld does not release this distinct inherited obligation.'}]
P=V.create_packet(R,{'kind':'mathematics','author_ids':Req['author_ids'],'inputs':list(Inputs.values()),'claims':Claims});(O/'dependency-review-packet.json').write_text(json.dumps(P,ensure_ascii=False,indent=2)+'\n');print(P['packet_sha256'],flush=True)
