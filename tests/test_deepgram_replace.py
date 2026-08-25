import json
from pathlib import Path

from amina.deepgram_replace import add_replacement, load_deepgram_replace, remove_replacement


def test_load_empty_replace_map(tmp_path: Path) -> None:
    p = tmp_path / "deepgram-replace.json"
    p.write_text(
        json.dumps({"replacements": [{"from": "a", "to": "b"}]}, ensure_ascii=False),
        encoding="utf-8",
    )
    assert load_deepgram_replace(p) == {"a": "b"}


def test_add_and_remove_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "deepgram-replace.json"
    p.write_text(json.dumps({"replacements": []}, ensure_ascii=False), encoding="utf-8")
    add_replacement("flaširana", "flasirana", p)
    assert load_deepgram_replace(p) == {"flaširana": "flasirana"}
    assert remove_replacement("flaširana", p)
    assert load_deepgram_replace(p) == {}
