# Pilot v6 H^s-domain OOD three-arm preregistration

Registered: 2026-08-28, before any pilot v6 solver call.

## Objective

Evaluate the optimized research plugin on the previously unrun main task from
`runs/three-arm-pilot-v2/blind-main/task.md`. The task concerns membership in
the operator domain of powers of the Krein Sturm-Liouville operator, equality
with an abstract polynomial completion, and density of the transported
orthogonal system.

This task has a historical project answer at hidden-gold commit `0f9b2b0` and
a blind-start commit `e9aee2c`. Solvers receive neither commit, repository
history, project files, prior answer, nor network access. The task SHA256 is
`359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.

The coordinator saw only commit metadata before registration. No solver has
received mathematical content from the hidden gold. This is OOD relative to
the isolated solver context and the v1.7 optimization task, not a claim that
the problem is historically new to the project.

## Arms

| Arm | Frozen system |
| --- | --- |
| A | `gpt-5.6-sol`, `xhigh`, rigorous-open-math-research v1.7.0 at parent commit `957d80b7f1c58b60972a4ece87945cd93c0a1476`, at most 3 concurrent research children |
| B | Same model and reasoning, task prompt only, no skills, plugins, memories, agents, apps, browser, computer use, or network |
| C | Same model and reasoning through QED commit `121900964e6572aaf094412d434b5ac2a792a65f`, offline content-inline adapter, one decomposition, one proof attempt, one revision |

All arms use Codex CLI `0.149.0-alpha.4.3`, SHA256
`1c8b7f5221f6779c1e689b00bfa2dd95503f2aa595b9e6c752550ddd8ddf26b6`.

## Run count and schedule

One scored run per arm, in order A, B, C. A replacement is permitted only for
an infrastructure-invalid launch and must use a fresh work root. No score is
assigned to an infrastructure-invalid run. Additional repetitions require a
new preregistration and are not inferred from the first-round outcome.

## Budgets

- Arm A: 75 minute root wall cap, maximum 3 research child sessions.
- Arm B: 45 minute wall cap, no child session.
- Arm C: 90 minute pipeline wall cap.
- One arm at a time because all arms share the account quota.
- The user reports both quota windows fully reset and has previously removed
  the emergency reserve. A run may use the active window until its wall cap or
  service hard limit, whichever occurs first.

## Isolation

- Fresh external root: `F:\benchmark\PILOT-V6-HS-DOMAIN-20260828`.
- Fresh `CODEX_HOME` and work directory per arm.
- No `.git`, `AGENTS.md`, project memory, sibling outputs, hidden gold, or
  repository path in a solver work directory.
- Model-side network is disabled. QED literature metadata is preseeded with an
  explicit offline/unknown status and contains no mathematical hint.
- A and B prompts are frozen before launch. C receives the same task content
  in its required `problem.tex` path.
- Posthoc audits and hidden-gold comparisons are outside scored usage and are
  never copied into a live arm.

## Completion and scoring

Required mathematical gates:

1. a necessary and sufficient condition for
   `Q_n^(s) in D(K_c^(s/2))` for every integer `s>=4`;
2. a correct equality or non-equality decision for operator-domain and
   abstract completions, with the precise interface;
3. a correct density decision for `span{Q_n^(s)}` under the operator-domain
   reading.

The complete polynomial-degree spectrum is bonus only.

Score out of 100:

- mathematical correctness and closure: 40;
- contract fidelity and completeness: 20;
- strict progress over the blind statement: 15;
- epistemic calibration: 10;
- evidence and citation fidelity: 10;
- reproducibility: 5.

Acceptance requires score at least 70, correctness at least 32/40, and no
`FATAL_GAP`, `WRONG_PROBLEM`, circular load-bearing lemma, fabricated source,
or numerical-evidence-as-proof error.

Every arm first receives a label-blind audit against the frozen contract.
Only after all solver artifacts are frozen may a separate evaluator inspect
hidden gold and score agreement or genuinely stronger audited mathematics.

## Infrastructure amendment log

The initial Arm C launch at `arm-c-qed-run1` exited before any model process was created. QED commit
`1219009` unconditionally checks that executables named `claude` and `python3` exist, although the
frozen configuration assigns every active role to Codex. The launch produced no wrapper log, no
Codex session, and no mathematical output, so it is classified `INFRA_INVALID` and excluded.

Before the permitted fresh-root replacement, the harness was amended only as follows:

- add a fail-closed executable named `claude` that exits 70 if it is ever invoked;
- parameterize the C work root and `CODEX_HOME` names;
- preserve every frozen provider, model, effort, prompt, QED commit, budget, isolation rule, and run count.

The replacement roots are `arm-c-qed-replacement1` and `codex-home-c-replacement1`. The shim only
satisfies QED's unconditional `which` check and cannot produce a model response.

## Stage reporting

After every arm report wall time, sessions, responses, tools, token metrics,
quota before/after when exposed, result label, strongest exact claim, audit
status, and first remaining gap. All useful audited mathematics is archived
and committed even if the global benchmark target is not completed.
