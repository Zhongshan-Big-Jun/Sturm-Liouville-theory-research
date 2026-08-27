# Arm C infrastructure-invalid run 2

Status: `INFRA_INVALID`. This run is excluded from mathematical scoring.

The replacement disabled the Codex Code Mode host to enforce the frozen no-network contract.
That setting also disabled every model-side filesystem operation. QED passed file paths, not
file contents, to its roles. The decomposer and prover therefore returned explicit tool-access
blockers instead of mathematical artifacts. QED saved those responses through its fallback,
then ran structural and regulator roles over the empty outputs. The final regulator call ended
with a TLS connection failure.

No role received the frozen problem contents. The run cannot be interpreted as a failed proof
attempt.

## Resource data

| Metric | Value |
|---|---:|
| Wall time | 250 s |
| Sessions | 6 |
| Model responses | 21 |
| Model tool calls | 0 |
| Input tokens | 242392 |
| Cached input tokens | 150272 |
| Uncached input tokens | 92120 |
| Output tokens | 5680 |
| Reasoning output tokens | 2818 |
| API-equivalent normalized estimate | USD 0.5421888 |

The normalized estimate uses the same cross-arm proxy as the scored arms. The final failed TLS
session exposed no token counter and contributes zero to token totals.

The prompt-input probe passed with SHA256
`732774EC079D1A52E52C2984849B9C7E6947E81579D2668DEA6F3B59922E324F` and zero
project-document, skill, plugin, memory, or multi-agent leakage markers.
