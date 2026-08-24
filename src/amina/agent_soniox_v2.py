"""Amina v2_soniox — Nina + tts-rt-v2 + speed 0.9 + Soniox tags. Fish stays."""

from __future__ import annotations

from livekit import agents
from livekit.agents import Agent, AgentServer, JobContext, ModelSettings

from amina.agent import AminaAgent
from amina.agent_soniox import build_session
from amina.prompts_soniox import OPENER_INSTRUCTIONS_SONIOX, SYSTEM_INSTRUCTIONS_SONIOX
from amina.telemetry import setup_langfuse


class AminaSonioxV2Agent(AminaAgent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS_SONIOX)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=OPENER_INSTRUCTIONS_SONIOX)

    async def tts_node(self, text, model_settings: ModelSettings):
        return Agent.default.tts_node(self, text, model_settings)


server = AgentServer()


@server.rtc_session(agent_name="amina-soniox-v2")
async def amina_soniox_v2_entry(ctx: JobContext) -> None:
    provider = setup_langfuse(
        metadata={
            "langfuse.session.id": ctx.room.name,
            "agent": "amina-soniox-v2",
        }
    )

    async def flush_trace() -> None:
        if provider is not None:
            provider.force_flush()

    ctx.add_shutdown_callback(flush_trace)
    session = build_session()
    await session.start(room=ctx.room, agent=AminaSonioxV2Agent())


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
