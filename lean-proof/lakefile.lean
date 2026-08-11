import Lake
open Lake DSL

package LeanProof where
  -- Formalizations for the Sturm-Liouville theory research project.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"

@[default_target]
lean_lib SL where
  globs := #[`SL.+]