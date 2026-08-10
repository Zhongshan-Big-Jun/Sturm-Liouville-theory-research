# -*- coding: utf-8 -*-
import json, hashlib, os, datetime

root = r"F:\LaTeX\BVE research"
def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

run_root = os.path.join(root, r"runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
keys = [
    os.path.join(run_root, "problem_contract.md"),
    os.path.join(run_root, "O1_reduction_draft.md"),
    os.path.join(run_root, "agentA_O2_single_crossing.md"),
    os.path.join(run_root, "agentB_O3a_fixed_point.md"),
    os.path.join(run_root, "agentC_O3b_boundary.md"),
    os.path.join(run_root, "research_ledger.md"),
    os.path.join(root, "docs", "SL_gap_n1_research_summary.tex"),
    os.path.join(root, "docs", "SL_gap_n1_research_summary.pdf"),
    os.path.join(root, "tools", "gap-n1-reduction.md"),
    os.path.join(root, "tools", "two-block-gap-bounds.md"),
    os.path.join(root, "tools", "key-lemma-decomposition.md"),
]
for k in keys:
    print(os.path.basename(k), sha(k) if os.path.exists(k) else "MISSING")