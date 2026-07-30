---
tags: [3dprint, cura, settings, sot]
updated: 2026-07-29
---

# PRINTER SETTINGS - MASTER TABLE (single source of truth)

> **This table is the ONLY place printer settings are recorded.** If a value here disagrees with
> `CR-10 Max Machine Profile.md`, `Ender-3 Pro Machine Profile.md` or `_PRINT_PROFILES.md`,
> **this table wins** and the other document is stale. Those documents hold the *reasoning*, the
> diagnoses and the change history - not the values.

Generated directly from the `.inst.cfg` files on disk on **2026-07-29**, not transcribed by hand.
Source: `C:\Users\gator\AppData\Roaming\cura\5.13\quality_changes\`

📦 **Version control:** `D:\GatorForge\printer-config` (git, local disk, **no remote - this is
history, not backup**). Holds a copy of this table plus all 24 `.inst.cfg` files.

💾 **Backup:** `_AI_OBS\10 Attachments\printer-config-backup\` - inside Google Drive, so synced
offsite with Drive's own per-file version history. Contains **plain copies of all 24 `.inst.cfg`
files** (restorable with nothing but a file copy - no git needed) plus `printer-config.bundle`
carrying the full repo history, and `RESTORE.md`. Verified byte-identical to source: 24/24 SHA-256
match. A bad edit or a Cura upgrade wiping a profile is now a file copy, not a re-tune.

⚠️ The working repo is deliberately **outside** Drive. A live `.git` object store and Drive sync
corrupt each other; a bundle is a single finished file and syncs safely. **This vault copy of the
table is the live one** - re-copy into the repo and refresh the backup after changes.

## How to read it

- **`—` means the setting is not overridden** and inherits from the Cura quality profile /
  `creality_base.def.json`. It does NOT mean zero or off.
- **`Sc`** = scope. **`E`** = per-extruder, lives in `creality_base_extruder_0_%23N_<name>.inst.cfg`.
  **`G`** = GLOBAL, lives in `creality_<machine>_<name>.inst.cfg`.
  ⛔ **A `G` setting written into an `E` file is silently ignored** - no error, it just does
  nothing. This has bitten twice. Check `fdmprinter.def.json`
  (`settable_per_mesh` / `settable_per_extruder` both false = global) before writing anything new.
- `%232` = Ender-3 Pro extruder, `%233` = CR-10 Max extruder. The `_%23` underscore encoding is
  used by `quality_changes`; `extruders` uses `+%23`. **Mixing them creates duplicate profiles.**

## Machines

| | CR-10 Max | Ender-3 Pro |
|---|---|---|
| Cura build volume | 450 x 450 x 470 mm | 220 x 220 x 250 mm |
| Nozzle fitted | 0.4 mm | **0.8 mm** |
| Extruder | Bondtech DDX v3, 50:17 (~2.94:1) | Micro Swiss direct drive |
| Hotend | All-metal (exact model unconfirmed) | Micro Swiss all-metal |
| E-steps | **415** - applied via `M92 E415` + `M500` in start G-code | not recorded |
| Bed levelling | BLTouch (`G29` in start G-code) | manual |
| Bed springs | silicone spacers (stock springs removed) | silicone spacers |
| Accel caps (firmware) | `M201 X500 Y500 Z100 E5000` / `M204 P500 R1000 T500` | not recorded |
| Jerk | `M205 X8 Y8 Z0.4 E5` | not recorded |
| Start G-code quirk | e-steps written every print | `G92 Z0.05` first-layer squish comp |
| `quality_type` available | full ladder - profiles use `standard` | **`draft` ONLY** (0.8 nozzle) |

⛔ **Acceleration reality check.** `M201 X500 Y500` is the hard per-axis cap. Raising `M204` alone
does nothing - Marlin clamps it. Any speed work is `M201` + `M204` + Cura speeds as **one coupled
change**. At 500 mm/s2 a move needs 8.1 mm to reach 90 mm/s and 8.1 mm to stop, so a 16.2 mm
minimum move length - longer than most infill moves in a small part. This is why raising
`speed_infill` on its own buys nothing.

## THE TABLE

<!-- TABLE:BEGIN -->
*Generated 2026-07-29 20:25 from the .inst.cfg files. Do not edit cells by hand.*

| Setting | Key | Sc | CR10 PLA 0.2 | CR10 PLA 0.3 | CR10 PETG | CR10 FLOW | E3 PLA | E3 PETG | E3 TPU | E3 NYLON | E3 PLA 0.6 | E3 FLOW 0.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Layer & geometry** | | | | | | | | | | | | |
| Layer height | `layer_height` | G | `0.2` | `0.3` | `0.2` | `0.2` | `0.4` | `0.4` | — | `0.3` | `0.3` | `0.3` |
| Initial layer height | `layer_height_0` | G | `0.28` | `0.3` | `0.2` | `0.2` | `0.4` | `0.4` | — | `0.3` | `0.3` | `0.3` |
| Line width | `line_width` | E | — | — | — | `0.4` | `0.9` | `0.9` | — | `0.6` | `0.6` | `0.6` |
| Wall line width | `wall_line_width` | E | — | — | — | `0.4` | — | — | — | `0.6` | `0.6` | `0.6` |
| Wall count | `wall_line_count` | E | `3` | `3` | `3` | `1` | `4` | `3` | `3` | `4` | `3` | `1` |
| Top/bottom thickness | `top_bottom_thickness` | E | `1.2` | `0.9` | — | — | `1.6` | `1.6` | — | `1.2` | `1.2` | — |
| Top layers | `top_layers` | E | — | — | — | `0` | — | — | — | — | — | `0` |
| Bottom layers | `bottom_layers` | E | — | — | — | `3` | — | — | — | — | — | `3` |
| Infill density % | `infill_sparse_density` | E | `20` | `20` | `20` | `0` | `20` | `20` | `12` | `35` | `20` | `0` |
| Print thin walls | `fill_outline_gaps` | E | — | — | — | — | `True` | — | — | — | — | — |
| Spiralize (vase) | `magic_spiralize` | G | — | — | — | `True` | — | — | — | — | — | `True` |
| Smooth spiralized | `smooth_spiralized_contours` | G | — | — | — | `True` | — | — | — | — | — | `True` |
| **Temperature** | | | | | | | | | | | | |
| Nozzle C | `material_print_temperature` | E | `200` | `210` | `240` | `200` | `215` | `240` | `225` | `250` | `205` | `205` |
| Nozzle, layer 1 C | `material_print_temperature_layer_0` | E | `205` | `210` | `245` | `205` | `220` | `245` | `225` | `255` | `210` | `210` |
| Bed C (layers 2+) | `material_bed_temperature` | G | `55` | `60` | `80` | `60` | `60` | `80` | — | `70` | `60` | `60` |
| Bed, layer 1 C | `material_bed_temperature_layer_0` | G | `60` | `60` | `80` | `60` | `60` | `80` | — | `70` | `60` | `60` |
| **Flow** | | | | | | | | | | | | |
| Flow % | `material_flow` | E | `93.6` | `94.1` | — | `100` | `94.4` | — | — | — | `100` | `100` |
| Flow, layer 1 % | `material_flow_layer_0` | E | `100` | `105` | `103` | `100` | `105` | `103` | — | — | `100` | `100` |
| Skirt/brim flow % | `skirt_brim_material_flow` | E | — | — | — | — | `100` | — | — | — | — | — |
| **Speed (mm/s)** | | | | | | | | | | | | |
| Print (base) | `speed_print` | E | `45` | `55` | `40` | `30` | `35` | `25` | `20` | `35` | `45` | `30` |
| Wall | `speed_wall` | E | — | `45` | — | — | — | — | — | — | — | — |
| Outer wall | `speed_wall_0` | E | `25` | `30` | `25` | `30` | `25` | `18` | `18` | `22` | `25` | `30` |
| Inner wall | `speed_wall_x` | E | — | — | — | `30` | — | — | — | — | — | `30` |
| Top/bottom | `speed_topbottom` | E | — | `45` | — | `30` | — | — | — | — | — | `30` |
| Initial layer | `speed_layer_0` | E | — | `20` | `20` | `20` | — | `15` | `15` | `20` | `20` | `20` |
| Travel | `speed_travel` | E | `150` | `150` | `130` | `150` | `150` | `130` | `100` | `120` | `150` | `150` |
| **Retraction & travel** | | | | | | | | | | | | |
| Retract mm | `retraction_amount` | E | `1.0` | `1.0` | `1.2` | — | `1.5` | `1.5` | `0.6` | `1.5` | `1.0` | — |
| Retract mm/s | `retraction_speed` | E | `40` | `40` | `35` | — | `35` | `35` | `25` | `35` | `35` | — |
| Z hop | `retraction_hop_enabled` | E | `False` | `False` | `False` | `False` | `False` | `False` | `False` | `False` | `False` | `False` |
| Extra prime mm3 | `retraction_extra_prime_amount` | E | — | — | — | — | `0.15` | `0.15` | — | — | — | — |
| Combing mode | `retraction_combing` | G | `no_outer_surfaces` | — | — | — | — | — | — | `no_outer_surfaces` | `no_outer_surfaces` | — |
| **Cooling** | | | | | | | | | | | | |
| Fan % | `cool_fan_speed` | E | `100` | `100` | `40` | `100` | `100` | `40` | `40` | `20` | `100` | `100` |
| Fan, layer 1 % | `cool_fan_speed_0` | E | `0` | `0` | `0` | `0` | `0` | `0` | — | `0` | `0` | `0` |
| Min layer time s | `cool_min_layer_time` | E | — | — | — | `3` | — | — | — | — | — | `3` |
| **Surface & seam** | | | | | | | | | | | | |
| Z seam | `z_seam_type` | E | `random` | `random` | — | — | `random` | `random` | — | `random` | `random` | — |
| Monotonic top/bottom | `skin_monotonic` | E | `True` | — | — | — | — | — | — | — | `True` | — |
| Ironing | `ironing_enabled` | E | `True` | — | — | — | — | — | — | — | — | — |
| Ironing pattern | `ironing_pattern` | E | `concentric` | — | — | — | — | — | — | — | — | — |
| Ironing flow % | `ironing_flow` | E | `8` | — | — | — | — | — | — | — | — | — |
| Ironing inset mm | `ironing_inset` | E | `0.4` | — | — | — | — | — | — | — | — | — |
| Iron top layer only | `ironing_only_highest_layer` | E | `True` | — | — | — | — | — | — | — | — | — |
| **Dimensional compensation** | | | | | | | | | | | | |
| Horizontal expansion | `xy_offset` | E | — | — | — | — | `0.15` | — | — | — | — | — |
| Initial layer h. expansion | `xy_offset_layer_0` | E | `-0.2` | `-0.2` | — | — | — | — | — | — | — | — |
| Hole expansion | `hole_xy_offset` | E | — | — | — | — | `0.15` | — | — | — | — | — |
| **Adhesion** | | | | | | | | | | | | |
| Build plate adhesion | `adhesion_type` | G | `brim` | `brim` | `brim` | `skirt` | `brim` | `brim` | — | `brim` | `skirt` | `skirt` |
<!-- TABLE:END -->

## Live GUI overrides - these BEAT the table

Settings changed in the Cura interface land in the `user` container, which sits **above**
`quality_changes` in the stack. They are invisible in the profile files. As of 2026-07-29:

| Container | Setting | Value | Note |
|---|---|---|---|
| `creality_base_extruder_0+%233_user` | `speed_wall_0` | `20` | Threaded-part quality trade. Costs real time |
| `creality_base_extruder_0+%233_user` | `wall_line_count` | `4` | Same. Revert to 3 for non-threaded parts |
| `Creality+CR-10+Max_user` | `adhesion_type` | `skirt` | Set 2026-07-29 to remove brim remnant from the base |

⚠️ **When a slice looks wrong, check the `user` container before anything else.** A stale override
here caused a 7 g slice of a 28 g part, and no amount of checking the profile files revealed it.

## Known defects in the profile set - NOT yet fixed

1. ⛔ **`CE3PRO TPU` and `CE3PRO NYLON` are unusable.** Both carry `quality_type = standard`, but
   the Ender's 0.8 nozzle offers **only `draft`**, so neither ever appears in the profile list.
   Their global files are also completely **empty** - no layer height, no bed temperature at all.
   Fix: flip both to `draft` and populate the globals, or delete them.
2. ⚠️ **`CR10MAX PLA 0.3 FAST` has diverged** from the 0.2 profile: still `material_flow = 94.1`
   and `material_flow_layer_0 = 105`. The 0.2 profile is now 93.6 / 100. Decide whether the 0.3
   profile should follow.
3. ⚠️ **`CR10MAX PETG` global still has `layer_height_0 = 0.2`** - it did not get the 0.28
   first-layer change that fixed elephant foot on PLA. Same machine, same physics.
4. ⚠️ **`CR10MAX PETG` has no `material_flow` at all** - deliberate. PETG flow has never been
   measured on this machine. Do not copy the PLA number across; flow is material-specific.
5. ⚠️ **`CE3PRO PETG` has no `material_flow`** either, for the same reason.
6. ⚠️ **Custom profiles are shared across all Creality machines** (all carry
   `definition = creality_base`) and are filtered only by `quality_type`. `CE3PRO` profiles show
   up in the CR-10's list. Always use the machine prefix in the name.

## Provenance of the two numbers people will question

- **`material_flow = 93.6` (CR-10 Max PLA).** Measured value was **94.1 %** from a vase-mode
  single-wall run (0.42 / 0.43 mm against a 0.400 mm target). Mark directed a further 0.5 %
  reduction on 2026-07-29 against a reference Ender part. **That last 0.5 % is operator judgement,
  not measurement.** If a print argues for reverting, 94.1 is the number with evidence behind it.
- **`material_flow = 94.4` (Ender-3 PLA).** Independently measured. Two different machines landing
  within 0.3 % of each other is the generic ~6 % over-extrusion from filament diameter tolerance
  (real spools run 1.71-1.74 mm against a slicer assuming 1.75) plus die swell. Expected, not a
  fault.

## Rules for changing anything in here

1. **Close Cura first.** Cura rewrites its config on exit and will clobber edits made while it runs.
2. **One variable at a time**, or the result is unreadable.
3. **Check the scope** (`E` vs `G`) in `fdmprinter.def.json` before writing a new key.
4. **Verify by re-reading the file**, not by the fact that a write was issued.
5. **Regenerate this table from disk** rather than editing cells by hand.

Reasoning, diagnoses and history live in `CR-10 Max Machine Profile.md` and
`Ender-3 Pro Machine Profile.md`. Values live here.
