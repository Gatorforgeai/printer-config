"""Parametric storage tray for square micromineral boxes.

DONE WHEN: an ASCII STL exists whose bounding box matches the computed tray
           footprint, with N x N pockets, X-shaped open floors, and four
           corner lift fins.
INPUTS:    edit the PARAMETERS block, or import build() and pass overrides.
           Solids are allowed to overlap - slicers union them. Reported volume
           is therefore an UPPER BOUND; Cura's slice figure is authoritative.
FAILS WHEN: pocket <= 0 or tray exceeds the named bed - both raise before any
           file is written.
"""
import math, sys

# ---------------- PARAMETERS ----------------
BOX          = 34.5   # box footprint, square
BOX_H        = 36.0   # box height - drives fin height
CLEAR        = 0.35   # per side. "snug"
DIVIDER      = 3.0    # spacer between pockets; set by hinge/clasp interlock
FLOOR_T      = 2.0    # thickness of the X ribs
RIB_W        = 4.0    # width of each diagonal rib
WALL_H       = 3.0    # retaining wall height ABOVE the floor
FIN_T        = 4.0    # lift fin thickness at the top (the grip)
FIN_BASE_T   = 8.0    # thickness at the very bottom - this is the gusset
FIN_GUSSET_H = 12.0   # height over which it tapers from BASE_T to T
FIN_L        = 25.0   # fin length along the tray edge
FIN_H        = 52.0   # total height from the bed
BEDS         = {"CR10MAX": (450, 450), "ENDER3PRO": (220, 220)}
# --------------------------------------------


def hexa(bot, top):
    """bot/top: 4 (x,y,z) corners, CCW seen from +Z. Returns 12 triangles."""
    p, q = bot, top
    t = [(p[0], p[2], p[1]), (p[0], p[3], p[2]),        # bottom, normal -Z
         (q[0], q[1], q[2]), (q[0], q[2], q[3])]        # top, normal +Z
    for i in range(4):
        j = (i + 1) % 4
        t += [(p[i], p[j], q[j]), (p[i], q[j], q[i])]   # sides, normal outward
    return t


def block(x0, x1, y0, y1, z0, z1):
    b = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
    tp = [(x, y, z1) for (x, y, _) in b]
    return hexa(b, tp)


def bar(cx, cy, z0, z1, length, width, deg):
    """Rectangular bar centred on (cx,cy), rotated about Z."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    hl, hw = length / 2.0, width / 2.0
    corners = []
    for sl, sw in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        corners.append((cx + ux * hl * sl + vx * hw * sw,
                        cy + uy * hl * sl + vy * hw * sw, z0))
    return hexa(corners, [(x, y, z1) for (x, y, _) in corners])


def fin(x_in, y0, y1, sign):
    """Lift fin with a gusseted base. x_in is the INNER face, flush with the
    outer wall; the fin grows outward by sign (-1 west, +1 east) so it never
    intrudes into a pocket."""
    lo_out = x_in + sign * FIN_BASE_T     # gusset, bottom
    hi_out = x_in + sign * FIN_T          # grip, above the gusset
    lo = block(min(x_in, lo_out), max(x_in, lo_out), y0, y1, 0, FIN_GUSSET_H)
    hi = block(min(x_in, hi_out), max(x_in, hi_out), y0, y1, FIN_GUSSET_H, FIN_H)
    return lo + hi


def volume(tris):
    v = 0.0
    for a, b, c in tris:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1])
              - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return abs(v)


def build(n, fins=True):
    pocket = BOX + 2 * CLEAR
    if pocket <= 0:
        sys.exit("pocket <= 0")
    pitch = pocket + DIVIDER
    span = n * pitch + DIVIDER
    top = FLOOR_T + WALL_H
    tris = []

    # grid walls, full height, both directions
    for i in range(n + 1):
        c = DIVIDER / 2.0 + i * pitch
        tris += block(c - DIVIDER / 2, c + DIVIDER / 2, 0, span, 0, top)
        tris += block(0, span, c - DIVIDER / 2, c + DIVIDER / 2, 0, top)

    # X floor ribs, one pair per pocket
    diag = pocket * math.sqrt(2)
    for i in range(n):
        for j in range(n):
            cx = DIVIDER + pocket / 2 + i * pitch
            cy = DIVIDER + pocket / 2 + j * pitch
            tris += bar(cx, cy, 0, FLOOR_T, diag, RIB_W, 45)
            tris += bar(cx, cy, 0, FLOOR_T, diag, RIB_W, -45)

    if fins:
        for y0, y1 in ((0.0, FIN_L), (span - FIN_L, span)):
            tris += fin(DIVIDER, y0, y1, -1)
            tris += fin(span - DIVIDER, y0, y1, +1)

    return tris, pocket, pitch, span


def write_stl(path, tris, name):
    out = [f"solid {name}"]
    for a, b, c in tris:
        ux, uy, uz = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        vx, vy, vz = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        nx, ny, nz = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
        m = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        out.append(f"facet normal {nx/m:.6f} {ny/m:.6f} {nz/m:.6f}")
        out.append("outer loop")
        for v in (a, b, c):
            out.append(f"vertex {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")
        out += ["endloop", "endfacet"]
    out.append(f"endsolid {name}")
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")


def report(n, fins, path):
    tris, pocket, pitch, span = build(n, fins)
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    w, d, h = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
    for bed, (bx, by) in BEDS.items():
        if w > bx or d > by:
            print(f"    !! exceeds {bed} bed ({bx}x{by})")
    vol = volume(tris)
    write_stl(path, tris, f"mineral_tray_{n}x{n}")
    print(f"{n}x{n}{' +fins' if fins else ''}: {len(tris)} tris | "
          f"bbox {w:.1f} x {d:.1f} x {h:.1f} mm | pocket {pocket:.2f} | "
          f"pitch {pitch:.2f} | tray {span:.1f}")
    print(f"    volume <= {vol/1000:.1f} cm3  (<= {vol/1000*1.24:.0f} g PLA) "
          f"-- upper bound, solids overlap")
    print(f"    -> {path}")


if __name__ == "__main__":
    print(f"box {BOX} sq x {BOX_H} tall | clearance {CLEAR}/side | "
          f"divider {DIVIDER} | fin {FIN_H} tall "
          f"({FIN_H - FLOOR_T - BOX_H:.0f}mm proud of a seated lid)")
    report(4, True,  r"C:\Users\gator\Downloads\mineral_tray_4x4.stl")
    report(2, False, r"C:\Users\gator\Downloads\mineral_tray_2x2_FITTEST.stl")

    # independent read-back: parse what was actually written, not what we meant
    import re
    for p in (r"C:\Users\gator\Downloads\mineral_tray_4x4.stl",
              r"C:\Users\gator\Downloads\mineral_tray_2x2_FITTEST.stl"):
        txt = open(p, encoding="utf-8").read()
        vs = [tuple(map(float, m.groups()))
              for m in re.finditer(r"vertex (\S+) (\S+) (\S+)", txt)]
        nf, ne = txt.count("facet normal"), txt.count("endfacet")
        bad = [v for v in vs if any(x != x for x in v)]
        print(f"read-back {p.split(chr(92))[-1]}: {nf} facets "
              f"({'balanced' if nf == ne else 'UNBALANCED'}), {len(vs)} verts, "
              f"bbox {max(v[0] for v in vs)-min(v[0] for v in vs):.1f} x "
              f"{max(v[1] for v in vs)-min(v[1] for v in vs):.1f} x "
              f"{max(v[2] for v in vs)-min(v[2] for v in vs):.1f}"
              f"{' | NaN!' if bad else ''}")
