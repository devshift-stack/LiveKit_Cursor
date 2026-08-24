"""Prepare LLM text for Fish s2.1-pro."""

from __future__ import annotations

import re

from amina.lexicon import apply_lexicon

_S1_ROUND = re.compile(r"\((happy|calm|sad|angry|excited|whispering|serious)\)", re.IGNORECASE)


def prepare_tts_text(text: str) -> str:
    cleaned = _S1_ROUND.sub("", text)
    cleaned = re.sub(r" {2,}", " ", cleaned).strip()
    return apply_lexicon(cleaned)
