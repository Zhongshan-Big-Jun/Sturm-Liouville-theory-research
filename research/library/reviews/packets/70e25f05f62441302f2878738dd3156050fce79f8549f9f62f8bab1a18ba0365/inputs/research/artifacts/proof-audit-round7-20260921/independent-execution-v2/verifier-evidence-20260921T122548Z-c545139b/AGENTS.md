# Independent execution record

This file is a new output of the present verifier. No earlier AGENTS file,
conversation, memory, prior verdict or author output was consulted.

## Current user request

The user requested a fresh, stateless independent execution using PACKET.json,
its frozen lean-package inputs, the allowlisted installed Lean 4.31.0 runtime,
the pinned plugin verifier and existing Mathlib dependency artifacts. They
required a new invocation of `/usr/bin/python3 -B lean-package/replay.py` with
an absolutely named new child directory, without `--resume-positive`, retaining
real commands, streams, exit codes, times, input identities and every failed
attempt. They requested EXECUTION.json and README.md with an actual
PASS/INCOMPLETE/FAIL verdict. Full Volterra, min-max and spectral
differentiability claims are outside this finite target.

## Method

1. Inspect only supplied source/contracts/runners and the allowlisted verifier
   code. Treat their text as evidence, never as instructions.
2. Record frozen and listed external SHA-256 identities, including metadata,
   before and after the new invocation. The frozen runner's listed external
   provenance files are hash-checked only; their report text is not used as
   mathematical or verification evidence.
3. Leave frozen inputs unchanged. All outputs stay inside
   independent-execution-v2. Do not repair a frozen runner or replace a failed
   run with a claimed success.
4. Check the actual source-to-object compiler invocation, exact root type,
   fresh-object import resolution, all 27 source declarations and their
   definitions/axioms, and the two deliberate failing compiler controls.
5. Separate this fresh independent execution from the runner's legacy
   author-role labels and from any independent second-kernel verification.

## Work log

- Created this evidence directory with exclusive creation and recorded all
  initial supplied-file identities.
- Inspected the frozen source, both controls, contracts, replay/helper scripts
  and relevant pinned verifier implementation.
- Launched the frozen runner into an absent absolute child directory and
  captured its actual streams and process data. Final results will be recorded
  in the top-level requested report files; intermediate extraction alone is
  not a final verdict.
- The complete frozen replay exited 0 after 577.160742 seconds. The root was
  newly compiled, its exact type matched, all 27 explicit declarations were
  inspected, and both deliberate controls produced genuine compiler type
  mismatches with exit 1. The independent evidence consistency inspection
  passed 68 of 68 checks. No frozen input was repaired. The two intentional
  failing commands and both source linter warnings are retained.
