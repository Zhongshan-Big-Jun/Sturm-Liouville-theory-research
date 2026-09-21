from pathlib import Path
import sys,time,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round7-20260921')
if str(R.resolve())!='/mnt/f/LaTeX/BVE research':raise RuntimeError('Original dispatch path mapping differs')
Runtime=R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'
Expected=json.loads((R/'research/artifacts/proof-audit-round7-20260921/plugin-runtime.json').read_text())['used_plugin_sources']
for N,H in Expected.items():
 if hashlib.sha256((Runtime/N).read_bytes()).hexdigest()!=H:raise RuntimeError('Plugin source changed')
sys.path.insert(0,str(Runtime))
import research_review as V
Started=time.monotonic()
D=json.loads((O/'math-review-dispatch.json').read_text())
Result=V.verify_review_bundle(R,D['bundle'])
Prior=json.loads((O/'math-review-receipt.json').read_text())
if Result!=Prior:raise RuntimeError('Original WSL review result differs')
Seconds=time.monotonic()-Started
ModuleFiles={}
Private=O/'posix-native-probe/root/usr'
for Name,Module in list(sys.modules.items()):
 File=getattr(Module,'__file__',None)
 if not File or File.startswith('<'):continue
 P=Path(File).resolve()
 if not P.is_relative_to(Private) and not P.is_relative_to(Runtime) and P!=Path(__file__).resolve():raise RuntimeError('Unexpected imported file '+str(P))
 ModuleFiles[Name]=dict(path=str(P),sha256=hashlib.sha256(P.read_bytes()).hexdigest())
Record=dict(status='PASS',scope='Read-only same-path execution of unchanged review verifier; not a new mathematical review',
 python=sys.version,executable=sys.executable,executable_sha256=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
 project=str(R.resolve()),plugin_source_hashes=Expected,math_receipt_equal_to_original=True,packet_sha256=Result['packet_sha256'],
 checked_input_paths=len(Result['bindings']),read_only_verification_seconds=Seconds,modules=ModuleFiles,
 private_runtime_manifest='posix-native-probe/source.json',no_source_or_receipt_modification=True)
(O/'posix-native-probe/verification.json').write_text(json.dumps(Record,ensure_ascii=False,indent=2)+'\n')
print('Original review unchanged and fully reverified:',len(Result['bindings']),'inputs;',round(Seconds,3),'seconds')
