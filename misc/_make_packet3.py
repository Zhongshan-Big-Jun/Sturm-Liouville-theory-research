# -*- coding: utf-8 -*-
import hashlib, json, io, os

ROOT = r"F:\LaTeX\BVE research"

def h6(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:6].upper()

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", os.path.relpath(path, ROOT))

t3_hash = h6("gap-n1 O1 reduction draft independent audit 2026-08-06")
t3_task = "Q-20260806-o1-audit-" + t3_hash
t3_run  = "R-20260806T011500Z-o1audit-" + t3_hash

packet3 = """# Research task packet

- **Task ID**: @@TASK@@
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T01:20:00Z
- **Task type**: rigorously audit
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

The n=1 adjacent-gap extremal proof rests on the reduction theorem O1 (SUP/INF over the box
class 1<=rho<=R equals SUP/INF over the 2-parameter barrier/well families). A draft proof
exists but has never been independently audited. The program cannot ship the final theorem
until every obligation O1a-O1f is checked against primary sources. This audit is read-only
verification and runs in parallel with the KEY LEMMA and O3a delegations.

## Authoritative problem source

The document to audit is:
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md
The proof obligations are listed as O1a-O1f in:
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md (O1 node)

Audit goal: for each obligation, decide PROVED / PARTIAL / FAILED / OPEN with exact reasons,
recheck every cited theorem against its original source (Keller 1976, Mahar-Willner 1976,
Ahrami-El Allali-Harrell arXiv:2407.02459 Lemma 2.1-2.2, Cheng-Kung-Law-Lian 2010 as relevant),
check all hypotheses, quantifiers, boundary cases (a=0, b=1, constant densities), and the
measure-zero-change claim. Produce audit_report.md with a line-by-line verdict.

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| O1 draft | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md | audit target | read-only |
| Obligation graph | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md | O1a-O1f list | recheck |
| Research ledger | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/research_ledger.md | context and derivations | recheck |
| AEH paper | arXiv:2407.02459 | papers/fundamental_gap.txt | Lemma 2.1-2.2 source | must verify exact statement |
| Keller 1976 | DOI 10.1137/0131042 | papers/keller1976.txt | variational facts | must verify exact statement |
| Mahar-Willner 1976 | DOI 10.1002/cpa.3160290505 | papers/mw1976.txt | extremal mechanism | must verify exact statement |
| Problem contract | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md | intended theorem | recheck consistency |

## Related paper analyses

Legacy notes in research_cache/; prior session records in AGENTS.md (sessions 15-18).

## Relevant tool-library leads

- tools/gap-n1-reduction.md (reduction pattern; provenance UPSTREAM_AUDITED pending this audit)
- tools/feynman-hellmann.md, tools/bang-bang.md (leads used inside O1)
Leads only; do not treat as verified premises.

## Known ambiguities and bibliographic risks

- O1a (L^1 continuity of lambda_k on the box class) is marked OPEN in the obligation graph and
  cited as standard; the auditor must decide whether the draft provides an acceptable proof or
  needs a precise citation.
- The Wronskian monotonicity argument (O1c) is rho-independent per the draft; verify the
  deduction of at-most-2-zeros and the single-positive-interval property.
- Bang-bang (O1f) via one-sided FH derivative: check the argument at densities taking interior
  values on intervals, and that measure-zero changes do not affect eigenvalues.
- The draft is not yet integrated with O2/O3; audit only the reduction itself.

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- Environment: Python 3.10 at C:\\Users\\HuangZY\\AppData\\Local\\Programs\\Python\\Python310\\python.exe
  (numpy 2.2.6, scipy 1.15.3); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe.
- The audit may rerun numeric checks as evidence but must clearly separate evidence from proof.

## Required run location

runs/rigorous-open-math-research/@@RUN@@/

## Upstream invocation

Use $rigorous-open-math-research on the concrete problem in this task packet. Treat this
packet as project context, not as a verified theorem contract. Independently normalize and
audit the exact statement, and recheck every theorem used as a premise against its original
source and exact version. Follow the upstream skill's own problem-level workflow and output
protocol. Write all standard artifacts under RUN_ROOT. Return the upstream result status
verbatim together with the run root and artifact locations. Do not call
manage-math-research-program from inside the solver run.

## Manager ingestion checklist

- [ ] Preserve upstream status verbatim.
- [ ] Index the run root and artifact paths/hashes.
- [ ] Do not copy or replace upstream standard artifacts.
- [ ] Update the portfolio, maps, tool candidates, budget, checkpoint, and resume entry.
- [ ] Promote reusable knowledge only from exact source or audited artifact locations.
"""
p3 = packet3.replace("@@TASK@@", t3_task).replace("@@RUN@@", t3_run)
write_utf8(os.path.join(ROOT, "agenda", "task-packets", t3_task + ".md"), p3)

p = os.path.join(ROOT, "index", "task-packets.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    tp = json.load(f)
tp["items"].append(
    {"task_id": t3_task, "path": "agenda/task-packets/" + t3_task + ".md",
     "problem_id": "O-2026-SL-GAP-3B7A2C", "state": "READY",
     "run_id": t3_run, "dispatched_at": "2026-08-06T01:20:00Z"})
tp["updated_at"] = "2026-08-06T01:20:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

rr = os.path.join(ROOT, "runs", "rigorous-open-math-research", t3_run)
os.makedirs(rr, exist_ok=True)
manifest = {
    "schema_version": 1,
    "run_id": t3_run,
    "project_id": "MRP-20260731-BVE-SL",
    "task_id": t3_task,
    "upstream_skill": "$rigorous-open-math-research",
    "upstream_skill_version_or_hash": "v2026-08-05 (changelog)",
    "started_at": "2026-08-06T01:20:00Z",
    "completed_at": None,
    "run_root": "runs/rigorous-open-math-research/" + t3_run,
    "task_packet_path": "agenda/task-packets/" + t3_task + ".md",
    "task_packet_sha256": None,
    "upstream_status_verbatim": None,
    "artifacts": [],
    "environment": {"model": None,
        "tools": ["Python 3.10 (numpy 2.2.6, scipy 1.15.3)", "xelatex (TeX Live 2024)"],
        "formal_systems": [], "unknown_fields": ["model"]},
    "manager_ingestion_state": "DISPATCHED",
    "missing_or_unavailable_artifacts": [],
    "notes": ["manager-created run root; upstream writes problem-level artifacts"]
}
write_utf8(os.path.join(rr, "run-manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
write_utf8(os.path.join(rr, "task-packet-link.txt"), "task packet: agenda/task-packets/" + t3_task + ".md\n")
print("T3:", t3_task, t3_run)