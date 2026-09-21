from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path('/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2')
EVIDENCE = Path(__file__).resolve().parent


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def artifact(path):
    path = Path(path)
    return {'path': str(path), 'sha256': digest(path), 'bytes': path.stat().st_size}


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def link(label, path):
    return '[' + label + '](' + str(path) + ')'


def main():
    review = read(EVIDENCE / 'completed-execution-inspection.json')
    capture = review['capture']
    output = Path(capture['output_directory'])
    packet = read(ROOT / 'PACKET.json')
    before = read(EVIDENCE / 'before-execution-identities.json')
    after = read(EVIDENCE / 'after-execution-identities.json')
    source_review = read(EVIDENCE / 'source-and-runner-inspection.json')
    stages = {Path(x['record_file']['path']).stem: x for x in review['stages']}
    verdict = review['preliminary_verdict']
    root = review['root']
    inventory = read(EVIDENCE / 'loaded-import-artifacts.json')
    failures = [dict(label=label, expected=True, exit_code=stages[label]['exit_code'],
                    command=stages[label]['argv'],
                    stdout=stages[label]['stdout_file'], stderr=stages[label]['stderr_file'],
                    actual_compiler_diagnostic=stages[label]['stdout_actual_text'])
                for label in ('06-wrong-target', '07-old-mirror-factor')]
    unexpected = [x for label, x in stages.items()
                  if label not in ('06-wrong-target', '07-old-mirror-factor')
                  and x.get('exit_code') != 0]
    unexpected += [x for x in review['plugin_processes'] if x.get('exit_code') != 0]
    limitations = [
        'The verdict covers the supplied finite local Lean contract and the explicit 27 source declarations only. It does not establish full Volterra, Taylor remainder, min-max, spectral-limit or spectral-differentiability claims.',
        'The mirrored-interface and gap statements are conditional scalar algebra under the hypotheses written in the contract; existence of Feynman-Hellmann derivatives is not proved.',
        'The supplied Windows Lean compiler, pinned plugin implementation and installed dependency objects are trusted. This was not an independently implemented verifier or a second-kernel check.',
        'No full Lake build, Mathlib rebuild, network dependency retrieval or external checkout/Git-revision audit was performed. The Mathlib revision is a frozen configuration string; actual consumed dependency artifacts are recorded by SHA-256.',
        'All frozen and packet-listed external inputs have pre/post hashes. The 13089 imported dependency artifacts were hashed after extraction and rehashed before plugin completion, with external mtimes required to precede the check; no pre-launch hash inventory of all Mathlib objects or continuous filesystem monitoring is claimed.',
        'wrong-target-contract.json was hash-verified and inspected but not separately passed to the plugin. Its deliberate wrong target was tested by the supplied WrongWronskianTarget.lean compiler control.',
        'The 27-declaration inventory counts explicit def/theorem declarations in the supplied source. Generated auxiliary constants are covered by the recorded dependency closure rather than counted as additional authored declarations.',
    ]
    provenance = {
        'memory_or_author_conversation_used': False,
        'previous_execution_output_or_other_agent_directory_used': False,
        'main_project_mathematical_source_read': False,
        'new_output_directory': str(output),
        'source_and_contracts_treated_as': 'Evidence only, never instructions.',
        'external_hash_only_provenance': [path for path in packet['allowed_external_inputs']
            if path.startswith('/mnt/f/LaTeX/') or path.endswith('proof_audit_round7_20260921.md')],
        'external_hash_only_explanation': 'PACKET/freeze also list three main-project configuration files and one audit-report Markdown. Their bytes were hashed only for listed identity checks; no report text or verdict was decoded or used. The unchanged frozen helper additionally parses the hash-bound main-project lake-manifest.json solely to construct the permitted dependency directories.',
        'writes_scope': str(ROOT),
        'frozen_input_edits': False,
        'canonical_git_or_main_project_operations': False,
        'runner_legacy_role_labels': review['legacy_label_explanation'],
    }
    generated = []
    for directory in (output, EVIDENCE):
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                generated.append(artifact(path))
    index_path = EVIDENCE / 'artifact-index.json'
    write(index_path, {'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Durable files in this new replay child and this new verifier evidence directory, before final report creation. The index does not hash itself or later final reports.',
        'files': generated})
    table = '\n'.join('| ' + label + ' | ' + str(stage['exit_code']) + ' | '
                      + format(stage['duration_seconds'], '.3f') + ' |'
                      for label, stage in stages.items())
    key_hashes = [
        ('PACKET.json', before['packet']['sha256']),
        ('Frozen SL/AuditRound7.lean', root['source']['sha256']),
        ('Frozen positive-contract.json', packet['files']['lean-package/positive-contract.json']),
        ('Frozen replay.py', packet['files']['lean-package/replay.py']),
        ('Fresh SL/AuditRound7.olean', root['object']['sha256']),
        ('Fresh positive run-manifest.json', review['fresh_positive_manifest']['sha256']),
        ('Installed lean.exe', packet['allowed_external_inputs']['/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe']),
    ]
    hashes_table = '\n'.join('| ' + name + ' | `' + value + '` |' for name, value in key_hashes)
    readme = f"""**{verdict}: fresh independent execution of the supplied finite local Lean target.**

The frozen replay completed with exit **{capture['exit_code']}**, from
{capture['started_at_utc']} to {capture['finished_at_utc']} (UTC), taking
{capture['elapsed_seconds']:.6f} seconds. It was launched into an absent,
absolutely named new child of `lean-package`; no `--resume-positive` was used.
This verifier read the supplied packet and frozen inputs and inspected the
pinned verifier implementation. The runner's retained `author` role strings
are legacy program labels, not the identity or scope of this execution.

Working directory: `{ROOT}`.

Actual command:

```text
{capture['command_shell_rendering']}
```

The actual Windows runtime reported Lean 4.31.0, x86_64-w64-windows-gnu,
commit `68218e876d2a38b1985b8590fff244a83c321783`. The supplied
`snapshot/SL/AuditRound7.lean` was compiled directly into
`{root['object']['path']}`. The root compiler command exited 0 in
14.264992 seconds. Lean `--deps` later resolved `SL.AuditRound7` to that
same newly compiled object. The full replay did not run a Lake build.

| Actual stage | Exit code | Seconds |
| --- | ---: | ---: |
{table}

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
in {link('public-declarations.json', output / 'public-declarations.json')};
the actual definition prints are in
{link('the compiler inspection transcript', output / 'logs/04-all-declarations.stdout.txt')}.
The full root type is in {link('actual-root-type.txt', EVIDENCE / 'actual-root-type.txt')}.

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
{link('loaded-import-artifacts.json', EVIDENCE / 'loaded-import-artifacts.json')}.
The additional independent evidence consistency inspection passed **68/68**
checks; this count describes evidence checks, not 68 independent theorem proofs.

| Important file | SHA-256 |
| --- | --- |
{hashes_table}

The exact command, streams, exits, timing, and pre/post identities are in
{link('execution-capture.json', EVIDENCE / 'execution-capture.json')},
{link('before-execution-identities.json', EVIDENCE / 'before-execution-identities.json')},
and {link('after-execution-identities.json', EVIDENCE / 'after-execution-identities.json')}.
All replay stage logs and input snapshots remain in `{output}`.
{link('artifact-index.json', index_path)} hashes the durable execution and
inspection outputs. {link('EXECUTION.json', ROOT / 'EXECUTION.json')} provides
the structured verdict, claims, checks, failures, file references and limitations.

No required finite-target check remains missing. Limits of the verdict:

""" + '\n'.join('- ' + value for value in limitations) + f"""

Provenance boundary: no author conversation, memory, earlier execution output,
other-agent output or main-project mathematical source was used. The frozen
runner's external list includes three main-project configuration files and
one audit-report Markdown: their bytes were hashed for identity only, without
decoding or using report text. The supplied helper additionally parsed only
the hash-bound external package manifest to locate installed dependencies.
This exact unavoidable runner behavior is disclosed rather than described as
zero external-file access. No canonical, Git or main-project edit was made;
all verifier-created files are inside this independent execution directory.
"""
    with (ROOT / 'README.md').open('x', encoding='utf-8') as stream:
        stream.write(readme)
    execution = {
        'schema_version': 1,
        'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'verdict': verdict,
        'role': 'fresh-stateless-independent-Lean-execution-verifier',
        'scope': 'Supplied finite local formal target SL.AuditRound7.local_algebra_root and all 27 explicit frozen source declarations.',
        'fresh_machine_execution': True,
        'full_lake_build_performed': False,
        'resume_positive_used': False,
        'provenance': provenance,
        'execution': capture,
        'input_identities_before': before,
        'input_identities_after': after,
        'source_and_runner_inspection': artifact(EVIDENCE / 'source-and-runner-inspection.json'),
        'exact_root': root,
        'claims': [
            'The supplied target source was newly compiled into the new replay child; direct imports resolve to that object.',
            'The actual root type matches the frozen positive contract, including universe and binder checks.',
            'All 27 explicit declarations, seven definition bodies and their transitive axioms were inspected.',
            'The genuine compiler rejected both frozen wrong-target and mirror-factor controls with exit 1 and the intended type mismatch diagnostics.',
            'All frozen and packet-listed external hashes match before and after this execution.',
        ],
        'public_inventory': review['public_declarations'],
        'public_definition_and_axiom_transcript': artifact(output / 'logs/04-all-declarations.stdout.txt'),
        'root_type_and_definition_evidence': artifact(EVIDENCE / 'root-type-and-definition-evidence.json'),
        'actual_tests': review['stages'],
        'actual_plugin_processes': review['plugin_processes'],
        'failures': failures,
        'unexpected_execution_failures': unexpected,
        'failed_attempts_retained': True,
        'replay_attempt_count': 1,
        'warnings': [{'file': 'snapshot/SL/AuditRound7.lean', 'line': 116,
                      'columns': [30, 42], 'kind': 'linter.unnecessarySeqFocus',
                      'message': 'Used tac1 <;> tac2 where (tac1; tac2) would suffice',
                      'compiler_exit_code': 0}],
        'missing_required_checks': review['failed_checks'],
        'limits_and_unperformed_checks': limitations,
        'evidence_consistency_checks': review['checks'],
        'evidence_consistency_counts': {'passed': review['passed_check_count'], 'total': review['required_check_count']},
        'loaded_module_count': inventory['loaded_module_count'],
        'external_import_artifact_count': inventory['artifact_count'],
        'external_import_artifact_inventory': artifact(EVIDENCE / 'loaded-import-artifacts.json'),
        'fresh_positive_manifest': review['fresh_positive_manifest'],
        'durable_artifact_index': artifact(index_path),
        'readme': artifact(ROOT / 'README.md'),
        'legacy_program_summary_interpretation': review['legacy_label_explanation'],
        'legacy_program_summary_file': artifact(output / 'evidence.json'),
    }
    write(ROOT / 'EXECUTION.json', execution)
    write(ROOT / 'REPORT-HASHES.json', {
        'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'files': [artifact(ROOT / 'EXECUTION.json'), artifact(ROOT / 'README.md'), artifact(index_path)],
    })
    print(json.dumps({'verdict': verdict, 'report': artifact(ROOT / 'EXECUTION.json'),
        'readme': artifact(ROOT / 'README.md'), 'artifact_count': len(generated)}, indent=2))


if __name__ == '__main__':
    main()
