from pathlib import Path
import hashlib,json,re,subprocess,datetime
from urllib.parse import unquote
O=Path('/mnt/f/tools/math-audit-round9-20260923');R=Path('/mnt/f/LaTeX/BVE research');A=R/'research/artifacts/proof-audit-round9-20260923';Checks=[]
def require(v,m):
    if not v:raise RuntimeError(m)
    Checks.append(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
Gate=read(A/'library-final-check.json');require(Gate['status']=='PASS' and Gate['available']==78 and Gate['blocked']==1,'Actual final library gate passed')
for n in ['math-review2','renewal-review','software-isolated-review2','formal-isolated-readback','formal-isolated-semantic']:
    d=read(O/(n+'-received.json'));require(d['verdict']=='APPROVED','Received independent approval '+n)
    spawn=read(O/(n+'-spawn.json'));s=json.dumps(spawn);require('fork_context' in s and ': false' in s,'Actual fresh-session provenance '+n)
for row in Gate['checked_current_cards']:require(sha(R/row['path'])==row['sha256'],'Current exact card '+row['path'])
expected=read(O/'stage-expected-sha256.json')
for n,h in expected.items():require(sha(R/n)==h,'Frozen publication bytes '+n)
Report=R/'reports/proof-audit-round9-20260923/REPORT.md';Text=Report.read_text()
require(not re.search('仍在验收中|验收进行中|待完成后|将在完成后补齐|候选仍须',Text),'Report has no stale pending acceptance')
require('O1/O2' in Text and '全局' in Text and '不覆盖' in Text,'Report preserves mathematical/formal boundaries')
Links=[]
for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',Text):
    link=match.group(1).strip().strip('<>')
    if '://' in link or link.startswith('#'):continue
    target=(Report.parent/unquote(link.split('#')[0])).resolve();require(target.exists(),'Report link exists '+link);Links.append(link)
require('第九轮审计修缮 (研究与验收完成)' in (R/'AGENTS.md').read_text(),'Root AGENTS updated')
require('ninth-round audit repair completed' in (R/'state/RESUME.md').read_text()[:4000],'Current resume updated')
require('round9 final independent acceptance' in (R/'state/AGENTS_SESSION_LOG.md').read_text(),'Append-only session log updated')
Map=(R/'research_map.md').read_text();require('| B3-CANDIDATE-LIMIT |' in Map and '| B3 |' in Map and '| PARTIAL |' in Map.split('| B3 |',1)[1].splitlines()[0],'Map separates solved candidate from global problem')
Status=(R/'lean-proof/STATUS.md').read_text().split('## 2026-09-22',1)[0]
require('APPROVED' in Status and '验收进行中' not in Status and '未形式化' in Status,'Lean status distinguishes acceptance and analytic gaps')
Manifest=read(A/'coordinator/manifest.json')
for x in Manifest['files']:require(sha(A/'coordinator'/x['path'])==x['sha256'],'Coordinator archive identity '+x['path'])
S=read(A/'software-final-integration.json');require(S['exit_code']==0 and S['numerical_payload_identical_to_accepted_candidate'] and sha(R/'scripts/_gapn2_second_variation_probe.py')==S['accepted_new_sha256'],'Live program is exact independently accepted version and ran successfully')
require(sha(R/'lean-proof/SL/AuditRound9.lean')=='0668291e3ac37f2608483b009e4b5726fc9cd3deeb89849e0da8cc8c60ebd208','Live Lean source is exact reviewed source')
Active=['AGENTS.md','README.md','README_EN.md','PROJECT.md','research_map.md','docs/PROJECT_UNDERSTANDING.md','docs/research-guide.md','state/RESUME.md','lean-proof/STATUS.md','tools/README.md','scripts/README.md','scripts/_gapn2_second_variation_probe.py','scripts/_gapn2_k_global_rank2.py']
p=subprocess.run(['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--check','--',*Active],cwd=R,capture_output=True,text=True)
require(p.returncode==0,'Changed active files whitespace check '+p.stdout+p.stderr)
Result=dict(status='PASS',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=len(Checks),local_report_links=len(Links),publication_paths=len(expected),mathematical_boundary='B3 balanced candidate solved; global O1/O2 and G1 remain open; local Lean only',whitespace_command=p.args,checks_detail=Checks)
(O/'final-document-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('Final documents and exact artifact identities PASS',len(Checks),'checks,',len(Links),'report links')
