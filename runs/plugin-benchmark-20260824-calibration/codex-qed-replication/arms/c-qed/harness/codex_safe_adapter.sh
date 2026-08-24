#!/usr/bin/env bash
set -euo pipefail

RealCodex=${QED_REAL_CODEX:-/home/huangzy/.local/bin/codex}
QEDCodexHome=/home/huangzy/.codex-benchmark/B3-O3-CAL-20260824/arm-c
QuotaScript=/mnt/f/benchmark/B3-O3-CAL-20260824/harness/latest_quota.py
WrapperLog=${QED_WRAPPER_LOG:-/mnt/f/benchmark/B3-O3-CAL-20260824/arm-c-qed-run1/wrapper.log}
QuotaStop=${QED_QUOTA_STOP_USED_PERCENT:-75}

QuotaUsed=$(python3 "$QuotaScript" "$QEDCodexHome/sessions")
if [ "$QuotaUsed" != "-1" ] && [ "${QuotaUsed%.*}" -ge "$QuotaStop" ]
then
	printf '%s BLOCK quota_used=%s threshold=%s\n' "$(date -Iseconds)" "$QuotaUsed" "$QuotaStop" >> "$WrapperLog"
	echo "QED safe adapter stopped before a new model call because weekly use reached ${QuotaUsed}%." >&2
	exit 75
fi

FilteredArgs=()
for Arg in "$@"
do
	case "$Arg" in
		--search|--dangerously-bypass-approvals-and-sandbox)
			;;
		*)
			FilteredArgs+=("$Arg")
			;;
	esac
done

ExecIndex=-1
for Index in "${!FilteredArgs[@]}"
do
	if [ "${FilteredArgs[$Index]}" = "exec" ]
	then
		ExecIndex=$Index
		break
	fi
done

if [ "$ExecIndex" -lt 0 ]
then
	echo 'QED safe adapter accepts only codex exec invocations.' >&2
	exit 64
fi

PreArgs=("${FilteredArgs[@]:0:$ExecIndex}")
PostStart=$((ExecIndex + 1))
PostArgs=("${FilteredArgs[@]:$PostStart}")
PromptArg=${FilteredArgs[$((${#FilteredArgs[@]} - 1))]}
PromptHash=$(printf '%s' "$PromptArg" | sha256sum | cut -d ' ' -f 1)
printf '%s START pid=%s quota_used=%s prompt_chars=%s prompt_sha256=%s\n' "$(date -Iseconds)" "$$" "$QuotaUsed" "${#PromptArg}" "$PromptHash" >> "$WrapperLog"

ProxyUrl=${QED_MODEL_PROXY_URL:?QED_MODEL_PROXY_URL is required}
export HTTP_PROXY="$ProxyUrl"
export HTTPS_PROXY="$ProxyUrl"
export ALL_PROXY="$ProxyUrl"
export http_proxy="$ProxyUrl"
export https_proxy="$ProxyUrl"
export all_proxy="$ProxyUrl"
export NO_PROXY=127.0.0.1,localhost
export no_proxy=127.0.0.1,localhost
export CODEX_HOME="$QEDCodexHome"
export CODEX_PERMISSION_PROFILE=:workspace
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

exec "$RealCodex" \
	"${PreArgs[@]}" \
	exec \
	--ignore-rules \
	--skip-git-repo-check \
	--strict-config \
	--color never \
	-s workspace-write \
	-c 'approval_policy="never"' \
	-c 'sandbox_mode="workspace-write"' \
	-c 'sandbox_workspace_write.network_access=false' \
	-c 'agents.enabled=false' \
	"${PostArgs[@]}"
