from pathlib import Path
import hashlib
import json
import shutil
import subprocess

Root = Path('/mnt/f/LaTeX/BVE research')
Ops = Path('/mnt/f/tools/math-audit-round13-20260927')
Evidence = Root / 'research/artifacts/proof-audit-round13-20260927/operations'
Baseline = json.loads((Ops / 'baseline.json').read_text())
Name = 'state/AGENTS_SESSION_LOG.md'
Original = subprocess.check_output(['git', 'show', Baseline['head'] + ':' + Name], cwd=Root)
Current = (Root / Name).read_bytes()
NormalizedOriginal = Original.replace(b'\r\n', b'\n')
if not Current.startswith(NormalizedOriginal):
    raise RuntimeError('Current history differs in content; do not reconstruct it automatically')
Repaired = Original + Current[len(NormalizedOriginal):]
if Repaired.replace(b'\r\n', b'\n') != Current.replace(b'\r\n', b'\n'):
    raise RuntimeError('Repair would alter log text')
Failure = json.loads((Ops / 'final-protected-files.json').read_text())
if Failure['mismatches'] or Failure['historical_log_prefix_preserved']:
    raise RuntimeError('Unexpected preservation check state')
shutil.copyfile(Ops / 'final-protected-files.json', Ops / 'final-protected-files-before-newline-repair.json')
shutil.copyfile(Ops / 'final-protected-files.json', Evidence / 'pre-repair-protected-files.json')
(Root / Name).write_bytes(Repaired)
Note = '\n发布前字节核对另发现: 最终追加日志时统一了旧混合换行; 已从基线恢复历史前缀原字节, 本轮追加正文不变. 原失败检查与修复记录见 research/artifacts/proof-audit-round13-20260927/operations/post-reception-preservation.json.\n'
Agents = Root / 'AGENTS.md'
Text = Agents.read_text()
Anchor = '\n## 2026-09-26 第十二轮审计修缮'
if Anchor not in Text:
    raise RuntimeError('Missing maintenance insertion anchor')
Agents.write_text(Text.replace(Anchor, Note + Anchor, 1))
Result = dict(path=Name, original_prefix_sha256=hashlib.sha256(Original).hexdigest(),
              before_sha256=hashlib.sha256(Current).hexdigest(), after_sha256=hashlib.sha256(Repaired).hexdigest(),
              original_prefix_exact=Repaired.startswith(Original), log_text_unchanged=True,
              cause='Finalization used text-mode read/write and normalized 3412 historical CRLF line endings.',
              action='Restore exact baseline bytes as prefix; retain every current append; preserve failed check.',
              mathematical_sources_changed=False)
(Evidence / 'post-reception-preservation.json').write_text(json.dumps(Result, indent=2) + '\n')
shutil.copyfile(Path(__file__), Evidence / Path(__file__).name)
print(json.dumps(Result))
