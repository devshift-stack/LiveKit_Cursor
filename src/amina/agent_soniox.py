"""Amina v1_soniox — same sales agent, Soniox TTS (Fish Ela untouched)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    ModelSettings,
    TurnHandlingOptions,
    inference,
)
from livekit.plugins import soniox

from amina.agent import KEYTERMS, AminaAgent, build_deepgram_stt
from amina.telemetry import setup_langfuse

load_dotenv(Path(__file__).resolve().parents[2] / ".env.local")

SONIOX_WS = os.getenv("SONIOX_TTS_WS", "wss://tts-rt.eu.soniox.com/tts-websocket")
SONIOX_VOICE = os.getenv("SONIOX_TTS_VOICE", "Nina")
SONIOX_MODEL = os.getenv("SONIOX_TTS_MODEL", "tts-rt-v2")
SONIOX_SPEED = float(os.getenv("SONIOX_TTS_SPEED", "0.9"))


class AminaSonioxAgent(AminaAgent):
    """v1 text path: no Fish hyphen lexicon."""

    async def tts_node(self, text, model_settings: ModelSettings):
        return Agent.default.tts_node(self, text, model_settings)


def build_session(
    *,
    voice: str | None = None,
    extra_keyterms: list[str] | None = None,
) -> AgentSession:
    keyterms = list(KEYTERMS)
    if extra_keyterms:
        keyterms.extend(extra_keyterms)
    return AgentSession(
        stt=build_deepgram_stt(keyterms),
        llm=inference.LLM(model="openai/gpt-4.1", provider="azure"),
        tts=soniox.TTS(
            model=SONIOX_MODEL,
            language="bs",
            voice=voice or SONIOX_VOICE,
            speed=SONIOX_SPEED,
            websocket_url=SONIOX_WS,
        ),
        turn_handling=TurnHandlingOptions(turn_detection=inference.TurnDetector()),
        allow_interruptions=True,
        min_interruption_duration=0.45,
    )


server = AgentServer()


@server.rtc_session(agent_name="amina-soniox")
async def amina_soniox_entry(ctx: JobContext) -> None:
    provider = setup_langfuse(
        metadata={"langfuse.session.id": ctx.room.name, "agent": "amina-soniox"}
    )

    async def flush_trace() -> None:
        if provider is not None:
            provider.force_flush()

    ctx.add_shutdown_callback(flush_trace)
    session = build_session()
    await session.start(room=ctx.room, agent=AminaSonioxAgent())


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
