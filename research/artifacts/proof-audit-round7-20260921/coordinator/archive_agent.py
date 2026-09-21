"""Losslessly archive completed scoped evidence; retain raw-path identities."""
from pathlib import Path
import gzip,hashlib,json,shutil,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round7-20260921')
Name=sys.argv[1];Source=O/Name;Dest=R/'research/artifacts/proof-audit-round7-20260921'/Name
if not (O/'receipts'/(Name+'-completion.json')).is_file():raise RuntimeError('Native completion required')
if (Dest/'archive-manifest.json').exists():raise RuntimeError('Archive already frozen')
Dest.mkdir(parents=True,exist_ok=True)
def digest(P):
 with P.open('rb') as F:return hashlib.file_digest(F,'sha256').hexdigest()
def save(P,D):P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
Rows=[];Stored={};Excluded=[]
for P in sorted(Source.rglob('*')):
 if not P.is_file():continue
 Rel=P.relative_to(Source)
 if '__pycache__' in Rel.parts or P.suffix=='.pyc':continue
 Hash=digest(P);Size=P.stat().st_size
 if P.name=='tools-AGENTS.md':
  Excluded.append(dict(original_relative_path=str(Rel),sha256=Hash,bytes=Size,reason='Unrelated private F:/tools workspace instructions, not executed by the regression; retained locally, not published.'))
  continue
 if Hash in Stored:Entry=dict(Stored[Hash],original_relative_path=str(Rel),deduplicated=True)
 else:
  Q=Dest/Rel
  if P.suffix in ['.olean','.ilean','.ir','.private','.server']:Q=Q.with_name(Q.name+'.bin')
  Compress=Size>1_000_000
  if Compress:Q=Q.with_name(Q.name+'.gz')
  Q.parent.mkdir(parents=True,exist_ok=True)
  if Q.exists():
   if Compress:raise RuntimeError('Unexpected existing compressed archive')
   if digest(Q)!=Hash:raise RuntimeError('Existing archive bytes differ '+str(Q))
  elif Compress:
   with P.open('rb') as Input,Q.open('xb') as Output,gzip.GzipFile(filename='',mode='wb',fileobj=Output,mtime=0) as Zip:shutil.copyfileobj(Input,Zip)
  else:shutil.copyfile(P,Q)
  if Compress:
   with gzip.open(Q,'rb') as F:
    if hashlib.file_digest(F,'sha256').hexdigest()!=Hash:raise RuntimeError('Compression mismatch')
  if digest(P)!=Hash:raise RuntimeError('Source changed during archive')
  Entry=dict(original_relative_path=str(Rel),archived_relative_path=str(Q.relative_to(Dest)),encoding='gzip' if Compress else 'identity',original_sha256=Hash,original_bytes=Size,stored_sha256=digest(Q),stored_bytes=Q.stat().st_size,deduplicated=False)
  Stored[Hash]=Entry
 Rows.append(Entry)
for P in sorted((O/'receipts').glob(Name+'-*.json')):
 Q=Dest/'native-tool-records'/P.name;Q.parent.mkdir(exist_ok=True);shutil.copyfile(P,Q)
Manifests=[]
for P in sorted(Source.rglob('run-manifest.json')):
 Hash=digest(P)
 if Hash in [X['raw_sha256'] for X in Manifests]:continue
 J=json.loads(P.read_text());T=J.get('target',{});Omit=['dependencies','expected_statement','imported_modules','semantic_dependencies','semantic_modules','import_artifacts','definition_hashes','type_expression']
 Compact={K:V for K,V in J.items() if K!='target'};Compact['target']={K:V for K,V in T.items() if K not in Omit}
 Compact['raw_evidence']=dict(source_relative_path=str(P.relative_to(Source)),raw_sha256=Hash,storage=Stored[Hash],omitted_from_this_index_only=Omit,note='Derived readable index only; complete raw receipt is losslessly retained in the mapped archive.')
 Q=Dest/'receipt-indexes'/(str(P.relative_to(Source)).replace('/','__')+'.compact.json');Q.parent.mkdir(exist_ok=True);save(Q,Compact)
 Manifests.append(dict(path=str(Q.relative_to(Dest)),raw_sha256=Hash))
save(Dest/'archive-manifest.json',dict(source_directory=str(Source),role=Name,files=Rows,excluded_context_only=Excluded,receipt_indexes=Manifests,logical_bytes=sum(X['original_bytes'] for X in Rows),unique_stored_bytes=sum(X['stored_bytes'] for X in Stored.values()),deduplication='Identical payloads stored once; every original relative path retains identity and mapping.'))
(Dest/'ARCHIVE.md').write_text('''# Exact scoped evidence archive

`archive-manifest.json` maps original relative paths to unchanged payloads. Verify stored SHA256, decompress deterministic gzip if marked, then verify original SHA256 and size. Large full Lean receipts and failed/interrupted attempts are retained. Readable `receipt-indexes` omit large fields only in the derived index; the full raw receipt remains available. Compiled objects use `.bin` to keep them out of live import search. Original absolute run paths are preserved rather than rewritten.

Native tool records are actual coordinator-recorded calls/results, not cryptographic service attestations. Author checks, independent execution and semantic approval are distinct. For replay, materialize the mapped payloads in a separate directory and use the frozen runtime configuration. Pinned Windows compiler/Mathlib binaries remain external inputs.

`excluded_context_only`, when nonempty, lists unrelated private workspace instructions by hash; these are retained locally and were never used as executable regression dependencies. They are deliberately not published. This exclusion does not remove mathematical source, executed program, command log or compiler receipt. Archive paths are not proof of a mathematical claim.
''')
print(Name,len(Rows),'mapped paths',len(Excluded),'context-only omissions',sum(X['stored_bytes'] for X in Stored.values()),'unique stored bytes',flush=True)
