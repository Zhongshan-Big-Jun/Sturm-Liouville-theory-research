# Plugin performance test: DensBC O1' round 2

Date: 2026-08-16
Scope: measure how the math-research-workflow plugin behaves on a second DensBC
O1' run, and identify optimization points that reduce detours and avoid
reinventing the wheel.

## 1. What was measured

Round-1 run (R-...-densbc-o1p) artifact sizes:

| Artifact | Size (bytes) | Role |
| --- | --- | --- |
| candidate_proof.md | ~15,048 | full STRICT proof (heavy read) |
| audit_report.md | ~8,823 | independent audit (only final audit retained) |
| research_ledger.md | ~3,748 | chronological record |
| approach_registry.md | ~1,807 | directions tried |
| whiteboard.md | ~2,185 | planner memory (lightweight) |
| research_map.md | ~117 lines | project-wide survey |

Reuse assets:

| Asset | Before round 2 | After round 2 |
| --- | --- | --- |
| lean-proof/LEMMA_INDEX.md | MISSING | regenerated (487 declarations) |
| research_map.md | per-problem only | project-wide problem graph |

## 2. Observed costs and duplication

1. **Re-reading heavy proofs**: a full candidate_proof (15KB) + audit (8.8KB)
   is expensive to load into context. The research_map (117 lines) is the cheap
   entry point and should be read first; full proofs should be read on demand.
2. **LEMMA_INDEX was missing**: no reuse index existed before round 2, so an
   agent could re-prove an already-formalized lemma. Now regenerated.
3. **Two audit passes collided**: the solver produced its own independent-audit
   report, and the orchestrator started a second audit; both wrote
   `audit_report.md`, and the later one overwrote the earlier. This is
   acceptable (canonical single report per revision) but should be intentional
   and recorded in the ledger.
4. **Registration files overlap**: `run-manifest.json`, `formalization_progress.md`
   and `proof-submission-audit.md` repeat the same run/status bookkeeping. The
   overlap is small but a single source of truth would be cleaner.
5. **Literature re-confirmation**: round 2 re-confirmed the novelty status that
   round 1 already recorded. A search-log keyed by query (in `research_cache/`)
   would avoid re-searching the same question.

## 3. Optimization points (prevent detours / re-inventing the wheel)

### P1. Reuse-first workflow (do not re-derive or re-prove)
- Regenerate `lean-proof/LEMMA_INDEX.md` whenever Lean files change; consult it
  before proving a new lemma.
- Read the `research_map.md` routes + avoid list before any deep dive; do not
  resume a mapped dead end without a materially new mechanism.
- Reuse the existing `status_and_literature.md` of an upstream run instead of
  re-running a novelty sweep (append, do not redo).

### P2. Canonical single audit per revision
- Keep exactly one `audit_report.md` per proof revision; route repair findings
  through `research_ledger.md`; when two auditors run, record both verdicts in
  the ledger and keep the final report as the merged/canonical one.

### P3. Token budget discipline (make it operational)
- Write a `budget_state.json` per run (`total/consumed/remaining`, phase,
  status) alongside `run-manifest.json`; check at Planner/Worker/Verifier/Lean
  boundaries; on exhaustion follow pause + handoff + resume (never data loss).

### P4. Lightweight access pattern
- Agents default to reading: `research_map.md` + `repo_index.md` + latest
  handoff + last `research_ledger.md` entries; read full proofs/audits on
  demand only. This reduces context load substantially.

### P5. Single source of truth for registration
- Make `run-manifest.json` canonical and auto-derive
  `formalization_progress.md` / `proof-submission-audit.md` from it (or vice
  versa) at stage close.

### P6. Stage-close automation
- On each Stage C close: regenerate `LEMMA_INDEX.md`, update `research_map.md`,
  refresh `budget_state.json`, and run the pipeline gate. Make these checklist
  items explicit.

## 4. Verdict

The plugin runs correctly end to end (gate passed, solver + audits + scaffold +
research-map + report, all committed). The main performance headroom is: reduce
context by reading lightweight summaries first, restore and use the lemma reuse
index, canonicalize single audits, and operationalize token budgets. These are
all implementable as workflow rules/scripts and would cut both tokens and
duplicate work.
