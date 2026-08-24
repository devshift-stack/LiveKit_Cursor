from amina.syllables import hyphenate_last_syllable, hyphenate_text


def test_ear_verified_last_syllable() -> None:
    assert hyphenate_last_syllable("Amina") == "Ami-na"
    assert hyphenate_last_syllable("pitanja") == "pita-nja"
    assert hyphenate_last_syllable("trenutak") == "trenu-tak"


def test_skips_short_words() -> None:
    assert hyphenate_last_syllable("Dobar") == "Dobar"
    assert hyphenate_last_syllable("dan") == "dan"
    assert hyphenate_last_syllable("kuće") == "kuće"
    assert hyphenate_last_syllable("vodi") == "vodi"


def test_skips_already_hyphenated() -> None:
    assert hyphenate_last_syllable("Ami-na") == "Ami-na"


def test_sentence_keeps_short_and_brands() -> None:
    raw = (
        "Dobar dan, ovdje Amina iz firme Firmira, zovem vas zbog kratkog "
        "pitanja o vodi kod kuće. Da li ste sad tu na trenutak?"
    )
    out = hyphenate_text(raw, skip={"Firmira", "Aquaphor", "Smile"})
    assert "Ami-na" in out
    assert "pita-nja" in out
    assert "trenu-tak" in out
    assert "Firmira" in out
    assert "Dobar dan" in out
