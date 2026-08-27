# Reproducibility manifest

- Benchmark ID: `PILOT-V5-CODEX-U2-20260825`.
- Preregistered at repository commit: `9b1ae2f`.
- Repository branch: `main`.
- Pre-existing untracked files: `scratch_1d_numeric.py`, `scratch_1d_numeric2.py`.
- Frozen task: `frozen_task.md`.
- Frozen task sha256: `6859E0AF922BA8454758E2195FCEFCFE8FA164A40E2C23022EC7EBB2DA228943`.
- Arm A prompt: `arm-a-prompt.md`.
- Arm A prompt sha256: `0AB0AF8E6936C0597626493029004DC4F8851BF79E5F6AE4076CCC2605D012A7`.
- Arm A model: `gpt-5.6-sol`.
- Arm A reasoning effort: `xhigh`.
- Arm A plugin: installed `rigorous-open-math-research` v1.6.0 plugin cache.
- Arm A plugin SKILL.md sha256: `ABC45897207D4BD445282CCFEB2B53840CB45A1FB956D9C312264C2426E0252F`.
- Excluded source: the separate personal skill directory has a different hash and is not copied into the arm.
- Arm A maximum subagent concurrency: `3`.
- Network during blind discovery: disabled.
- Primary quota at preregistration: `3` percent used, `300` minute window.
- Secondary quota at preregistration: `0` percent used, `10080` minute window.
- Primary reset observed: `2026-08-26 04:16:38 +08:00`.
- Secondary reset observed: `2026-09-01 23:16:38 +08:00`.
- Unknown field: account plan type was not exposed by local rate-limit telemetry.

## Completed-arm bindings

- Arm A scored thread: `01a03b91-c0d3-7792-ab90-c80bb7b40e46` plus seven child sessions.
- Arm A candidate SHA256: `C76537D71604F3F5402D520423BCB045B8E203B4FC967C6FB8D1EBBF8ABF043B`.
- Arm B Codex CLI: `0.149.0-alpha.4.3`.
- Arm B candidate SHA256: `3B50DCBFD96EA8F0BF746F419E8D4E4AC43F8BAED76EE66A66F6399BEF8AA761`.
- Arm C QED commit: `121900964e6572aaf094412d434b5ac2a792a65f`.
- Arm C Codex CLI: `0.149.1`.
- Arm C QED source export contained no `.git` directory and was verified before launch.
- Arm C prompt probe SHA256: `6DB0A0B35F9BB0BC63E4F03095506A6386FE90FA11E648B008BDBF2866642738`.
- Arm C offline wrapper SHA256: `54E987AFF2E18849F072AFFB937CCEE08FF9237A971E720F723F817498A61826`.
- Arm C inline adapter SHA256: `AD7E8B6986C611819F2C73FF3D2EF122ECED928273D571CAE5CF0918D8EA9D79`.
- Arm C model-visible tools, skills, plugins, memories, network, and subagents: disabled.
- Arm C candidate SHA256: `A528FECC631800697BC35A626BA7B562F145D254DD1DFAA99D313A6557000AAC`.
- Arm C scored event span: `2026-08-27T00:53:14.911Z` to `2026-08-27T01:29:53.781Z`.
- Arm C parser normalization: the unchanged decomposer response replaced a 55-byte scalar
  produced by QED's first-fence fallback parser. Both files are retained.
- Arm C raw sessions: retained outside git because they contain encrypted model internals.
  Seven sanitized telemetry files are committed.
- External label-blind audits for all arms are post-hoc and excluded from scored usage.
