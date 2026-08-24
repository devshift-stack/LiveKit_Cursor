"""Phonetic replacements applied after the LLM, before Fish TTS."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_DEFAULT = Path(__file__).resolve().parents[2] / "docs" / "voice" / "phonetic-lexicon.json"


@dataclass(frozen=True)
class Replacement:
    src: str
    dest: str


@dataclass(frozen=True)
class Lexicon:
    engine: str
    replacements: tuple[Replacement, ...]
    do_not_touch: tuple[str, ...]


def load_lexicon(path: Path | None = None) -> Lexicon:
    data = json.loads((path or _DEFAULT).read_text(encoding="utf-8"))
    reps = tuple(
        Replacement(src=item["from"], dest=item["to"]) for item in data.get("replacements", [])
    )
    return Lexicon(
        engine=data["engine"],
        replacements=reps,
        do_not_touch=tuple(data.get("do_not_touch", [])),
    )


def apply_lexicon(text: str, lexicon: Lexicon | None = None) -> str:
    lex = lexicon or load_lexicon()
    out = text
    for rep in sorted(lex.replacements, key=lambda r: len(r.src), reverse=True):
        out = out.replace(rep.src, rep.dest)
    return out
