#!/usr/bin/env python3
"""Rebuild AGENTEN.md from src/ — run after adding or renaming an agent."""

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AGENTEN.md"

# Fallback if tomllib missing (should not happen on 3.11+)
try:
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore


def git_when(path: Path) -> str:
    r = subprocess.run(
        ["git", "log", "-1", "--format=%h %cI", "--", str(path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return r.stdout.strip() or "—"


def load_toml(path: Path) -> dict:
    if tomllib is None:
        return {}
    return tomllib.loads(path.read_text())


def discover() -> list[dict]:
    rows: list[dict] = []
    src = ROOT / "src"
    for agent_py in sorted(src.rglob("agent.py")) + sorted(src.rglob("agent_*.py")):
        if agent_py.name.startswith("test"):
            continue
        text = agent_py.read_text()
        toml_path = agent_py.parent / "project.toml"
        name = None
        display = None
        voice = ""
        if toml_path.exists():
            ed = load_toml(toml_path).get("editable", {})
            name = ed.get("agent_name")
            display = ed.get("display_name")
            locked = load_toml(toml_path).get("locked", {})
            voice = str(locked.get("tts", ""))
        lit = re.findall(r'agent_name\s*=\s*["\']([^"\']+)["\']', text)
        if not name and lit:
            name = lit[0]
        if agent_py.parent.name == "template_v1" or "soniox" in agent_py.name:
            kind = "Soniox Nina"
        elif "Daniel" in text or "Daniel" in voice:
            kind = "Soniox Daniel"
        elif "soniox" in voice.lower() or "Nina" in voice:
            kind = "Soniox Nina"
        elif "fishaudio" in text or (
            agent_py.name == "agent.py" and "amina" in str(agent_py.parent)
        ):
            kind = "Fish Ela"
        else:
            kind = "—"
        if agent_py.parent.name == "template_v1":
            role = "Vorlage (Klon)"
        elif agent_py.parent.name == "alans_mujo_v3":
            role = "Familien-Demo Dr Mujo"
        elif agent_py.name == "agent_soniox_v2.py":
            role = "Amina Verkauf — Cloud"
        elif agent_py.name == "agent_soniox.py":
            role = "Amina Soniox alt"
        elif agent_py.name == "agent.py":
            role = "Amina Verkauf Fish"
        else:
            role = "—"
        rows.append(
            {
                "display": display or name or agent_py.stem,
                "name": name or "?",
                "file": str(agent_py.relative_to(ROOT)),
                "kind": kind,
                "role": role,
                "git": git_when(agent_py),
            }
        )
    # unique by file
    seen: set[str] = set()
    out = []
    for r in rows:
        if r["file"] in seen:
            continue
        seen.add(r["file"])
        out.append(r)
    return out


def render(rows: list[dict]) -> str:
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    lines = [
        "# Agenten-Registry",
        "",
        "Ein Blick. Quelle: Dateien unter `src/`. Neu schreiben:",
        "",
        "```bash",
        "uv run python scripts/update-agent-registry.py",
        "```",
        "",
        f"Zuletzt gebaut: **{now}**",
        "",
        "| Anzeige | LiveKit-Name | Datei | Stimme | Rolle | Letzter Git |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['display']} | `{r['name']}` | `{r['file']}` | {r['kind']} | {r['role']} | {r['git']} |"
        )
    lines += [
        "",
        "## Cloud (manuell prüfen: `lk agent list --project aai`)",
        "",
        "| ID | Name |",
        "|---|---|",
        "| `CA_J8AZ7K6yJ5o3` | `amina-soniox-v2` |",
        "",
        "Mujo und Template sind **nicht** deployed.",
        "",
        "## Start",
        "",
        "| Agent | Befehl |",
        "|---|---|",
        "| Fish | Desktop `01-Amina-Fish.command` |",
        "| Amina Soniox alt | Desktop `02-Amina-Soniox-alt.command` |",
        "| Amina v2 | Desktop `03-Amina-v2-Soniox.command` |",
        "| Template V1 | Desktop `04-Template-V1.command` |",
        "| Mujo | Desktop `05-Alans-Mujo-V3.command` |",
        "| Cloud-Anruf (wählen) | Desktop `00-Cloud-Anruf.command` |",
        "| GSM-Call (Cloud-Amina) | `./scripts/call-live-gsm.sh` |",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    text = render(discover())
    OUT.write_text(text)
    print(OUT)


if __name__ == "__main__":
    main()
