from pathlib import Path
import json,hashlib,gzip
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
def sha(B):return hashlib.sha256(B).hexdigest()
Results=[]
for Name in ['execution-archive-manifest.json','formal-execution-archive-manifest.json','delivery-evidence-manifest.json']:
    Data=(A/Name).read_bytes();Rows=json.loads(Data)['files'];Compressed=0
    for Row in Rows:
        P=(A/Row['path']).resolve()
        if not P.is_relative_to(A.resolve()):raise RuntimeError('Archive path escapes artifact root')
        B=P.read_bytes()
        if sha(B)!=Row['sha256'] or len(B)!=Row['bytes']:raise RuntimeError('Archived bytes differ: '+str(P))
        if Row.get('encoding')=='gzip':
            Original=gzip.decompress(B)
            if sha(Original)!=Row['original_sha256'] or len(Original)!=Row['original_bytes']:raise RuntimeError('Lossless archive identity differs: '+str(P))
            Compressed+=1
    Results.append(dict(manifest=Name,sha256=sha(Data),verified_entries=len(Rows),lossless_gzip_entries=Compressed))
D=dict(status='PASS',scope='Archived byte identities and lossless decompression only; not additional scientific validation.',manifests=Results)
(O/'evidence-archive-verification.json').write_text(json.dumps(D,indent=2)+'\n')
(A/'integration/evidence-archive-verification.json').write_bytes((O/'evidence-archive-verification.json').read_bytes())
print('Evidence archive verification PASS',sum(X['verified_entries'] for X in Results),'manifest entries')
