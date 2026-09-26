import Lean
import AuditRound12

open Lean Elab Command Meta

set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.maxSteps 10000000
set_option pp.deepTerms true

private def declarationKind (Info : ConstantInfo) : String :=
  match Info with
  | .axiomInfo _ => "axiom"
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "definition"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient_primitive"

private partial def binderKinds (E : Expr) : List String :=
  match E with
  | .forallE _ _ B K => reprStr K :: binderKinds B
  | _ => []

elab "#export_round12" : command => do
  let Env := (← getEnv).setExporting false
  let Names := Env.constants.toList.map Prod.fst |>.filter (fun N =>
    "AuditRound12.".isPrefixOf N.toString) |>.toArray |>.qsort Lean.Name.lt
  let mut Records := #[]
  for Name in Names do
    let some Info := Env.checked.get.find? Name | throwError "missing {Name}"
    let PrintedType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.all false |>.setBool `pp.universes true |>.setBool `pp.explicit false)
      (do return (← ppExpr Info.type).pretty)
    let Readable ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.all false |>.setBool `pp.universes true |>.setBool `pp.explicit false)
      (do return (← ppExpr Info.type).pretty)
    let Body ← if Info.isTheorem then pure Json.null else
      match Info.value? (allowOpaque := true) with
      | none => pure Json.null
      | some V => do
        let S ← liftTermElabM <| withOptions
          (fun O => O.setBool `pp.all false |>.setBool `pp.universes true |>.setBool `pp.explicit false)
          (do return (← ppExpr V).pretty)
        pure (toJson S)
    let Axioms ← collectAxioms Name
    Records := Records.push <| Json.mkObj [
      ("name", toJson Name.toString), ("kind", toJson (declarationKind Info)),
      ("universes", toJson (Info.levelParams.map Lean.Name.toString)),
      ("binder_kinds", toJson (binderKinds Info.type)),
      ("type_explicit", toJson PrintedType), ("type_readable", toJson Readable),
      ("definition_value_explicit", Body),
      ("transitive_axioms", toJson (Axioms.qsort Lean.Name.lt |>.map Lean.Name.toString)),
      ("unsafe", toJson Info.isUnsafe),
      ("type_dependencies", toJson (Info.type.getUsedConstants.map Lean.Name.toString)),
      ("body_dependencies", toJson ((Info.value? (allowOpaque := true) |>.map Expr.getUsedConstants |>.getD #[]).map Lean.Name.toString))]
  IO.FS.writeFile "F:/tools/math-audit-round12-20260926/formal-reviewer/d080d3cc-independent-bk5cllgu/readable-declarations.json"
    ((Json.arr Records).pretty ++ "\n")
  logInfo m!"Exported {Names.size} namespace declarations with actual types, definition values and collectAxioms."

#export_round12
