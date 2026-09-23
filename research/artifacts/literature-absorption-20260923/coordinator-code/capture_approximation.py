from pathlib import Path
import sys,json
O=Path('/mnt/f/tools/sl-literature-absorption-20260923');B=O/'author-approximation';Q=O/'source-cache'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
S=json.loads((B/'source-manifest.json').read_text());Titles={'L07':'The Full Muntz Theorem in Lp[0,1] for0<p<infinity','L08':'Efficient Spectral-Galerkin Method I','L09':'Frames and Numerical Approximation'};Rows=[]
for s in S['primary_sources']:
    if 'reference_id' not in s:continue
    Id=s['reference_id'];Raw=B/s['raw_path'];Txt=B/s['text_path']
    if L.digest(Raw.read_bytes())!=s['raw_sha256'] or L.digest(Txt.read_bytes())!=s['text_sha256']:raise RuntimeError('Source drift '+Id)
    Locators=[f"PDF{x['pdf_pages']}: "+'; '.join(x['locators']) for x in s['read_segments']]
    Reading=dict(read_segments=s['read_segments'],not_read=s['not_read'],visual=s['visually_inspected_pages'])
    Cap=L.capture_source(Q,Raw,s['requested_url'],s['version'],Titles[Id],Txt,s['extraction'],'primary',json.dumps(Reading,ensure_ascii=False),Locators)
    Rows.append(dict(id=Id,capture=Cap,read_probe=L.read_source(Q,Cap['source_id'],1,20),reading=Reading,raw_path=str(Raw),text_path=str(Txt)))
(O/'approximation-capture-receipts.json').write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({r['id']:r['capture']['source_id'] for r in Rows}),flush=True)
