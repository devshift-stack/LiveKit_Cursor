"""Bosnian last-syllable hyphen for Fish G2P. Not IPA."""

from __future__ import annotations

import re

_VOWELS = set("aeiouAEIOU")
_DIGRAPHS = ("dž", "Dž", "DŽ", "lj", "Lj", "LJ", "nj", "Nj", "NJ", "dj", "Dj", "DJ")
_TOKEN = re.compile(r"(\[[^\]]+\]|[A-Za-zÀ-žđĐ]+(?:-[A-Za-zÀ-žđĐ]+)*|[^\s])")


def _units(word: str) -> list[str]:
    units: list[str] = []
    i = 0
    lower = word
    while i < len(lower):
        pair = lower[i : i + 2]
        if pair in _DIGRAPHS:
            units.append(word[i : i + 2])
            i += 2
        else:
            units.append(word[i])
            i += 1
    return units


def _is_vowel_unit(unit: str) -> bool:
    return len(unit) == 1 and unit in _VOWELS


def hyphenate_last_syllable(word: str) -> str:
    if "-" in word or not word.isalpha():
        return word
    units = _units(word)
    vowel_idx = [i for i, u in enumerate(units) if _is_vowel_unit(u)]
    if len(vowel_idx) < 3:
        return word
    last = vowel_idx[-1]
    start = last
    if last > 0 and not _is_vowel_unit(units[last - 1]):
        start = last - 1
    if start <= 0:
        return word
    return "".join(units[:start]) + "-" + "".join(units[start:])


def hyphenate_text(text: str, skip: set[str] | None = None) -> str:
    blocked = {s.casefold() for s in (skip or ())}

    def one(match: re.Match[str]) -> str:
        tok = match.group(0)
        if tok.startswith("["):
            return tok
        if not tok[0].isalpha():
            return tok
        if tok.casefold() in blocked:
            return tok
        return hyphenate_last_syllable(tok)

    return _TOKEN.sub(one, text)
