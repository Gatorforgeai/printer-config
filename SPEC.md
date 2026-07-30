# SPEC — Printer Config

Status: DRAFT — not yet ratified
Ratified: <date, by Mark>

> ⚠️ Written after the work, not before it. This project grew out of a calibration session rather
> than an interview, so read it as a transcription of what was actually built and check it, rather
> than a contract agreed up front.

---

## WHY

Printer settings were spread across three documents that disagreed with each other, and the Cura
profiles themselves existed as a single unversioned copy under `%APPDATA%`. A Cura upgrade, a bad
edit, or a disk event meant re-tuning both machines from nothing. Separately, a week of failed
prints was traced to an e-step value nobody had ever recorded — the settings were undocumented in
exactly the places that mattered.

If never built: every calibration is repeated from scratch after each mishap, and no value is
traceable to the measurement that produced it.

## WHAT

One generated table that is the single source of truth for every Cura setting on both printers,
version control and offsite backup of the underlying `.inst.cfg` files, the calibration instruments
that produce the numbers, and the recorded reasoning behind each value.

**Success artifact:** `refresh.py` runs, the table regenerates from disk, the verifier reports zero
mismatches across every value, and a commit lands on the remote. If the feature were dead the
verifier would report a nonzero count or refuse on zero values compared.

**Explicitly NOT:** a slicer replacement, a profile-authoring GUI, or a general 3D-printing wiki.
It documents these two machines and nothing else.

## WHO

Mark, and any AI session resuming printer work. Triggered by hand after tuning — nothing schedules
it.

## WHERE

Repo `D:\GatorForge\AI CAD 3D Print Laser\Printer Config`, GitHub remote `Gatorforgeai/printer-config`.
Live table in the vault at
`_AI_OBS\02 Projects\AI CAD 3D Print Laser\Printer Config\_PRINTER SETTINGS MASTER TABLE.md`.
Backup at `_AI_OBS\10 Attachments\printer-config-backup\`.

Reads `%APPDATA%\cura\5.13\` — **SACRED, never written to by this project.**

## WHEN

On demand, after any settings change. A run takes well under a minute.

## HOW

`refresh.py` copies live Cura config into the repo and the Drive backup, regenerates the table
between markers in the vault document, verifies it against disk, then commits and pushes.

Riskiest part: it must refuse to run while Cura is open, because Cura rewrites its config on exit
and would silently capture a stale snapshot.

## CONSTRAINTS

- Cura must be closed; the tool aborts otherwise.
- Never write into `%APPDATA%\cura` — read-only from this project's perspective.
- Git internals must stay out of Google Drive (Drive corrupts a live object store); the working
  repo is on local disk and only a finished bundle goes to Drive.
- No hard deletes; removals go to a dated quarantine and the Removal Log.
- Prices, where hardware is discussed, are live-data-only.

## VERIFICATION

```
python refresh.py
```

Expected: `values compared: <N> | errors: 0`, a new commit, `pushed`. The verifier refuses to pass
on zero values compared, so an empty or broken parse cannot masquerade as success.

---

## Components

- `refresh.py` — orchestrator: capture, regenerate, verify, commit, push
- `tools\generate_table.py` — emits the table between markers; exits nonzero on an uncategorised
  setting or a missing profile rather than silently omitting it
- `tools\verify_table.py` — independent check of table against `.inst.cfg`; catches hand edits
- `calibration\` — flow-cal cylinder + generator; the superseded plain cube kept as history
- `cura-5.13\` — the versioned profile copies

## Open decisions

Tracked in the vault ledger:
`_AI_OBS\02 Projects\AI CAD 3D Print Laser\Printer Config\02 Next Actions.md`
