# Reproducibility manifest

## Frozen inputs and environment

- Run date: 2026-08-26; timezone: Asia/Shanghai.
- Working directory: `/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2`.
- Authoritative prompt: `PROMPT.md`; SHA-256 `0ab0af8e6936c0597626493029004dc4f8851bf79e5f6ae4076ccc2605d012a7`.
- Skill: `.agents/skills/rigorous-open-math-research/SKILL.md`; SHA-256 `abc45897207d4bd445282ccfeb2b53840cb45a1fb956d9c312264c2426e0252f`.
- Restrictions obeyed: no internet; no read outside the current directory; no user questions; no more than three concurrent subagents. `/tmp` was used only for an ephemeral command-output hash, never as a proof source.
- OS/tools: Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; GNU bash `5.3.9`; Python `3.14.4`.
- Git: `git status` and `git rev-parse` report that this is not a Git repository, despite a read-only `.git` directory entry; no commit or clean-tree receipt exists.
- Random seeds: none. All mathematical computation used exact Python integers.
- Network calls/external sources: none.
- Unknown: model build identifier and host package lock were not exposed.

## Proof and audit package

- `candidate_proof.md`: `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`.
- `subagents/direct_coupling.md`: `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c`.
- `subagents/range_translation.md`: `07f2c63d3a0670fff434b78778c35ddfecc1ffdb41dc8c7c1b3fa70b9890d5e7`.
- `subagents/partial_validator.md`: `82f3f1b8261ea9c6d75af2d01cc25c6ab758713581771eab1c361006fa797542`.
- `subagents/aggregate_coarea.md`: `537b367fb01bd1175781daa3e543273e0912a9a2d3c266b359d0ff8d03e22fff`.
- `subagents/global_audit.md`: `ba55ad7ed8a2f05a458b45f9ada841aa8fe28ad92fbd3c0040a6a82bace2d82a`.
- `audit_report.md`: `0a7265fce21890e2cb2f1b60e2486f31a87af82740ff5894eee48b5251fafdbd`.
- `final_report.md`: `7dcfd080ac2b5372795280fbe80581e82e80f3fae103eb79459fc3608a98781b`.

The global audit is content-bound to the listed candidate hash and returned `PASS` only for the explicit partial theorem. The original target remains incomplete.

## Code and replay

- `reproducibility/enumerate_triples.py`: `fa0e24f8af0c9709f17dbfb2392000636f4b6d2bf3888e6f5c71b1c5fa8dd391`.
- `reproducibility/audit_exact.py`: `0b1efa20baed0081cd549444aa5001502fe9b19352166baacbd43fdd9d90ccbf`.

Commands:

```text
python3 -m py_compile reproducibility/enumerate_triples.py reproducibility/audit_exact.py
python3 reproducibility/enumerate_triples.py 40
python3 reproducibility/audit_exact.py 100
sha256sum -c artifact_hashes.sha256
```

Expected final audit output:

`PASS exact finite identities and conjecture probes for 0<=t<=100`

The finite AVI and MC assertions are discovery/falsification checks, not proof bridges. General conclusions use only the natural-language proofs audited in the hash-bound package.

## Subagent provenance

- `SUB-O3b-COUPLE`: returned a hash-checked reflection-coupling obstruction and exact lamp-kernel module.
- `SUB-VAL-RANGE`: independently validated the one-sided/log module and localized one non-load-bearing false recurrence display.
- `SUB-O3f-AVI`: returned the hash-checked killed-kernel/image/coarea reduction.
- `SUB-AUDIT-U2-GLOBAL`: fresh first-time adversarial audit, `PASS` for the partial theorem.
- `SUB-O3e-MC`: stopped at the resource boundary without a returned artifact; no result from it was merged.

## Formalization status

No `lean-proof/` or other proof-assistant project exists in the current directory, so no scaffold or machine proof was produced. See `formalization_progress.md`. This is an independently audited natural-language partial proof, not a formally verified result.
