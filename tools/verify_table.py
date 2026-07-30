"""Prove the master table matches the .inst.cfg files. Catches hand-edited cells.

DONE WHEN: every value in every profile file appears in the table with the same
           value, and the table claims nothing the files do not. Prints the
           compared count so a silently-empty run is visible.
INPUTS:    --cura, --target (same as generate_table.py).
FAILS WHEN: any mismatch or extra -> exit 1, one line per discrepancy.
"""
import argparse, configparser, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_table import PROFILES, BLANK


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cura", default=os.path.join(os.environ.get("APPDATA", ""), "cura", "5.13"))
    ap.add_argument("--target", required=True)
    a = ap.parse_args()
    qc = os.path.join(a.cura, "quality_changes")

    truth, hdrs = {}, []
    for ex, gl, hdr in PROFILES:
        hdrs.append(hdr)
        v = {}
        for fn in (ex, gl):
            c = configparser.ConfigParser()
            c.read(os.path.join(qc, fn), encoding="utf-8")
            if c.has_section("values"):
                v.update(dict(c["values"]))
        truth[hdr] = v

    parsed = {h: {} for h in hdrs}
    rows = 0
    for line in open(a.target, encoding="utf-8").read().splitlines():
        m = re.match(r"^\| .*? \| `([a-z0-9_]+)` \| (G|E) \|(.*)\|\s*$", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(3).split("|")]
        if len(cells) != len(hdrs):
            print(f"BAD CELL COUNT for {m.group(1)}: {len(cells)} vs {len(hdrs)}")
            sys.exit(1)
        rows += 1
        for h, c in zip(hdrs, cells):
            if c != BLANK:
                parsed[h][m.group(1)] = c.strip("`")

    errs = 0
    for h in hdrs:
        for k, v in truth[h].items():
            if parsed[h].get(k) != v:
                print(f"MISMATCH {h} {k}: file={v!r} table={parsed[h].get(k)!r}"); errs += 1
        for k, v in parsed[h].items():
            if k not in truth[h]:
                print(f"EXTRA IN TABLE {h} {k} = {v!r}"); errs += 1

    total = sum(len(v) for v in truth.values())
    print(f"rows: {rows} | values compared: {total} | errors: {errs}")
    if total == 0:
        print("REFUSING to pass on zero values compared"); sys.exit(1)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
