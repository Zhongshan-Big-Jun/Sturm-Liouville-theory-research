from pathlib import Path
import hashlib,json,difflib,shutil
O=Path('/mnt/f/tools/sl-literature-absorption-20260923');R=Path('/mnt/f/LaTeX/BVE research');B=R/'literature/absorption-20260923/domains';A=R/'research/artifacts/literature-absorption-20260923/reviews/domains'
def sha(raw):return hashlib.sha256(raw).hexdigest()
# Preserve the exact first-review public inputs before replacing any active draft.
prov=json.loads((A/'provenance.json').read_text());frozen=[]
for row in prov['inputs']:
    if row['availability']=='PUBLIC_EXACT_INPUT':
        raw=(R/row['public_path']).read_bytes();assert sha(raw)==row['sha256']
        dst=A/'frozen-inputs'/row['input_path'];dst.parent.mkdir(parents=True,exist_ok=True)
        if dst.exists():assert dst.read_bytes()==raw
        else:dst.write_bytes(raw)
        frozen.append(dict(input_path=row['input_path'],sha256=row['sha256'],public_path=dst.relative_to(R).as_posix()))
(A/'frozen-input-map.json').write_text(json.dumps(dict(scope='Permanent first-review input locations; supersedes location-only pointers in provenance.json where an active draft was later corrected. The original hashes and native verdict are unchanged.',inputs=frozen),ensure_ascii=False,indent=2)+'\n')
Changes=[]
def change(rel,old,new):
    p=B/rel;raw=p.read_bytes();text=raw.decode();assert old in text,rel
    updated=text.replace(old,new);p.write_text(updated)
    Changes.append(dict(path=rel,before_sha256=sha(raw),after_sha256=sha(p.read_bytes()),diff=''.join(difflib.unified_diff(text.splitlines(True),updated.splitlines(True),fromfile='before/'+rel,tofile='after/'+rel))))
change('proofs/04-boundary-algebra-and-gkn-scope.md','The project eigenfunctions are affine, cosine and sine modes; the p_n are not eigenfunctions.','The project eigenfunctions are affine, cosine and sine modes. The affine members p_0=1 and p_1=x are c-eigenfunctions; the nonaffine named members p_n, n>=4, are not eigenfunctions.')
change('proofs/02-fractional-trace-dictionary.md','also arXiv:1412.3744v4 PDF p.3. That page was visually inspected.','also arXiv:1412.3744v4 PDF pp.3-4: Definition 2.1/Theorem 2.2 are on p.3, and Corollary 2.3/equation (2.7) on p.4. The source pages were visually inspected.')
change('notes/L03-source-to-claim.md','Its front page says online 27 October 2015; the publisher search record says 26 October. The publication year/volume/pages agree; this one-day online-date discrepancy is recorded without guessing a correction.','Its front page says online 27 October 2015. The earlier draft asserted a publisher-search date of 26 October, but the retained search evidence does not support that assertion; it is withdrawn. The journal year, volume and pages are confirmed by the primary PDF.')
p=B/'source-manifest.json';raw=p.read_bytes();obj=json.loads(raw)
for src in obj['sources']:
    if src.get('id')=='L03' or src.get('reference_id')=='L03':
        src['limitation']='The journal PDF states online 27 October 2015. The earlier publisher-search assertion of 26 October is unsupported by the retained search record and is withdrawn. Publication year 2016, volume 289(7), pages 831-844 are supported by the original. Original author manifest remains frozen in the first-review input archive.'
updated=json.dumps(obj,ensure_ascii=False,indent=2)+'\n';p.write_text(updated)
Changes.append(dict(path='source-manifest.json',before_sha256=sha(raw),after_sha256=sha(p.read_bytes())))
for p in sorted((B/'proposed-tool-cards').glob('*.json')):
    raw=p.read_bytes();card=json.loads(raw)
    for source in card['sources']:
        if 'path' in source and (B/source['path']).is_file():source['sha256']=sha((B/source['path']).read_bytes())
        if source.get('source_id')=='L03':source['locator']='Definition2.1/Theorem2.2 arXiv PDF p3; Corollary2.3/equation2.7 p4; author-posted journal p833 (PDF p4)'
    updated=(json.dumps(card,ensure_ascii=False,indent=2)+'\n').encode()
    if updated!=raw:
        p.write_bytes(updated);Changes.append(dict(path=p.relative_to(B).as_posix(),before_sha256=sha(raw),after_sha256=sha(updated)))
log=dict(schema='scoped-literature-correction/v1',original_verdict='CHANGES_REQUIRED',original_packet_sha256=prov['packet_sha256'],changes=Changes,scope='Affine exception and two bibliographic source assertions; no other analytic proof change. Exact original author drafts and review remain preserved.',next='Fresh stateless independent review required before card admission.')
(B/'corrections.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
# Build a new frozen project from the original packet, then overlay only revised own inputs.
spec=json.loads((O/'domains-review-spec.json').read_text());Q=O/'verification/domains2'
for row in spec['inputs']:
    rel=row['path'];src=B/rel
    if not src.is_file():src=O/'verification/domains'/rel
    dst=Q/rel;dst.parent.mkdir(parents=True,exist_ok=True);raw=src.read_bytes();dst.write_bytes(raw);row['sha256']=sha(raw)
for rel,src in [('prior-review/report.json',A/'runtime/report.json'),('corrections.json',B/'corrections.json')]:
    dst=Q/rel;dst.parent.mkdir(parents=True,exist_ok=True);raw=src.read_bytes();dst.write_bytes(raw);spec['inputs'].append(dict(path=rel,sha256=sha(raw),role='Actual first independent review and precise correction overlay; assess the revised originals yourself'))
spec['claims'].append(dict(id='P1-review-findings-closure',verification='analytic',statement='Verify first-review F1/F2 closure: p0 and p1 retained as c-eigenfunctions while n>=4 nonaffine members are not; Cor2.3/equation2.7 located at arXiv PDF p4, Def2.1/Thm2.2 at p3. Confirm journal PDF online27October2015 and withdrawal of unsupported search26 claim. Check all proposal proof hashes bind current exact inputs, without expanding approval to an entire source article.'))
(O/'domains2-review-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('Repaired',len(Changes),'active files; preserved original review and prepared',len(spec['inputs']),'fresh inputs.')
