"""Alans_mujo V3 Soniox — Dr Mujo. Does not replace Amina."""

from __future__ import annotations

import tomllib
from pathlib import Path

from livekit import agents
from livekit.agents import Agent, AgentServer, JobContext, ModelSettings

from alans_mujo_v3.prompts import OPENER_INSTRUCTIONS, SYSTEM_INSTRUCTIONS
from amina.agent_soniox import build_session
from amina.telemetry import setup_langfuse

_PROJECT = tomllib.loads((Path(__file__).with_name("project.toml")).read_text())
AGENT_NAME = str(_PROJECT["editable"]["agent_name"])
VOICE = "Daniel"
KEYTERMS = ["Alan", "Mujo", "Bihać", "Bihac", "Ljubijankić", "pisa"]


class AlansMujoV3Agent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=OPENER_INSTRUCTIONS)

    async def tts_node(self, text, model_settings: ModelSettings):
        return Agent.default.tts_node(self, text, model_settings)


server = AgentServer()


@server.rtc_session(agent_name=AGENT_NAME)
async def alans_mujo_v3_entry(ctx: JobContext) -> None:
    provider = setup_langfuse(
        metadata={"langfuse.session.id": ctx.room.name, "agent": AGENT_NAME}
    )

    async def flush_trace() -> None:
        if provider is not None:
            provider.force_flush()

    ctx.add_shutdown_callback(flush_trace)
    session = build_session(voice=VOICE, extra_keyterms=KEYTERMS)
    await session.start(room=ctx.room, agent=AlansMujoV3Agent())


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
