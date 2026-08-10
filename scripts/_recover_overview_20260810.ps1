$ErrorActionPreference = 'Stop'
$p = 'F:\LaTeX\BVE research\docs\SL_spectral_topics_summary.tex'
$bak = 'F:\LaTeX\BVE research\misc\_summary_mangled_20260810.tex.bak'
$lines = Get-Content -LiteralPath $p -Encoding UTF8
if ($lines.Count -ne 1511) { throw "unexpected current count $($lines.Count)" }

# locate stray P1 paragraph (the abstract paragraph displaced into the body)
$iP1 = -1
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^本版 \(2026-08-05, 会话 13\)') { $iP1 = $i } }
if ($iP1 -lt 0) { throw 'stray P1 not found' }
# locate second \end{abstract} (start of the faithful tail)
$ends = @()
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^\\end\{abstract\}') { $ends += $i } }
if ($ends.Count -ne 2) { throw "expected 2 end-abstract markers, got $($ends.Count)" }
$iTail = $ends[1]

$orig = @()
$orig += $lines[0..26]
$orig += ($lines[27].TrimEnd() + ' ' + $lines[$iP1])
$orig += $lines[28..52]
$orig += $lines[$iTail..($lines.Count - 1)]

if ($orig.Count -ne 943) { throw "reconstruction count $($orig.Count) != 943" }
if ($orig[27] -notmatch '本版 \(2026-08-05, 会话 13\)') { throw 'P1 not restored into line 28' }
if ($orig[53] -notmatch '^\\end\{abstract\}') { throw 'line 54 not end-abstract' }
$nb = ($orig | Where-Object { $_ -match '^本版 \(' }).Count
if ($nb -ne 4) { throw "expected 4 本版 paragraphs, got $nb" }
$ne = ($orig | Where-Object { $_ -match '^\\end\{abstract\}' }).Count
if ($ne -ne 1) { throw "expected 1 end-abstract, got $ne" }

# marker-count checks (each edit should appear exactly the expected number of times)
$t = $orig -join "`n"
$checks = @{
  '[22]; 平衡相位' = 1
  '(arccos 形式) [21].' = 1
  '\begin{thebibliography}{23}' = 1
  '(38 页, 零警告)' = 2
  '阱族侧已由会话 56' = 1
  '独立子代理审计' = 1
  '并保持特征函数系的完备性' = 1
}
foreach ($k in $checks.Keys) {
  $c = ([regex]::Matches($t, [regex]::Escape($k))).Count
  if ($c -ne $checks[$k]) { throw "marker '$k' count $c != $($checks[$k])" }
}

# backup mangled then write reconstructed
Copy-Item -LiteralPath $p -Destination $bak -Force
$text = $orig -join "`r`n"
[IO.File]::WriteAllText($p, $text, (New-Object System.Text.UTF8Encoding($true)))
Write-Output ('RECONSTRUCTED OK lines=' + $orig.Count)
