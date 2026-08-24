"""Template V1 must keep the locked Soniox stack."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "src" / "amina" / "template_v1" / "agent.py"


def test_template_imports_locked_stack() -> None:
    text = AGENT.read_text()
    assert "from amina.agent_soniox import build_session" in text
    assert "soniox.TTS" not in text
    assert "fishaudio" not in text
    assert "deepgram.STT" not in text


def test_template_project_toml_has_editable() -> None:
    import tomllib

    data = tomllib.loads((AGENT.parent / "project.toml").read_text())
    assert data["editable"]["agent_name"] == "template-v1"
    assert "prompts.py" in {p.name for p in AGENT.parent.iterdir()}
    assert (AGENT.parent / "soul.md").is_file()
