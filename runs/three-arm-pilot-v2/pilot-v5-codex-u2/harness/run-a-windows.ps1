$RunRoot = 'F:\benchmark\PILOT-V5-CODEX-U2-20260825'
$WorkRoot = Join-Path $RunRoot 'arm-a-plugin'
$RepoRoot = 'F:\LaTeX\BVE research'
$PilotRoot = Join-Path $RepoRoot 'runs\three-arm-pilot-v2\pilot-v5-codex-u2'
$PromptSource = Join-Path $PilotRoot 'arm-a-prompt.md'
$PromptPath = Join-Path $WorkRoot 'PROMPT.md'
$SkillSource = 'C:\Users\HuangZY\.codex\plugins\cache\math-research\rigorous-open-math-research\1.6.0\skills\rigorous-open-math-research'
$SkillTarget = Join-Path $WorkRoot '.agents\skills\rigorous-open-math-research'
$CodexHome = 'F:\benchmark\B3-O3-CAL-20260824\codex-home-a-windows'
$EventsPath = Join-Path $WorkRoot 'events.jsonl'
$StderrPath = Join-Path $WorkRoot 'stderr.log'
$FinalPath = Join-Path $WorkRoot 'final_response.md'
$WallCapMinutes = 80

if(-not (Test-Path -LiteralPath $CodexHome))
{
	throw 'Isolated Codex home is missing.'
}

New-Item -ItemType Directory -Path $WorkRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $SkillTarget) -Force | Out-Null
Copy-Item -LiteralPath $PromptSource -Destination $PromptPath -Force

if(-not (Test-Path -LiteralPath $SkillTarget))
{
	Copy-Item -LiteralPath $SkillSource -Destination $SkillTarget -Recurse
}

$env:CODEX_HOME = $CodexHome
$env:CODEX_PERMISSION_PROFILE = ':workspace'
Remove-Item Env:CODEX_SESSION_ID,Env:CODEX_THREAD_ID,Env:CODEX_INTERNAL_ORIGINATOR_OVERRIDE -ErrorAction SilentlyContinue

$CodexArgs = @(
	'exec',
	'--ignore-rules',
	'--skip-git-repo-check',
	'--strict-config',
	'--json',
	'--color',
	'never',
	'-m',
	'gpt-5.6-sol',
	'-c',
	'model_reasoning_effort="xhigh"',
	'-c',
	'approval_policy="never"',
	'-c',
	'sandbox_mode="workspace-write"',
	'-c',
	'sandbox_workspace_write.network_access=false',
	'-c',
	'agents.enabled=true',
	'-c',
	'agents.default_subagent_model="gpt-5.6-sol"',
	'-c',
	'agents.default_subagent_reasoning_effort="xhigh"',
	'-c',
	'agents.max_concurrent_threads_per_session=3',
	'-s',
	'workspace-write',
	'-C',
	$WorkRoot,
	'-o',
	$FinalPath,
	'-'
)

$CodexPath = (Get-Command codex).Source
$StartedAt = Get-Date
$Process = Start-Process -FilePath $CodexPath -ArgumentList $CodexArgs -PassThru -WindowStyle Hidden -RedirectStandardInput $PromptPath -RedirectStandardOutput $EventsPath -RedirectStandardError $StderrPath
Write-Output "PID=$($Process.Id)"
Write-Output "STARTED_AT=$($StartedAt.ToString('o'))"

$Deadline = $StartedAt.AddMinutes($WallCapMinutes)
while(-not $Process.HasExited)
{
	if((Get-Date) -ge $Deadline)
	{
		Stop-Process -Id $Process.Id
		Write-Output 'STOP_REASON=WALL_CAP'
		break
	}

	Start-Sleep -Seconds 5
	$Process.Refresh()
}

$EndedAt = Get-Date
Write-Output "ENDED_AT=$($EndedAt.ToString('o'))"
Write-Output "WALL_SECONDS=$([Math]::Round(($EndedAt-$StartedAt).TotalSeconds,3))"
if($Process.HasExited)
{
	Write-Output "EXIT_CODE=$($Process.ExitCode)"
}
