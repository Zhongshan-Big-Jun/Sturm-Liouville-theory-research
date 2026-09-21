# NIST DLMF 4.22.3: read equation excerpt

Source: https://dlmf.nist.gov/4.22.E3 . Actual reading: equation 4.22.3 and its stated exclusion z != n*pi for n in Z, as rendered by the web tool. The full HTML page and its cited books were not downloaded. This is an explicitly transcribed equation, not raw website bytes.

cot(z) = 1/z + 2*z*sum_(n=1)^infinity 1/(z^2-n^2*pi^2), when z is not an integer multiple of pi.

The project uses this identity only for real 0<z<pi. The inference to positive summands and monotonicity of (1/z-cot(z))/z is derived in the project's proof, not attributed as an independently read statement from this excerpt.

The official chapter page reported version 1.2.8, release date 2026-09-15. A direct Python fetch of the TeX endpoint failed with SSL UNEXPECTED_EOF_WHILE_READING; the web tool's TeX fetch refused application/x-tex. Neither failure is a source-body download or a mathematical failure. The successful HTML-equation tool response is preserved in web-page-response.json.
