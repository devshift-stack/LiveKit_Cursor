from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mujo_does_not_replace_amina() -> None:
    v2 = (ROOT / "src/amina/agent_soniox_v2.py").read_text()
    assert 'agent_name="amina-soniox-v2"' in v2
    docker = (ROOT / "Dockerfile").read_text()
    assert "amina.agent_soniox_v2" in docker
    assert "alans_mujo" not in docker


def test_mujo_uses_locked_stack_and_daniel() -> None:
    text = (ROOT / "src/alans_mujo_v3/agent.py").read_text()
    assert "from amina.agent_soniox import build_session" in text
    assert 'voice=VOICE' in text
    assert 'VOICE = "Daniel"' in text
    assert "AminaAgent" not in text
    assert "record_water" not in text


def test_mujo_prompt_is_doctor_not_sales() -> None:
    p = (ROOT / "src/alans_mujo_v3/prompts.py").read_text()
    assert "Mujo" in p and "Alan" in p
    assert "ZABRANJENO" in p and "prodaja" in p
    assert "Aquaphor Smile" not in p
    assert "SONIOX TAGOVI" in p
    assert "Ami-na" not in p or "crtice" in p
