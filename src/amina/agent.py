"""Amina LiveKit agent — Fish Ela + Deepgram EU + Azure GPT-4.1 via Inference."""

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
    RunContext,
    TurnHandlingOptions,
    function_tool,
    inference,
)
from livekit.plugins import deepgram, fishaudio

from amina.fish_text import prepare_tts_text
from amina.prompts import OPENER_INSTRUCTIONS, SYSTEM_INSTRUCTIONS

load_dotenv(Path(__file__).resolve().parents[2] / ".env.local")

FISH_VOICE = os.getenv("FISH_AUDIO_DEFAULT_VOICE", "d9b1befa09a34947b8c334268767abb6")
DEEPGRAM_EU = os.getenv("DEEPGRAM_BASE_URL", "https://api.eu.deepgram.com/v1/listen")
KEYTERMS = [
    "Aquaphor",
    "Smile",
    "Firmira",
    "Amina",
    "bokal",
    "pouzeće",
    "flaširana",
    "slavina",
    "kamenac",
]


class AminaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)
        self.permission: bool | None = None
        self.water: str | None = None
        self.no_count = 0
        self.dnc = False

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=OPENER_INSTRUCTIONS)

    async def tts_node(self, text, model_settings: ModelSettings):
        async def rewritten():
            async for chunk in text:
                yield prepare_tts_text(chunk)

        return Agent.default.tts_node(self, rewritten(), model_settings)

    @function_tool
    async def record_permission(self, context: RunContext, granted: bool) -> str:
        """Record whether the person has a moment to talk."""
        self.permission = granted
        if not granted:
            return "Nema vremena. Ponudi kratki povratni poziv ili se ljubazno javi."
        return "Ima trenutak. Postavi jedno pitanje o vodi (slavina, flaširana, mješovito, ili već uređaj)."

    @function_tool
    async def record_water_source(self, context: RunContext, source: str) -> str:
        """Save how they drink water: slavina, flasirana, mjesovito, or filter."""
        self.water = source.strip().lower()
        return f"Zabilježeno: {self.water}. Jedna rečenica bola, pa pitaj da li smeta."

    @function_tool
    async def record_clear_no(self, context: RunContext) -> str:
        """Call when the person clearly refuses."""
        self.no_count += 1
        if self.no_count >= 2:
            return "Drugo jasno ne. Zahvali se i završi. Bez pritiska."
        return "Prvo ne. Jedna kratka rečenica, pa ponudi kraj ili kasniji poziv."

    @function_tool
    async def mark_dnc(self, context: RunContext) -> str:
        """Do-not-call. End immediately."""
        self.dnc = True
        return "Ne zovi. Odmah prekini. Bez prodaje."

    @function_tool
    async def request_callback(self, context: RunContext, when: str, phone: str) -> str:
        """Schedule a callback. when is morning or afternoon. phone is digits."""
        return f"Povratni poziv zabilježen: {when}, {phone}. Potvrdi i završi."

    @function_tool
    async def start_order(self, context: RunContext) -> str:
        """Only after they clearly say yes to an order."""
        if self.dnc:
            return "Zabrana poziva je aktivna. Ne uzimaj narudžbu."
        return (
            "Prvo pitaj saglasnost za ime i adresu. "
            "Zatim jedno polje po potezu: ime, adresa, telefon. "
            "Telefon pročitaj broj po broj."
        )

    @function_tool
    async def submit_order_draft(
        self,
        context: RunContext,
        name: str,
        address: str,
        phone: str,
    ) -> str:
        """Save a draft order after they confirm the readback."""
        if self.dnc:
            return "Ne zovi. Ne šalji narudžbu."
        return (
            f"Nacrt spreman: {name}, {address}, {phone}, Aquaphor Smile bokal, pouzeće. "
            "Ponovi sve i traži izričito da."
        )


def build_session() -> AgentSession:
    return AgentSession(
        stt=deepgram.STT(
            model="nova-3",
            language="bs",
            keyterm=KEYTERMS,
            filler_words=True,
            punctuate=True,
            base_url=DEEPGRAM_EU,
        ),
        llm=inference.LLM(model="openai/gpt-4.1", provider="azure"),
        tts=fishaudio.TTS(
            model="s2.1-pro",
            voice_id=FISH_VOICE,
            normalize=False,
            normalize_loudness=True,
            latency_mode="normal",
            temperature=0.25,
            top_p=0.5,
            chunk_length=300,
            min_chunk_length=80,
            condition_on_previous_chunks=True,
        ),
        turn_handling=TurnHandlingOptions(turn_detection=inference.TurnDetector()),
    )


server = AgentServer()


@server.rtc_session(agent_name="amina")
async def amina_entry(ctx: JobContext) -> None:
    session = build_session()
    await session.start(room=ctx.room, agent=AminaAgent())


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
