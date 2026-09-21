# Exact evidence archive

`archive-manifest.json` maps every original relative path to a stored payload. Files larger than 1 MB use deterministic gzip; duplicate raw payloads are stored once. Verify `stored_sha256`, decompress when `encoding` is `gzip`, then verify `original_sha256` and `original_bytes`. This preserves the complete verifier receipts, exports, raw logs, source snapshots and compiled objects, including interrupted/failed attempts. Do not edit old receipts to make their absolute execution paths point here.

`receipt-indexes/` contains readable derived indexes. Large nested environment/expression fields are omitted only from these indexes; the unchanged full receipts are retained in the mapped archive. These indexes are not replacement machine evidence. `native-tool-records/` holds the coordinator-recorded actual tool calls, not cryptographic service attestations.

For replay, use the frozen `replay.py` and input snapshot in the original author package or first materialize all original paths from this archive into a separate directory. The configured Windows Lean/Mathlib installation is an external pinned runtime, not redistributed here. Full mathematical analysis is outside this local real-algebra formalization.
