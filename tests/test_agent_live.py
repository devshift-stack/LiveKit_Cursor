"""Live behavioral tests — needs LIVEKIT_* (Inference)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from livekit.agents import AgentSession, inference

from amina.agent import AminaAgent

load_dotenv(Path(__file__).resolve().parents[1] / ".env.local")

pytestmark = pytest.mark.integration


def _has_lk() -> bool:
    return bool(os.getenv("LIVEKIT_API_KEY") and os.getenv("LIVEKIT_API_SECRET"))


@pytest.mark.skipif(not _has_lk(), reason="LIVEKIT credentials missing")
@pytest.mark.asyncio
async def test_opener_asks_permission_not_product() -> None:
    async with (
        inference.LLM(model="openai/gpt-4.1", provider="azure") as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(AminaAgent())
        result = await session.run(user_input="Halo?")
        await result.expect.next_event().is_message(role="assistant").judge(
            llm,
            intent=(
                "Speaks Bosnian. Introduces herself as Amina from Firmira. "
                "Asks if the person has a moment. Does NOT mention Aquaphor, "
                "price, or placing an order."
            ),
        )


@pytest.mark.skipif(not _has_lk(), reason="LIVEKIT credentials missing")
@pytest.mark.asyncio
async def test_does_not_pitch_or_price_on_permission() -> None:
    async with (
        inference.LLM(model="openai/gpt-4.1", provider="azure") as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(AminaAgent())
        await session.run(user_input="Halo?")
        result = await session.run(user_input="Da, slušam, imam trenutak.")
        result.expect.contains_function_call(name="record_permission")
        result.expect.skip_next_event_if(type="function_call")
        result.expect.skip_next_event_if(type="function_call_output")
        await result.expect.next_event().is_message(role="assistant").judge(
            llm,
            intent=(
                "Bosnian. Asks one question about how they drink water "
                "(tap, bottled, mixed, or already a filter). "
                "Does not name a price. Does not close an order."
            ),
        )


@pytest.mark.skipif(not _has_lk(), reason="LIVEKIT credentials missing")
@pytest.mark.asyncio
async def test_second_no_ends_politely() -> None:
    async with (
        inference.LLM(model="openai/gpt-4.1", provider="azure") as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(AminaAgent())
        await session.run(user_input="Halo?")
        await session.run(user_input="Ne zanima me.")
        result = await session.run(user_input="Rekao sam ne, ne zovi više.")
        result.expect.skip_next_event_if(type="function_call")
        result.expect.skip_next_event_if(type="function_call_output")
        await result.expect.next_event().is_message(role="assistant").judge(
            llm,
            intent="Bosnian, polite goodbye. No more sales pitch, no price, no order.",
        )
