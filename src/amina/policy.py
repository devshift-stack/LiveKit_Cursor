"""Sales and language-lock rules that must not depend on the LLM."""

from __future__ import annotations

import re

_CROATIAN = (
    r"\bvrč\b",
    r"\bboca\b",
    r"\btjedan\b",
    r"\btisuć",
    r"\btko\b",
    r"\bšto\b",
    r"\btvrtka\b",
    r"\bsugovornik\b",
    r"\bsuglasnost\b",
    r"\bobitelj\b",
    r"\bsiječanj\b",
    r"\bveljača\b",
    r"\btočno\b",
    r"\btočka\b",
)

_CROATIAN_RE = re.compile("|".join(_CROATIAN), re.IGNORECASE)

_PRICE_ASK = re.compile(
    r"\b(koliko|cijena|cijenu|košta|kosta|cijeni|price|košta)\b",
    re.IGNORECASE,
)


def contains_croatian_lock_word(text: str) -> bool:
    return bool(_CROATIAN_RE.search(text))


def may_mention_price(user_text: str) -> bool:
    return bool(_PRICE_ASK.search(user_text))


def should_end_after_second_no(*, no_count: int) -> bool:
    return no_count >= 2
