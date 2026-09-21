from pathlib import Path
import hashlib,json,re,subprocess,sys,urllib.parse
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round5-20260921')
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
Names=['AGENTS.md','README.md','README_EN.md','docs/PROJECT_UNDERSTANDING.md','docs/research-guide.md','research_map.md','lean-proof/STATUS.md','state/RESUME.md','state/AGENTS_SESSION_LOG.md','tools/README.md','tools/leftdef-o1pld-l2-structural.md','index/tools.json','research/library/card-bindings/catalog.json','research/library/corrections-journal.json']
Report='reports/proof-audit-round5-20260921/REPORT.md'
Text=(R/Report).read_text()
assert '<!--' not in Text,'Unfilled report placeholders'
assert '当前状态: 两项审计发现已修复' in Text
assert '独立执行报告' in Text and 'INCOMPLETE' in Text
assert '第五轮审计修缮 (本轮完成)' in (R/'AGENTS.md').read_text()
assert 'fifth-round audit repair completed' in (R/'state/RESUME.md').read_text()
subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check','--',*Names],cwd=R,check=True)
# Only new/changed navigation links: old unrelated broken links are not silently rewritten.
Checked=[]
for Name in [*Names,Report]:
 if not Name.endswith('.md'):continue
 if Name==Report:Content=(R/Name).read_text()
 else:
  Diff=subprocess.check_output(['git','diff','--unified=0','--',Name],cwd=R,text=True)
  Content='\n'.join(L[1:] for L in Diff.splitlines() if L.startswith('+') and not L.startswith('+++'))
 for Target in re.findall(r'\]\(([^)]+)\)',Content):
  if Target.startswith(('https://','http://','mailto:','#','codex:')):continue
  Target=Target.strip('<>');Target=urllib.parse.unquote(Target.split('#')[0])
  if not Target:continue
  Target=(R/Name).parent/Target
  assert Target.exists(),('missing new navigation target',Name,str(Target))
  Checked.append({'from':Name,'target':str(Target.relative_to(R))})
Expected={'docs/SL_cofinite_left_definite.tex':'ed07e47fd370a9db3b6a6a2d125d9eec996288e53a6024a0e9fb533ca1b3c0bb','docs/SL_cofinite_left_definite.pdf':'83ac21d78656e90e36fb37de0980019c40ace47e25c08f977b5216f96ab31056','lean-proof/SL/AuditRound5.lean':'035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45','tools/leftdef-o1pld-l2-structural.md':'f7fb9661112adbc744be991b923e39b9bd6bedec4dbbb89ced1cbc36962e7430'}
for Name,ExpectedHash in Expected.items():
 assert hashlib.sha256((R/Name).read_bytes()).hexdigest()==ExpectedHash,Name
Receipts={}
for Name in ['mathematics','dependency-v2','readback','semantic-v2','dependency','semantic']:
 Dispatch=json.loads((O/(Name+'-review-dispatch.json')).read_text());CheckedReview=Review.verify_review_bundle(R,Dispatch['bundle'])
 ExpectedVerdict='INCOMPLETE' if Name in ['dependency','semantic'] else 'APPROVED'
 assert CheckedReview['verdict']==ExpectedVerdict,(Name,CheckedReview)
 Receipts[Name]={'bundle':Dispatch['bundle'],'verdict':CheckedReview['verdict']}
Result={'status':'PASS','scope':'New navigation, final report status, immutable new source/PDF/card identities and actual review-bundle integrity; no new mathematical or full-project test is claimed.','new_links_checked':len(Checked),'links':Checked,'source_hashes':Expected,'review_receipts':Receipts}
(O/'final-document-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('Final documents PASS:',len(Checked),'new links,',len(Receipts),'actual review bundles')
