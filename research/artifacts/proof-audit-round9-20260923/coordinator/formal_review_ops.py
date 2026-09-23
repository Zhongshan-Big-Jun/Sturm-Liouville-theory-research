from pathlib import Path
import sys,json
O=Path('/mnt/f/tools/math-audit-round9-20260923');RootFile=sys.argv[3] if len(sys.argv)>3 else 'formal-review-root.json';R=Path(json.loads((O/RootFile).read_text())['project'])
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
Mode,Name=sys.argv[1:3]
def read(S):return json.loads((O/(Name+S+'.json')).read_text())
if Mode=='prepare':Result=V.create_packet(R,read('-spec'))
elif Mode=='dispatch':Result=V.record_dispatch(R,read('-packet')['packet'],read('-spawn'))
elif Mode=='receive':Result=V.receive_review(R,read('-dispatch')['bundle'],read('-completion')['result'])
elif Mode=='verify':Result=V.verify_review_bundle(R,read('-dispatch')['bundle'])
else:raise ValueError(Mode)
Suffix={'prepare':'packet','dispatch':'dispatch','receive':'received','verify':'verified'}[Mode]
(O/(Name+'-'+Suffix+'.json')).write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:Value for K,Value in Result.items() if K in ('verdict','packet_sha256','reviewer_id','bundle','state','trust')},ensure_ascii=False),flush=True)
