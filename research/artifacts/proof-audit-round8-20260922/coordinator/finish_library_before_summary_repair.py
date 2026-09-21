from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
import research_corrections as C
import research_review as V
done=json.loads((O/'release-results.json').read_text());cards=json.loads((O/'cards.json').read_text())
if len(done)!=4 or len(cards)!=4 or any(x['result']['verdict']!='RELEASED' for x in done):raise RuntimeError('Incomplete releases')
renewed=json.loads((O/'renewal-release-results.json').read_text())
renewal_bundle=json.loads((O/'renewal-review-dispatch.json').read_text())['bundle']
if len(renewed)!=18 or V.verify_review_bundle(R,renewal_bundle)['verdict']!='APPROVED':raise RuntimeError('Incomplete renewal')
renewals={x['old_release']:x for x in renewed}
unchanged={x['target']['location']:x['target'] for x in renewed}
notes=json.loads((O/'annotations.json').read_text()) if (O/'annotations.json').exists() else {}
texts={
'inf-limit-comparison':'第八轮研究经验: 将实际射击向量的辐角连续展开, 先识别半区间基态, 再控制相位速度与第一频率, 可以覆盖完整连续薄层域. 本三层对称阱获得全R>=1的统一谱隙下界, 使T1不再依赖高精度T3数值. 迁移到更多层或其它边界条件仅为待证想法, 必须重新识别模式及界面变换. 固定u的1/R展开加全域下界才推出最优值O(1/R), 不能推出精确优化系数或参数速度. 当前证明/独立验收/局部Lean指针见第八轮报告.',
'cot-series-certificate':'第八轮纠错经验: 普通超越函数值加一次nextafter不能当作严格区间; 必须有已证明误差包络或可验证的精确算术构造. Laurent下标、紧区间一致收敛与极点排除是工具契约的一部分. 本次实际读取NIST DLMF4.22.3公式和极点条件, source_id保存真实工具响应及明确转录, 不宣称读取其引用书籍. 细常数可复用, 但新的A-doubleprime主链只需要初等粗界.'}
for name,text in texts.items():
    if name in notes:continue
    c=cards[name];notes[name]=L.annotate(R,c['location'],c['sha256'],author='coordinator-20260922-round8',kind='observation',locator='Round8 continuous phase proof, exact scalar certificate and isolated review',text=text)
    (O/'annotations.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
index=L.make_index(R);(O/'index-result.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
query=L.query_tools(R,' '.join(list(cards)+list(unchanged)),limit=50);(O/'final-query-result.json').write_text(json.dumps(query,ensure_ascii=False,indent=2)+'\n')
hits={h['location']:h for h in query['hits']}
for c in list(cards.values())+list(unchanged.values()):
    if c['location'] not in hits or not hits[c['location']]['reuse_allowed'] or hits[c['location']]['sha256']!=c['sha256']:raise RuntimeError('Current card still blocked '+c['location'])
    f,_,_=L.read_metadata((R/c['location']).read_bytes())
    if not f.get('summary') or hits[c['location']]['summary']!=f['summary'][:500]:raise RuntimeError('Stale summary '+c['location'])
current=json.loads((R/'index/tools.json').read_text())
if len(current['items'])!=78 or len(current['blocked_items'])!=1 or current['blocked_items'][0]['location']!='tools/left-definite-orthogonal-systems.md':raise RuntimeError('Unexpected final retrieval state')
active={x['location']:x for x in current['items']};store=C.load_store(R);classified=[]
initial={p['release'] for p in json.loads((O/'initial-impact.json').read_text())['problems']}
for problem in query['issues']:
    if problem.get('status')!='REVIEW_NO_LONGER_VALID' or problem['release'] not in initial|set(renewals):raise RuntimeError('Unexpected stale review '+str(problem))
    release=store['requests'][problem['release']]['payload'];rev=store['requests'][release['revision']]['payload'];loc=rev['new']['location']
    if loc not in active or not active[loc]['reuse_allowed']:raise RuntimeError('Unresolved current version '+loc)
    latest=[e['request'] for e in store['events'] if store['requests'][e['request']]['kind']=='revision' and store['requests'][e['request']]['payload']['issue']==rev['issue'] and store['requests'][e['request']]['payload']['new']['location']==loc][-1]
    classification='SUPERSEDED_HISTORICAL_REVISION'
    if latest==release['revision']:
        renewal=renewals.get(problem['release'])
        if not renewal or renewal['revision']!=latest or renewal['bundle']!=renewal_bundle:raise RuntimeError('Latest review invalid without exact renewal '+loc)
        request=store['requests'][renewal['result']['request_id']]
        if request['kind']!='release' or request['payload']['revision']!=latest or request['payload']['bundle']!=renewal_bundle:raise RuntimeError('Renewal receipt mismatch '+loc)
        classification='SAME_REVISION_WITH_NEW_APPROVED_REVIEW'
    classified.append(dict(problem,location=loc,classification=classification,current_revision=latest))
if {p['release'] for p in classified}!=initial|set(renewals):raise RuntimeError('Historical warnings unexpectedly lost')
result=dict(status='PASS',available_cards=78,blocked_cards=1,cards=cards,unchanged_renewed_cards=unchanged,versions=len(store['nodes']),correction_events=len(store['events']),current_reviewed_obligations=22,distinct_current_cards=12,release_results=done,renewal_release_results=renewed,historical_superseded_review_warnings=classified,distinct_historical_warning_releases=len({p['release'] for p in classified}),annotations=notes,canonical_modified=False,default_query_verdict=query['verdict'])
for p in [O/'library-final.json',A/'library-final.json']:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(A/'default-query.json').write_text(json.dumps(query,ensure_ascii=False,indent=2)+'\n')
print('Actual library query PASS:',len(current['items']),'available,',len(current['blocked_items']),'blocked;',len(store['nodes']),'versions;',len(store['events']),'events',flush=True)
