"""Regenerate the printer settings master table from live Cura .inst.cfg files.

DONE WHEN: the target .md contains a table, between the TABLE:BEGIN/TABLE:END
           markers, whose every cell matches the .inst.cfg files on disk. Prose
           outside the markers is untouched.
INPUTS:    --cura   Cura config dir (default %APPDATA%\\cura\\5.13)
           --target .md file containing both markers. Missing marker -> exit 2.
           A setting key present in a .cfg but absent from CATS -> exit 3, never
           a silent omission.
FAILS WHEN: a profile file is missing (exit 4). An empty [values] section is
           legal and renders as an all-dash column - that is real state.
"""
import argparse, configparser, os, sys

PROFILES = [
    ("creality_base_extruder_0_%233_cr10max_pla.inst.cfg",      "creality_cr10max_cr10max_pla.inst.cfg",      "CR10 PLA 0.2"),
    ("creality_base_extruder_0_%233_cr10max_pla_03.inst.cfg",   "creality_cr10max_cr10max_pla_03.inst.cfg",   "CR10 PLA 0.3"),
    ("creality_base_extruder_0_%233_cr10max_petg.inst.cfg",     "creality_cr10max_cr10max_petg.inst.cfg",     "CR10 PETG"),
    ("creality_base_extruder_0_%233_cr10max_flowtest.inst.cfg", "creality_cr10max_cr10max_flowtest.inst.cfg", "CR10 FLOW"),
    ("creality_base_extruder_0_%232_ce3pro_pla.inst.cfg",       "creality_ender3pro_ce3pro_pla.inst.cfg",     "E3 PLA"),
    ("creality_base_extruder_0_%232_ce3pro_petg.inst.cfg",      "creality_ender3pro_ce3pro_petg.inst.cfg",    "E3 PETG"),
    ("creality_base_extruder_0_%232_ce3pro_tpu.inst.cfg",       "creality_ender3pro_ce3pro_tpu.inst.cfg",     "E3 TPU"),
    ("creality_base_extruder_0_%232_ce3pro_nylon.inst.cfg",     "creality_ender3pro_ce3pro_nylon.inst.cfg",   "E3 NYLON"),
]

CATS = [
 ("Layer & geometry", [
   ("layer_height", "G", "Layer height"), ("layer_height_0", "G", "Initial layer height"),
   ("line_width", "E", "Line width"), ("wall_line_width", "E", "Wall line width"),
   ("wall_line_count", "E", "Wall count"), ("top_bottom_thickness", "E", "Top/bottom thickness"),
   ("top_layers", "E", "Top layers"), ("bottom_layers", "E", "Bottom layers"),
   ("infill_sparse_density", "E", "Infill density %"), ("fill_outline_gaps", "E", "Print thin walls"),
   ("magic_spiralize", "G", "Spiralize (vase)"), ("smooth_spiralized_contours", "G", "Smooth spiralized"),
 ]),
 ("Temperature", [
   ("material_print_temperature", "E", "Nozzle C"),
   ("material_print_temperature_layer_0", "E", "Nozzle, layer 1 C"),
   ("material_bed_temperature", "G", "Bed C (layers 2+)"),
   ("material_bed_temperature_layer_0", "G", "Bed, layer 1 C"),
 ]),
 ("Flow", [
   ("material_flow", "E", "Flow %"), ("material_flow_layer_0", "E", "Flow, layer 1 %"),
   ("skirt_brim_material_flow", "E", "Skirt/brim flow %"),
 ]),
 ("Speed (mm/s)", [
   ("speed_print", "E", "Print (base)"), ("speed_wall", "E", "Wall"),
   ("speed_wall_0", "E", "Outer wall"), ("speed_wall_x", "E", "Inner wall"),
   ("speed_topbottom", "E", "Top/bottom"), ("speed_layer_0", "E", "Initial layer"),
   ("speed_travel", "E", "Travel"),
 ]),
 ("Retraction & travel", [
   ("retraction_amount", "E", "Retract mm"), ("retraction_speed", "E", "Retract mm/s"),
   ("retraction_hop_enabled", "E", "Z hop"),
   ("retraction_extra_prime_amount", "E", "Extra prime mm3"),
   ("retraction_combing", "G", "Combing mode"),
 ]),
 ("Cooling", [
   ("cool_fan_speed", "E", "Fan %"), ("cool_fan_speed_0", "E", "Fan, layer 1 %"),
   ("cool_min_layer_time", "E", "Min layer time s"),
 ]),
 ("Surface & seam", [
   ("z_seam_type", "E", "Z seam"), ("skin_monotonic", "E", "Monotonic top/bottom"),
   ("ironing_enabled", "E", "Ironing"), ("ironing_pattern", "E", "Ironing pattern"),
   ("ironing_flow", "E", "Ironing flow %"), ("ironing_inset", "E", "Ironing inset mm"),
   ("ironing_only_highest_layer", "E", "Iron top layer only"),
 ]),
 ("Dimensional compensation", [
   ("xy_offset", "E", "Horizontal expansion"),
   ("xy_offset_layer_0", "E", "Initial layer h. expansion"),
   ("hole_xy_offset", "E", "Hole expansion"),
 ]),
 ("Adhesion", [("adhesion_type", "G", "Build plate adhesion")]),
]

BEGIN, END = "<!-- TABLE:BEGIN -->", "<!-- TABLE:END -->"
# Em dash = "not overridden, inherits". Must match the legend in the doc prose.
BLANK = "—"


def load(qc):
    merged = {}
    for ex, gl, hdr in PROFILES:
        vals = {}
        for fn in (ex, gl):
            p = os.path.join(qc, fn)
            if not os.path.exists(p):
                sys.exit(f"[4] missing profile file: {p}")
            c = configparser.ConfigParser()
            c.read(p, encoding="utf-8")
            if c.has_section("values"):
                vals.update(dict(c["values"]))
        merged[hdr] = vals
    return merged


def build(merged, stamp):
    hdrs = [h for _, _, h in PROFILES]
    L = [f"*Generated {stamp} from the .inst.cfg files. Do not edit cells by hand.*", "",
         "| Setting | Key | Sc |" + "".join(f" {h} |" for h in hdrs),
         "|---|---|---|" + "---|" * len(hdrs)]
    covered = set()
    for cat, rows in CATS:
        L.append(f"| **{cat}** | | |" + " |" * len(hdrs))
        for key, scope, label in rows:
            covered.add(key)
            cells = "".join(
                f" {BLANK if merged[h].get(key) is None else '`' + merged[h][key] + '`'} |"
                for h in hdrs)
            L.append(f"| {label} | `{key}` | {scope} |" + cells)
    missing = sorted({k for v in merged.values() for k in v} - covered)
    if missing:
        sys.exit(f"[3] settings on disk but not categorised in CATS: {missing}\n"
                 f"    Add them to CATS with the correct scope, then regenerate.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cura", default=os.path.join(os.environ.get("APPDATA", ""), "cura", "5.13"))
    ap.add_argument("--target", required=True)
    ap.add_argument("--stamp", required=True)
    a = ap.parse_args()

    table = build(load(os.path.join(a.cura, "quality_changes")), a.stamp)
    doc = open(a.target, encoding="utf-8").read()
    if BEGIN not in doc or END not in doc:
        sys.exit(f"[2] markers {BEGIN} / {END} not found in {a.target}")
    pre, rest = doc.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    open(a.target, "w", encoding="utf-8").write(pre + BEGIN + "\n" + table + "\n" + END + post)
    print(f"table regenerated: {table.count(chr(10)) + 1} lines -> {a.target}")


if __name__ == "__main__":
    main()
