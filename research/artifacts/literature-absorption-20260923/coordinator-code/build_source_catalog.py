from pathlib import Path
import json,re,sys,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923');Root=R/'literature/absorption-20260923';Q=O/'source-cache'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Captures={}
for fn in ['p0/capture-receipts.json','domains-capture-receipts.json','approximation-capture-receipts.json','interfaces-capture-receipts.json']:
    for row in json.loads((O/fn).read_text()):Captures[row['id']]=row
Specs=[
 ('L01','domains/notes/L01-source-to-claim.md','左定谱模型与空间传输','2025期刊；实际读arXiv v1','一般正自伴谱框架；不替代指定稀疏族的完备性'),
 ('L02','notes/L02-L12-L13-source-to-claim.md','原第二左定问题的对象对齐','2025期刊原PDF','同算子/移位/范数/族；项目已有s=2结果回答其问题'),
 ('L03','domains/notes/L03-source-to-claim.md','分数与临界幂域','arXiv v4及作者提供期刊PDF','经全区间Neumann/移位Robin桥接；临界条件不能删除'),
 ('L04','domains/notes/L04-source-to-claim.md','GKN边界商空间与秩','2019期刊；实际读arXiv v1','秩只给适当边界商信息；v1奇异例维数存疑，不移植'),
 ('L05','domains/notes/L05-source-to-claim.md','反射对称与奇偶分解','2025期刊；实际读arXiv v2','必须验证整个算子域的反射不变性及sqrt2归一化'),
 ('L06','domains/notes/L06-source-to-claim.md','奇异Legendre比较工具','2026预印本v1；未核实期刊','加权高阶控制的比较阅读；保留v1公式/匹配条件疑点'),
 ('L07','approximation/notes/01_primary_sources.md','Müntz与差分族的矩接口','作者提供26页版本','满足源定理指数与可积性条件；不直接推任意删项判据'),
 ('L08','approximation/notes/01_primary_sources.md','相容Legendre重组','作者提供1994论文版本','项目另证s=2/4边界、张成及稳定性；不照抄一般Robin式'),
 ('L09','approximation/notes/01_primary_sources.md','有限TSVD误差与系数范数','2019期刊；实际读arXiv v4','Gram截断epsilon对应sqrt(epsilon)惩罚；非自动frame'),
 ('L10','interfaces/notes/L10-source-to-claim.md','二阶边界变分的适用性检查','2022期刊；实际读arXiv v1','固定对称算子桥梁仍开放；项目有限界面定理另行推导'),
 ('L11','interfaces/notes/L11-source-to-claim.md','测度系数、点质量及Green集中','2013期刊；实际读arXiv v2','delta是测度而delta-prime不是；固定核极限与动核微分分开'),
 ('L12','notes/L02-L12-L13-source-to-claim.md','首对谱值的新颖性与条件对照','1982期刊原PDF；旧文件名1983','一般L1类，盒界特例L∞；C(1,4)区域依赖数值正确性'),
 ('L13','notes/L02-L12-L13-source-to-claim.md','最小谱隙线索，待补模型','出版社元数据及缺公式预览；未得全文','S1/S2完整约束未匹配，禁止作为证明依赖')]
Bib=(Root/'selected_references.bib').read_text();Entries=re.findall(r'@(article|misc)\{([^,]+),([\s\S]*?)(?=\n@|\Z)',Bib)
if len(Entries)!=13:raise RuntimeError('Expected13 bib entries')
Rows=[];FullProbes=[]
for (Id,Rel,Use,Version,Limit),(Kind,Key,Body) in zip(Specs,Entries):
    doi=re.search(r'\bdoi\s*=\s*\{([^}]+)\}',Body).group(1);note=Root/Rel;raw=note.read_bytes();cap=Captures[Id]['capture']
    Src=Q/cap['source'];meta=json.loads(Src.read_text())
    if L.digest((Src.parent/'raw.bin').read_bytes())!=cap['raw_sha256'] or L.digest((Src.parent/'text.txt').read_bytes())!=cap['text_sha256']:raise RuntimeError('Raw cache drift '+Id)
    N=L.capture_source(R,note,'https://doi.org/'+doi,'original reading note 2026-09-23 '+hashlib.sha256(raw).hexdigest()[:12],Id+' 项目原创阅读/适配笔记: '+Use,None,'author-written UTF8 Markdown; not extracted publisher text','secondary','Original note only. Actual primary reading coverage and raw-source namespace are separate in source-catalog.json.',[Rel,Id+' section/source mapping'])
    Text=raw.decode();offset=Text.find('## '+Id)
    Probe=L.read_source(R,N['source_id'],1,40,max(offset,0))
    FullProbes.append(dict(id=Id,probe=Probe))
    Probe={k:v for k,v in Probe.items() if k not in ['content','metadata']}
    Rows.append(dict(id=Id,bib_key=Key,doi=doi,use=Use,version_note=Version,boundary=Limit,primary_capture=cap,primary_cache_project=str(Q),primary_capture_namespace='private source-cache project; not this repository',primary_source_record_sha256=L.digest(Src.read_bytes()),primary_reading_coverage=cap.get('coverage'),note_path=note.relative_to(R).as_posix(),note_sha256=L.digest(raw),public_note_capture=N,actual_note_read_probe=Probe,reading_status='METADATA_AND_INCOMPLETE_PREVIEW_ONLY_NO_THEOREM_DEPENDENCY' if Id=='L13' else 'FULL_ORIGINAL_AVAILABLE_TARGETED_READING_NOT_FULL_PROOF_AUDIT'))
for row in Rows:
    if row['id']=='L03':
        row['metadata_corrections']=[dict(field='online_date',current='27 October 2015, as printed in the author-posted journal PDF',withdrawn='26 October 2015 publisher-search attribution',reason='The retained search does not contain supporting L03 evidence; previous raw-capture coverage is a historical assertion, not current verification.',evidence='literature/absorption-20260923/domains/notes/L03-source-to-claim.md')]
Extra=Captures['L03-journal']['capture']
Catalog=dict(schema='sl-literature-source-catalog/v1',baseline='902d2a931a76dae5fe1ef6d7dacdcfa230897f9c',source_count=13,full_original_count=12,metadata_incomplete_count=1,public_capture_kind='secondary original notes, not original papers',private_additional_primary=[dict(id='L03-journal',capture=Extra)],sources=Rows)
(Root/'source-catalog.json').write_text(json.dumps(Catalog,ensure_ascii=False,indent=2)+'\n')
(O/'public-note-read-probes.json').write_text(json.dumps(FullProbes,ensure_ascii=False,indent=2)+'\n')
Lines=['# 来源、阅读位置与用途指针表','','共13项：12项取得原文并定点阅读；L13仅元数据及不完整预览。原文未逐篇逐式审计。精确URL、版本、原件/文本哈希、缓存与笔记source_id均在 [source-catalog.json](source-catalog.json)。公开source_id捕获的是原创笔记，原件source_id属于独立本地缓存。','','| ID | 用途与阅读笔记 | 实际版本 | 推论边界 |','| --- | --- | --- | --- |']
for row,spec in zip(Rows,Specs):Lines.append(f"| {row['id']} | [{row['use']}]({spec[1]}) | {row['version_note']} | {row['boundary']} |")
Lines+=['','复用时先读上述边界，再核对工具卡、原文定位和项目对象。原文引用与项目独立推导分开；[验收记录](../../reports/literature-absorption-20260923/REPORT.md)说明具体审查范围。','']
(Root/'SOURCE_TABLE.md').write_text('\n'.join(Lines))
(O/'source-catalog-build.json').write_text(json.dumps(dict(sources=len(Rows),full_originals=12,secondary_note_captures=len(Rows),source_catalog_sha256=L.digest((Root/'source-catalog.json').read_bytes())),indent=2)+'\n')
print('Built 13 precise source pointers and 13 secondary note captures;12 originals plus1 metadata-only lead.')
