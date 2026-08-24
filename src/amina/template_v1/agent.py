"""Template V1 worker — locked Soniox stack, editable prompt/soul/project.toml."""

from __future__ import annotations

import tomllib
from pathlib import Path

from livekit import agents
from livekit.agents import Agent, AgentServer, JobContext, ModelSettings

from amina.agent import AminaAgent
from amina.agent_soniox import build_session
from amina.telemetry import setup_langfuse
from amina.template_v1.prompts import OPENER_INSTRUCTIONS, SYSTEM_INSTRUCTIONS

_PROJECT = tomllib.loads((Path(__file__).with_name("project.toml")).read_text())
AGENT_NAME = str(_PROJECT["editable"]["agent_name"])


class TemplateV1Agent(AminaAgent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=OPENER_INSTRUCTIONS)

    async def tts_node(self, text, model_settings: ModelSettings):
        return Agent.default.tts_node(self, text, model_settings)


server = AgentServer()


@server.rtc_session(agent_name=AGENT_NAME)
async def template_v1_entry(ctx: JobContext) -> None:
    provider = setup_langfuse(
        metadata={"langfuse.session.id": ctx.room.name, "agent": AGENT_NAME}
    )

    async def flush_trace() -> None:
        if provider is not None:
            provider.force_flush()

    ctx.add_shutdown_callback(flush_trace)
    session = build_session()
    await session.start(room=ctx.room, agent=TemplateV1Agent())


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
