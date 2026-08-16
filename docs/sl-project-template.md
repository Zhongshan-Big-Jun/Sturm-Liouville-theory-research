# Sturm-Liouville Research Project Template

Use this template when bootstrapping a new Sturm-Liouville (SL) spectral
optimization project with the `math-research-dsh` plugin set. It mirrors the
layout used by the BVE research project and satisfies the
`manage-math-research-program` / `rigorous-open-math-research` / `lean-verify`
contracts.

## Minimal directory layout

```text
.
├── AGENTS.md                  # rules + session pointer (keep small)
├── PROJECT.md                 # ownership, research directions, key files
├── project.json               # git_sync.push_order
├── docs/                      # LaTeX proofs and summaries
├── scripts/                   # numeric/verification scripts (EVIDENCE only)
├── tools/                     # reusable math tools (Obsidian-compatible md)
├── papers/                    # reference PDFs and human-readable proof LaTeX
├── runs/                      # rigorous-open-math-research run roots
├── state/                     # manager-owned state, checkpoints, session logs
├── knowledge/                 # accepted-knowledge pipeline
├── literature/                # curated literature records
├── lean-proof/                # Lean 4 formalization project
└── .gitignore                 # ignore __pycache__, .lake, temp artifacts
```

## AGENTS.md skeleton

```markdown
# AGENTS.md

## 项目目标
- 定义 SL 边值问题与优化类 (势/权/边界).
- 检索前沿文献, 记录证明技术.
- 严格区分 STRICT / EVIDENCE / 猜想.

## 当前关注问题
1. <open problem 1>
2. <open problem 2>

## 工作方法
1. 进入项目先读 AGENTS.md.
2. 数学研究调用 `$rigorous-open-math-research`.
3. 项目管理调用 `$manage-math-research-program`.
4. Lean 验证调用 `$lean-verify`.
5. 任何断言如实标注严格性.

## 会话记录
- 完整历史会话日志: `state/AGENTS_SESSION_LOG.md`.
```

## Research workflow contract

1. **管理**: `manage-math-research-program` initializes the workspace,
   maintains literature/tools/state, and dispatches task packets.
2. **研究**: `rigorous-open-math-research` owns each run under `runs/` with
   `problem_contract.md`, `research_ledger.md`, `candidate_proof.md`,
   `audit_report.md`, `run-manifest.json`.
3. **验证**: `lean-verify` audits Lean formalizations; only
   `FORMALLY_VERIFIED` results may be called machine-verified.
4. **交付**: after Lean verification, `manage-math-research-program`
   workflow 8c requires `papers/<SLUG>/<SLUG>-en.tex` and `<SLUG>-zh.tex`.

## Conventions

- All text: UTF-8, no BOM, LF, English punctuation.
- Numeric scripts: header documents precision and that they are EVIDENCE.
- Git sync: `project.json` declares `git_sync.push_order`; use
  `scripts/sync_remotes.py` or the documented git commands.
- Keep AGENTS.md small; move long session logs to `state/AGENTS_SESSION_LOG.md`.
