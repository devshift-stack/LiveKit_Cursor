"""Synthesize one Ela line for an ear check. Saves WAV, prints path."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents.utils import http_context
from livekit.plugins import fishaudio

from amina.fish_text import prepare_tts_text

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env.local")

TEXT = prepare_tts_text(
    "[happy] Dobar dan. Zovem se Amina iz firme [emphasis] Firmira. "
    "[break] Zovem zbog kratkog pitanja o vodi kod kuće. "
    "Da li ste sada tu na trenutak?"
)
OUT = ROOT / "docs" / "voice" / "samples" / "amina-ela-opener.wav"


async def main() -> None:
    if not os.getenv("FISH_API_KEY"):
        raise SystemExit("FISH_API_KEY missing in .env.local")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    async with http_context.open():
        tts = fishaudio.TTS(
            model="s2.1-pro",
            voice_id=os.getenv("FISH_AUDIO_DEFAULT_VOICE", "d9b1befa09a34947b8c334268767abb6"),
            normalize=False,
            normalize_loudness=True,
            latency_mode="balanced",
            output_format="wav",
            temperature=0.6,
        )
        stream = tts.synthesize(TEXT)
        audio = bytearray()
        sample_rate = 44100
        num_channels = 1
        async for ev in stream:
            audio.extend(ev.frame.data)
            sample_rate = ev.frame.sample_rate
            num_channels = ev.frame.num_channels
    import wave

    with wave.open(str(OUT), "wb") as wav:
        wav.setnchannels(num_channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(bytes(audio))
    print("wrote", OUT, "bytes", len(audio), "rate", sample_rate, "text", TEXT)


if __name__ == "__main__":
    asyncio.run(main())
