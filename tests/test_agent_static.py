from amina.agent import AminaAgent
from amina.prompts import SYSTEM_INSTRUCTIONS


def test_instructions_lock_language_and_price() -> None:
    text = SYSTEM_INSTRUCTIONS
    assert "bosansk" in text.lower() or "ijekavica" in text.lower()
    assert "pouzeće" in text
    assert "cijena" in text.lower() or "cijen" in text
    assert "vrč" in text  # listed as forbidden


def test_agent_starts_without_room() -> None:
    agent = AminaAgent()
    assert "Amina" in agent.instructions
