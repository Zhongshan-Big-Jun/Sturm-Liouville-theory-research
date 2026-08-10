$ErrorActionPreference = 'Stop'
$p = 'F:\LaTeX\BVE research\docs\SL_spectral_topics_summary.tex'
$lines = Get-Content -LiteralPath $p -Encoding UTF8

# ---------- 1. abstract changelog: chronological reorder ----------
$iIntro = -1; $iP13 = -1; $iP2a = -1; $iP2b = -1; $iP3a = -1; $iP3b = -1; $iP4 = -1; $iP5a = -1; $iP5b = -1; $iEndAbs = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    $t = $lines[$i]
    if ($t -match '文档同时总结各结果背后的证明技术') { $iIntro = $i }
    if ($t -match '本版 \(2026-08-05, 会话 13\)') { $iP13 = $i }
    if ($t -match '^本版 \(2026-08-04, 会话 10\)') { $iP2a = $i }
    if ($t -match 'summary\.pdf\}') { $iP2b = $i }
    if ($t -match '^本版 \(2026-08-09, 会话 34/35/40\)') { $iP3a = $i }
    if ($t -match '开放问题清单相应更新') { $iP3b = $i }
    if ($t -match '^本版 \(2026-08-10, 会话 56\)') { $iP4 = $i }
    if ($t -match '^本版 \(2026-08-10, 会话 50\)') { $iP5a = $i }
    if ($t -match '不声称首创') { $iP5b = $i }
    if ($t -match '^\\end\{abstract\}') { $iEndAbs = $i }
}
$need = @($iIntro, $iP13, $iP2a, $iP2b, $iP3a, $iP3b, $iP4, $iP5a, $iP5b, $iEndAbs)
if ($need -contains -1) { throw 'abstract markers not all found' }
if (-not ($iP2a -lt $iP2b -and $iP3a -lt $iP3b -and $iP5a -lt $iP5b)) { throw 'abstract block ordering unexpected' }

$introLine = $lines[$iIntro]
$k = $introLine.IndexOf('本版 (2026-08-05')
if ($k -lt 0) { throw 'P13 split marker missing' }
$introText = $introLine.Substring(0, $k).TrimEnd()
$p13Text = $introLine.Substring($k)

$newAbstract = @()
$newAbstract += $lines[0..($iIntro - 1)]
$newAbstract += $introText
$newAbstract += $lines[$iP2a..$iP2b]
$newAbstract += ''
$newAbstract += $p13Text
$newAbstract += ''
$newAbstract += $lines[$iP3a..$iP3b]
$newAbstract += ''
$newAbstract += $lines[$iP5a..$iP5b]
$newAbstract += ''
$newAbstract += $lines[$iP4]
$newAbstract += $lines[$iEndAbs..($lines.Count - 1)]
$lines = $newAbstract

# ---------- 2. content edits ----------
for ($i = 0; $i -lt $lines.Count; $i++) {
    $t = $lines[$i]
    if ($t.Contains('[21]; 平衡相位闭式推导')) { $t = $t.Replace('[21]; 平衡相位闭式推导', '[22]; 平衡相位闭式推导') }
    if ($t.Contains('(arccos 形式) [20].')) { $t = $t.Replace('(arccos 形式) [20].', '(arccos 形式) [21].') }
    if ($t.Contains('\begin{thebibliography}{19}')) { $t = $t.Replace('\begin{thebibliography}{19}', '\begin{thebibliography}{23}') }
    if ($t.Contains('(O3a/C1 只覆盖垒族)')) { $t = $t.Replace('(O3a/C1 只覆盖垒族)', '(O3a/C1 的相位比刚性只覆盖垒族; 阱族侧已由会话 56 对一切 $R>1$ 补齐)') }
    if ($t.Contains('(25 页, 零警告)')) { $t = $t.Replace('(25 页, 零警告)', '(38 页, 零警告)') }
    $lines[$i] = $t
}

# ---------- 3. jumbled proof-technique list fix ----------
$iLd = -1; $iOrphan = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '左定理论: 用算子分数幂') { $iLd = $i }
    if ($lines[$i] -match '并保持特征函数系的完备性, 是主题一的理论骨架') { $iOrphan = $i }
}
if ($iLd -lt 0 -or $iOrphan -lt 0) { throw 'list markers missing' }
if ($iOrphan -le $iLd) { throw 'unexpected list layout' }
$ins = "`t`t并保持特征函数系的完备性, 是主题一的理论骨架."
$lines = @($lines[0..$iLd]) + @($ins) + @($lines[($iLd + 1)..($iOrphan - 1)]) + @($lines[($iOrphan + 1)..($lines.Count - 1)])

# ---------- 4. audit note ----------
$note = ' 独立子代理审计 (2026-08-10, Nash/Curie/Linnaeus): 后半与证书链全部 PASS; 前半逐行检查 83/83 通过, 唯一定性缺口在 lines 412--439 --- 文本证明了 $E(\alpha_1)=c\alpha_1$, $O(\alpha_2)=c\alpha_2$ 解的唯一性, 但未证明实际相位落在 $k=0$ 分支 ($\alpha_1\in(0,\pi/2)$, $\alpha_2\in(0,\pi)$); 断言本身为真 (短证思路: $y_1$ 偶正 $\Rightarrow$ Prüfer 相位 $\theta_1(1/2)=\pi/2\Rightarrow\alpha_1\in(0,\pi/2)$; $y_2>0$ 于 $(0,1/2)\Rightarrow\alpha_2\in(0,\pi)$), 数行内可修复, 尚未修复.'
$iAud = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'PDF 说明 8.1 如实标注') { $iAud = $i }
}
if ($iAud -lt 0) { throw 'audit marker missing' }
$lines[$iAud] = $lines[$iAud].Replace('PDF 说明 8.1 如实标注). 旧归约的失败路线', 'PDF 说明 8.1 如实标注).' + $note + ' 旧归约的失败路线')

# ---------- 5. write back with BOM ----------
$text = $lines -join "`r`n"
[IO.File]::WriteAllText($p, $text, (New-Object System.Text.UTF8Encoding($true)))
Write-Output ('OK lines=' + $lines.Count)
