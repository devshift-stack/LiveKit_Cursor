from amina.agent_soniox import SONIOX_MODEL, SONIOX_SPEED, SONIOX_VOICE, AminaSonioxAgent


def test_soniox_uses_v2_model() -> None:
    assert SONIOX_MODEL == "tts-rt-v2"


def test_soniox_ear_settings() -> None:
    assert SONIOX_VOICE == "Nina"
    assert SONIOX_SPEED == 0.9


def test_soniox_agent_is_amina_subclass() -> None:
    assert issubclass(AminaSonioxAgent, object)
    assert AminaSonioxAgent.__name__ == "AminaSonioxAgent"
