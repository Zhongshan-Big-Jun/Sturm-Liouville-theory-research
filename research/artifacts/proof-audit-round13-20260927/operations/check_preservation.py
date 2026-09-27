from pathlib import Path
import hashlib,json,subprocess
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');B=json.loads((O/'baseline.json').read_text())
# Only deliberate current source/navigation/reading copies and derived library state.
Allowed=set('''AGENTS.md state/AGENTS_SESSION_LOG.md state/RESUME.md README.md research_map.md docs/research-guide.md literature/maps/FRONTIER.md scripts/README.md docs/.gitattributes scripts/.gitattributes index/tools.json tools/README.md research/library/corrections-journal.json research/library/card-bindings/catalog.json misc/e1_certgen.py misc/e1_cert_tables.py misc/e1_cert_ledger.json misc/e1_cert_tables.tex misc/rigid1d.py scripts/_gapn2_symmetry_recon.py scripts/_gapn2_jacobian_analytic.py scripts/_gapn2_jacobian_spectral.py scripts/_gapn2_half_problem_probe.py'''.split())
for Name in ['SL_gap_n1_O3a_phase_rigidity_proof','SL_spectral_topics_summary','SL_stability_moment_jump','SL_ratio_summary']:
 for Pattern in ['docs/'+Name+'.tex','docs/'+Name+'.pdf','docs/build/'+Name+'.pdf']:Allowed.add(Pattern)
for Name in ['rational-envelope-certificates','true-curve-region-decomposition','interval-dec-directed-rounding','helly-compactness','bang-bang','jump-stability']:Allowed.add('tools/'+Name+'.md')
Unexpected=[];Changed=[]
for Name,Sha in B['tracked'].items():
 P=R/Name;Now=hashlib.sha256(P.read_bytes()).hexdigest() if P.exists() else None
 if Now!=Sha:
  Changed.append(Name)
  if Name not in Allowed:Unexpected.append(Name)
UntrackedChanged=[]
for Name,Sha in B['untracked'].items():
 P=R/Name
 if not P.exists() or hashlib.sha256(P.read_bytes()).hexdigest()!=Sha:UntrackedChanged.append(Name)
Result=dict(tracked=len(B['tracked']),original_untracked=len(B['untracked']),changed_tracked=Changed,unexpected_tracked=Unexpected,changed_original_untracked=UntrackedChanged,allowed=sorted(Allowed))
(O/'preservation.json').write_text(json.dumps(Result,indent=2)+'\n')
print(json.dumps(Result,ensure_ascii=False))
raise SystemExit(1 if Unexpected or UntrackedChanged else 0)
