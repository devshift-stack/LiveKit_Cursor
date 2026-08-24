"""TTFT bench: LiveKit Inference vs Foundry EU. No secrets printed."""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env.local")
load_dotenv(Path.home() / ".hermes" / ".env", override=False)

PROMPT = (
    "Odgovori na bosanskom, jedna kratka rečenica, sa tagom [calm]. "
    "Nemoj spominjati cijenu. Reci samo: razumijem, flaše dodijaju."
)


def _ttft_azure(endpoint: str, key: str, deployment: str, api_version: str = "2024-10-21") -> float:
    client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=api_version)
    t0 = time.perf_counter()
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": PROMPT}],
        max_tokens=80,
        stream=True,
    )
    first = None
    text = []
    for chunk in stream:
        delta = ""
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
        if delta:
            if first is None:
                first = time.perf_counter()
            text.append(delta)
    t1 = time.perf_counter()
    out = "".join(text).replace("\n", " ")
    print(f"azure {deployment:16} ttft={first-t0:.3f}s total={t1-t0:.3f}s text={out[:120]!r}")
    return first - t0 if first else -1


async def _ttft_inference() -> float:
    from livekit.agents import inference

    llm = inference.LLM(model="openai/gpt-4.1", provider="azure")
    from livekit.agents import llm as lkllm

    ctx = lkllm.ChatContext()
    ctx.add_message(role="user", content=PROMPT)
    t0 = time.perf_counter()
    first = None
    parts = []
    async with llm.chat(chat_ctx=ctx) as stream:
        async for chunk in stream:
            piece = getattr(getattr(chunk, "delta", None), "content", None) or ""
            if piece:
                if first is None:
                    first = time.perf_counter()
                parts.append(piece)
    t1 = time.perf_counter()
    out = "".join(parts).replace("\n", " ")
    print(f"lk-inf gpt-4.1/azure ttft={(first-t0) if first else -1:.3f}s total={t1-t0:.3f}s text={out[:120]!r}")
    return (first - t0) if first else -1


def main() -> None:
    foundry_key = os.environ.get("AZURE_FOUNDRY_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY")
    # activids = West Europe DataZone
    activids = "https://activids.cognitiveservices.azure.com/"
    se = "https://dsselmanovic-6165-resource.cognitiveservices.azure.com/"
    if foundry_key:
        print("--- Foundry ---")
        _ttft_azure(activids, foundry_key, "gpt-4.1-mini")
        _ttft_azure(se, foundry_key, "gpt-4.1-mini")
        _ttft_azure(se, foundry_key, "gpt-4.1")
        _ttft_azure(se, foundry_key, "gpt-5-nano")
    else:
        print("no foundry key")
    print("--- LiveKit Inference ---")
    asyncio.run(_ttft_inference())


if __name__ == "__main__":
    main()
