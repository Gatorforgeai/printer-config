"""Capture the current Cura printer config into the repo, the vault and the Drive backup.

DONE WHEN: repo, vault table and Drive backup all reflect the .inst.cfg files as they
           are on disk right now, and (if anything changed) a commit exists on origin.
INPUTS:    no args. Cura RUNNING -> exit 1 without touching anything, because Cura
           rewrites its config on exit and the capture would be of a stale state.
           Nothing changed -> prints "no changes" and exits 0 without committing.
           --no-push -> do everything locally, skip the push.
FAILS WHEN: table regeneration fails (uncategorised setting, missing marker) - the
           run aborts BEFORE committing, so a half-captured state is never pushed.
"""
import argparse, datetime, glob, os, shutil, subprocess, sys

REPO = r"D:\GatorForge\AI CAD 3D Print Laser\Printer Config"
CURA = os.path.join(os.environ.get("APPDATA", ""), "cura", "5.13")
VAULT_DOC = r"D:\Google Drive\_AI_OBS\02 Projects\AI CAD 3D Print Laser\Printer Config\_PRINTER SETTINGS MASTER TABLE.md"
BACKUP = r"D:\Google Drive\_AI_OBS\10 Attachments\printer-config-backup"
SUBS = ("quality_changes", "definition_changes", "user", "variants")


def die(code, msg):
    print("ABORT:", msg)
    sys.exit(code)


def cura_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq UltiMaker-Cura.exe"],
                       capture_output=True, text=True, errors="replace")
    return "UltiMaker-Cura.exe" in r.stdout


def mirror(dest):
    n = 0
    for sub in SUBS:
        src = os.path.join(CURA, sub)
        if not os.path.isdir(src):
            continue
        d = os.path.join(dest, sub)
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(os.path.join(src, "*.inst.cfg")):
            shutil.copy2(f, os.path.join(d, os.path.basename(f)))
            n += 1
    return n


def git(*a, check=True):
    r = subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.stdout.strip():
        print(r.stdout.rstrip())
    if r.stderr.strip():
        print("[git]", r.stderr.rstrip())
    if check and r.returncode != 0:
        die(5, f"git {a[0]} failed rc={r.returncode}")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    if cura_running():
        die(1, "Cura is running. Close it first - it rewrites its config on exit, "
               "so anything captured now would be a stale snapshot.")

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    n = mirror(os.path.join(REPO, "cura-5.13"))
    print(f"profiles -> repo: {n}")

    # regenerate the table IN THE VAULT (the live copy), abort before commit on failure
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "generate_table.py"),
                        "--cura", CURA, "--target", VAULT_DOC, "--stamp", stamp],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout.rstrip() or r.stderr.rstrip())
    if r.returncode != 0:
        die(3, "table regeneration failed - nothing committed")

    v = subprocess.run([sys.executable, os.path.join(REPO, "tools", "verify_table.py"),
                        "--cura", CURA, "--target", VAULT_DOC],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(v.stdout.rstrip() or v.stderr.rstrip())
    if v.returncode != 0:
        die(3, "table failed verification against the .cfg files - nothing committed")

    shutil.copy2(VAULT_DOC, os.path.join(REPO, "PRINTER-SETTINGS-MASTER-TABLE.md"))

    m = mirror(os.path.join(BACKUP, "cura-5.13"))
    shutil.copy2(VAULT_DOC, os.path.join(BACKUP, "PRINTER-SETTINGS-MASTER-TABLE.md"))
    print(f"profiles -> Drive backup: {m}")

    git("add", "-A")
    if not git("status", "--porcelain").stdout.strip():
        print("no changes - nothing to commit")
        return

    git("commit", "-m", f"Config capture {stamp}\n\nAutomated by refresh.py from live Cura state.")

    bundle = os.path.join(BACKUP, "printer-config.bundle")
    git("bundle", "create", bundle, "--all")
    print(f"bundle refreshed: {os.path.getsize(bundle)} bytes")

    if a.no_push:
        print("--no-push set, skipping push")
        return
    if git("push", check=False).returncode != 0:
        print("PUSH FAILED - commit is local only. Everything else succeeded.")
        sys.exit(6)
    print("pushed")


if __name__ == "__main__":
    main()
