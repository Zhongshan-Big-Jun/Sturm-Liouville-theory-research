from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
# One actual native query for the full batch. A single token avoids noisy unrelated OR matches.
query=L.query_tools(R,'literature-absorption-20260923',limit=50)
(O/'retrieval-result.json').write_text(json.dumps(query,ensure_ascii=False,indent=2)+'\n')
new=[x for g in ['domains','approximation','interfaces'] for x in json.loads((O/(g+'-cards.json')).read_text())]
hits={r['location']:r for r in query['hits']}
for item in new:
    h=hits.get(item['location']);assert h and h['sha256']==item['sha256'] and h['reuse_allowed']
    assert any(n['state']=='CURRENT' for n in h['annotations'])
    assert all(x['binding_state']=='CURRENT' for typ in ['sources','evidence'] for x in h[typ] if x.get('path') or x.get('source_id'))
assert not query['changed_paths'] and query['verdict']=='RETRIEVAL_ONLY' and query['blocked']==1
print('Actual query returned all11 new tools with current evidence, sources and version-bound annotations.',flush=True)
