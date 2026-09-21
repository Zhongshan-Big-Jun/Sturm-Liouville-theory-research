**PASS: fresh independent execution of the supplied finite local Lean target.**

The frozen replay completed with exit **0**, from
2026-09-21T12:28:28.775398+00:00 to 2026-09-21T12:38:05.950789+00:00 (UTC), taking
577.160742 seconds. It was launched into an absent,
absolutely named new child of `lean-package`; no `--resume-positive` was used.
This verifier read the supplied packet and frozen inputs and inspected the
pinned verifier implementation. The runner's retained `author` role strings
are legacy program labels, not the identity or scope of this execution.

Working directory: `/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2`.

Actual command:

```text
/usr/bin/python3 -B lean-package/replay.py /mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/lean-package/fresh-independent-20260921T122826Z-27cdbba98232
```

The actual Windows runtime reported Lean 4.31.0, x86_64-w64-windows-gnu,
commit `68218e876d2a38b1985b8590fff244a83c321783`. The supplied
`snapshot/SL/AuditRound7.lean` was compiled directly into
`/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/lean-package/fresh-independent-20260921T122826Z-27cdbba98232/positive/lean-verification-runs/88fa8bbd41f549c08bcb415d2ec245e7/lib/SL/AuditRound7.olean`. The root compiler command exited 0 in
14.264992 seconds. Lean `--deps` later resolved `SL.AuditRound7` to that
same newly compiled object. The full replay did not run a Lake build.

| Actual stage | Exit code | Seconds |
| --- | ---: | ---: |
| 01-version | 0 | 0.253 |
| 02-exact-root | 0 | 526.796 |
| 03-positive-control | 0 | 11.159 |
| 04-all-declarations | 0 | 11.030 |
| 05-import-resolution | 0 | 0.119 |
| 06-wrong-target | 1 | 10.152 |
| 07-old-mirror-factor | 1 | 10.290 |

`SL.AuditRound7.local_algebra_root` is an actual theorem with no universe
parameters. Its ten-conjunct type matches the frozen positive contract by
Lean definitional equality, universe count and binder kinds. Its serialized
type expression also equals the serialized elaborated expected expression;
that serialization ignores binder names and metadata. The direct positive
control compiled successfully. The expected-type carrier introduced by the
inspection probe is not an axiom of the root: the root was compiled first.

The ten conjuncts establish the normalized trigonometric-mode derivative,
the exact Wronskian product-to-sum formula, the finite sine-square identity,
strict Wronskian negativity for positive natural n and 0 < x < 1,
W(2,1/2) = -4*pi and rejection of the old value, the endpoint coefficient
identity and negativity, conditional mirrored-gap algebra with factor 2,
and the stationarity equivalence when the jump is nonzero. The endpoint
coefficient is `2*pi^4*(n^4-(n+1)^4)`; no Taylor remainder is asserted.

All **27 explicit source declarations (20 theorems, 7 definitions)** were
checked in the fresh imported environment. All seven actual definition
bodies were printed and inspected. Root and public transitive axiom sets
contain only `propext`, `Classical.choice`, and `Quot.sound`; the root
dependency closure has 26,508 constants with no reported missing or unsafe
dependency and no extra axiom. The declarations, actual types and axioms are
in [public-declarations.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/lean-package/fresh-independent-20260921T122826Z-27cdbba98232/public-declarations.json);
the actual definition prints are in
[the compiler inspection transcript](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/lean-package/fresh-independent-20260921T122826Z-27cdbba98232/logs/04-all-declarations.stdout.txt).
The full root type is in [actual-root-type.txt](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/actual-root-type.txt).

Both deliberate failing attempts were retained. The wrong Wronskian target
actually failed with compiler exit 1: its proof has value `-4 * Real.pi`
while the requested type has `-6 * Real.pi`. The old mirror factor actually
failed with exit 1: the proof has coefficient `-2 * eigenvalue` while the
requested type has `-eigenvalue`. These are actual compiler `Type mismatch`
diagnostics, not inferred or manufactured failures. There were no unexpected
execution failures. Root compilation emitted two non-failing
`linter.unnecessarySeqFocus` warnings at line 116; they remain unchanged.

All **12 frozen file hashes and 14 packet-listed external hashes** matched
before and after execution, with recorded stat identities unchanged. The
freeze and packet maps agree. The fresh inspection environment loaded 4,365
modules; the plugin recorded and rechecked **13,089 external import artifact
hashes**, excluding its two freshly compiled local modules. Full actual
hashes and paths are in
[loaded-import-artifacts.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/loaded-import-artifacts.json).
The additional independent evidence consistency inspection passed **68/68**
checks; this count describes evidence checks, not 68 independent theorem proofs.

| Important file | SHA-256 |
| --- | --- |
| PACKET.json | `e9a48406f354b57262ef128201a81e7e70e72990059bb546b38a6777c5bfb9ee` |
| Frozen SL/AuditRound7.lean | `c1b464f60cc7cef7a1052a0cf97cde4cacd01b36f69a83ac94056128a7fb8af6` |
| Frozen positive-contract.json | `bfbc41cba0d1e61182495c1aaae1165842e5c16520492ceede2528de9468af58` |
| Frozen replay.py | `f25b569f8ea4cb2da406e9707d340b13bc370e0afd43b4dd34d6d4079373ba8f` |
| Fresh SL/AuditRound7.olean | `ab758356cd8b3dcd7a17f3153d24cbeae58d3c4ff19ff6ba9ae9b837686c31ef` |
| Fresh positive run-manifest.json | `0dc0c85da2523662736e7224584cc4f779ad72c86e40a8230372a5c741c285c9` |
| Installed lean.exe | `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f` |

The exact command, streams, exits, timing, and pre/post identities are in
[execution-capture.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/execution-capture.json),
[before-execution-identities.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/before-execution-identities.json),
and [after-execution-identities.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/after-execution-identities.json).
All replay stage logs and input snapshots remain in `/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/lean-package/fresh-independent-20260921T122826Z-27cdbba98232`.
[artifact-index.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/verifier-evidence-20260921T122548Z-c545139b/artifact-index.json) hashes the durable execution and
inspection outputs. [EXECUTION.json](/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2/EXECUTION.json) provides
the structured verdict, claims, checks, failures, file references and limitations.

No required finite-target check remains missing. Limits of the verdict:

- The verdict covers the supplied finite local Lean contract and the explicit 27 source declarations only. It does not establish full Volterra, Taylor remainder, min-max, spectral-limit or spectral-differentiability claims.
- The mirrored-interface and gap statements are conditional scalar algebra under the hypotheses written in the contract; existence of Feynman-Hellmann derivatives is not proved.
- The supplied Windows Lean compiler, pinned plugin implementation and installed dependency objects are trusted. This was not an independently implemented verifier or a second-kernel check.
- No full Lake build, Mathlib rebuild, network dependency retrieval or external checkout/Git-revision audit was performed. The Mathlib revision is a frozen configuration string; actual consumed dependency artifacts are recorded by SHA-256.
- All frozen and packet-listed external inputs have pre/post hashes. The 13089 imported dependency artifacts were hashed after extraction and rehashed before plugin completion, with external mtimes required to precede the check; no pre-launch hash inventory of all Mathlib objects or continuous filesystem monitoring is claimed.
- wrong-target-contract.json was hash-verified and inspected but not separately passed to the plugin. Its deliberate wrong target was tested by the supplied WrongWronskianTarget.lean compiler control.
- The 27-declaration inventory counts explicit def/theorem declarations in the supplied source. Generated auxiliary constants are covered by the recorded dependency closure rather than counted as additional authored declarations.

Provenance boundary: no author conversation, memory, earlier execution output,
other-agent output or main-project mathematical source was used. The frozen
runner's external list includes three main-project configuration files and
one audit-report Markdown: their bytes were hashed for identity only, without
decoding or using report text. The supplied helper additionally parsed only
the hash-bound external package manifest to locate installed dependencies.
This exact unavoidable runner behavior is disclosed rather than described as
zero external-file access. No canonical, Git or main-project edit was made;
all verifier-created files are inside this independent execution directory.
