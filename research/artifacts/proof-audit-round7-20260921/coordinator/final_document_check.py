from pathlib import Path
import hashlib,json,re,subprocess,sys,urllib.parse
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round7-20260921');A=R/'research/artifacts/proof-audit-round7-20260921'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as V
B=json.loads((O/'baseline.json').read_text());Protection=json.loads((O/'protection-result.json').read_text());Library=json.loads((O/'library-final.json').read_text())
if Protection['status']!='PASS' or Library['status']!='PASS':raise RuntimeError('Final protection/library checks missing')
Reviews={}
for Name in ['math','formal-v2','propagation']:
 D=json.loads((O/(Name+'-review-dispatch.json')).read_text());Receipt=V.verify_review_bundle(R,D['bundle'])
 if Receipt['verdict']!='APPROVED':raise RuntimeError('Review not approved '+Name)
 Reviews[Name]=dict(bundle=D['bundle'],reviewer_id=D['reviewer_id'],verdict=Receipt['verdict'])
Software=json.loads((O/'software-review-v2/REVIEW.json').read_text())
if Software['verdict']!='APPROVED':raise RuntimeError('Software review not approved')
S=json.loads((O/'software-review-v2/PACKET.json').read_text())
if Software['packet_sha256']!=hashlib.sha256((O/'software-review-v2/PACKET.json').read_bytes()).hexdigest():raise RuntimeError('Software review packet identity differs')
for Name,H in S['files'].items():
 if hashlib.sha256((O/'software-review-v2'/Name).read_bytes()).hexdigest()!=H:raise RuntimeError('Software input changed '+Name)
for Name,H in S['files'].items():
 if Name.startswith('candidates/scripts/'):
  Current=R/Name.removeprefix('candidates/')
  if hashlib.sha256(Current.read_bytes()).hexdigest()!=H:raise RuntimeError('Reviewed software source differs from live source '+str(Current))
for Name,Data in Library['cards'].items():
 if hashlib.sha256((R/Data['location']).read_bytes()).hexdigest()!=Data['sha256']:raise RuntimeError('Current card identity differs '+Name)
Plugin=json.loads((A/'plugin-runtime.json').read_text());Runtime=R/Plugin['checkout']/'plugins/manage-math-research-program/skills/manage-math-research-program/scripts'
for N,H in Plugin['used_plugin_sources'].items():
 if hashlib.sha256((Runtime/N).read_bytes()).hexdigest()!=H:raise RuntimeError('Plugin runtime changed '+N)
Pattern=re.compile(r'(?<!!)\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)\)')
Names=[N for N in Protection['authorized_changed_tracked'] if N.endswith('.md')]+['reports/proof-audit-round7-20260921/REPORT.md']
Checked=[]
for Name in Names:
 T=(R/Name).read_text();Old=subprocess.check_output(['git','show',B['head']+':'+Name],cwd=R).decode() if Name in B['tracked'] else ''
 OldLinks=set(Pattern.findall(Old))
 for Link in set(Pattern.findall(T))-OldLinks:
  Link=Link.strip('<>');Target=urllib.parse.unquote(Link.split('#',1)[0])
  if not Target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',Target):continue
  P=(R/Name).parent/Target
  if not P.exists():raise RuntimeError('Broken new link '+Name+' -> '+Link)
  Checked.append(dict(source=Name,target=Link))
Map=(R/'research_map.md').read_text();Readme=(R/'README.md').read_text();Status=(R/'lean-proof/STATUS.md').read_text()
for Required in ['| B4-SUP-LIMIT |','B4L[','B4 -->|solved asymptotic subproblem| B4L']:
 if Required not in Map:raise RuntimeError('Missing map update '+Required)
if '第七轮修订' not in Readme or 'AuditRound7.lean' not in Status:raise RuntimeError('Current navigation missing')
Result=dict(status='PASS',new_links_checked=len(Checked),new_local_links=Checked,review_receipts=Reviews,software_review='APPROVED; input hashes rechecked',current_cards_exact=True,plugin_sources_unchanged=True,canonical_modified=False,scope='Current source-bound reviews, five released card identities, new active Markdown links, human map graph and formal scope. Not a re-audit of all historical mathematics or old links.')
(O/'final-document-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('Final document check PASS',len(Checked),'new local links',flush=True)
