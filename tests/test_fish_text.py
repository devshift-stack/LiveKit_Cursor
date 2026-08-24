from amina.fish_text import prepare_tts_text


def test_keeps_official_emotion_tags() -> None:
    raw = "[happy] Dobar dan. [break] Jeste li tu?"
    out = prepare_tts_text(raw)
    assert out.startswith("[happy]")
    assert "[break]" in out


def test_strips_round_s1_tags() -> None:
    raw = "(happy) Dobar dan."
    out = prepare_tts_text(raw)
    assert "(happy)" not in out
    assert "Dobar dan." in out


def test_applies_lexicon_after_tags() -> None:
    raw = "[confident] Baš zbog toga spominjem [emphasis] Aquaphor Smile bokal."
    out = prepare_tts_text(raw)
    assert "[confident]" in out
    assert "[emphasis]" in out
    assert "A-kva-for" in out
    assert "Smaj-l" in out
