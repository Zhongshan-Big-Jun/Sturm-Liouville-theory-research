# Initial frozen-input observations

Reviewer native task identity: /root/r14_software_review. Authors: /root and /root/kernel_repair.

The initial code/hashes.json had SHA256 11b39ddc3aaace3246062bcb865da86e9080689a421fecd7f4d42c131261b399; all 20 listed inputs matched. Tests had not been executed when the coordinator announced a portable-test reference-path correction.

The subsequent manifest had SHA256 a7addb2ecf7921c6318a9ad219a5bda71d5e504517e07f26da753afc10a970fa. Its 20 source/test entries matched, but an added self-entry hashes.json erroneously expected the previous manifest hash. This exact mismatch is preserved in software-second-input-hashes.json. The coordinator acknowledged and corrected the generator.

Before any execution, independent source reading found unfrozen top-level local imports: reflection_seeds from _gapn2_symmetry_recon.py:16; _gapn2_reduced_endpoint_hunt from _gapn2_endpoint_targeted.py:17 and _gapn2_kidentity_audit.py:12. I did not read or execute these unlisted files, did not import from the live workspace, and did not borrow another review's conclusions.

Static source finding in the initial package: _gapn2_ktilde_positivity.run at lines 46-56 directly enumerates and forms spectral denominators without the shared mode-coverage and denominator-resolution checks. A runtime negative control was proposed but not yet performed. This is a statement about the source, not a claim that the proposed runtime already failed.

The initial reduced candidate paths at _gapn2_endpoint_targeted.py:54-61 and _gapn2_kidentity_audit.py:56-68 accept only a small absolute least-squares residual, without optimizer success or shared relative-balance/zero-correction checks. The coordinator announced a new code-v2 freeze with the missing dependency and revised reduced acceptance. The original code package was not edited by this reviewer.

No initial checks.py or kernel_checks.py execution is claimed. No Lean execution, analytic-supplement audit, global theorem validation, memory/skill reading, author-session reading, or live-project access occurred.
