# v1.7 regression continuation preflight

- Registered: `2026-08-27T12:31:29Z`.
- User-reported remaining quota: 57 percent of the five-hour window and 11
  percent of the weekly window.
- Root session: `01a041fc-0f14-79b3-86b3-aef3d4aa1b8a`.
- First-segment root wall: 1311.844 seconds.
- Continuation root wall cap: 1727 seconds.
- Total target-preserving root wall cap: 3038.844 seconds.
- Research wave policy: no new subagents, no Route B retry, no new route.
- Continuation objective: hash-check Route A/C, record Route B incomplete, run
  a files-only convergence check, and finalize an honest partial package.
- Proxy preflight: port 7898 responded HTTP 400 to the unauthenticated models
  probe, confirming transport reachability.
- Pinned CLI: `codex-cli 0.149.0-alpha.4.3`.
- Pinned CLI path:
  `/mnt/c/Program Files/WindowsApps/OpenAI.Codex_26.818.8289.0_x64__2p2nqsd0c76g0/app/resources/codex`.
- Pinned CLI SHA256:
  `1c8b7f5221f6779c1e689b00bfa2dd95503f2aa595b9e6c752550ddd8ddf26b6`.
- Installed plugin: `rigorous-open-math-research` v1.7.0.
- Plugin SKILL SHA256:
  `ffcddca13446f35a275ebe199e136e26fe1ee5f960bdc58023260f7c0cfdcde3`.
- Scored work directory contains only first-segment artifacts. Repository-side
  results and the post-hoc neutral audit have not been copied into it.
- Prompt contamination policy: the continuation prompt contains process and
  stopping instructions only, with no new mathematical lemma or proof hint.
