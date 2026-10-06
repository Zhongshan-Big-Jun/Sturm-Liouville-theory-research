import sys, json
from pathlib import Path
ROOT=Path('F:/tools/math-audit-round16-20261006/software-review-v4/root')
sys.path.insert(0,str(ROOT/'scripts'))
import _gapn2_second_variation_probe as V
rows=[]
for outer in (.375,.25,.5):
    for exponent in (19,20):
        for rho in (1e9,1e10,4e10,8e10,1e11):
            d=2.**-exponent
            blocks=[(outer,1.),(d,rho),(1.-outer-d,1.)]
            try:
                p=V.SpectralProbe(blocks,61,32)
                rows.append(dict(blocks=blocks,accepted=True,first=float(p.roots[0]),last=float(p.roots[-1])))
            except Exception as error:
                rows.append(dict(blocks=blocks,accepted=False,error=repr(error)))
Path('F:/tools/math-audit-round16-20261006/software-review-v4-case-search.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
for row in rows:
    print(row)
