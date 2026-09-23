from pathlib import Path
import re,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923')
paths=['AGENTS.md','README.md','README_EN.md','research_map.md','docs/PROJECT_UNDERSTANDING.md','docs/research-guide.md','tools/README.md','literature/maps/PAPER_MAP.md','literature/maps/FRONTIER.md','literature/absorption-20260923/README.md','literature/absorption-20260923/SOURCE_TABLE.md','literature/absorption-20260923/tasks/P0-P4.md','reports/literature-absorption-20260923/REPORT.md']
rows=[];bad=[];links=0;deferred=[]
for rel in paths:
    p=R/rel;raw=p.read_bytes();text=raw.decode()
    for m in re.finditer(r'\]\((<?[^)\n]+>?)\)',text):
        link=m[1].strip('<>').split('#')[0]
        if not link or re.match(r'[a-zA-Z]+:',link):continue
        target=(p.parent/link).resolve();links+=1
        if target==R/'reports/literature-absorption-20260923/publication-manifest.json':
            deferred.append(dict(path=target.relative_to(R).as_posix(),verification='Generated and verified by exact publication prepare/stage before committing.'))
        elif not target.exists():bad.append(dict(file=rel,link=link))
    rows.append(dict(path=rel,sha256=hashlib.sha256(raw).hexdigest()))
if bad:raise RuntimeError('Broken active navigation '+json.dumps(bad,ensure_ascii=False))
text=(R/'research_map.md').read_text()
for Id in ['A8','A9','A10','A11','B7']:
    assert len(re.findall(r'^\| '+Id+r' \|',text,re.M))==1,Id
assert '| B6' in text and '\n\n| B7' not in text
assert 'SOLVED' in next(l for l in text.splitlines() if l.startswith('| A8 |'))
assert 'PARTIAL' in next(l for l in text.splitlines() if l.startswith('| A11 |'))
assert 'O1/O2' in text and 'G1' in text
cat=json.loads((R/'literature/absorption-20260923/source-catalog.json').read_text());assert len(cat['sources'])==13 and cat['full_original_count']==12 and cat['metadata_incomplete_count']==1
idx=json.loads((R/'index/tools.json').read_text());assert len(idx['items'])==89 and len(idx['blocked_items'])==1
checkpoint=json.loads((O/'checkpoint-result.json').read_text());cp=json.loads(Path(checkpoint['snapshot']).read_text());assert hashlib.sha256((R/cp['progress']).read_bytes()).hexdigest()==cp['progress_sha256']
for name,info in cp['inputs'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==info['sha256'],name
result=dict(status='PASS',scope='Current navigation, declared literature limits, map nodes, actual existing index counts and exact new checkpoint hashes. No additional mathematical or formal certification.',files=rows,local_links_checked=links,broken_links=bad,publication_manifest_deferred_to_exact_stage=deferred,checkpoint=checkpoint['sha256'],checkpoint_inputs=len(cp['inputs']))
(O/'final-document-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(R/'reports/literature-absorption-20260923/final-document-check.json').write_bytes((O/'final-document-check.json').read_bytes())
print('Navigation/checkpoint PASS:',len(rows),'documents,',links,'local links,',len(cp['inputs']),'bound inputs; manifest checked at exact stage.')
