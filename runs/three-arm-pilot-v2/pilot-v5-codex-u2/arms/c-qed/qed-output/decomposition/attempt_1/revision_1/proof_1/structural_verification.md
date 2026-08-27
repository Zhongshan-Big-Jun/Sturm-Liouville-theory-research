# Structural Verification Results (Phases 1–5) — Decomposition Mode

**Problem:** /mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run3/output/problem.tex  
**Proof:** /mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run3/output/decomposition/attempt_1/revision_1/proof_1/proof.md  
**Decomposition:** /mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run3/output/decomposition/attempt_1/revision_1/decomposition.yaml  
**Mode:** Structural verification (Phases 1–5)

---

## Phase 1: Problem-Statement Integrity

**Status:** PASS

**Original problem (from /mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run3/output/problem.tex):**

~~~~text
# Frozen task: U2 total-variation asymptotics

Blind benchmark. Do not inspect any repository, git history, internet source, external memory,
prior benchmark output, or prior solution to this exact problem. Scratch exact or numerical
computation may be used only for falsification. Numerical evidence does not constitute proof.

Let `Z_2 wr Z` be the lamplighter group. Write each state as `(eta,z)`, where
`eta: Z -> Z_2` has finite support and `z in Z` is the base position. Let `0` denote the
all-zero lamp configuration.

Consider the discrete-time switch-walk-switch chain. From `(eta,z)`, independently resample the
lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each,
then independently resample the lamp at the arrival site from `Bernoulli(1/2)`. Let `P_t^x`
denote the law at integer time `t>=0` started from `x`.

Set

```text
x=(0,0),
y=(0,2).
```

Thus both initial lamp configurations are all zero, and the two initial base positions are `0`
and `2`.

Prove that there are explicit constants `0<c<=C<infinity` and an explicit integer `t_0` such
that, for every integer `t>=t_0`,

```text
c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t).
```

Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1`
distance on the countable state space.

State every external theorem in the exact form used and verify all hypotheses. Audit parity,
small times, the effect of the two forced initial zero lamps, and every conditioning or
coupling step. Do not replace the chain by a different lamp convention or interpret `(0,2)` as
a lamp lit at site `2`.

A complete result requires both bounds with explicit constants. If incomplete, return the
strongest exact partial result and the first unresolved obligation without claiming completion.
~~~~

**Problem as stated/implied in proof:** The proof reproduces the complete problem statement verbatim. Its GOAL section states:

> **Claim:** There are explicit constants \(0<c\leq C<\infty\) and an explicit integer \(t_0\) such that
> \[
> \frac c{\sqrt t}
> \leq\|P_t^x-P_t^y\|_{\rm TV}
> \leq\frac C{\sqrt t}
> \qquad(t\geq t_0).
> \]

The proof then expressly limits its actually established result to:

> \[
> \boxed{
> \frac1{2\sqrt t}
> \leq\|P_t^x-P_t^y\|_{\rm TV}
> \leq\frac{5+3\log t}{\sqrt t}
> \qquad(t\geq1).
> }
> \]

**Discrepancies:** None in the stated problem—the statement is reproduced exactly, with the same chain, initial states, quantifiers, domain, and requested bounds. The actually proved theorem is weaker, but the proof admits that fact rather than silently weakening the problem. That is a fatal completeness issue under Phase 2, not a problem-statement alteration.

---

## Phase 2: Completeness and Originality Check

### 2a. Questions Addressed

**Questions/tasks identified in problem:** 9 total

| # | Question/Task | Addressed | Location in Proof |
|---|---------------|-----------|-------------------|
| 1 | Establish an explicit lower bound \(c/\sqrt t\) for all sufficiently large integer \(t\) | YES | STEP8 and STEP10; \(c=1/2,\ t_0=1\) |
| 2 | Establish an explicit upper bound \(C/\sqrt t\) with constant \(C<\infty\) independent of \(t\) | NO | STEP6, STEP7, STEP10, and GOAL explicitly say this remains unresolved |
| 3 | Supply explicit constants and an explicit threshold | PARTIAL | \(c=1/2\) and \(t_0=1\) are supplied; no valid constant \(C\) for the required upper bound is established |
| 4 | State external results exactly and verify their hypotheses | PARTIAL | Definitions are cited in STEP1–STEP2; one source citation cannot be independently verified |
| 5 | Audit parity | YES | STEP3, STEP5, and STEP8 |
| 6 | Audit small times | YES | STEP9 |
| 7 | Audit the effect of the two forced initial zero lamps | YES | STEP1 and STEP9 |
| 8 | Audit conditioning/coupling and retain the specified lamp convention | YES | STEP1, STEP2, STEP6 substitute, and STEP9 |
| 9 | If incomplete, report the strongest partial result and first unresolved obligation without claiming completion | YES | Status, STEP10, GOAL, and “First Unresolved Obligation” |

**All questions addressed:** NO  
**Any acknowledged gap/hole:** YES

The proof repeatedly acknowledges that STEP6, the constant-order upper bound, STEP7’s planned conclusion, STEP10, and GOAL are unproved. This alone prevents publication as a proof of the stated result.

### 2b. Originality Check

**Contains original proof work:** YES

**Evidence of genuine reasoning:** STEP1–STEP5 contain explicit conditional-law, kernel-contraction, path-counting, inclusion-exclusion, image-kernel, and binomial arguments. STEP6 also supplies a new reflection-coupling substitute and derives a logarithmically weaker estimate. These are substantive arguments rather than a bibliography or a list of unproved external theorems.

**Issues found:** Genuine work is present, but it does not close the central obligation. The proof itself says, “The required constant upper bound is not proved” and “the original main result remains incomplete.”

**Phase 2 overall:** FAIL

---

## Phase 3: Citation Verification

**Citations found:** 3 total

All three citations contain the required fields in the required order: `type`, `label`, `title`, `authors`, `source_url`, `verifier_locator`, `statement_match`, `statement`, and `usage`.

### Citation 1: Offline literature status

**Source:** *Related work under the blind offline protocol*, QED benchmark  
**Format check:** PASS  
**URL check:** Unable to verify. The cited target `related_info/related_work.md` was not supplied among the available source contents.  
**Statement check:** The quoted statement appears in decomposition source node S0, but that does not independently establish an exact match with the separately claimed source file.  
**Usage check:** Conditionally appropriate if the source statement is genuine; it is used only to explain why estimates are supplied self-containedly.  
**Verdict:** UNABLE_TO_VERIFY

### Citation 2: Switch-walk-switch transition

**Source:** *Frozen task: U2 total-variation asymptotics*, QED benchmark problem setter  
**Format check:** PASS  
**URL check:** Works as a local source reference to the supplied `problem.tex`.  
**Statement check:** Matches the transition-definition sentence in `problem.tex` word-for-word.  
**Usage check:** Correct. It is used to identify the independent last resampling at each visited site.  
**Verdict:** PASS

### Citation 3: Total variation convention

**Source:** *Frozen task: U2 total-variation asymptotics*, QED benchmark problem setter  
**Format check:** PASS  
**URL check:** Works as a local source reference to the supplied `problem.tex`.  
**Statement check:** Matches the total-variation sentence in `problem.tex` word-for-word.  
**Usage check:** Correct. It is used for the direct countable-state kernel-contraction calculation.  
**Verdict:** PASS

**Citation Summary:**

| # | Label | Source verified | Statement matches | Usage correct | Verdict |
|---|-------|-----------------|-------------------|---------------|---------|
| 1 | Offline literature status | NO | UNABLE TO CHECK AGAINST CLAIMED SOURCE | CONDITIONAL | UNABLE_TO_VERIFY |
| 2 | Switch-walk-switch transition | YES | YES | YES | PASS |
| 3 | Total variation convention | YES | YES | YES | PASS |

**Phase 3 overall:** FAIL

A structural verification cannot certify all citations when one claimed source is unavailable for independent comparison. Repetition of the statement inside the decomposition is not verification of the cited source.

---

## Phase 4: Decomposition Plan Adherence

### 4a. Decomposition Structure

**Source nodes:**

- S0: Offline literature-status statement.
- S1: Switch-walk-switch transition definition.
- S2: Total-variation convention.

**Steps in decomposition plan:** 10 total  
**Target:** GOAL  
**Key steps:** STEP6  
**Proof order:** STEP1, STEP2, STEP3, STEP4, STEP5, STEP6, STEP7, STEP8, STEP9, STEP10, GOAL

### 4b. Step Format and Coverage

| Step ID | Header Found | Claim Stated | Proof Present | Dependencies Listed | Is Key Step | heuristics given | Issues |
|---------|--------------|---------------|---------------|---------------------|-------------|------------------|--------|
| STEP1 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP2 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP3 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP4 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP5 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP6 | YES | YES | NO | YES | YES | YES | Planned diagonal-variation claim explicitly unresolved; only a weaker substitute is proved |
| STEP7 | YES | YES | PARTIAL | YES | NO | N/A | \(A_t\le144/\sqrt t\) is not established |
| STEP8 | YES | YES | YES | YES | NO | N/A | Listed dependencies differ from the plan: STEP2 is used in place of the planned direct S1/S2 dependency |
| STEP9 | YES | YES | YES | YES | NO | N/A | None structurally |
| STEP10 | YES | YES | PARTIAL | YES | NO | N/A | Required constant upper bound is explicitly unproved |

**Target coverage:** The GOAL header and claim are present, but its proof status explicitly says the main result is incomplete.

**All steps properly formatted:** NO. STEP6, STEP7, and STEP10 use “Proof status” because their planned claims are not proved; this is honest reporting but not completed step-proof format.

**All steps addressed:** NO. Sections exist for every step, but STEP6 and the dependent upper-bound conclusions are not proved.

### 4c. Key Steps Treatment

| Key Step | Rigorous Treatment | Marked with `<key-original-step>` | Hand-waving Found | Issues |
|----------|---------------------|-----------------------------------|-------------------|--------|
| STEP6 | NO for the planned claim | PARTIAL | NO proof is falsely presented as complete | The tags wrap the weaker coupling lemma, not the planned \(A_t\le144/\sqrt t\) claim. The required key argument is absent. |

**Key steps adequately addressed:** NO

The proof deserves no credit for merely identifying the hard step and then proving a weaker statement. The key step was the whole point of the decomposition.

### 4d. Deviations

**Declared deviations in proof:**

- STEP6’s planned diagonal-variation estimate is not asserted.
- A reflection-coupling estimate \(A_t\le(5+3\log t)/\sqrt t\) is supplied instead.
- STEP7, STEP10, and GOAL are consequently reported as incomplete.
- The “Deviations from Decomposition Plan” section expressly identifies the STEP6 replacement.

**Undeclared deviations found:**

- STEP8’s dependency list differs from the decomposition: the proof lists STEP2 and STEP5 instead of S1, S2, and STEP5.
- The key-original-step tags mark the substitute coupling lemma rather than the planned key claim.

**Deviations justified:** NO. The proof explains why it chose the weaker substitute, but a justified deviation must still produce a complete proof. This one does not.

### 4e. Source Usage

**Sources from plan used:** S0, S1, S2

**Sources used correctly:** NO

S1 and S2 are faithfully quoted and used as definitions. S0 is cited, but its claimed source cannot be independently checked. Thus source usage cannot be certified in full.

### 4f. Refuted Plan Steps (prover complaints against the decomposition)

**Complaints found:** 1 total

**Verbatim complaint:**

> “The first inequality in (6.1) is not proved by STEP4 and STEP5 alone. Substitution of the image formula produces several signed families with different image periods \(2d\), \(2(d+1)\), and \(2(d+2)\). Applying the triangle inequality before reconciling these periods loses the cancellation needed for \(t^{-1/2}\). The decomposition asks for a summation-by-parts identity performing that reconciliation, but does not supply the identity or its boundary terms. Consequently, asserting (6.1) here would be circular.”

| # | Step ID | Complaint Type | Prover Evidence (quote) | Independent Verdict | Verifier Reasoning |
|---|---------|----------------|-------------------------|---------------------|--------------------|
| 1 | STEP6 | ABANDONED | “The decomposition asks for a summation-by-parts identity performing that reconciliation, but does not supply the identity or its boundary terms. Consequently, asserting (6.1) here would be circular.” | UNSUPPORTED | No counterexample to STEP6 is supplied. No circular dependence through GOAL is identified, and no no-go argument shows that the suggested image/summation route cannot work. The observation that a premature triangle inequality loses cancellation merely explains why the step is difficult. A decomposition strategy is not required to contain the missing proof—the prover was supposed to produce it. The logarithmic coupling bound also does not show that the planned estimate is false or unattainable. |

**Summary for regulator:**

- **Verified refutations** (plan step is genuinely broken): None
- **Unsupported complaints** (prover gave up without evidence): STEP6
- **Refuted complaints** (prover's complaint is wrong — step is fine): None

The independent verdict does not establish that STEP6 is true; it establishes only that the prover supplied no valid refutation or no-go result against it.

**Phase 4 overall:** FAIL

This failure is based on the absent key-step proof and incomplete dependent steps, not merely on the existence of a complaint.

---

## Phase 5: Additional Verification Rules

**Rules found:** None. No non-empty additional verification-rule content was supplied.

**Phase 5 overall:** PASS (no rules)

---

## Summary

| Check | Status |
|-------|--------|
| Phase 1: Problem-Statement Integrity | PASS |
| Phase 2: Completeness and Originality Check | FAIL |
| Phase 3: Citation Verification | FAIL |
| Phase 4: Decomposition Plan Adherence | FAIL |
| Phase 5: Additional Verification Rules | PASS |

### Overall Verdict: FAIL

### Failed Items (if any):

1. The proof does not establish the required \(C/\sqrt t\) upper bound with a constant independent of \(t\).
2. STEP6—the sole key step—is explicitly unproved.
3. STEP7, STEP10, and GOAL consequently remain incomplete.
4. The proof’s complaint against STEP6 is unsupported: it identifies difficulty, not a false, impossible, circular, or structurally broken plan step.
5. The “Offline literature status” citation cannot be independently verified against its claimed source.
6. The `<key-original-step>` tags wrap a weaker substitute rather than the decomposition’s actual key claim.
7. STEP8’s dependency change is not declared.

### Specific Issues to Fix (if FAIL):

1. Prove STEP6’s explicit diagonal-variation estimate, including the claimed signed cancellation, image-period reconciliation, and boundary terms; alternatively, replace it with another complete self-contained \(O(t^{-1/2})\) argument.
2. Once STEP6 is established, complete STEP7, STEP10, and GOAL with explicit constants.
3. Do not characterize an omitted proof as a refutation of the decomposition unless a genuine counterexample, no-go theorem, or circular dependency is supplied.
4. Place `<key-original-step>` tags around the proof of the actual planned key claim, not merely around a weaker replacement.
5. Make `related_info/related_work.md` available for exact verification or remove the unverifiable citation.
6. Align STEP8’s dependencies with the decomposition or disclose and justify the change.