# printer-config

Version control and restore point for the CR-10 Max and Ender-3 Pro Cura configuration.

## What is here

| Path | What |
|---|---|
| `PRINTER-SETTINGS-MASTER-TABLE.md` | Copy of the master settings table. **The live copy lives in the vault** at `_AI_OBS\02 Projects\AI CAD 3D Print Laser\_PRINTER SETTINGS MASTER TABLE.md` |
| `cura-5.13/quality_changes/` | All custom print profiles (both machines, all materials) |
| `cura-5.13/definition_changes/` | Machine-level settings, including the start G-code carrying `M92 E415` |
| `cura-5.13/user/` | Live GUI overrides. These sit ABOVE quality_changes in the container stack and beat everything else |
| `cura-5.13/variants/` | Nozzle variants, if any |

## Why this repo exists outside the vault

The Obsidian vault is at `D:\Google Drive\_AI_OBS`, which is inside Google Drive. Drive syncs
`.git` internals mid-write and can corrupt the object store, so the vault is deliberately **not**
a git repo. This repo lives on local disk instead.

## Restoring a profile

Cura must be **closed** - it rewrites its config on exit and will clobber anything restored
while it is running.

```
copy "cura-5.13\quality_changes\<file>" "%APPDATA%\cura\5.13\quality_changes\"
```

## Refreshing this repo after a settings change

The master table is generated from these files, not typed by hand. After changing settings:

1. Close Cura.
2. Re-copy `%APPDATA%\cura\5.13\{quality_changes,definition_changes,user}\*.inst.cfg` here.
3. Regenerate the table and diff - the diff shows exactly which settings moved.

## Gotchas worth knowing before editing anything in here

- **Scope matters.** A setting whose `settable_per_mesh` and `settable_per_extruder` are BOTH
  false in `fdmprinter.def.json` is GLOBAL and belongs in `creality_<machine>_<name>.inst.cfg`.
  Written into the extruder file it is **silently ignored** - no error. `retraction_combing` and
  `layer_height_0` are both global.
- **Filename encoding differs by folder.** `quality_changes` uses `_%23N`; `extruders` and `user`
  use `+%23N`. Mixing them creates duplicate profiles rather than replacing.
- **`quality_type` filtering.** A profile only appears in Cura if its `quality_type` exists for the
  current nozzle + material. The Ender's 0.8 nozzle offers **only `draft`**, which is why
  `CE3PRO TPU` and `CE3PRO NYLON` (both `standard`) have never been selectable.
