# L01/L03/L04/L05/L06 literature and domain adaptation author report

Completed author package at 2026-09-23T07:17:24.300849+00:00. Role: literature/adaptation AUTHOR, not final verifier. Every new proof and card awaits the coordinator's fresh independent review. No independent approval, canonical acceptance, library release, commit, or remote write is claimed.

All writes are under `/mnt/f/tools/sl-literature-absorption-20260923/author-domains`. The SL project, installed plugin, canonical graph, existing library, historical evidence, and other author directories were read-only for this author.

## Delivered mathematical results

1. `proofs/01-parity-unitary.md`: complete normalized unitary U f=(sqrt(2) f_e|_(0,1),sqrt(2) f_o|_(0,1)), inverse, both operator-domain inclusions (including H2 gluing), and all Borel functional-calculus domains. The half-interval domains are Neumann-Neumann and Dirichlet-Robin. Both affine eigenmodes are retained. Status: author proof.

2. `proofs/02-fractional-trace-dictionary.md`: a fully specified adaptation of Grubb using full-interval Neumann and shifted Robin operators; the Robin shift is +4 and positivity is proved. Off s=3/2+2k, require exactly B(f^(2j))=0 for 2j+3/2<s. At equality impose the explicit distance-weighted integral on the highest parity residual. The bridge checks the cited uniform-order local boundary hypotheses and avoids assuming an unverified mixed-order theorem. Both domain inclusions and critical-norm control are explained. Status: author proof from an identified external theorem, pending independent review.

3. `proofs/03-s3-cofinite-closure.md`: a complete author sufficiency proof, not merely a proposed obstruction. For cofinite N in {0,1,4,5,...}, the Hc3 closure is precisely the functions with f(0)=0 if 0 is missing, f'(0)=0 if 1 is missing, and f''(0)=0 if 4 is missing. Codimension is |{0,1,4} minus N|. The proof establishes Hc3=H3_Sob intersect ker B, then local third-derivative cutoff estimates, divisible polynomial approximation, and a fixed endpoint correction. The old s=2 two-trace classification is not extended by assertion. Status: author-proved candidate theorem awaiting review.

4. `proofs/04-boundary-algebra-and-gkn-scope.md`: independently recalculated project boundary algebra with dimensions, isotropy, and right inverses distinguished. This reproduces existing four-trace structure (determinant15360), not a new proof of the already established full-family density. Status: author derivation plus exact algebra checks.

L06 is comparative extension reading only. `notes/L06-comparative-extension.md` explains the singular weighted descent and a sufficient matching choice in its sharpness example; it does not replace Krein boundary conditions.

## Exact progress and remaining gaps

- The current project's 0<=s<7/2 whole-family density and all-member threshold were respected. No previously solved density window was reopened.
- The proposed s=3 cofinite question now has a written author proof of both inclusions; no analytic step is intentionally left as an unnamed lemma. Independent scrutiny of the form-domain identification, local cutoff bounds, and the sequential limits is still required before acceptance.
- No deletion classification at s=5/2, general noninteger s, infinite deletions, arbitrary constrained/projection-generated spaces, or frame/Riesz/Schauder basis theorem is supplied.
- The fractional dictionary is restricted to the smooth constant-coefficient project realization and fixed c>0; it gives no uniform-in-c estimates or alternative fractional-Laplacian interpretation.
- None of the Sobolev analysis was formalized in Lean. Exact finite algebra does not certify it.

## Sources actually read and access limits

| ID | Original actually read | Depth and limitation |
|---|---|---|
| L01 | [arXiv2408.01514v1](https://arxiv.org/pdf/2408.01514v1), 50 pages | Section2, pp10-14. Journal metadata verified; journal body not obtained. |
| L03 | [arXiv1412.3744v4](https://arxiv.org/pdf/1412.3744v4), 14 pages, and [author-posted journal original](https://web.math.ku.dk/~grubb/MN16.pdf) | Section2; journal pp832-833, especially Definition2.1/Thm2.2 p833 (PDF p4). Critical formulas visually checked. Later regularity theory not fully audited. |
| L04 | [arXiv1706.01539v1](https://arxiv.org/pdf/1706.01539v1), 28 pages | Targeted pp4-20, general GKN/rank statements and Sections3-4. Journal revised body not obtained; v1 singular examples not adopted. |
| L05 | [arXiv2410.04647v2](https://arxiv.org/pdf/2410.04647v2), 36 pages | Hyp2.1 and Section4 pp20-26, including actual symmetry/domain hypotheses and normalized map. No whole-paper audit. |
| L06 | [arXiv2607.19758v1](https://arxiv.org/pdf/2607.19758v1), 19 pages | Existence and version verified, submission2026-07-22; model plus Sections7-9 and pp11-17. No journal publication verified. |

All five versioned arXiv PDFs and metadata were actually downloaded with HTTP200. Four direct publisher requests returned HTTP403; publisher journal metadata was read through indexed primary-publisher search records, not silently equated with direct full-text access. Grubb's author-hosted journal PDF returned HTTP200. Actual requested/final URLs, UTC start/completion times, statuses, raw/text SHA256, extraction method and reading locators are preserved in `source-manifest.json` and its linked capture logs. The capture records remain labeled CAPTURE_ONLY; separate reading records describe what was subsequently read.

Original-page cautions: L04 v1 p15 uses deficiency(1,1) in its full-interval Legendre discussion; the both-limit-circle model has(2,2). We imported only the general quotient argument with independently derived project counts; whether the journal body repairs its examples is unknown. L06 (7.5)/(9.5) have inconsistent notation, visually verified; consistent formulas (1.3)/(10.2) anchor the note. The source sharpness example's C^n matching alone is insufficient for the stated higher local regularity; the author supplies Taylor matching through2n-1. No independent erratum review is claimed. Grubb's online publication day differs by one between the indexed publisher record and PDF; bibliographic year/volume/pages agree.

## Verification actually performed

- `python3 scripts/exact_checks.py`: 98 exact SymPy assertions passed, including symbolic all-index residual identities, sqrt(2) normalization, trace matrices, q6, and boundary-form isotropy. Four counterfactual controls were explicitly rejected. Run and script SHA256 are in `evidence/exact-checks.json`.
- `python3 scripts/verify_delivery.py`: 74 package identity/schema checks passed, binding the captured raw/extracted sources, visual pages, current read inputs, proposed cards and proof files. This is package self-checking, not mathematical review.
- No Lean compilation, project maintenance script, plugin mutation, accepted-knowledge receiver, subdelegation or remote write was used. The workspace-dependency discovery tool returned unavailable; existing local Python/PyMuPDF/SymPy handled capture and algebra.

## Project input identity and naming

Current read baseline HEAD: `902d2a931a76dae5fe1ef6d7dacdcfa230897f9c`. The requested `docs/SL_fractional_spaces.tex` is absent; the actual source is `/mnt/f/LaTeX/BVE research/docs/SL_fractional_left_definite.tex`. Also read `SL_cofinite_left_definite.tex`, relevant H3 setup, `tools/spectral-domain-checks.md`, `tools/krein-power-domain-polynomial-obstruction.md`, and `tools/leftdef-o1pld-l2-structural.md`. Exact absolute paths, hashes and bounded reading coverage are in `evidence/project-input-manifest.json`.

## Proposed integration and private originals

Four JSON cards are proposals only. Source IDs L01/L03/L04/L05/L06 are local author-manifest labels, not registered library identifiers. The coordinator must register the actual captured originals and map locators/IDs, freeze the supplied proof bytes, and obtain fresh independent review before accepted reuse. No existing card was edited.

Raw PDFs, full extracted text, source page images and raw publisher-search text are in `private-sources/`, excluded by `.gitignore`. They remain local and must not be included in public Git publication. Original notes/proofs/cards are the proposed publication material. The source manifest and checks are provenance material; review any administrative paths before publishing.

## Exact changed paths and hashes

Every file in this new author root was created by this author. `FILES.json` lists every absolute changed path, size, SHA256 and private-source classification except its own recursive entry and SHA256SUMS. `SHA256SUMS` binds all files including FILES.json and this REPORT, excluding itself. Its own hash is returned in the final handoff. No changed path outside this root is claimed.

Primary reading artifact SHA256:

| ID | PDF SHA256 | Extracted text SHA256 |
|---|---|---|
| L01 | `454516433db2d5bcab7cc331ded464d322367c6204d1938f2671473bc38cbe40` | `77150eaab5dbb6931aced265d887b080e725193bed3db574f4ab4d1385e355de` |
| L03 | `8dec5ce7ffe30c5f43c68dd6b93a2cedf038d47cf42b54a621a65eb178350f36` | `e7a4a1d6e119364a09410de2cddfb4013896e2fb512dc757fc5d8af2dddc34ad` |
| L04 | `73f6d4f8d074542f04c3b90d1badcea36b204e424d06e49cea27f8690f809957` | `87e17f097007dbc81ada097f1d7a5beeccd6734a6405be8710971b32d88a548a` |
| L05 | `e3cc4394c7a613395a5ae56ef275face5bf38c805f7599065547465973c44045` | `dcf871f890ec7df30cece96e386d29744c9a504d2fe53c8d514bafa2b2e94b6b` |
| L06 | `eebcb1e07b1326dff50a6a6a3b0c147e6b4c3849a04ced012d5510dcb408ba8d` | `707e4abea8893e3d4edc54b9015fc43938bf9836d8f3bde6959421aff8ccb39f` |
| L03 journal author copy | `e5ef9c099f756a1ee5485663bfcf7314dbb6721fc61b745f36001f42ff50c09a` | `3b21273cbdfbf4faf15f11669c0077fa8e0d708eaf1adfe960ec2c66386df4c0` |

Author deliverables (absolute paths):

- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/AGENTS.md` — SHA256 `cea6fc43956a00d06961bb41d6f7492d4c9b69a12d400be7675c9746dbb95d55`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/source-manifest.json` — SHA256 `74efeef0f4424cb50b63af202843cd7855061c945237a23d294790aa80ab6502`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L01-source-to-claim.md` — SHA256 `22292437d94b72084d941606e642f9b5d9460eeba0db9c95c7b3b8d1ad3842b2`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L03-source-to-claim.md` — SHA256 `e26c2d0df848ac77cacd2040b138d14603b608d5ba75685880184ca01ed9ce58`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L04-source-to-claim.md` — SHA256 `31bba0be9680a2b42586a407a0f2dec027c6d926e43f751c6aab58c24a796aa2`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L05-source-to-claim.md` — SHA256 `6c3b5b1cc3563afdcb8ef452ff23984b33fcfd4f7155b889d2ac394dbf661d2c`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L06-comparative-extension.md` — SHA256 `73e320e04e426ab873258caaab32b0fb95b6de196e37cb9ae03d25695b89fda3`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/notes/L06-source-to-claim.md` — SHA256 `2b9ee49238d3342b547301b19ec389e91a1ea141133d1c066b5d6f839e2a95ab`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proofs/01-parity-unitary.md` — SHA256 `3e0a5c5c56298ffc31b7f98a30848fa0ec32d3d2ec24dedcd2ffd061c82a3aaa`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proofs/02-fractional-trace-dictionary.md` — SHA256 `111370dd245470b17545d462d507e39add29134c5961867446d4e039f482c0fe`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proofs/03-s3-cofinite-closure.md` — SHA256 `72a80213f816072e4fdeb50b0a839c0b4e6f25a8182e627ef7db087498719e42`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proofs/04-boundary-algebra-and-gkn-scope.md` — SHA256 `cb3a3f2c67da73d7ec31bf5b1d7794eb2125b2f324ec3f992d8f965f7e3567e7`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proposed-tool-cards/krein-boundary-right-inverses.json` — SHA256 `ce2305b26e7680f8759157648967519a98988666b67a1bd85c3327a9e0d056da`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proposed-tool-cards/krein-fractional-trace-dictionary.json` — SHA256 `a22ab1786ed919309e2ab236e2302aaac5a2ca4d574762f218c9d3deceb4fbd2`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proposed-tool-cards/krein-parity-unitary.json` — SHA256 `681471a1821ee24b0e556d992a8e3c2dec4de386102391bb7d81b959efc2b2a1`.
- `/mnt/f/tools/sl-literature-absorption-20260923/author-domains/proposed-tool-cards/krein-s3-cofinite-three-traces.json` — SHA256 `e7615ef2dc4c159dfb3b441c92288d381b0595059dd7bc072f4e7c744005f4a1`.

Current next action: fresh independent mathematical review of the frozen proofs 01-04, with emphasis on the Grubb auxiliary-operator bridge and the new order-three cofinite sufficiency argument. Source limitations above remain attached to their specific versions.
