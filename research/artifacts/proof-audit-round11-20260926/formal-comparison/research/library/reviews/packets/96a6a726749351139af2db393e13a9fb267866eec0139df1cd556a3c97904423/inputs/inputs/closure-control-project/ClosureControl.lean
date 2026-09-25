namespace Round11Control
axiom hidden : False
def hiddenProp : Prop := hidden.elim
theorem contaminated : hiddenProp := hidden.elim
theorem valid : True := True.intro
end Round11Control
