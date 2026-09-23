from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
catalog=json.loads((R/'literature/absorption-20260923/source-catalog.json').read_text());sources={r['id']:r['public_note_capture']['source_id'] for r in catalog['sources']}
rows=[
('krein-boundary-right-inverses','L04','scope-check','秩、缺陷指数和各向同性是不同义务。这里只把有限边界右逆与解析逼近结合，不以满秩断言任意受约束族稠密。L04的v1奇异Legendre例子未直接导入。'),
('krein-fractional-trace-dictionary','L03','research-lead','后续可固定s=5/2检查删除p4的闭包；二阶中心点迹在临界阶不连续，不能照搬s=3。全区间Neumann/移位Robin桥接是当前引用的关键前提。'),
('krein-parity-unitary','L05','scope-check','复用时同时核对系数与实际算子域的反射不变性，并保留sqrt2归一化；只有系数对称不足以传输幂域。'),
('krein-s3-cofinite-three-traces','L02','cross-result','本轮新结果补充既有s=2两迹分类：s=3删除p4使闭包满足f″(0)=0，删除p5无影响。这里是余有限指定指标族，不能自动改成任意闭空间或无限删项分类。'),
('finite-synthesis-tsvd','L09','implementation-lead','若实现Galerkin/TSVD，先说明截断对象：Gram阈值epsilon与合成奇异值tau满足epsilon=tau²。下一步把实际求积导致的矩误差放入已有噪声界，尚无本轮离散求积认证。'),
('krein-integrated-legendre-riesz','L08','research-lead','积分高模态加有限低阶提升提供新坐标。解析Riesz界对次数一致但固定c>0；后续可测试参数缩放是否改善c趋零退化，当前未证。'),
('full-muntz-krein-moment-interface','L07','scope-check','扩大单项式空间非稠密可推出差分像族非稠密；反向需要额外结构。矩序列必须实现为真实L2向量，不能跨缺项继续递推。'),
('krein-infinite-deletion-subclasses','L07','research-lead','等差型正结果与倒数和有限负结果由不同机制证明。下一步可选两支倒数和发散但不含完整等差数列的明确集合；本卡没有一般充要判据。'),
('finite-interface-second-derivative','L10','scope-check','每次迁移核对坐标、归一化及加速度；即使路径对接口位置是仿射，几何对角项仍在。公式本身不决定约束切空间上的全局符号。'),
('fixed-operator-boundary-extension-check','L10','research-lead','直接应用L10前须找到固定对称算子、固定Hilbert空间和C²扩张路径。当前项目有限界面定理是另证结果，不伪装为该文主定理的自动推论。'),
('measure-weight-atoms-and-concentration','L11','scope-check','delta是测度，delta-prime不是有限Radon测度；固定Green核的集中极限与移动核的可微性分开，碰撞与极限换序未在本轮证明。'),
('leftdef-o1pld-l2-structural','L02','cross-result','2026-09-23新工具krein-s3-cofinite-three-traces已补出固定c>0的s=3余有限三迹闭包；本旧卡的s=2证据范围不扩大。无限删项仅新增明确等差/快速稀疏子类。'),
('spectral-domain-checks','L03','cross-result','新增分数域字典借全区间辅助算子与奇偶降低核对Grubb假设，包含临界权条件；原完整稀疏族0≤s<7/2的既有结论保持。'),
('second-variation-weighted-eigenvalues','L10','cross-result','新增finite-interface-second-derivative补上固定正块值、不碰撞局部接口路径的几何与坐标加速度；旧固定密度Hessian保持原范围，G1′仍开放。'),
('ratio-first-pair-variational','L12','source-attribution','L12原文的首对切换机制与lambda加权切换函数已对照，应归属经典文献；其一般系数类是L1，常数盒界特例是L∞。C(1,4)区域含数值假定，不能据此认证全R结果或任意n。'),
('gap-band-extremals','L13','unverified-source-lead','Hongli Sun2022文章元数据已核实，但S₁/S₂完整约束尚未取得。仅作为后续读取线索，不构成本卡证明依赖，也不证明项目同一盒类的全部n=1结论。')]
notes=[]
for name,Id,kind,text in rows:
    p='tools/'+name+'.md';h=L.digest((R/p).read_bytes())
    notes.append(L.annotate(R,p,h,'agent:literature-absorption-20260923',kind,'2026-09-23 source-to-claim / P0-P4',text,sources[Id]))
(O/'annotations.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print('Saved',len(notes),'version-bound candidate annotations, including unverified L13 lead.',flush=True)
result=L.make_index(R,ReadmePath='tools/README.md')
(O/'index-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='issues'}),flush=True)
if result['verdict']!='INDEXED' or result['indexed']!=89 or result['blocked']!=1:raise RuntimeError('Unexpected library state; inspect actual gate, do not bypass')
# One actual native query for the full batch. A single token avoids noisy unrelated OR matches.
query=L.query_tools(R,'literature-absorption-20260923',limit=50)
(O/'retrieval-result.json').write_text(json.dumps(query,ensure_ascii=False,indent=2)+'\n')
new=[x for g in ['domains','approximation','interfaces'] for x in json.loads((O/(g+'-cards.json')).read_text())]
hits={r['location']:r for r in query['hits']}
for item in new:
    h=hits.get(item['location']);assert h and h['sha256']==item['sha256'] and h['reuse_allowed']
    assert any(n['state']=='CURRENT' for n in h['annotations'])
    assert all(x['binding_state']=='CURRENT' for typ in ['sources','evidence'] for x in h[typ] if x.get('path') or x.get('source_id'))
assert not query['changed_paths'] and query['verdict']=='RETRIEVAL_ONLY' and query['blocked']==1
print('Actual query returned all11 new tools with current evidence, sources and version-bound annotations.',flush=True)
