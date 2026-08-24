from amina.fish_text import prepare_tts_text
from amina.lexicon import apply_lexicon, load_lexicon


def test_load_lexicon_from_repo() -> None:
    lex = load_lexicon()
    assert lex.engine == "fish-audio-s2.1-pro"
    assert any(r.src == "Amina" for r in lex.replacements)


def test_keeps_brands_unhyphenated() -> None:
    text = "Aquaphor Smile bokal kod slavine u Sarajevu."
    out = apply_lexicon(text)
    assert out == text
    assert "A-kva-for" not in out
    assert "Smaj-l" not in out


def test_does_not_touch_protected_words() -> None:
    text = "pouzeće, flaša, sedmica, bokal"
    assert apply_lexicon(text) == text


def test_replaces_inflected_djenita() -> None:
    assert "Dženita" in apply_lexicon("Zovem Đenita.")


def test_hyphenates_ear_verified_opener_words() -> None:
    raw = (
        "Dobar dan, ovdje Amina iz firme Firmira, zovem vas zbog kratkog "
        "pitanja o vodi kod kuće. Da li ste sad tu na trenutak?"
    )
    out = prepare_tts_text(raw)
    assert "kratkog" in out
    assert "Ami-na" in out
    assert "pita-nja" in out
    assert "trenu-tak" in out
    assert "Firmira" in out
    assert "Amina" not in out.replace("Ami-na", "")
