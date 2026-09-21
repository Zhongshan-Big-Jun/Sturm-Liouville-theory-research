from pathlib import Path
import hashlib
import json
import shutil
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round8-20260922')
Plugin = Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'
Expected = json.loads((Out/'source-verification.json').read_text())['plugin_sources']
for Name, Digest in Expected.items():
	if hashlib.sha256((Plugin/Name).read_bytes()).hexdigest() != Digest:
		raise RuntimeError('Plugin source changed')
sys.path.insert(0,str(Plugin))
import research_library as Library

Result = Library.capture_source(Root, Out/'literature/web-page-response.json', 'https://dlmf.nist.gov/4.22.E3', 'DLMF1.2.8; release2026-09-15; retrieved2026-09-22', 'NIST DLMF4.22.3 cotangent partial fractions', TextPath=Out/'literature/dlmf-equation-extract.md', method='Actual web-tool HTML parsed response plus explicitly transcribed equation excerpt; not raw HTML/TeX download', SourceKind='primary', Coverage='Equation4.22.3 and its excluded poles; no cited books read', Locators=['Section4.22 equation4.22.3'])
(Out/'literature/capture-result.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
Reading=Library.read_source(Root,Result['source_id'],StartLine=1,MaxLines=80)
(Out/'literature/read-result.json').write_text(json.dumps(Reading,ensure_ascii=False,indent=2)+'\n')
Target=Root/'research/artifacts/proof-audit-round8-20260922/literature'
Target.mkdir(exist_ok=True)
for File in (Out/'literature').iterdir():
	if File.is_file():
		Destination=Target/File.name
		if Destination.exists() and Destination.read_bytes()!=File.read_bytes():
			raise RuntimeError('Literature archive conflict')
		if not Destination.exists():
			shutil.copyfile(File,Destination)
print(json.dumps({'status':'CAPTURED_AND_READ','source_id':Result['source_id'],'next_offset':Reading['next_offset'],'scope':Result['coverage']}),flush=True)
