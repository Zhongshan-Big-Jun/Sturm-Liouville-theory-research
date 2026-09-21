from pathlib import Path
import datetime
import hashlib
import json
import os
import shlex
import subprocess
import time
import traceback
import uuid

ROOT = Path('/mnt/f/tools/math-audit-round7-20260921/independent-execution-v2')
EVIDENCE = Path(__file__).resolve().parent


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path, expected=None):
    path = Path(path)
    result = {'path': str(path), 'resolved_path': str(path.resolve())}
    try:
        stat = path.stat()
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        result.update(sha256=digest, size=stat.st_size, mtime_ns=stat.st_mtime_ns,
                      device=stat.st_dev, inode=stat.st_ino, mode=oct(stat.st_mode))
        if expected is not None:
            result.update(expected_sha256=expected, matches=digest == expected)
    except Exception as error:
        result.update(error=repr(error), matches=False)
    return result


def write(name, value):
    with (EVIDENCE / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def inputs(packet):
    return {
        'captured_at_utc': now(),
        'packet': identity(ROOT / 'PACKET.json'),
        'frozen': [identity(ROOT / name, digest) for name, digest in packet['files'].items()],
        'external': [identity(name, digest) for name, digest in packet['allowed_external_inputs'].items()],
    }


def main():
    packet = json.loads((ROOT / 'PACKET.json').read_text())
    output = ROOT / 'lean-package' / ('fresh-independent-' +
        datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') +
        '-' + uuid.uuid4().hex[:12])
    assert not output.exists()
    assert output.is_absolute() and output.parent == ROOT / 'lean-package'
    before = inputs(packet)
    write('before-execution-identities.json', before)
    command = ['/usr/bin/python3', '-B', 'lean-package/replay.py', str(output)]
    record = {
        'role': 'fresh-independent-execution-verifier',
        'argv': command, 'command_shell_rendering': shlex.join(command),
        'cwd': str(ROOT), 'output_directory': str(output),
        'output_directory_existed_before_launch': output.exists(),
        'resume_positive_used': False, 'wrapper': identity(__file__),
        'python_requested': identity('/usr/bin/python3'),
        'started_at_utc': now(),
        'stdout_file': str(EVIDENCE / 'replay.stdout.txt'),
        'stderr_file': str(EVIDENCE / 'replay.stderr.txt'),
        'environment_overrides': {'PYTHONDONTWRITEBYTECODE': '1'},
    }
    write('launch.json', record)
    print(json.dumps({'launch': record}, ensure_ascii=False), flush=True)
    started = time.monotonic()
    try:
        with (EVIDENCE / 'replay.stdout.txt').open('xb') as stdout, \
             (EVIDENCE / 'replay.stderr.txt').open('xb') as stderr:
            process = subprocess.Popen(command, cwd=ROOT,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
            write('process.json', {'pid': process.pid, 'started_at_utc': now(), 'argv': command})
            record['pid'] = process.pid
            record['exit_code'] = process.wait()
    except BaseException as error:
        record['capture_error'] = repr(error)
        record['capture_traceback'] = traceback.format_exc()
        raise
    finally:
        record['finished_at_utc'] = now()
        record['elapsed_seconds'] = time.monotonic() - started
        after = inputs(packet)
        write('after-execution-identities.json', after)
        record['frozen_hashes_match_before'] = all(x.get('matches') for x in before['frozen'])
        record['frozen_hashes_match_after'] = all(x.get('matches') for x in after['frozen'])
        record['external_hashes_match_before'] = all(x.get('matches') for x in before['external'])
        record['external_hashes_match_after'] = all(x.get('matches') for x in after['external'])
        record['packet_hash_unchanged'] = before['packet']['sha256'] == after['packet']['sha256']
        record['stdout'] = identity(EVIDENCE / 'replay.stdout.txt')
        record['stderr'] = identity(EVIDENCE / 'replay.stderr.txt')
        write('execution-capture.json', record)
        print(json.dumps({'completed': record}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
