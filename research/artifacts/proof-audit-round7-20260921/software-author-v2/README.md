# R7-SW-001 bounded software-author repair (v2)

This submission repairs replay provenance observation/enforcement. The ten numerical candidate scripts and all eight dependency files retain their supplied bytes. `prior-review.json` is unchanged and still says **CHANGES_REQUIRED**. These are author checks; a new independent reviewer must decide approval.

All work was confined to `/mnt/f/tools/math-audit-round7-20260921/software-author-v2`. No memory, live research tree, other author/reviewer directories, Git, canonical knowledge, plugins or additional mathematical scans were used.

## Self-contained inputs and entry points

The final input-only freeze is `final-inputs/`, also archived as `final-inputs.tar` with its SHA-256 sidecar. It contains the listed sources, documentation, prior review, new v2 `manifest.json`, and **`manifest.sha256`**. Execution evidence remains outside this freeze. Copy the freeze into a writable directory before running:

```bash
/usr/bin/python3 -B regression/verify_package.py
/usr/bin/python3 -B regression/replay.py --label independent-normal
/usr/bin/python3 -B -O regression/replay.py --label independent-optimized
```

`regression/verify_package.py` is the unchanged supplied verifier and **is runnable with this v2 package**, because both files it requires are now present and its `package_files` entries are supplied. The old packet did not supply them; the new manifest is not a reconstructed or silently rewritten old manifest. The verifier checks input integrity, not software correctness or authorship.

The installed Python must be able to discover installed NumPy and SciPy. Each replay copies exactly its manifest-listed inputs and manifest sidecars into a new `work/replay-*` directory. Its numerical/CLI subprocesses use `-B -S`, plus an explicit Python search path consisting of the discovered NumPy/SciPy installation parent directories. This disables site startup hooks without granting the whole site-packages directory permission in the provenance gate. No download or global Python configuration change is made.

Each replay runs both normal and `-O` children: four numerical executions (originals/candidates), two candidate op03 CLI executions, and eight provenance controls. `--controls-only` runs the same eight controls without the six clean executions. Original numerical exit 1 is required (117 checks, 79 failures); candidates must pass 117/117. Normal/optimized check names must agree. The CLI must print and satisfy all four original FD/FH comparisons. Every negative-control execution also completes the same numerical checks or CLI loop before its expected gate exit 86.

## Provenance contract

`regression/provenance.py` observes every currently file-backed `sys.modules` entry without filtering by the replay directory. The raw map is retained in each result. Runtime policy is explicit and recorded per process:

- Standard-library roots come from `sysconfig` (`stdlib`, `platstdlib`); paths under `site-packages` or `dist-packages` do not inherit that allowance.
- Installed runtime package roots are only the resolved NumPy and SciPy package directories. Their bundled/internal Python dependencies fall within those roots. Arbitrary installed packages or other workspace paths are not accepted.
- Fresh project/harness modules must be manifest-listed files under the selected originals/candidates scripts directory or the fresh regression directory, and their observed source SHA-256 must match the frozen manifest. Merely being somewhere under the fresh directory is insufficient.

Required bindings are explicit in `expected_bindings`: the thirteen common numerical project modules plus the selected op03 backend (`precise` for originals, `fixed` for candidates), and the numerical entry point, backend probe and provenance helper. Each must be present at its exact selected-tree path with its frozen digest. The CLI requires its actual `__main__` at `candidates/scripts/op03_gap_fh.py`, `op03_gap_fixed`, and its provenance helper. A missing name, wrong selected path, digest mismatch, unreadable allowed source or unexpected file-backed module causes refusal.

The two expressions-only files `_gapn2_o3_scan.py` and `_gapn2_second_variation_probe.py` remain AST-based tests, not newly imported or executed scans. Their entire source files, the unused backend, JSON table and all other copied inputs are independently checked against the manifest before replay and against before/after hashes afterwards. They are not misrepresented as loaded modules.

The CLI launcher executes the unmodified op03 file as real `__main__`, with its script path, `__file__`, argv and candidate working directory. Every top-level statement and all four print iterations execute; there is no loop removal or handwritten numerical surrogate in this CLI path. This is an instrumented CLI launch, not a claim that an uninstrumented bare-script process emits provenance. The numerical loader and expression tests retain their prior behavior.

Both numerical processes and the CLI return exit 86 on gate refusal, using explicit conditionals unaffected by `-O`. Replay independently rechecks their complete recorded maps and required bindings against its own frozen manifest and runtime policy, instead of trusting a child PASS field. JSON records include real PID, optimization flag, file paths, allowed source hashes, policy, required names/hashes, controls and specific refusal reasons. Arbitrary rejected external files are not read merely to hash them; the owned imported control fixture has its own recorded digest.

This is an end-of-execution provenance observation and acceptance gate, **not an OS sandbox, import-prevention mechanism, continuous import trace or malicious `sys.modules` evasion guarantee**. Imported code runs before acceptance is checked; built-in modules without files are outside the file-backed map. No such stronger security claim is made.

## Real controls and sensitivity

The outside control imports `control-fixtures/outside_probe.py` from the enclosing package, outside the fresh `work/replay-*` directory but inside the author's owned directory. The real module executes and prints a token; its actual `sys.modules` binding, path, token and source digest are retained. It must be the specific unexpected module that triggers exit 86 in numerical and CLI processes under both optimization modes.

The missing-binding control removes the already executed `gap_lib` (numerical) or `op03_gap_fixed` (CLI) binding immediately before observation, recording the real removed path/hash. The raw map must actually lack that required name and the gate must refuse for that precise reason. This is a deliberate presence-check control, not fabricated module metadata or a claim about resisting adversarial deletion.

A separate filter-only mutant restores the old observation-time `is_relative_to(Base)` filter, while retaining the repaired required-name checks and all controls. Its manifest is explicitly rebound to those mutated bytes and is kept separate from the repaired freeze. All four outside child processes then incorrectly exit 0, and the unchanged control suite returns **1 (FAIL)**. The four missing controls still refuse. This proves the outside tests fail under the old filtering behavior rather than accepting a handwritten fake source map. The real streams, full results, mutation text and source hashes are retained under `evidence/`.

## Evidence and historical failures

`evidence/author-summary.json` indexes final executions and hashes; `evidence/source-integrity.json` records before/after hashes for all 36 original/candidate files. Each replay retains raw stdout/stderr and argv/cwd/status/time/input/output hash receipts. Outer receipts also bind all package inputs before and after each process. The final freeze is executed through a byte-identical writable copy, keeping generated output outside the input-only freeze.

The first v2 execution (`01-repaired-normal`) failed because the now unfiltered gate correctly observed `_distutils_hack`, `apport_python_hook` and `/etc/python3.14/sitecustomize.py` outside its allowed roots. Its full 14-case failed run and source copy remain intact. The repair uses controlled `-S` startup; these three unrelated hooks were not added to the runtime allowlist. Both initial and final filter-only mutation failures are also retained with their actual exit 1.

Earlier first executions described by the old author/reviewer are retained as supplied evidence: `prior-review.json` records the reviewer's initial missing-NumPy failure, and `evidence/before/README.md` preserves the old author's backend and selector failures. Their raw historical execution directories were **not supplied here**; they were not read, fabricated, deleted or recertified. All new failures in this directory are preserved verbatim.

`inputs/tools-AGENTS.md` was deliberately not supplied. It is unrelated private workspace context, not executable input, and is excluded from the final freeze. Historical references/hashes in the unchanged `inputs/snapshot-manifest.json` and prior review are retained as historical statements; they are not instructions or a live-file read allowlist. The other supplied contextual copies remain unchanged.

No new mathematical claim is made. The inherited bounded numerical/AST scope and the excluded legacy `op03_gap_precise` normalization defect (R7-SW-002) remain as described by the prior review. No global scans, proof/certificate audit, analytic/spectral-Jacobian certification or independent approval was added.
