# Repro manifest - R-20260806T140000Z-o1revise-2ED02A

## Task and inputs (sha256)

| Item | File | sha256 | Role | Verification note |
|---|---|---|---|---|
| Task packet | agenda/task-packets/Q-20260806-o1-revise-2ED02A.md | 4A2452D9DC53F4FCE77A541EBA0B85054A354B07893F642271ABF00638479225 | repair+reaudit spec | rechecked per R1-R4 |
| O1 draft | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md | C647297430348618A5120A3EAE5FAD09003B25EAFB9C8A8CCD9F449D1B397341 | repair target | read-only |
| O1 audit report | runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md | E6D1688963184DCBB87EC71EF8DB3B095A322D8B10D229CF8547ADB198B162CA | verdicts O1a-O1f | rechecked |
| Repair list | runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/candidate_proof.md | 7DF07F84810788BC2AF5E5F718AB019AB731B26F19B98CD35008CEB0B53B4C06 | R1-R4 | rechecked |
| Obligation graph | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md | 62998C6E8066AAC9E6676FD0B78288830439E964330F7B84E404A604E7ADC7B2 | O1 dependencies | rechecked |
| Draft problem contract | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md | 0FCD9F94293C7847342F4BDD7BE2B8B2F517D32F6E7D41536AB7409AECDBF779 | normalization base | rechecked |
| AEH paper | papers/fundamental_gap.txt | 2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14 | Lemma 2.1, 2.2 source | verified verbatim |
| Keller 1976 | papers/keller1976.txt | 7EEAB2777926C4BA5ED3C3806647B4D8A9A9750AD75A5B0BB2A77653F422EF3C | context | class difference noted |
| Mahar-Willner 1976 | papers/mw1976.txt | 0DCD8172BAA80ECE55DC64804DC709279C6C56DA83FE470122644F63332C7B01 | context | class difference noted |
| Tool lead | tools/gap-n1-reduction.md | 5611C69D6CF68740B795C0AD94D664729D4DAF04018E2040BDFC2983C76A027D | lead only | not a premise |
| Tool lead | tools/feynman-hellmann.md | EE5FDD872E06841EAE056A566CF898D5279657EDBE744054B5178544BBCD43AC | lead only | not a premise |
| Tool lead | tools/bang-bang.md | 4291285F2A9C842E32E58A3308E50D47B17421F66E3946D0D8F7DC1E8E91528B | lead only | not a premise |

## Environment

- OS: Windows 10+, PowerShell 7; cwd F:\LaTeX\BVE research
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  3.10.11 (numpy 2.2.6, scipy 1.15.3) with PYTHONUTF8=1
- xelatex: D:\texlive\2024\bin\windows\xelatex.exe (available; no PDF required
  by this run's deliverable, only markdown artifacts)
- No formal prover used.  All numeric claims are evidence; proof-level claims
  are argued in candidate_proof.md and audit_report.md.
- Network: enabled; used for the Phase 11 literature novelty check.

## Known unknowns

- model field: null (manager run-manifest.json).
- Exact version header of the O1 draft: dated 2026-08-05 in the draft-run
  manifest; no in-file version string.
- OCR of the primary-source txt files has occasional glyph corruption; every
  quoted statement was re-read in context and cross-checked against the
  mathematical content.

## Reproducibility artifacts (this run)

See reproducibility/ subdirectory:
- verify_o1_revision.py (main numeric verification battery)
- verify_hs_bound.py (Hilbert-Schmidt bound + eigenvalue continuity check)
- verify_fh_sign.py (moving-jump derivative signs, one-sided and two-sided)
- verify_structure_f.py (O1c structure checks on hostile configs)
- verify_reduction_search.py (random adversarial configs vs barrier/well max/min)
- outputs: *out.json
Random seeds are fixed and recorded in each script header.

## Sun 2022 access log (2026-08-06 continuation session)

Target: Sun, "On the minimum eigenvalue gap for vibrating string", JMAA 516
(2022) No. 1, 126513, Zbl 1506.34110, DOI 10.1016/j.jmaa.2022.126513.

| Route | Result | Evidence saved |
|---|---|---|
| zbMATH Open API an:1506.34110 | 200; full review + references | research_cache/sun2022_zbmath.json (+ sun2022_zbmath_parsed.txt) |
| OpenAlex works/doi:10.1016/j.jmaa.2022.126513 | 200; closed access, no abstract | research_cache/sun2022_openalex.json |
| Crossref works/10.1016/j.jmaa.2022.126513 | 200; no abstract | research_cache/sun2022_crossref.json |
| ScienceDirect landing page + r.jina.ai proxy | blocked (connection closed/failed) | - |
| Peeref works/26609210 | login wall | - |
| Semantic Scholar Graph API | HTTP 429 (twice) | - |
| MaRDI portal Publication:2166449 | 200; empty metadata page | research_cache/mardi4nfdi_sun2022.html |
| zbMATH pdf/07574902.pdf | HTTP 403 | - |
| Web search | abstract sentence only; S1/S2 not exposed | recorded in status_and_literature.md N1-N3 |

Verdict: Sun's class per the zbMATH review is piecewise continuous with a
bounded number of jumps (a strictly narrower class than O1's measurable box
class K); Sun treats the MINIMUM gap only; S1/S2 exact definitions
NOT_VERIFIABLE from public metadata.  See status_and_literature.md N1-N5.
Related records also saved: research_cache/qi2020.json (Qi-Li-Xie 2020,
Zbl 1456.34022), research_cache/sun_subelliptic.json (Sun-Yang 2023,
Zbl 1521.34080).  The _parse*.py files in research_cache/ are the scratch
parsers used to extract these records.

## Continuation-session notes (2026-08-06)

- audit_report.md was delivered in this continuation session (the original
  session's ledger entry R-010 claimed it was written, but the file was lost;
  R-010 is not retro-edited; see ledger R-011..R-014).
- candidate_proof.md Section 3 (b) carries the F-001 correction (Hilbert-
  Schmidt constant derivation; see audit_report.md findings log).
- Run output artifacts and their sha256 hashes are listed in the table below
  (final values; the manifest itself and run-manifest.json hash at closure).

## Run output artifacts (sha256, final at closure; BOM-stripped 2026-08-06)

Root:
| File | sha256 |
|---|---|
| problem_contract.md | F37D3D692C736FDB1B5D848F938227E4E1BE65B1A73439D8370842E393DB7FBC |
| obligation_graph.md | 14F33F80EF9DA8EB3B641E9E45AFC061279C57E1B8CD51A2A315419903E153A8 |
| approach_registry.md | 34E26E68D95DE385B188AA34D0B87121D56483738E2B7E519EFC2B02F201188B |
| candidate_proof.md | 728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404 |
| audit_report.md | F7AB2963AFACFAD332F77E9D43F6021DD9ACC1F534C22D1E60A2A820BE9B5F6B |
| research_ledger.md | CB3719A9F327E440F5CC4D414084CA07A765D209CFB9F999FE75658B26F1981C |
| counterexample_log.md | FF29A92D45558EE309C0E02F923A8A35A5713B759BBAE5B7DB748292EDD53366 |
| status_and_literature.md | 6A196C64F81489506728B0D535F106B1986FB038F3A6D017672326001F6BEC6C |
| task-packet-link.txt | 96F4051C359DC34FA11187E455E289B3C9CF0ECC02CA3D0047776FA9D9099422 |
| run-manifest.json | REFRESHED-AT-CLOSURE (see file; hash not self-referential) |

reproducibility/ (scripts and recorded outputs; seeds fixed in headers):
| File | sha256 |
|---|---|
| sl_lib.py | A703A4DF8BCD038ACE5F0BD6B8A2A2C3CA7BD50E0EFB801EE23F92E0974FAE2D |
| verify_hs_bound.py | FB1FE429114542DEDD5E475E58222446796DD30CDA0F159968BFEA0871ACCF3D |
| verify_hs_bound_out.json | 52FDA4D0F2AC79F097A0CF4934A550F5F8B164396800C181E7D692E34B8444DD |
| verify_fh_sign.py | E8A3269C680E1C9D4B9A593BFDEFD9271A7BD129ED41D7317FF74566BFA2705C |
| verify_fh_sign_out.json | F13172C8E8439F5B4455F24DD9F9F371829EEE22643405E818964C48159E6D03 |
| verify_structure_f.py | FEB377CC7BA9B1DBF54CB8D4BD4D0D834B2470FF9243608146227A8B5F7B88DF |
| verify_structure_f_out.json | 44F053567732AE7858F73250909F6C2930C51854E222750AA9E925B8FB79DE3A |
| verify_smoothing_r4.py | FFFB26BCD36B86CF1D17B87A0FF55BC6BD6F636BDB0F91C948FCA83CD3F8BF0A |
| verify_smoothing_r4_out.json | 02B159BB9CB1F294385B3EACB4DB5A3FE68EE661D5632DA5971F6622C9E859B4 |
| verify_bangbang.py | E6B2BED990C33D875C950AB999523C0E79CC237CB9677803B129C170991A0760 |
| verify_bangbang_out.json | 4096D6B9EB40917533F21BB9D09D8F02D31E4B2FEF5438FF34728009A1893F0D |
| verify_reduction_search.py | C2B6FD3A681C25BC0D41A8B0DA21374F3DB89CD5FEAA0695CF1EC1E82C07414D |
| verify_reduction_search_out.json | BBB4FEC01E33B70592C34A7466E913CDC042CB62C3FD28B6E3C1F11CA2615E9C |
| diag_*.py (10 files, diagnostic only) | diag_accuracy.py=EED997C41D6B350AE8AF2C0CD589654E12990FB3A72E154CEEBCBCA8B0DB42E0; diag_calibrate.py=80BCDAEFF2583E4B31546CDAB7F7EFB933F4C1B6EEB6A3F2DBD6127BF0053786; diag_fd_debug.py=C8E70EC52118418081C6CE689DFD000833E38A452931D8B03ADEAEB42B536FA0; diag_fd_small.py=C45A7FDC7058DD8E38890F1E2B26029CE780742F4B21C75D6D3007F9D704B04E; diag_roots.py=E73A5685D4747098FC927A09374F30B0A57280ABC6009B1251CF85EDACCBF41F; diag_scan.py=8907F76FEE8E666875FBAC9710BB07ED3F28A48E652E87000EE79F3ED8DB8B4A; diag_smooth2.py=AB60241489E5604B611C01D34F9DAEB020A4AA1B6897AA35E9358ACEFD843B1A; diag_u1.py=BB068BA758E7C84B700B5114D541E189EC20F2A270A07305335F4A528D492583; diag_u_star.py=45F8F5D59968C81156450FE5703C2F03BE74445C174BCB21123CE3C12DCDD9B8; diag_weyl.py=616C1BFDAF4CD8E610059F054CD31FAB11CB992B0E5E531AA1ABB026BC433803 |

research_cache/ (literature evidence, 2026-08-06):
| File | sha256 |
|---|---|
| sun2022_zbmath.json | C7A9A0B3DE0FCA2F1AEE5120AEFC05515EB2F05D9695357378C3B38B84658FF6 |
| sun2022_zbmath_parsed.txt | 330A082E42CBC2A6FDCBE80EF08A4D3145DA440542A1CC2AA4D583E317684C4B |
| sun2022_openalex.json | 04404E6422BB5F1D93D4C21079EB4DF85125F4588437635E88AB4A9FE60C98B3 |
| sun2022_crossref.json | 91894283BCBCBD33F5793F2DCD55C41DA4371AB0F6693C897F89DD0430C23B7B |
| qi2020.json | 9BE21B51492E8B0955F2C65CC50EDE3286459B0DD1A59C706CDBC0786740B1AF |
| sun_subelliptic.json | 2D5D7E2C19BDB307A0D6CFA0CC16581D4EA8E22C94A33FC7C82955EC876C9F2C |
| mardi4nfdi_sun2022.html | 89B38F82FED3C843E6758807C569CE5EF143865FA6390BB6ABC75A4B6B3F9618 |

Scratch helpers in research_cache/ (_parse*.py, _final_check.py, _hash_all.py,
_strip_bom.py, _upd_agents.py, _upd_tools.py): internal tooling for extraction
and maintenance; not part of the evidence set.

Verification note: verify_bangbang.py and verify_smoothing_r4.py were re-run
fresh in the 2026-08-06 continuation session and produced bit-identical outputs
to the recorded *out.json (reproducibility spot check).
