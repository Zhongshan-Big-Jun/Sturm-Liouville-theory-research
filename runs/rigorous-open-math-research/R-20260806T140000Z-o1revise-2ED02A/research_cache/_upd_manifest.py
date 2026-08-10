import io, os, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest().upper()

# ---- build the outputs table for repro_manifest.md ----
root_rows = [
    ("problem_contract.md", "F37D3D692C736FDB1B5D848F938227E4E1BE65B1A73439D8370842E393DB7FBC"),
    ("obligation_graph.md", "14F33F80EF9DA8EB3B641E9E45AFC061279C57E1B8CD51A2A315419903E153A8"),
    ("approach_registry.md", "34E26E68D95DE385B188AA34D0B87121D56483738E2B7E519EFC2B02F201188B"),
    ("candidate_proof.md", "728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404"),
    ("audit_report.md", "F7AB2963AFACFAD332F77E9D43F6021DD9ACC1F534C22D1E60A2A820BE9B5F6B"),
    ("research_ledger.md", "CB3719A9F327E440F5CC4D414084CA07A765D209CFB9F999FE75658B26F1981C"),
    ("counterexample_log.md", "FF29A92D45558EE309C0E02F923A8A35A5713B759BBAE5B7DB748292EDD53366"),
    ("status_and_literature.md", "6A196C64F81489506728B0D535F106B1986FB038F3A6D017672326001F6BEC6C"),
    ("task-packet-link.txt", "96F4051C359DC34FA11187E455E289B3C9CF0ECC02CA3D0047776FA9D9099422"),
    ("run-manifest.json", "REFRESHED-AT-CLOSURE (see file; hash not self-referential)"),
]
repro_rows = [
    ("sl_lib.py", "A703A4DF8BCD038ACE5F0BD6B8A2A2C3CA7BD50E0EFB801EE23F92E0974FAE2D"),
    ("verify_hs_bound.py", "FB1FE429114542DEDD5E475E58222446796DD30CDA0F159968BFEA0871ACCF3D"),
    ("verify_hs_bound_out.json", "52FDA4D0F2AC79F097A0CF4934A550F5F8B164396800C181E7D692E34B8444DD"),
    ("verify_fh_sign.py", "E8A3269C680E1C9D4B9A593BFDEFD9271A7BD129ED41D7317FF74566BFA2705C"),
    ("verify_fh_sign_out.json", "F13172C8E8439F5B4455F24DD9F9F371829EEE22643405E818964C48159E6D03"),
    ("verify_structure_f.py", "FEB377CC7BA9B1DBF54CB8D4BD4D0D834B2470FF9243608146227A8B5F7B88DF"),
    ("verify_structure_f_out.json", "44F053567732AE7858F73250909F6C2930C51854E222750AA9E925B8FB79DE3A"),
    ("verify_smoothing_r4.py", "FFFB26BCD36B86CF1D17B87A0FF55BC6BD6F636BDB0F91C948FCA83CD3F8BF0A"),
    ("verify_smoothing_r4_out.json", "02B159BB9CB1F294385B3EACB4DB5A3FE68EE661D5632DA5971F6622C9E859B4"),
    ("verify_bangbang.py", "E6B2BED990C33D875C950AB999523C0E79CC237CB9677803B129C170991A0760"),
    ("verify_bangbang_out.json", "4096D6B9EB40917533F21BB9D09D8F02D31E4B2FEF5438FF34728009A1893F0D"),
    ("verify_reduction_search.py", "C2B6FD3A681C25BC0D41A8B0DA21374F3DB89CD5FEAA0695CF1EC1E82C07414D"),
    ("verify_reduction_search_out.json", "BBB4FEC01E33B70592C34A7466E913CDC042CB62C3FD28B6E3C1F11CA2615E9C"),
]
diag_hashes = {
    "diag_accuracy.py": "EED997C41D6B350AE8AF2C0CD589654E12990FB3A72E154CEEBCBCA8B0DB42E0",
    "diag_calibrate.py": "80BCDAEFF2583E4B31546CDAB7F7EFB933F4C1B6EEB6A3F2DBD6127BF0053786",
    "diag_fd_debug.py": "C8E70EC52118418081C6CE689DFD000833E38A452931D8B03ADEAEB42B536FA0",
    "diag_fd_small.py": "C45A7FDC7058DD8E38890F1E2B26029CE780742F4B21C75D6D3007F9D704B04E",
    "diag_roots.py": "E73A5685D4747098FC927A09374F30B0A57280ABC6009B1251CF85EDACCBF41F",
    "diag_scan.py": "8907F76FEE8E666875FBAC9710BB07ED3F28A48E652E87000EE79F3ED8DB8B4A",
    "diag_smooth2.py": "AB60241489E5604B611C01D34F9DAEB020A4AA1B6897AA35E9358ACEFD843B1A",
    "diag_u1.py": "BB068BA758E7C84B700B5114D541E189EC20F2A270A07305335F4A528D492583",
    "diag_u_star.py": "45F8F5D59968C81156450FE5703C2F03BE74445C174BCB21123CE3C12DCDD9B8",
    "diag_weyl.py": "616C1BFDAF4CD8E610059F054CD31FAB11CB992B0E5E531AA1ABB026BC433803",
}
cache_rows = [
    ("sun2022_zbmath.json", "C7A9A0B3DE0FCA2F1AEE5120AEFC05515EB2F05D9695357378C3B38B84658FF6"),
    ("sun2022_zbmath_parsed.txt", "330A082E42CBC2A6FDCBE80EF08A4D3145DA440542A1CC2AA4D583E317684C4B"),
    ("sun2022_openalex.json", "04404E6422BB5F1D93D4C21079EB4DF85125F4588437635E88AB4A9FE60C98B3"),
    ("sun2022_crossref.json", "91894283BCBCBD33F5793F2DCD55C41DA4371AB0F6693C897F89DD0430C23B7B"),
    ("qi2020.json", "9BE21B51492E8B0955F2C65CC50EDE3286459B0DD1A59C706CDBC0786740B1AF"),
    ("sun_subelliptic.json", "2D5D7E2C19BDB307A0D6CFA0CC16581D4EA8E22C94A33FC7C82955EC876C9F2C"),
    ("mardi4nfdi_sun2022.html", "89B38F82FED3C843E6758807C569CE5EF143865FA6390BB6ABC75A4B6B3F9618"),
]

def table(rows):
    out = []
    for name, h in rows:
        out.append("| %s | %s |" % (name, h))
    return "\n".join(out)

new_section = "## Run output artifacts (sha256, final at closure; BOM-stripped 2026-08-06)\n\nRoot:\n| File | sha256 |\n|---|---|\n" + table(root_rows) + "\n\nreproducibility/ (scripts and recorded outputs; seeds fixed in headers):\n| File | sha256 |\n|---|---|\n" + table(repro_rows) + "\n| diag_*.py (10 files, diagnostic only) | " + "; ".join("%s=%s" % (k, v) for k, v in diag_hashes.items()) + " |\n\nresearch_cache/ (literature evidence, 2026-08-06):\n| File | sha256 |\n|---|---|\n" + table(cache_rows) + "\n\nScratch helpers in research_cache/ (_parse*.py, _final_check.py, _hash_all.py,\n_strip_bom.py, _upd_agents.py, _upd_tools.py): internal tooling for extraction\nand maintenance; not part of the evidence set.\n\nVerification note: verify_bangbang.py and verify_smoothing_r4.py were re-run\nfresh in the 2026-08-06 continuation session and produced bit-identical outputs\nto the recorded *out.json (reproducibility spot check).\n"

p = os.path.join(root, "repro_manifest.md")
s = io.open(p, encoding="utf-8").read()
i = s.find("## Run output artifacts")
if i < 0:
    raise SystemExit("table section not found")
s = s[:i] + new_section
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("repro_manifest.md table regenerated")
