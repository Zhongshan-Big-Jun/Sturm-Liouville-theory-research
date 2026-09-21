# Exact scoped evidence archive

`archive-manifest.json` maps original relative paths to unchanged payloads. Verify stored SHA256, decompress deterministic gzip if marked, then verify original SHA256 and size. Large full Lean receipts and failed/interrupted attempts are retained. Readable `receipt-indexes` omit large fields only in the derived index; the full raw receipt remains available. Compiled objects use `.bin` to keep them out of live import search. Original absolute run paths are preserved rather than rewritten.

Native tool records are actual coordinator-recorded calls/results, not cryptographic service attestations. Author checks, independent execution and semantic approval are distinct. For replay, materialize the mapped payloads in a separate directory and use the frozen runtime configuration. Pinned Windows compiler/Mathlib binaries remain external inputs.

`excluded_context_only`, when nonempty, lists unrelated private workspace instructions by hash; these are retained locally and were never used as executable regression dependencies. They are deliberately not published. This exclusion does not remove mathematical source, executed program, command log or compiler receipt. Archive paths are not proof of a mathematical claim.
