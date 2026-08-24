"""Copy local secrets into .env.local. Never prints values."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".env.local"


def _kv(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        s = s.removeprefix("export ")
        k, v = s.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def _lk() -> dict[str, str]:
    raw = subprocess.check_output(["lk", "project", "list", "--json"], text=True)
    projects = json.loads(raw)
    if isinstance(projects, dict):
        projects = projects.get("projects") or projects.get("Projects") or []
    current = None
    for p in projects:
        if p.get("Name") == "aai" or p.get("name") == "aai":
            current = p
            break
    if current is None and projects:
        current = projects[0]
    if not current:
        return {}
    return {
        "LIVEKIT_URL": current.get("URL") or current.get("url") or "",
        "LIVEKIT_API_KEY": current.get("APIKey") or current.get("api_key") or "",
        "LIVEKIT_API_SECRET": current.get("APISecret") or current.get("api_secret") or "",
    }


def main() -> None:
    hermes = _kv(Path.home() / ".hermes" / ".env")
    dograh = _kv(Path.home() / "Projects" / "dograh-devshift" / "api" / ".env")
    merged = {}
    merged.update(_lk())
    if hermes.get("DEEPGRAM_API_KEY"):
        merged["DEEPGRAM_API_KEY"] = hermes["DEEPGRAM_API_KEY"]
    if hermes.get("AZURE_OPENAI_API_KEY"):
        merged["AZURE_OPENAI_API_KEY"] = hermes["AZURE_OPENAI_API_KEY"]
    if hermes.get("AZURE_OPENAI_BASE_URL"):
        merged["AZURE_OPENAI_ENDPOINT"] = hermes["AZURE_OPENAI_BASE_URL"]
        merged["AZURE_OPENAI_BASE_URL"] = hermes["AZURE_OPENAI_BASE_URL"]
    fish = dograh.get("FISH_AUDIO_API_KEY") or hermes.get("FISH_API_KEY")
    if fish:
        merged["FISH_API_KEY"] = fish
    merged["FISH_AUDIO_DEFAULT_VOICE"] = "d9b1befa09a34947b8c334268767abb6"
    merged["DEEPGRAM_BASE_URL"] = "https://api.eu.deepgram.com/v1/listen"
    lines = ["# generated — not for git\n"]
    for k, v in merged.items():
        if v:
            lines.append(f"{k}={v}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    present = [k for k, v in merged.items() if v]
    print("wrote", OUT, "keys:", ",".join(present))


if __name__ == "__main__":
    main()
