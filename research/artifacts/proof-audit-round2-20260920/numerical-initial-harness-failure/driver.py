import contextlib,importlib.util,io,sys
from scipy import integrate
from unittest.mock import patch
buf=io.StringIO()
with patch.object(integrate,"quad",side_effect=RuntimeError("quadrature at import")),contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
 spec=importlib.util.spec_from_file_location("audit_target",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert not buf.getvalue(),repr(buf.getvalue())
print("IMPORT_CONTROL: no output or quadrature at import",flush=True)
m.main()
