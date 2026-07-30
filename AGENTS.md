# AGENTS.md — Printer Config

⛔ **Open items live ONLY in the vault ledger** —
`_AI_OBS\02 Projects\AI CAD 3D Print Laser\Printer Config\02 Next Actions.md`.
STATE below is session-scope and must never duplicate it.

## STATE

Purpose: one generated source of truth for every Cura setting on both printers, with the profiles
version-controlled and restorable.

Project DONE-WHEN: both machines producing dimensionally accurate parts from documented,
version-controlled profiles, every value traceable to a measurement or a logged decision.

Last verified on disk: 2026-07-30 — `refresh.py` completed a full end-to-end pass (28 profile files
captured, table regenerated, 238 values verified 0 mismatches, bundle refreshed, pushed).

Open work:
[x] Table generated from disk and verified against it — 238 values, 0 mismatches
[x] All 24 `.inst.cfg` under git + GitHub + Drive backup (plain copies and bundle)
[x] Profiles renamed to `N<nozzle> L<layer>`
[x] Flow-cal cylinder authored and verified
[x] Ender adhesion root-caused to `G92 Z` disagreeing with the measured cold gap
[~] Ender flow calibration — cylinder patched to `G92 Z0.35`, not yet printed successfully
[!] CR-10 elephant foot — blocked on judging the next print at `material_flow_layer_0 = 93.1`
[ ] `gate.py` pre-commit hook not installed
[ ] SPEC.md not ratified; no Register row

Async job in flight: none

NEXT ACTION: print the patched `CE3PRO_flow_cal_cylinder_32x30.gcode` from the SD card, cut it at
mid-height, measure the wall.

⚠️ Re-verify the `[x]` lines against disk on resume. A checked box is not evidence.

## ARCHITECTURE

*Proposed — awaiting Mark's ratification.*

Components & flow:
  Cura `%APPDATA%` → refresh.py → { repo cura-5.13\, Drive backup } → generate_table → vault table
                                                                    → verify_table → commit + push

- `refresh.py`: orchestrator. Contract out: refuses to proceed if Cura is running; aborts before
  committing if generation or verification fails, so a half-captured state is never pushed.
- `tools\generate_table.py`: reads `.inst.cfg`, writes the table between `TABLE:BEGIN`/`TABLE:END`
  markers in the vault doc. Contract out: prose outside the markers is preserved untouched. Exits
  nonzero on an uncategorised setting or an unlisted profile rather than omitting it silently.
- `tools\verify_table.py`: reparses the written table and diffs against `.inst.cfg`. Contract out:
  refuses to pass on zero values compared.

SACRED — do not touch:
  - `%APPDATA%\cura\5.13\**` — read-only from this project. Cura owns it. Backup:
    `_AI_OBS\10 Attachments\printer-config-backup\cura-5.13\`

Cross-component contracts (a wrong guess here is a silent bug):
  - The vault table is the LIVE copy; the repo holds no copy of it. A repo copy cannot satisfy the
    front-matter rules in both directions and would be a fork of the source of truth.
  - Blank cell sentinel is the em dash `—`, shared between generator and verifier via `BLANK`.
    They disagreed once and produced 186 phantom mismatches.
  - Cura setting scope: `settable_per_mesh` and `settable_per_extruder` both false means GLOBAL, and
    such a setting written into an extruder file is silently ignored.

## DECISIONS

- 2026-07-30 Working repo lives outside Google Drive; only a `git bundle` plus plain file copies go
  into Drive — a live `.git` object store and Drive sync corrupt each other, a finished single file
  does not. Reversible: yes.
- 2026-07-30 Generated STLs and the versioned `.inst.cfg` copies ARE committed — they are the
  artifacts that go to the slicer and the restore point respectively, not build output. Reversible: yes.
- 2026-07-30 Table is generated between markers inside the vault prose rather than being a whole
  generated file, so hand-written reasoning survives regeneration. Reversible: yes.
- 2026-07-30 Profile naming is `N<nozzle> L<layer>`. The prior scheme used a bare decimal in the
  same position for two different quantities. Reversible: no — renaming again costs more confusion
  than it saves.
- 2026-07-30 No copy of the master table in the repo. Reversible: no — it is a rule conflict, not a
  preference.
