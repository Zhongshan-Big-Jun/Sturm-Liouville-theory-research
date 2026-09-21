from pathlib import Path
import hashlib,json,re,subprocess,sys,urllib.parse
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as V
B=json.loads((O/'baseline.json').read_text());protection=json.loads((O/'protection-result.json').read_text());lib=json.loads((O/'library-final.json').read_text())
def require(x,m):
	if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
require(protection['status']=='PASS' and lib['status']=='PASS','Final state not ready')
reviews={}
for n in ['math-review','certificate-review','formal-readback','formal-semantic','renewal-review','summary-review']:
	d=json.loads((O/(n+'-dispatch.json')).read_text());receipt=V.verify_review_bundle(R,d['bundle']);require(receipt['verdict']=='APPROVED','Review not approved '+n);reviews[n]={'bundle':d['bundle'],'reviewer_id':d['reviewer_id'],'packet_sha256':receipt['packet_sha256'],'verdict':receipt['verdict']}
for n,c in (lib['cards']|lib['unchanged_renewed_cards']).items():require(sha(R/c['location'])==c['sha256'],'Card changed after release '+n)
require(sha(R/'lean-proof/SL/AuditRound8.lean')=='3cbc7e84dab06ffdc2cc974a9d7553c47847eca4227e49024f04a1e91ccc486e','Formal source changed')
plugin=R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'
for n,h in json.loads((O/'source-verification.json').read_text())['plugin_sources'].items():require(sha(plugin/n)==h,'Plugin source changed '+n)
pattern=re.compile(r'(?<!!)\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)\)');checked=[]
names=[n for n in protection['authorized_changed_tracked'] if n.endswith('.md')]+['reports/proof-audit-round8-20260922/REPORT.md']
baseline_markdown=json.loads((O/'baseline-markdown.json').read_text())
for n in names:
	t=(R/n).read_text();old=baseline_markdown[n]['text'] if n in B['tracked'] else ''
	if n in B['tracked']:require(baseline_markdown[n]['sha256']==B['tracked'][n] and hashlib.sha256(old.encode()).hexdigest()==B['tracked'][n],'Baseline Markdown bytes differ '+n)
	oldlinks=set(pattern.findall(old))
	for link in set(pattern.findall(t))-oldlinks:
		link=link.strip('<>');target=urllib.parse.unquote(link.split('#',1)[0])
		if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
		p=(R/n).parent/target
		# This manifest is written immediately after this check and contains its own explicit exclusion.
		if target=='publication-manifest.json' and n=='reports/proof-audit-round8-20260922/REPORT.md':continue
		require(p.exists(),'Broken new link '+n+' -> '+link);checked.append({'source':n,'target':link})
maptext=(R/'research_map.md').read_text()
for required in ['| B4-INF-LIMIT |','B4I[','B4 -->|symmetric-well asymptotic subproblem| B4I']:require(required in maptext,'Map missing '+required)
require('第八轮修订' in (R/'README.md').read_text(),'README missing update');require('AuditRound8.lean' in (R/'lean-proof/STATUS.md').read_text(),'Formal status missing')
pdf_receipts=list((O/'pdf-build').glob('*/*/run.json'))
require(len(pdf_receipts)==3,'Expected three PDF build receipts')
for d in pdf_receipts:
	r=json.loads(d.read_text());require(r['exit_code']==0 and r['source_unchanged'],'PDF build failure');require(sha(R/r['source'])==r['source_sha256'],'PDF source changed');require(sha(R/r['source'].replace('.tex','.pdf'))==r['pdf_sha256'],'PDF differs from checked build')
result={'status':'PASS','new_links_checked':len(checked),'new_local_links':checked,'review_receipts':reviews,'current_cards_exact':True,'plugin_sources_unchanged':True,'canonical_modified':False,'pdf_source_and_output_hashes_match':True,'scope':'Current exact source-bound reviews, four changed-card releases and eighteen obligations renewed on eight unchanged cards with actual retrieval, changed Markdown links, map graph, PDF source/output identities and declared formal scope. Not all old links, all historical mathematics or full formalization.'}
(O/'final-document-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Final document check PASS',len(checked),'new links, six current reviews',flush=True)
