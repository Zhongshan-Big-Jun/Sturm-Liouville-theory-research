#!/usr/bin/env bash
set -euo pipefail

RealCodex=${QED_REAL_CODEX:-/home/huangzy/.local/bin/codex}
CodexHome=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-c
WrapperLog=${QED_WRAPPER_LOG:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run1/wrapper.log}

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
printf '%s START pid=%s prompt_chars=%s prompt_sha256=%s\n' "$(date -Iseconds)" "$$" "${#PromptArg}" "$PromptHash" >> "$WrapperLog"

ProxyUrl=${QED_MODEL_PROXY_URL:?QED_MODEL_PROXY_URL is required}
export HTTP_PROXY="$ProxyUrl"
export HTTPS_PROXY="$ProxyUrl"
export ALL_PROXY="$ProxyUrl"
export http_proxy="$ProxyUrl"
export https_proxy="$ProxyUrl"
export all_proxy="$ProxyUrl"
export NO_PROXY=127.0.0.1,localhost
export no_proxy=127.0.0.1,localhost
export CODEX_HOME="$CodexHome"
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
	-c 'features.code_mode_host=false' \
	"${PostArgs[@]}"
