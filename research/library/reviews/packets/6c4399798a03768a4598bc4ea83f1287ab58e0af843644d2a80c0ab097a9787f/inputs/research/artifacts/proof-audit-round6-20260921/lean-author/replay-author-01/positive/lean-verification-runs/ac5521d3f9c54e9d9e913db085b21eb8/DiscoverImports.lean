import Lean

def main (Arguments : List String) : IO UInt32 := do
  let [FileName] := Arguments | throw (IO.userError "expected one source path")
  let Source <- IO.FS.readFile FileName
  let (Header, _, Messages) <- Lean.Parser.parseHeader (Lean.Parser.mkInputContext Source FileName)
  if Messages.hasErrors then
    throw (IO.userError "Lean import header parse failed")
  let Imports := Lean.Elab.headerToImports Header
  let Records := Imports.map fun Item => Lean.Json.mkObj [
    ("module", Lean.toJson Item.module.toString),
    ("components", Lean.toJson (Item.module.components.map Lean.Name.getString!))]
  IO.println (Lean.Json.arr Records).compress
  return 0
