"""Prepare LLM text for Fish s2.1-pro."""

from __future__ import annotations

import re

from amina.lexicon import apply_lexicon, load_lexicon
from amina.syllables import hyphenate_text

_S1_ROUND = re.compile(r"\((happy|calm|sad|angry|excited|whispering|serious)\)", re.IGNORECASE)


def prepare_tts_text(text: str) -> str:
    cleaned = _S1_ROUND.sub("", text)
    cleaned = re.sub(r" {2,}", " ", cleaned).strip()
    cleaned = apply_lexicon(cleaned)
    skip = set(load_lexicon().do_not_touch)
    return hyphenate_text(cleaned, skip=skip)
