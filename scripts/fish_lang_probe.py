"""Try undocumented Fish language=BS vs bs vs none. Saves WAVs, no secrets printed."""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env.local")
load_dotenv(Path.home() / ".hermes" / ".env", override=False)

TEXT = (
    "Dobar dan, ja sam Amina iz firme Firmira. "
    "Zovem vas zbog kratkog pitanja o vodi kod kuće. "
    "Jeste li sada tu na trenutak?"
)
VOICE = os.getenv("FISH_AUDIO_DEFAULT_VOICE", "d9b1befa09a34947b8c334268767abb6")
OUT = Path(__file__).resolve().parents[1] / "docs" / "voice" / "samples"
KEY = os.environ["FISH_API_KEY"]


def synth(label: str, extra: dict) -> None:
    body = {
        "text": TEXT,
        "reference_id": VOICE,
        "format": "wav",
        "sample_rate": 24000,
        "normalize": False,
        "temperature": 0.2,
        "prosody": {"normalize_loudness": True, "speed": 1.0, "volume": 0},
        **extra,
    }
    r = httpx.post(
        "https://api.fish.audio/v1/tts",
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "model": "s2.1-pro",
        },
        json=body,
        timeout=60,
    )
    dest = OUT / f"lang-{label}.wav"
    dest.write_bytes(r.content)
    ctype = r.headers.get("content-type", "")
    print(
        f"{label:8} http={r.status_code} ctype={ctype} bytes={len(r.content)} "
        f"head={r.content[:12]!r}"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    synth("none", {})
    synth("BS", {"language": "BS"})
    synth("bs", {"language": "bs"})
    synth("bs-BA", {"language": "bs-BA"})


if __name__ == "__main__":
    main()
