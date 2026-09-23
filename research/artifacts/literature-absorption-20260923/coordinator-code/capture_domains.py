from pathlib import Path
import sys,json,hashlib
O=Path('/mnt/f/tools/sl-literature-absorption-20260923');B=O/'author-domains';Q=O/'source-cache'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
D=json.loads((B/'source-manifest.json').read_text());Rows=[]
for S in D['sources']:
    Id=S['source_id'];C=next(x for x in S['captures'] if x['kind']=='pdf');Raw=B/C['raw_path'];Txt=B/C['extracted_path']
    if L.digest(Raw.read_bytes())!=C['sha256'] or L.digest(Txt.read_bytes())!=C['extracted_sha256']:raise RuntimeError('Source drift '+Id)
    Reading=dict(read=S['reading'],not_read=S['not_read'],visual=S['visual'],limitation=S['limitation'])
    Title=S['primary_arxiv_metadata']['citation_title'][0]
    Cap=L.capture_source(Q,Raw,C['requested_url'],S['version'],Title,Txt,C['extraction_tool'],'primary',json.dumps(Reading,ensure_ascii=False),S['reading'])
    Rows.append(dict(id=Id,capture=Cap,read_probe=L.read_source(Q,Cap['source_id'],1,20),reading=Reading,raw_path=str(Raw),text_path=str(Txt)))
# The separately inspected journal-version Grubb PDF remains a second exact source.
S=next(x for x in D['sources'] if x['source_id']=='L03');C=next(x for x in S['captures'] if x.get('raw_path')=='private-sources/L03/author-pdf.pdf')
Cap=L.capture_source(Q,B/C['raw_path'],C['requested_url'],'author-posted journal PDF','Grubb fractional boundary domains: journal version',B/'private-sources/L03/author-extracted.txt','PyMuPDF1.28.2','primary','Targeted original formula inspection: journal p833, definition2.1 theorem2.2 corollary2.3',['PDF4 / journal833'])
Rows.append(dict(id='L03-journal',capture=Cap,read_probe=L.read_source(Q,Cap['source_id'],1,10),raw_path=str(B/C['raw_path']),text_path=str(B/'private-sources/L03/author-extracted.txt')))
(O/'domains-capture-receipts.json').write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({r['id']:r['capture']['source_id'] for r in Rows}),flush=True)
