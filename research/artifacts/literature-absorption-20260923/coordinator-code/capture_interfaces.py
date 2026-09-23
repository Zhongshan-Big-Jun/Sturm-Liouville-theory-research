from pathlib import Path
import sys,json
O=Path('/mnt/f/tools/sl-literature-absorption-20260923');B=O/'author-interfaces';Q=O/'source-cache'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
D=json.loads((B/'source-manifest.json').read_text());Rows=[]
for Id,Version,Title in [('L10','arXiv:2110.07434v1','Resolvent expansions for self-adjoint operators via boundary triplets'),('L11','arXiv:1105.3755v2','Sturm-Liouville operators with measure-valued coefficients')]:
    Reading=next(x for x in D['paper_reading_coverage'] if x['source_id']==Id+'-arxiv-pdf')
    Raw=B/'private/sources'/(Id+'-arxiv-pdf.pdf');Txt=B/'private/text'/(Id+'-arxiv-pdf.txt')
    Url=next(x['requested_url'] for x in D['retrievals'] if x['id']==Id+'-arxiv-pdf')
    Cap=L.capture_source(Q,Raw,Url,Version,Title,Txt,'author PyMuPDF extraction; exact method in author source manifest','primary',json.dumps(Reading,ensure_ascii=False),Reading['theorem_locators'])
    Probe=L.read_source(Q,Cap['source_id'],1,20)
    Rows.append(dict(id=Id,capture=Cap,read_probe=Probe,reading=Reading,raw_path=str(Raw),text_path=str(Txt)))
(O/'interfaces-capture-receipts.json').write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({r['id']:r['capture']['source_id'] for r in Rows}),flush=True)
