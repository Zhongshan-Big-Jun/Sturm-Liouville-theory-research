import Lake
open Lake DSL

package LeanProof where
                                                                    

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"

@[default_target]
lean_lib SL where
  globs := #[`SL.+]

lean_lib SLVerified where
  roots := #[`SLVerified]

lean_lib SLDrafts where
  roots := #[`SLDrafts]
