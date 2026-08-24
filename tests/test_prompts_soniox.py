from amina.agent_soniox import SONIOX_SPEED, SONIOX_VOICE
from amina.agent_soniox_v2 import AminaSonioxV2Agent
from amina.prompts_soniox import OPENER_INSTRUCTIONS_SONIOX, SYSTEM_INSTRUCTIONS_SONIOX


def test_soniox_prompt_sets_english_tags() -> None:
    text = SYSTEM_INSTRUCTIONS_SONIOX
    for tag in ("[warm]", "[calm]", "[curious]", "[pause]", "[softly]"):
        assert tag in text
    assert "ZABRANJENO: bosanski tagovi" in text
    assert "Ami-na" in text  # listed as forbidden hyphen example
    assert "ćirilica" in text.lower() or "cirilica" in text.lower()


def test_opener_starts_with_warm_tag() -> None:
    assert "[warm]" in OPENER_INSTRUCTIONS_SONIOX
    assert "Ami-na" not in OPENER_INSTRUCTIONS_SONIOX


def test_v2_agent_uses_soniox_prompt() -> None:
    agent = AminaSonioxV2Agent()
    assert "[warm]" in agent.instructions
    assert "FISH TAGOVI" not in agent.instructions


def test_v2_uses_nina_and_speed() -> None:
    assert SONIOX_VOICE == "Nina"
    assert SONIOX_SPEED == 0.9
