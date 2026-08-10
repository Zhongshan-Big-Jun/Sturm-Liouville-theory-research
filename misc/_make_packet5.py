# -*- coding: utf-8 -*-
import hashlib, json, io, os

ROOT = r"F:\LaTeX\BVE research"

def h6(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:6].upper()

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

t_hash = h6("KEY LEMMA2 resume: verify certificates + assemble proof 2026-08-06")
t_task = "Q-20260806-keylemma2b-" + t_hash
t_run  = "R-20260806T070000Z-keylemma2b-" + t_hash

packet = """# Research task packet

- **Task ID**: @@TASK@@
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T07:00:00Z
- **Task type**: solve
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

A prior run (R-20260806T050000Z-keylemma2-5A35E5) was interrupted during its final
write-up. Its ledger records a nearly complete analytic reduction of the KEY LEMMA
residual obligations (R1, R2, L4box, L5box) to elementary one-variable facts plus four
sound outward-rounded interval certificates that are already computed but NOT yet
independently verified, and no candidate proof / audit report was assembled. This task
resumes that run: independently verify the certificates, complete the analytic proofs,
and produce the standard upstream artifacts. Success closes obligation O2 of the
n=1 gap-extremal proof.

## Authoritative problem source

The interrupted run's ledger and contract are the authoritative source of the current state:
- runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/research_ledger.md
  (entries 1-6: (q,u) reformulation, M2 route, CORNER, C4, L4box/L5box)
- runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/problem_contract.md
- runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/obligation_graph.md

The target claims (recheck before use):
- R1: G2 >= 0 for all q >= 2, c in (0,1/2).  Reduced to M2 ^ CORNER:
  (i) M2: dIN/du < 0 on D = {(q,u): q>1, 0<u<sqrt(2q+1)}, where u = q tan(pi-alpha2),
  IN(q,u) = (q^2+u^2) A (2 A q - 3 u + 2 arctan(u)) - 3 u q (1+u^2) arctan(u),
  A = pi - arctan(u/q);  Sign(IN) = Sign(G2).
  (ii) CORNER: G2(1/2;q) >= 0 for q >= 2, equivalent to pi > arccos(2/3) + sqrt(5)
  (elementary certificate started in the ledger).
- R2: G2 >= 0 for all q > 1, c in (0,0.4].  Reduced to M2 ^ C4, where C4 is
  G2(0.4;q) >= 0 for q >= 1; on the c=0.4 curve K(v) is increasing with
  min K = 2.615 at v = 2 pi/7 (ledger entry 5).
- L4box: H' = G2' - G1' < 0 on (1,2] x [0.4,0.5].  Interval certificate computed
  (128 boxes, worst upper bound -4.6569).
- L5box: F~'' = M~1 J1 - M~2 J2 > 0 on (1,2] x [0.4,0.5].  Interval certificate
  computed (128 boxes, worst lower bound +6.2429).
- dM2/dq < 0 on D: analytic for q >= 20 via the elementary bound B(q) (ledger entry 6),
  interval certificate computed on (1,20) x (0,sqrt(41)) (84 boxes, worst upper bound
  -0.1902).

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| Interrupted run ledger | 2026-08-06 | runs/.../R-20260806T050000Z-keylemma2-5A35E5/research_ledger.md | current state, derivations, TO DO list | recheck all formulas |
| Contract + obligation graph | 2026-08-06 | runs/.../R-20260806T050000Z-keylemma2-5A35E5/problem_contract.md, obligation_graph.md | normalized statements | recheck |
| Interval engine | 2026-08-06 | runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/riarith.py, rigorous.py, sound_bracket.py | outward-rounded arithmetic | verify soundness claims |
| Certificates | 2026-08-06 | runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/cert_dM2dq_boxes.json, cert_L4box_boxes.json, cert_L5box_boxes.json, cert_c4_boxes.json | computed enclosures | MUST be re-verified independently |
| Verify script | 2026-08-06 | runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/verify_certificates.py | tiling + re-evaluation checker | run it; report PASS/FAIL per certificate |
| Parent run | 2026-08-06 | runs/.../R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md + audit_report.md | original reduction and bases | recheck |
| Origin | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | G2, H, F~ definitions | recheck |

## Related paper analyses

No independent structured analysis beyond the run reports listed above.

## Relevant tool-library leads

- tools/key-lemma-decomposition.md (decomposition + 2026-08-06 reduction update)
- tools/interval-ad-certificate.md (interval certificate pattern; from O3a run)
Leads only; do not treat as verified premises.

## Known ambiguities and bibliographic risks

- The four certificate JSONs were produced by the interrupted run but not yet independently
  verified.  verify_certificates.py (tiling + re-evaluation) must be run and its output
  reported.  Do NOT claim the certificates as valid until this passes.
- Ledger entry 3 transcription of dIN/du was corrected in entry 5 (the entry-5 formula is
  the verified one).  Watch for stale formula copies.
- The c=0.4 curve parametrization: v = arctan(u) in [2 pi/7, 2 pi/5), q = tan(v)/tan(pi-2.5v),
  A = 2.5 v; IN = A K(v); K(v) increasing with min slope 88, K(2 pi/7) = 2.615.
- C1 (audited): (LOG) and (FP) forms are not logically equivalent; T4 consumes (FP).
- Do not relax the box endpoints: L4box/L5box are on (1,2] x [0.4,0.5]; endpoints must be
  included or handled by one-sided limits.

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- At least 8 hours of effective research time before concluding; failure routes and lessons
  must be recorded in the research ledger.
- Environment: Python 3.10 at C:\\Users\\HuangZY\\AppData\\Local\\Programs\\Python\\Python310\\python.exe
  (numpy 2.2.6, scipy 1.15.3, sympy, mpmath); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe.
- On success the integrated proof goes to docs/SL_gap_n1_proof.tex (manager compiles);
  the run must produce candidate_proof.md and audit_report.md.

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
p = packet.replace("@@TASK@@", t_task).replace("@@RUN@@", t_run)
write_utf8(os.path.join(ROOT, "agenda", "task-packets", t_task + ".md"), p)

p = os.path.join(ROOT, "index", "task-packets.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    tp = json.load(f)
tp["items"].append(
    {"task_id": t_task, "path": "agenda/task-packets/" + t_task + ".md",
     "problem_id": "O-2026-SL-GAP-3B7A2C", "state": "READY",
     "run_id": t_run, "dispatched_at": "2026-08-06T07:00:00Z"})
tp["updated_at"] = "2026-08-06T07:00:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

rr = os.path.join(ROOT, "runs", "rigorous-open-math-research", t_run)
os.makedirs(rr, exist_ok=True)
manifest = {
    "schema_version": 1,
    "run_id": t_run,
    "project_id": "MRP-20260731-BVE-SL",
    "task_id": t_task,
    "upstream_skill": "$rigorous-open-math-research",
    "upstream_skill_version_or_hash": "v2026-08-05 (changelog)",
    "started_at": "2026-08-06T07:00:00Z",
    "completed_at": None,
    "run_root": "runs/rigorous-open-math-research/" + t_run,
    "task_packet_path": "agenda/task-packets/" + t_task + ".md",
    "task_packet_sha256": None,
    "upstream_status_verbatim": None,
    "artifacts": [],
    "environment": {"model": None,
        "tools": ["Python 3.10 (numpy 2.2.6, scipy 1.15.3, sympy, mpmath)", "xelatex (TeX Live 2024)"],
        "formal_systems": [], "unknown_fields": ["model"]},
    "manager_ingestion_state": "DISPATCHED",
    "missing_or_unavailable_artifacts": [],
    "notes": ["resumes interrupted run R-20260806T050000Z-keylemma2-5A35E5"]
}
write_utf8(os.path.join(rr, "run-manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
write_utf8(os.path.join(rr, "task-packet-link.txt"), "task packet: agenda/task-packets/" + t_task + ".md\n")
print("TASK:", t_task)
print("RUN:", t_run)