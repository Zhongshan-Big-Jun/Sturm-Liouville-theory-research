import json, io, hashlib, os

root = r"F:\LaTeX\BVE research"
def load(p):
    with io.open(p, encoding="utf-8-sig") as f:
        return json.load(f)
def save(p, obj):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

# ---- 1. fix stale run-manifest for the C1 run ----
mp = root + r"\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\run-manifest.json"
m = load(mp)
m["completed_at"] = "2026-08-06T18:05:00Z"
m["upstream_status_verbatim"] = ("RIGOROUS_PARTIAL_RESULT (C1 OPEN; new reflection structure Lemmas R1-R6 PROVED; "
    "C1 reduced to (E1) endpoint signs + (M) M-shape of h', numerically verified R in {1.02..1e7} but analytically open; "
    "audit verdict REPAIRABLE_GAP for C1)")
m["manager_ingestion_state"] = "INGESTED"
m["notes"] = ["ingested by coordinator ACT-20260806-018; run-manifest completed_at written post-hoc by manager"]
save(mp, m)
print("C1 run-manifest updated")

# ---- 2. state/current.json ----
cp = root + r"\state\current.json"
c = load(cp)
c["current_stage"] = "gap-extremals-n1-proof-doc"
c["objective"] = ("Prove SUP/INF of lambda_2-lambda_1 over 1<=rho<=R box class attained by symmetric 3-block "
                  "[1,R,1] / [R,1,R]; O3a/C1 next attack and INF R->inf limit dispatched in parallel")
c["active_run_id"] = "R-20260806T200000Z-o3a-c1b-7F3A9B"
c["active_run_ids"] = ["R-20260806T200000Z-o3a-c1b-7F3A9B", "R-20260806T200000Z-inflimit-5B2C7D",
    "R-20260806T140000Z-o3ac1-42F931", "R-20260806T151000Z-o1reaudit-5A1C3D",
    "R-20260806T140000Z-o1revise-2ED02A", "R-20260806T140000Z-keylemmaaudit-2F83B1",
    "R-20260806T070000Z-keylemma2b-0A6D8F"]
c["active_task_ids"] = ["Q-20260806-o3a-c1b-7F3A9B", "Q-20260806-inflimit-5B2C7D"]
c["run_status_verbatim"] = ("O1: CLOSED (INDEPENDENTLY_AUDITED_PROOF); O2 KEY LEMMA: CLOSED (INDEPENDENTLY_AUDITED_PROOF); "
    "O3b(1): PROVED; O3a: PARTIAL (R1-R6 PROVED, C1 reduced to E1+M; C1 next attack DISPATCHED to Pasteur); "
    "INF R->inf limit proof DISPATCHED to Nash")
c["next_actions"] = [
    "1. wait for Pasteur (C1 next attack, R-20260806T200000Z-o3a-c1b-7F3A9B) and Nash (INF limit, R-20260806T200000Z-inflimit-5B2C7D)",
    "2. ingest both runs; update SL_gap_n1_proof.tex sections 5/6 (+INF limit section if proved)",
    "3. final validation: validate_project.py, budget settlement, checkpoint"
]
c["blockers"] = []
c["budget"] = {
    "mode": "effective_time",
    "target_hours": 8.0,
    "consumed_hours": 4.8,
    "note": "evidence-backed; combined subagent effort this and prior sessions far exceeds 8h effective; final accounting on stage close"
}
c["last_updated"] = "2026-08-06T20:15:00Z"
save(cp, c)
print("current.json updated")

# ---- 3. RESUME.md ----
rp = root + r"\state\RESUME.md"
resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF by symmetric [R,1,R].
Run status: O1 CLOSED (INDEPENDENTLY_AUDITED_PROOF), O2 KEY LEMMA CLOSED (INDEPENDENTLY_AUDITED_PROOF),
O3b(1) PROVED, O3a PARTIAL (R1-R6 PROVED; C1 = E1 + M open), INF R->inf limit open.

## Read these files first
1. `docs/SL_gap_n1_proof.tex` (O1/O3b/O2 complete; section 5 = O3a with R1-R6 + C1 status)
2. `state/checkpoints/2026-08-06T201500Z--c1b-inflimit-dispatch.md`
3. `runs/rigorous-open-math-research/R-20260806T140000Z-o3ac1-42F931/` (C1 run: R1-R6, gaps G-E1/G-M)
4. `runs/rigorous-open-math-research/R-20260806T200000Z-o3a-c1b-7F3A9B/` (C1 next attack, DISPATCHED)
5. `runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/` (INF limit proof, DISPATCHED)

## Last completed action
2026-08-06 20:15Z: ingested C1 run bookkeeping (run-manifest, current.json);
dispatched two parallel solver runs: Pasteur (C1 next attack), Nash (INF R->inf limit);
manager re-verified INF limit numerics (scripts/verify_inflimit.py: u*=0.3299225081, D*R=24.9438661384 < 3pi^2).

## Active tasks and runs
- Task: Q-20260806-o3a-c1b-7F3A9B, run R-20260806T200000Z-o3a-c1b-7F3A9B (DISPATCHED, Pasteur)
- Task: Q-20260806-inflimit-5B2C7D, run R-20260806T200000Z-inflimit-5B2C7D (DISPATCHED, Nash)

## Exact next action
1. Ingest Pasteur (C1) when it returns; if C1 PROVED: O3a closed -> full main theorem proof complete.
2. Ingest Nash (INF limit); integrate into SL_gap_n1_proof.tex if proved.
3. Final validation + budget settlement + checkpoint.

## Blockers or missing inputs
- None blocking. O3a/C1 is the last open obligation for the n=1 theorem.

## Budget remaining
8.0 h target, evidence-backed; consumed 4.8 h (ACT-001..006) + subagent effort; final accounting on stage close.

## Validation command
- `python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research`
"""
with io.open(rp, "w", encoding="utf-8", newline="\n") as f:
    f.write(resume)
print("RESUME.md updated")