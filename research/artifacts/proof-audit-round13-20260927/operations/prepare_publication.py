from pathlib import Path
import hashlib,json,subprocess,collections
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927')
B=json.loads((O/'baseline.json').read_text());P=json.loads((O/'preservation.json').read_text())
if P['unexpected_tracked'] or P['changed_original_untracked']:raise RuntimeError('Protection failure')
if (R/'research/library/writer.lock').exists():raise RuntimeError('Library writer is still active')
if not (R/'reports/proof-audit-round13-20260927/verification.json').exists():raise RuntimeError('Final verification missing')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
if git('rev-parse','HEAD').decode().strip()!=B['head']:raise RuntimeError('Unexpected HEAD drift')
if git('diff','--cached','--name-only','-z'):raise RuntimeError('Existing staged work must be reconciled')
Changed=git('diff','--name-only','-z').decode().strip('\0').split('\0')
Changed=[n for n in Changed if n and n not in B['original_dirty']]
if set(Changed)-set(P['allowed']):raise RuntimeError('Unexpected tracked scope '+repr(set(Changed)-set(P['allowed'])))
New=git('ls-files','--others','--exclude-standard','-z').decode().strip('\0').split('\0')
New=[n for n in New if n and n not in B['untracked']]
Prefixes=['research/artifacts/proof-audit-round13-20260927/','reports/proof-audit-round13-20260927/','research/library/card-versions/','research/library/card-bindings/','research/library/corrections/','research/library/reviews/','research/library/index-history/','research/library/annotations/']
Extra={'misc/.gitattributes','misc/e1_certificate_io.py','misc/e1_cert_receive.py','misc/e1_cert_ledger.status.json','scripts/test_round13_certificates.py'}
Bad=[n for n in New if n not in Extra and not any(n.startswith(p) for p in Prefixes)]
if Bad:raise RuntimeError('Unassigned new paths '+repr(Bad))
Files=sorted(set(Changed+New))
if any(n in B['untracked'] or n in B['original_dirty'] for n in Files):raise RuntimeError('Original work would be staged')
Manifest={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in Files}
(O/'publication-manifest.json').write_text(json.dumps(dict(baseline=B['head'],files=Manifest),ensure_ascii=False,indent=2)+'\n')
(O/'publication-paths.nul').write_bytes(('\0'.join(Files)+'\0').encode())
print(json.dumps(dict(count=len(Files),bytes=sum((R/n).stat().st_size for n in Files),groups=dict(collections.Counter(n.split('/')[0] for n in Files))),ensure_ascii=False))
