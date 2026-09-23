from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923');Q=O/'source-cache'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
Q.mkdir(exist_ok=True)
Rows=[]
for Id,File,Url,Title,Coverage,Locator in [
 ('L02','krein_sobolev_II_axioms_2025.pdf','https://doi.org/10.3390/axioms14020115','Krein–Sobolev Orthogonal Polynomials II','Actual primary PDF; full extraction, targeted reading of introduction/operator and section6','PDF pages1-2,9-10; equation25'),
 ('L12','willner1983.pdf','https://doi.org/10.1137/0513040','The Two-Dimensional Eigenvalue Range and Extremal Eigenvalue Problems','Actual primary PDF; full extraction, targeted reading pages1-5,9-11, no replay of section4 numerics','Print621-625,629-631; Theorems1-4; equations1.5,2.1,3.10')]:
    Cap=L.capture_source(Q,R/'papers'/File,Url,'journal-version',Title,O/'p0'/(Id+'-full.txt'),'PyMuPDF1.28.2 get_text(sort=True)','primary',Coverage,[Locator])
    Read=L.read_source(Q,Cap['source_id'],1,20)
    Rows.append(dict(id=Id,capture=Cap,actual_read_probe=Read))
Cap=L.capture_source(Q,O/'p0/L13-crossref.json','https://api.crossref.org/works/10.1016/j.jmaa.2022.126513','metadata retrieved2026-09-23','L13 publisher-deposited Crossref metadata ONLY',None,'UTF8 JSON metadata','primary','Bibliographic metadata only; not article text',['author,title,journal,volume,issue,article-number,DOI'])
Rows.append(dict(id='L13',capture=Cap,actual_read_probe=L.read_source(Q,Cap['source_id'],1,10)))
(O/'p0/capture-receipts.json').write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
Store=C.load_store(R);States,Problems=C.impact_states(R,Store)
(O/'impact-after-bibliography.json').write_text(json.dumps(dict(review_problems=Problems,blocked=[dict(location=k[0],sha256=k[1],state=s) for k,s in States.items() if not s['reuse_allowed']]),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(source_ids={r['id']:r['capture']['source_id'] for r in Rows},review_problems=len(Problems)),ensure_ascii=False),flush=True)
