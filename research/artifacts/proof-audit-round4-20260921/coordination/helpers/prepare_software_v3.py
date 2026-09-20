from pathlib import Path
import sys,json,shutil
Root=Path('/mnt/f/LaTeX/BVE research'); Out=Path('/mnt/f/tools/math-audit-round4-20260921');Art='research/artifacts/proof-audit-round4-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
Folder=Root/Art/'script-checks-revision3'; shutil.copytree(Out/'scripts-revision3',Folder)
Previous=json.loads((Out/'software-v2-review-dispatch.json').read_text())['bundle']
Inputs=[{'path':'scripts/d4_third_order_theory.py','role':'current-program'}, {'path':Previous+'/report.json','role':'actual-second-independent-rejection'}, {'path':Art+'/submitted/constructive_repairs.md','role':'original-coefficient-contract'}]
Inputs += [{'path':str(P.relative_to(Root)),'role':'actual-regression-and-execution-evidence'} for P in sorted(Folder.iterdir()) if P.is_file()]
Claims=[
	{'id':'R4-d4-v3-exact','verification':'software','statement':'Independently verify the entire current d4 program in its exact stated scope. In particular the two coefficient wrappers must preserve Python float binary-rational conversion (including 1.0 and0.1) just like coefficients, without changing existing SymPy expression semantics. Reduction must reject baselines provably zero (Float0, unevaluated Add(1,-1), unevaluated sin(pi)); unknown symbolic nonzeroness remains an explicit caller assumption. Verify the old c64 mixed integer/Fraction exact regression and the exact P/Q/R coefficients, four factorial solutions, beta identities, reduction signs/indexing, positive finite-terminal construction, normalization and failure exits. Add adversarial tests against the two observed defects and report remaining substantive bugs.'},
	{'id':'R4-d4-v3-execution','verification':'exact-computation','statement':'Re-execute the frozen program and behavior harness normally and under -O, using a disposable copied source root with AUDIT_SOURCE_ROOT and AUDIT_CHECK_OUTPUT set to disposable paths and PYTHONDONTWRITEBYTECODE=1. Check 36 current behavior cases,624 independent finite-mu comparisons and8 failure-exit injections. The previously rejected revisions remain historical; supplied first- and second-repair snapshots allow old-failure reproduction. No finite-precision output is an interval certificate, infinite limit proof or all-project test pass.'}
]
Packet=Review.create_packet(Root,{'kind':'mathematics','author_ids':['01a06f46-dd03-7c83-9267-32048412c359'],'inputs':Inputs,'claims':Claims})
(Out/'software-v3-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
print(Packet['packet_sha256'])
