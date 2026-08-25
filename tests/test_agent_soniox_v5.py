from pathlib import Path

from amina.agent import build_deepgram_stt
from amina.agent_soniox_v5 import AminaSonioxV5Agent

ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / "src" / "amina" / "agent_soniox_v5.py"


def test_v5_agent_name() -> None:
    text = V5.read_text(encoding="utf-8")
    assert 'agent_name="amina-soniox-v5"' in text
    assert "amina-soniox-v2" not in text


def test_v5_uses_soniox_prompt() -> None:
    agent = AminaSonioxV5Agent()
    assert "[warm]" in agent.instructions
    assert "FISH TAGOVI" not in agent.instructions


def test_build_deepgram_stt_has_voice_agent_flags() -> None:
    stt = build_deepgram_stt(["Amina"])
    opts = stt._opts
    assert opts.smart_format is True
    assert opts.endpointing_ms == 300
    assert opts.vad_events is True
