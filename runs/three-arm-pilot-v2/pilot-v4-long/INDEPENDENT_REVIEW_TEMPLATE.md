# Pilot v4 independent review template

Reviewer sees: (1) the frozen problem statement; (2) one arm's artifacts only; (3) no arm identity, no other arm outputs.

## Output format

```markdown
## Review
- Candidate ID: UUID assigned by orchestrator
- Problem: U1 / U2 / U3
- Verdict: PASS | REPAIRABLE_GAP | PARTIAL_NOT_COMPLETE | FATAL_GAP | WRONG_PROBLEM
- Scores (100 pts): correctness/40, contract/20, progress/15, calibration/10, citation/10, reproducibility/5
- Score total: __
- Fatal issues: none / ...
- Repair list (if applicable): ...
- Confidence: high/medium/low
```

## Rules
- Do not use numerical evidence as proof.
- External theorems must be stated with exact hypotheses.
- Mark an assertion as NOT-YET-STRICT if the submitted text does not establish it.
- Distinguish "problem solved" from "partial/relevant progress".
- Do not infer arm identity from style; if an artifact reveals its arm, ignore that clue and review on content only.
