"""Generate the vase-mode flow-calibration cylinder.

DONE WHEN: an ASCII STL exists whose bounding box is DIAM x DIAM x HEIGHT and whose
           facet/endfacet counts balance, verified by re-parsing the written file.
INPUTS:    edit the PARAMETERS block. SEGMENTS below 3 or a non-positive dimension
           exits before writing anything.
FAILS WHEN: nothing silently. A wrong bbox or unbalanced facets aborts with a message.

WHY A CYLINDER AND NOT A CUBE
  Extrusion width tracks speed, and a cube forces the nozzle to decelerate into every
  corner - so wall thickness varies around the part and the measurement depends on where
  the calipers land. A cylinder holds constant speed the whole way round, so every point
  on the wall was laid down under identical conditions. For an instrument whose entire
  job is measuring wall width, that matters.

WHY NO LETTERING
  Spiralize requires exactly one closed contour per layer. Embossed characters create
  extra contours, which is why the stock XYZ calibration cube cannot be used in vase mode.
"""
import math, os, re, sys

# ---------------- PARAMETERS ----------------
DIAM     = 32.0   # perimeter 100.5mm - deliberately matched to the old 25mm cube's 100mm,
                  # so print times and layer times stay comparable to previous runs
HEIGHT   = 30.0   # taller than the cube: mid-height cut sits clear of the solid base
                  # and of the top few layers, which always curl inward in vase mode
SEGMENTS = 120    # chord error 0.0055mm - invisible. 0.84mm segments at 30mm/s is
                  # ~36 moves/sec, safe for the CR-10's 8-bit board
OUT      = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "flow_cal_cylinder_32x30.stl")
# --------------------------------------------

if SEGMENTS < 3 or DIAM <= 0 or HEIGHT <= 0:
    sys.exit("bad parameters")

r = DIAM / 2.0
ring = [(r * math.cos(2 * math.pi * i / SEGMENTS),
         r * math.sin(2 * math.pi * i / SEGMENTS)) for i in range(SEGMENTS)]

tris = []
for i in range(SEGMENTS):
    (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % SEGMENTS]
    b0, b1 = (x0, y0, 0.0), (x1, y1, 0.0)
    t0, t1 = (x0, y0, HEIGHT), (x1, y1, HEIGHT)
    tris.append(((0.0, 0.0, 0.0), b1, b0))            # bottom cap, normal -Z
    tris.append(((0.0, 0.0, HEIGHT), t0, t1))         # top cap, normal +Z
    tris.append((b0, b1, t1))                         # side, normal outward
    tris.append((b0, t1, t0))

out = ["solid flow_cal_cylinder"]
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
out.append("endsolid flow_cal_cylinder")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")

# read back what was actually written, not what we intended
txt = open(OUT, encoding="utf-8").read()
nf, ne = txt.count("facet normal"), txt.count("endfacet")
vs = [tuple(map(float, m.groups()))
      for m in re.finditer(r"vertex (\S+) (\S+) (\S+)", txt)]
bb = [max(v[i] for v in vs) - min(v[i] for v in vs) for i in range(3)]
if nf != ne:
    sys.exit(f"ABORT: {nf} facets vs {ne} endfacets")
for got, want, ax in zip(bb, (DIAM, DIAM, HEIGHT), "XYZ"):
    if abs(got - want) > 0.02:
        sys.exit(f"ABORT: {ax} bbox {got:.3f} != {want}")

per = math.pi * DIAM
print(f"{OUT}")
print(f"  {nf} facets (balanced), bbox {bb[0]:.2f} x {bb[1]:.2f} x {bb[2]:.2f}")
print(f"  perimeter {per:.1f} mm  (25mm cube was 100.0)")
print(f"  chord error {r*(1-math.cos(math.pi/SEGMENTS))*1000:.1f} micron")
for lh in (0.2, 0.3):
    lt = per / 30.0
    print(f"  at {lh} layer: {int(HEIGHT/lh)} layers, {lt:.1f}s each at 30mm/s "
          f"-> cool_min_layer_time must be <= 3")
