from pathlib import Path
import hashlib,json,subprocess
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927')
M=json.loads((O/'publication-manifest.json').read_text())['files']
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
Staged=set(git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0'))
if Staged!=set(M):raise RuntimeError('Staged set mismatch')
Rows={line.split('\t',1)[1]:line.split()[1] for line in git('ls-files','--stage').decode().splitlines() if '\t' in line}
# One batch reader verifies actual stored blob bytes, including line endings.
Process=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
Bad=[]
for n,h in M.items():
 Process.stdin.write((Rows[n]+'\n').encode());Process.stdin.flush()
 Header=Process.stdout.readline().decode().split();Raw=Process.stdout.read(int(Header[2]));Process.stdout.read(1)
 if hashlib.sha256(Raw).hexdigest()!=h or hashlib.sha256((R/n).read_bytes()).hexdigest()!=h:Bad.append(n)
Process.stdin.close();Process.wait()
Result=dict(staged_count=len(M),exact_bytes=not Bad,mismatches=Bad)
(O/'staged-verification.json').write_text(json.dumps(Result,indent=2)+'\n');print(json.dumps(Result))
if Bad:raise SystemExit(1)
