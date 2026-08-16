"""Finite exact-dyadic Arb checks for the C2-N escape union."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve()
SRC=HERE.parent.parent/"finite_modulus_certificate/prototype_checker.py"
SPEC=importlib.util.spec_from_file_location("stable",SRC)
assert SPEC and SPEC.loader
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

def main():
    h=M.ball(0,1,16)
    beta_edge=M.arb(-3)/2
    max_alpha=None
    for i in range(256):                 # 0<=kappa<=4
        out=M.evaluate(h,M.ball(i,i+1,6),beta_edge)
        assert out["alpha"]<0
        u=float(M.upper(out["alpha"]))
        max_alpha=u if max_alpha is None else max(max_alpha,u)

    max_S=None
    count=0
    for i in range(24,256):              # 3/8<=kappa<=4
        kap=M.ball(i,i+1,6)
        for j in range(-96,0):           # -3/2<=beta<=0
            out=M.evaluate(h,kap,M.ball(j,j+1,6))
            assert out["S"]<0
            u=float(M.upper(out["S"]))
            max_S=u if max_S is None else max(max_S,u)
            count+=1

    print(json.dumps({
        "status":"FINITE_COMPUTATIONAL_RESULT",
        "result":"PASS",
        "h":"[0,2^-16]",
        "beta_escape_boundary":{
            "kappa":"[0,4]","beta":"-3/2","cells":256,
            "predicate":"alpha<0 (hence b<a)",
            "max_directed_upper":max_alpha},
        "kappa_escape_rectangle":{
            "kappa":"[3/8,4]","beta":"[-3/2,0]","cells":count,
            "predicate":"S=(rB-1)/h<0",
            "max_directed_upper":max_S},
        "failures":0,
        "precision_bits":256,
        "floating_sign_tests":0
    },indent=2))

if __name__=="__main__":
    main()
