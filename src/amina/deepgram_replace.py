"""Deepgram STT replace map — loaded at runtime; edited via scripts/replace.sh."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_DEFAULT = Path(__file__).resolve().parents[2] / "docs" / "voice" / "deepgram-replace.json"


def default_path() -> Path:
    return _DEFAULT


def load_deepgram_replace(path: Path | None = None) -> dict[str, str]:
    p = path or _DEFAULT
    data = json.loads(p.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for item in data.get("replacements", []):
        src = str(item["from"])
        out[src] = str(item["to"])
    return out


def _read_data(path: Path) -> dict:
    if not path.is_file():
        return {"note": "Deepgram STT replace (Transkript find→replace). Pflege: ./scripts/replace.sh", "replacements": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_data(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def list_replacements(path: Path | None = None) -> list[tuple[str, str]]:
    data = _read_data(path or _DEFAULT)
    return [(str(r["from"]), str(r["to"])) for r in data.get("replacements", [])]


def add_replacement(from_text: str, to_text: str, path: Path | None = None) -> str:
    p = path or _DEFAULT
    src = from_text.strip()
    dest = to_text.strip()
    if not src or not dest:
        raise ValueError("from und to dürfen nicht leer sein")
    data = _read_data(p)
    reps = data.setdefault("replacements", [])
    for item in reps:
        if str(item["from"]) == src:
            old = str(item["to"])
            item["to"] = dest
            _write_data(p, data)
            return f"aktualisiert: {src!r} {old!r} → {dest!r}"
    reps.append({"from": src, "to": dest})
    _write_data(p, data)
    return f"hinzugefügt: {src!r} → {dest!r}"


def remove_replacement(from_text: str, path: Path | None = None) -> bool:
    p = path or _DEFAULT
    src = from_text.strip()
    data = _read_data(p)
    reps = data.get("replacements", [])
    new = [r for r in reps if str(r["from"]) != src]
    if len(new) == len(reps):
        return False
    data["replacements"] = new
    _write_data(p, data)
    return True


def _print_list(path: Path) -> None:
    rows = list_replacements(path)
    if not rows:
        print("Keine Einträge in", path)
        return
    for src, dest in rows:
        print(f"  {src} → {dest}")


def _interactive(path: Path) -> None:
    print(f"Deepgram replace — {path}")
    _print_list(path)
    print()
    while True:
        try:
            src = input("From (leer = fertig): ").strip()
        except EOFError:
            print()
            break
        if not src:
            break
        dest = input("To: ").strip()
        if not dest:
            print("To leer — übersprungen.")
            continue
        try:
            print(add_replacement(src, dest, path))
        except ValueError as exc:
            print(f"Fehler: {exc}")
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deepgram STT replace map")
    parser.add_argument(
        "--file",
        type=Path,
        default=_DEFAULT,
        help="JSON-Datei (default: docs/voice/deepgram-replace.json)",
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Alle Einträge anzeigen")

    add_p = sub.add_parser("add", help="Eintrag hinzufügen oder aktualisieren")
    add_p.add_argument("from_text")
    add_p.add_argument("to_text")

    rm_p = sub.add_parser("remove", help="Eintrag nach from löschen")
    rm_p.add_argument("from_text")

    sub.add_parser("interactive", help="Interaktiv neue Wörter eingeben")

    args = parser.parse_args(argv)
    path = args.file

    if args.cmd is None:
        _interactive(path)
        return 0

    if args.cmd == "list":
        _print_list(path)
        return 0

    if args.cmd == "add":
        print(add_replacement(args.from_text, args.to_text, path))
        return 0

    if args.cmd == "remove":
        if remove_replacement(args.from_text, path):
            print(f"entfernt: {args.from_text!r}")
            return 0
        print(f"nicht gefunden: {args.from_text!r}", file=sys.stderr)
        return 1

    if args.cmd == "interactive":
        _interactive(path)
        return 0

    parser.error(f"unbekannter Befehl: {args.cmd}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
