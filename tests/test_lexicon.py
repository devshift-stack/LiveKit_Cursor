
from amina.lexicon import apply_lexicon, load_lexicon


def test_load_lexicon_from_repo() -> None:
    lex = load_lexicon()
    assert lex.engine == "fish-audio-s2.1-pro"
    assert any(r.src == "Aquaphor" for r in lex.replacements)


def test_replaces_brand_and_keeps_diacritics() -> None:
    text = "Aquaphor Smile bokal kod slavine u Sarajevu."
    out = apply_lexicon(text)
    assert "A-kva-for" in out
    assert "Smaj-l" in out
    assert "Sara-je-vu" in out
    assert "bokal" in out
    assert "slavine" in out


def test_does_not_touch_protected_words() -> None:
    text = "pouzeće, flaša, sedmica, bokal"
    assert apply_lexicon(text) == text


def test_replaces_inflected_djenita() -> None:
    assert "Dženita" in apply_lexicon("Zovem Đenita.")
