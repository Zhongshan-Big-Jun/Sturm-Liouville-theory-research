# Structural Verification Results (Phases 1–5) — Decomposition Mode

**Problem:** /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-c-qed-replacement1/output/problem.tex  
**Proof:** /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-c-qed-replacement1/output/decomposition/attempt_1/revision_1/proof_1/proof.md  
**Decomposition:** /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-c-qed-replacement1/output/decomposition/attempt_1/revision_1/decomposition.yaml  
**Mode:** Structural verification (Phases 1–5)

---

## Phase 1: Problem-Statement Integrity

**Status:** PASS

**Original problem (from /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-c-qed-replacement1/output/problem.tex):**

```text
# Frozen main task: H^s operator-domain vs abstract completion

Let `K_c = -d^2/dx^2 + c` on `[-1,1]` with Krein boundary condition
`f'(±1) = (f(1)-f(-1))/2`, `c > 0`. Let `H^s`, `s >= 4`, be the left-definite
space associated with `K_c`. Let `{Q_n^(s)}` be the SL_hs orthogonal polynomial
system defined via the isometries `K_c^{-r}` on `L^2` or `H^1`.

Prove or disprove, for integer `s >= 4`:

1. Give a necessary and sufficient condition for `Q_n^(s) ∈ D(K_c^(s/2))`.
2. Determine whether the operator-domain completion `D(K_c^(s/2))` equals the
   abstract completion obtained from the left-definite inner product on
   polynomials.
3. Determine whether `span{Q_n^(s)}` is dense in `D(K_c^(s/2))` under the
   operator-domain reading.

The complete polynomial degree spectrum is a bonus, not a completion gate.

Rules: do not inspect repository history, current project files, known solution,
or network. State all external theorems with hypotheses. Numerical evidence is
not proof.
```

**Problem as stated/implied in proof:** The proof reproduces the same text verbatim in its “Problem Statement” section.

**Discrepancies:** None — exact match. No quantifier, hypothesis, domain, boundary condition, exponent, or requested conclusion was changed.

---

## Phase 2: Completeness and Originality Check

### 2a. Questions Addressed

**Questions/tasks identified in problem:** 3 total

| # | Question/Task | Addressed | Location in Proof |
|---|---------------|-----------|-------------------|
| 1 | Give a necessary and sufficient condition for \(Q_n^{(s)}\in D(K_c^{s/2})\). | YES | STEP3 gives the trace criterion; STEP6 gives the complete degree classification; GOAL item 1 summarizes both. |
| 2 | Determine whether the operator-domain completion equals the abstract polynomial completion. | YES | STEP7 distinguishes unitary equivalence via \(J_s\) from equality under the identity realization; GOAL item 2 states the answer. |
| 3 | Determine density of \(\operatorname{span}\{Q_n^{(s)}\}\) under the operator-domain reading. | YES | STEP8 treats the literal span, the individually admissible subsystem, and the domain intersection; GOAL item 3 summarizes these interpretations. |

**All questions addressed:** YES  
**Any acknowledged gap/hole:** NO

The proof does not announce an unproved assertion, defer a required case, or claim that any required plan step is impossible.

### 2b. Originality Check

**Contains original proof work:** YES

**Evidence of genuine reasoning:** The document contains substantial arguments rather than a bibliography or theorem list. Structurally significant work includes:

- deriving the form identity, operator domain, power-domain trace conditions, and norm comparison in STEP1;
- transporting polynomial orthogonality through \(L^m\) in STEP2;
- deriving separate even- and odd-order energy obstructions in STEP4 and STEP5;
- constructing and analyzing the nonidentity completion map \(J_s\) in STEP7;
- constructing a finite-dimensional trace right inverse and corrected polynomial approximants in STEP8.

**Issues found:** None at the structural/originality level. Mathematical correctness of individual deductions is reserved for Phase 6.

**Phase 2 overall:** PASS

---

## Phase 3: Citation Verification

**Citations found:** 1 total

**Citation format check:** PASS. The citation contains all required fields in the prescribed order: `type`, `label`, `title`, `authors`, `source_url`, `verifier_locator`, `statement_match`, `statement`, and `usage`.

### Citation 1: Offline related-work status

**Source:** “Offline related-work status,” authors stated as “not supplied”  
**URL check:** Unable to verify. `related_info/related_work.md` is a relative local path, and that source file was not included in the supplied materials. Repetition of the citation inside `decomposition.yaml` is not independent source verification.  
**Statement check:** Not found independently. The claimed “opening paragraph” cannot be inspected, so the asserted exact match cannot be confirmed.  
**Usage check:** Correct at the structural level. It is used only as a related-work/status declaration and not as a mathematical theorem supporting a proof step.  
**Verdict:** UNABLE_TO_VERIFY

**Citation Summary:**

| # | Label | Source verified | Statement matches | Usage correct | Verdict |
|---|-------|-----------------|-------------------|---------------|---------|
| 1 | Offline related-work status | NO | UNVERIFIED | YES | UNABLE_TO_VERIFY |

**Phase 3 overall:** FAIL

The required independent citation verification cannot be completed. A citation does not become verified merely because the decomposition file repeats the same metadata and statement.

---

## Phase 4: Decomposition Plan Adherence

### 4a. Decomposition Structure

**Source nodes:**

- S1 — “Offline related-work status,” asserting that no external mathematical result is supplied and that the proof must be self-contained.

**Steps in decomposition plan:** 8 total

- STEP1 — operator/form domains and trace conditions
- STEP2 — algebraic left-definite polynomials
- STEP3 — reduction to a one-step boundary condition
- STEP4 — even-order obstruction
- STEP5 — odd-order obstruction
- STEP6 — complete degree spectrum
- STEP7 — abstract versus operator-domain completion
- STEP8 — density under operator-domain interpretations

**Target:** GOAL — answer all three questions in the frozen main task.

**Key steps:** STEP4, STEP5, STEP7

**Proof order:** STEP1, STEP2, STEP3, STEP4, STEP5, STEP6, STEP7, STEP8, GOAL

The aggregated proof follows this order exactly.

### 4b. Step Format and Coverage

| Step ID | Header Found | Claim Stated | Proof Present | Dependencies Listed | Is Key Step | heuristics given | Issues |
|---------|--------------|---------------|---------------|---------------------|-------------|------------------|--------|
| STEP1 | YES | YES | YES | YES | NO | N/A | None |
| STEP2 | YES | YES | YES | YES | NO | N/A | Its dependency line omits the plan’s nonmathematical status node S1, although S1 is cited globally and STEP1 is listed. This is a minor metadata mismatch, not a missing mathematical dependency. |
| STEP3 | YES | YES | YES | YES | NO | N/A | None |
| STEP4 | YES | YES | YES | YES | YES | YES | None |
| STEP5 | YES | YES | YES | YES | YES | YES | None |
| STEP6 | YES | YES | YES | YES | NO | N/A | None |
| STEP7 | YES | YES | YES | YES | YES | YES | None |
| STEP8 | YES | YES | YES | YES | NO | N/A | None |

The GOAL section is also present, has an explicit claim and proof summary, and lists STEP6, STEP7, and STEP8 as required.

**All steps properly formatted:** YES  
**All steps addressed:** YES

### 4c. Key Steps Treatment

| Key Step | Rigorous Treatment | Marked with `<key-original-step>` | Hand-waving Found | Issues |
|----------|---------------------|-----------------------------------|-------------------|--------|
| STEP4 | YES | YES | NO | Contains an explicit contradiction argument and displayed energy identity. |
| STEP5 | YES | YES | NO | Contains an explicit form-orthogonality argument and displayed conclusion. |
| STEP7 | YES | YES | NO | Supplies a polynomial approximation lemma, isometry computations, density argument, and nonidentity example. |

Each key step is immediately followed by a `<heuristics>...</heuristics>` block.

**Key steps adequately addressed:** YES, at the structural level. This does not certify the correctness of every mathematical deduction.

### 4d. Deviations

**Declared deviations in proof:** “None — followed the decomposition plan.”

**Undeclared deviations found:** None significant. Auxiliary arguments introduced inside STEP1, STEP7, and STEP8 support the planned claims rather than replace or bypass them. The STEP2 dependency line’s omission of S1 is a minor documentation mismatch only.

**Deviations justified:** N/A

### 4e. Source Usage

**Sources from plan used:** S1

**Sources used correctly:** YES as to its intended structural role. S1 is used solely to declare the absence of imported external mathematical results. Its authenticity remains independently unverifiable, as recorded in Phase 3.

### 4f. Refuted Plan Steps (prover complaints against the decomposition)

**Complaints found:** None

None — the proof did not claim any plan step is false, impossible, circular, or unprovable as stated.

**Summary for regulator:**

- **Verified refutations** (plan step is genuinely broken): None
- **Unsupported complaints** (prover gave up without evidence): None
- **Refuted complaints** (prover's complaint is wrong — step is fine): None

**Phase 4 overall:** PASS

---

## Phase 5: Additional Verification Rules

**Rules found:** None. No non-empty `additional_verify_rule_global.md` content was included among the supplied inputs.

**Phase 5 overall:** PASS (no rules)

---

## Summary

| Check | Status |
|-------|--------|
| Phase 1: Problem-Statement Integrity | PASS |
| Phase 2: Completeness and Originality Check | PASS |
| Phase 3: Citation Verification | FAIL |
| Phase 4: Decomposition Plan Adherence | PASS |
| Phase 5: Additional Verification Rules | PASS |

### Overall Verdict: FAIL

### Failed Items (if any):

1. The sole citation cannot be independently verified because its cited source, `related_info/related_work.md`, was not supplied. Its URL, title/authorship metadata, locator, and claimed exact statement therefore remain unverified.

### Specific Issues to Fix (if FAIL):

1. Supply `related_info/related_work.md` at a resolvable path and ensure its opening paragraph exactly matches the citation’s `statement` field.
2. Alternatively, remove or replace the unverifiable citation with a source that the verifier can inspect, while preserving the decomposition’s self-contained-proof requirement.