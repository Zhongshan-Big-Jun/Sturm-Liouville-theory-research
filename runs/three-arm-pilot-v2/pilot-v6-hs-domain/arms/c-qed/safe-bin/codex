#!/usr/bin/env bash
set -euo pipefail

RealCodex=${QED_REAL_CODEX:?QED_REAL_CODEX is required}
CodexHome=${QED_CODEX_HOME:?QED_CODEX_HOME is required}
WrapperLog=${QED_WRAPPER_LOG:?QED_WRAPPER_LOG is required}
PromptAdapter=${QED_PROMPT_ADAPTER:?QED_PROMPT_ADAPTER is required}

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
LastIndex=$((${#FilteredArgs[@]} - 1))
PromptArg=${FilteredArgs[$LastIndex]}
PromptHash=$(printf '%s' "$PromptArg" | sha256sum | cut -d ' ' -f 1)
AdaptedPrompt=$(python3 "$PromptAdapter" "$PromptArg" "$(pwd -P)")
AdaptedHash=$(printf '%s' "$AdaptedPrompt" | sha256sum | cut -d ' ' -f 1)
FilteredArgs[$LastIndex]=$AdaptedPrompt
PostStart=$((ExecIndex + 1))
PostArgs=("${FilteredArgs[@]:$PostStart}")
printf '%s START pid=%s prompt_chars=%s prompt_sha256=%s adapted_chars=%s adapted_sha256=%s\n' "$(date -Iseconds)" "$$" "${#PromptArg}" "$PromptHash" "${#AdaptedPrompt}" "$AdaptedHash" >> "$WrapperLog"

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
