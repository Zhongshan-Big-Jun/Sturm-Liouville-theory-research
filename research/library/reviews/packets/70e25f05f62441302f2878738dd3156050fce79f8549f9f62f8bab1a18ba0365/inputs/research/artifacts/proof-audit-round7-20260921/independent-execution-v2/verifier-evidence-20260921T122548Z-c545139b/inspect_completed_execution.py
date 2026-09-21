from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path('/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2')
EVIDENCE = Path(__file__).resolve().parent


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(',', ':')).encode()).hexdigest()


def host(path):
    text = str(path)
    if re.match(r'^[A-Za-z]:[\\/]', text):
        return Path('/mnt') / text[0].lower() / text[3:].replace('\\', '/')
    return Path(text)


def artifact(path):
    path = Path(path)
    return {'path': str(path), 'sha256': digest(path), 'bytes': path.stat().st_size}


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def main():
    capture = read(EVIDENCE / 'execution-capture.json')
    output = Path(capture['output_directory'])
    packet = read(ROOT / 'PACKET.json')
    source_review = read(EVIDENCE / 'source-and-runner-inspection.json')
    before = read(EVIDENCE / 'before-execution-identities.json')
    after = read(EVIDENCE / 'after-execution-identities.json')
    checks = []

    def check(name, result, details=None):
        checks.append({'check': name, 'passed': bool(result), 'details': details})

    check('all_12_frozen_hashes_before_and_after',
        capture['frozen_hashes_match_before'] and capture['frozen_hashes_match_after'])
    check('all_14_packet_listed_external_hashes_before_and_after',
        capture['external_hashes_match_before'] and capture['external_hashes_match_after'])
    check('packet_unchanged', capture['packet_hash_unchanged'])
    check('freeze_matches_packet', source_review['freeze_file_map_consistent_with_packet']
        and source_review['freeze_external_map_identical_to_packet'])
    check('exact_requested_command_and_new_child',
        capture['argv'] == ['/usr/bin/python3', '-B', 'lean-package/replay.py', str(output)]
        and not capture['output_directory_existed_before_launch']
        and output.parent == ROOT / 'lean-package' and not capture['resume_positive_used'])
    check('frozen_replay_completed_successfully', capture.get('exit_code') == 0,
        {'exit_code': capture.get('exit_code'), 'elapsed_seconds': capture['elapsed_seconds']})
    for group in ('frozen', 'external'):
        check(group + '_stat_identities_unchanged',
            [{k: row.get(k) for k in ('path', 'sha256', 'size', 'mtime_ns', 'device', 'inode')}
             for row in before[group]] ==
            [{k: row.get(k) for k in ('path', 'sha256', 'size', 'mtime_ns', 'device', 'inode')}
             for row in after[group]])

    stages = []
    for record_path in sorted((output / 'logs').glob('*.json')):
        record = read(record_path)
        entry = dict(record)
        entry['record_file'] = artifact(record_path)
        for stream in ('stdout', 'stderr'):
            log_path = record_path.with_suffix('.' + stream + '.txt')
            if log_path.exists():
                entry[stream + '_file'] = artifact(log_path)
                if record.get('exit_code'):
                    entry[stream + '_actual_text'] = log_path.read_text(errors='replace')
                if record.get(stream + '_sha256'):
                    check(record_path.stem + '_' + stream + '_hash',
                        digest(log_path) == record[stream + '_sha256'])
        stages.append(entry)
    by_label = {Path(s['record_file']['path']).stem: s for s in stages}
    for label in ('01-version', '02-exact-root', '03-positive-control',
                  '04-all-declarations', '05-import-resolution'):
        check(label + '_successful', by_label.get(label, {}).get('exit_code') == 0)
    for label in ('06-wrong-target', '07-old-mirror-factor'):
        stage = by_label.get(label, {})
        diagnostic = stage.get('stdout_actual_text', '')
        check(label + '_actually_rejected_with_type_mismatch',
            stage.get('exit_code') not in (None, 0) and 'Type mismatch' in diagnostic,
            {'exit_code': stage.get('exit_code'), 'compiler_stdout': diagnostic})

    manifest_path = output / 'positive/run-manifest.json'
    public_path = output / 'public-declarations.json'
    summary_path = output / 'evidence.json'
    manifest = read(manifest_path) if manifest_path.exists() else None
    public = read(public_path) if public_path.exists() else None
    legacy = read(summary_path) if summary_path.exists() else None
    root_details = None
    import_inventory = None
    jobs = []
    if manifest is not None:
        target = manifest.get('target') or {}
        check('manifest_machine_passed', manifest['machine_verification_passed'])
        check('manifest_exact_root_passed', manifest['exact_root_passed'])
        check('manifest_payload_hash', json_digest({k: v for k, v in manifest.items()
            if k != 'report_sha256'}) == manifest['report_sha256'])
        check('manifest_contract_is_frozen_positive_contract',
            manifest['evidence']['contract'] == read(ROOT / 'lean-package/positive-contract.json'))
        check('snapshot_is_exactly_the_four_supplied_files',
            manifest['input_hashes'] == {k.removeprefix('lean-package/snapshot/'): v
                for k, v in packet['files'].items() if k.startswith('lean-package/snapshot/')})
        check('snapshot_and_tools_and_dependencies_reported_unchanged',
            manifest['evidence']['status'] == 'current'
            and not any(manifest['evidence'].get(k) for k in
                ('changed_inputs', 'changed_imports', 'changed_tools')))
        check('fresh_run_directory_is_inside_new_output',
            Path(manifest['evidence']['run_directory']).is_relative_to(output))
        contract = read(ROOT / 'lean-package/positive-contract.json')
        comparison = target.get('comparison') or {}
        check('exact_actual_root_type_matches_frozen_contract',
            target.get('declaration') == contract['declaration']
            and target.get('universes') == contract['universes']
            and comparison.get('status') == 'matched'
            and all(comparison.get(k) for k in
                ('definitionally_equal', 'universe_parameters_match', 'binder_kinds_match')))
        check('serialized_actual_and_expected_type_expressions_equal',
            target.get('type_expression') is not None
            and target['type_expression'] == (target.get('expected_statement') or {}).get('type_expression'))
        check('root_axioms_and_transitive_dependencies_closed',
            set(target.get('axioms', [])) <= {'propext', 'Classical.choice', 'Quot.sound'}
            and not any(target.get(k) for k in
                ('unexpected_axioms', 'unknown_dependencies', 'unsafe_dependencies')))
        object_path = Path(manifest['evidence']['run_directory']) / 'lib/SL/AuditRound7.olean'
        expected_source = ROOT / 'lean-package/snapshot/SL/AuditRound7.lean'
        target_commands = [x for x in (manifest.get('build') or {}).get('commands', [])
            if x.get('kind') == 'target' and x.get('file') == 'SL/AuditRound7.lean']
        fresh_compile = len(target_commands) == 1
        if fresh_compile:
            command = target_commands[0]['command']
            fresh_compile = target_commands[0]['exit_code'] == 0 and '-o' in command \
                and host(command[-1]) == expected_source \
                and host(command[command.index('-o') + 1]) == object_path
        check('actual_compiler_newly_compiled_supplied_root', fresh_compile, target_commands)
        object_record = artifact(object_path) if object_path.exists() else None
        check('own_root_object_matches_compiled_artifact_hash', object_record is not None
            and manifest['evidence']['compiled_artifacts'].get(str(object_path)) == object_record['sha256'])
        resolution_path = output / 'logs/05-import-resolution.stdout.txt'
        resolutions = [host(x.strip()) for x in resolution_path.read_text().splitlines()
            if x.strip()] if resolution_path.exists() else []
        check('control_import_resolves_to_own_new_root_object', object_path in resolutions,
            [str(x) for x in resolutions])
        if (output / 'root-artifact.json').exists():
            root_record = read(output / 'root-artifact.json')
            check('runner_root_record_matches_actual_object_and_frozen_source',
                object_record and root_record['olean_sha256'] == object_record['sha256']
                and root_record['source_sha256'] == packet['files']['lean-package/snapshot/SL/AuditRound7.lean'])
        roots = [Path(manifest['environment']['prefix'])]
        config = read(ROOT / 'lean-package/runtime-config.json')
        roots += [host(x) for x in config['LEAN_PATH'].split(';')]
        imported = target.get('import_artifacts', {})
        outside = [item['path'] for item in imported.values()
            if not any(Path(item['path']).is_relative_to(root) for root in roots)]
        modules = target.get('imported_modules', [])
        check('loaded_module_inventory_complete', target.get('module_inventory_scope') == 'loaded_environment'
            and target.get('loaded_module_count') == len(modules)
            and len({x['module'] for x in modules}) == len(modules))
        check('all_external_import_artifacts_within_permitted_runtime_dependency_roots', not outside, outside)
        check('all_recorded_external_imports_have_actual_sha256', bool(imported)
            and all(re.fullmatch('[0-9a-f]{64}', x.get('sha256', '')) for x in imported.values()))
        import_inventory = {
            'loaded_module_count': target.get('loaded_module_count'),
            'artifact_count': len(imported), 'external_artifacts': imported,
            'scope': 'Loaded inspection environment, including standard Lean, Mathlib and supporting packages; not just minimal proof dependencies.',
            'hash_timing': 'Frozen verifier hashes artifacts after extraction and rehashes them before completion, requiring external mtimes to predate target checking. No claim of a pre-launch hash of every Mathlib artifact.',
            'source_manifest': artifact(manifest_path),
        }
        write(EVIDENCE / 'loaded-import-artifacts.json', import_inventory)
        root_details = {
            'declaration': target.get('declaration'), 'kind': target.get('kind'),
            'universes': target.get('universes'),
            'type_sha256': target.get('type_sha256'),
            'semantic_sha256': target.get('semantic_sha256'),
            'environment_sha256': target.get('environment_sha256'),
            'semantic_environment_sha256': target.get('semantic_environment_sha256'),
            'axioms': target.get('axioms'),
            'comparison': {k: v for k, v in comparison.items() if k != 'expected_type_expression'},
            'object': object_record,
            'source': artifact(expected_source),
            'actual_type_file': artifact(EVIDENCE / 'actual-root-type.txt') if (EVIDENCE / 'actual-root-type.txt').exists() else None,
            'type_expression_serialization': 'Verifier serialization ignores binder names and metadata; Lean definitional equality, universe count and binder kinds are separately checked.',
            'dependency_count': len(target.get('dependencies', [])),
            'unexpected_axioms': target.get('unexpected_axioms'),
            'unsafe_dependencies': target.get('unsafe_dependencies'),
            'unknown_dependencies': target.get('unknown_dependencies'),
        }
        for path in sorted((Path(manifest['evidence']['run_directory']) / 'logs').glob('*.job.json')):
            job = read(path)
            for stream in ('stdout', 'stderr'):
                if job.get(stream + '_sha256'):
                    check('job_' + job['job_id'] + '_' + stream + '_hash',
                        digest(job[stream + '_log']) == job[stream + '_sha256'])
            job['record_file'] = artifact(path)
            jobs.append(job)
        check('no_full_lake_build_was_run',
            manifest['environment']['mode'] == 'direct'
            and all(not (any(Path(c).name.lower() == 'lake.exe' for c in j['command'])
                and 'build' in j['command']) for j in jobs))
    else:
        check('fresh_positive_manifest_available', False)

    if public is not None:
        expected_names = [x['declaration'] for x in source_review['public_source_inventory']]
        check('public_inventory_exactly_27_source_declarations',
            [x['declaration'] for x in public] == expected_names and len(public) == 27)
        check('public_inventory_has_20_theorems_and_7_definitions',
            sum(x['is_theorem'] for x in public) == 20 and sum(not x['is_theorem'] for x in public) == 7)
        check('all_public_transitive_axioms_allowed',
            all(set(x['transitive_axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'} for x in public))
        transcript = (output / 'logs/04-all-declarations.stdout.txt').read_text()
        def_names = [x['declaration'] for x in source_review['public_source_inventory'] if x['kind'] == 'def']
        check('all_seven_actual_definitions_printed', all('def ' + name in transcript for name in def_names))
    else:
        check('public_declaration_inspection_available', False)
    check('runner_final_identity_check_all_passed', (output / 'final-input-identity-checks.json').exists()
        and all(read(output / 'final-input-identity-checks.json').values()))
    failed = [x for x in checks if not x['passed']]
    result = {
        'reviewed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'role': 'fresh-independent-execution-verifier',
        'preliminary_verdict': 'PASS' if not failed else 'INCOMPLETE',
        'required_check_count': len(checks), 'passed_check_count': len(checks) - len(failed),
        'checks': checks, 'failed_checks': failed,
        'execution_capture': artifact(EVIDENCE / 'execution-capture.json'),
        'capture': capture, 'stages': stages, 'plugin_processes': jobs,
        'root': root_details,
        'public_declarations': public,
        'import_inventory_file': artifact(EVIDENCE / 'loaded-import-artifacts.json') if import_inventory else None,
        'fresh_positive_manifest': artifact(manifest_path) if manifest else None,
        'legacy_runner_summary': legacy,
        'legacy_label_explanation': 'The frozen runner retains author role strings. This report describes a new independent execution launched by this verifier, without resume or any earlier author output. Independence is not a second kernel or an independently implemented verifier.',
    }
    write(EVIDENCE / 'completed-execution-inspection.json', result)
    print(json.dumps({'checks': len(checks), 'passed': len(checks)-len(failed),
        'failed_checks': failed, 'preliminary_verdict': result['preliminary_verdict']}, indent=2))


if __name__ == '__main__':
    main()
