"""One bounded replay for the three compact t-high annuli."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve()
PROJECT=HERE.parents[4]
sys.path.insert(0,str(PROJECT/"tmp/r12-flint312"))
UP=PROJECT/"runs/R-20260815T181317Z-min-reflection/routes/event_inertia/cover_collar.py"
SPEC=importlib.util.spec_from_file_location("cover",UP)
assert SPEC and SPEC.loader
C=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)

D=C.R17.DEN
Q=D//64
TUP=D-(1<<(C.R17.BITS-17))
ST={"L":(0,Q),"I":(Q,D-Q),"H":(D-Q,D)}

def root(code:str):
    k,_,y=code
    return (ST[k],(D-Q,TUP),ST[y])

def main():
    out={code:C.run(root(code),1_000_000) for code in ("LHL","IHL","LHH")}
    print(json.dumps({"status":"FINITE_COMPUTATIONAL_RESULT","targets":out},indent=2))

if __name__=="__main__":
    main()
