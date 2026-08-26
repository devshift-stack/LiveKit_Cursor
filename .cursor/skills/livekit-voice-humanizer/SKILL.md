---
name: livekit-voice-humanizer
description: >-
  Appends a short Voice-realism section to a LiveKit cascaded STT→LLM→TTS
  system prompt (Agent Builder Instructions or SDK Agent.instructions) so the
  agent sounds spoken, not written. Use when the user says the agent sounds
  robotic, fake, scripted, Wikipedia-like, leblos, vorgelesen, too perfect, or
  asks for filler words, SSML pauses, conversational style, personality, or to
  humanize a LiveKit / Agent Builder prompt. Complements livekit-agents. Never
  replace Identity, Output rules, Goals, Tools, or Guardrails.
license: MIT
metadata:
  author: activi
  version: "1.0.0"
  stack: livekit-cloud
---

# LiveKit Voice Humanizer

Add a **Voice-realism addendum** to an existing LiveKit prompt. Do not rewrite the whole system prompt.

Facts (SSML, TTS tags, Expressive Mode, Builder fields) come from LiveKit Docs MCP or `lk docs`. Never from memory.

## When not to use

- Building a new agent from scratch → `livekit-agents` + [Prompting guide](https://docs.livekit.io/agents/start/prompting.md)
- Simulations / test scenarios → `livekit-simulations`
- Realtime / speech-to-speech models → skip SSML and filler tags; they are not interpreted
- User wants a different voice or model first → check TTS / Expressive Mode in docs, then prompt

## Decision order

1. Confirm cascaded STT→LLM→TTS (Agent Builder is always cascaded).
2. Look up current TTS: SSML `<break>`? provider tags? Expressive Mode?
3. **If Expressive Mode is available and on** (SDK / Inference TTS such as Fish, Cartesia Sonic, Inworld, SpaceXAI): keep delivery out of the prompt. Add at most 2–3 spoken example pairs, no SSML dump.
4. **If Builder-only or TTS without Expressive**: append the realism section below.
5. Spoken-language of the agent = language of examples. German agent → German pairs. Never keep English `um` / `like` / `so` in a German prompt.

## Audit existing prompt

List only concrete failures:

- Vague adjectives (`freundlich`, `conversational`, `natürlich`) without hearable patterns
- Missing Bad → Good spoken pairs
- Naked fillers (`äh`, `um`) without pause + recovery
- Personality as adjectives instead of sentence openers / recoveries / closings
- Missing Output rules (plain text, spell numbers, 1–3 sentences)
- English examples on a German agent

Do not invent failures. If the prompt already has Identity / Output / Goals, leave them.

## Write the addendum

Append **one** markdown section. Target: short enough to sit beside Identity, Output rules, Goals, Tools, Guardrails.

Required pieces:

1. **4–6 Bad → Good pairs** covering greeting, clarify, lookup, bad news, confirm, close. Same language as the agent.
2. **Filler unit** (only if TTS supports pauses/SSML — verify first):
   - `filler + pause + recovery` (DE: `äh` + Pause + `also` / `genau` / `okay`)
   - Never a naked filler
3. **4–5 audible personality rules** in the agent language. Examples: rotate openers (`Also` / `Genau` / `Warte kurz`); loose callback (`zu dem anderen Punkt`); warm specific close. No `like frequently`. No “ask again even if you understood”.
4. **Emotion**: calm default. Strong emotion or laugh/sigh at most once per call; never on money, complaint, legal, health.
5. **Tool wait**: one short hold (`Einen Moment, ich schau kurz nach.`) — not a rambling “still looking” loop. If the Builder tool is Silent, do not prompt speech during the call.

Restate each critical rule once after the examples. Do not triple-repeat; that bloats latency.

## Builder vs SDK

| Surface | Do |
|---|---|
| Agent Builder Instructions | Paste addendum into the single Instructions field. Greeting stays in the Greeting field. |
| Data Collection | Put tool-trigger text on the **field**, not in the main realism block. |
| SDK after export | Prefer Expressive Mode for delivery. Prompt owns *what*; Expressive owns *how*. |
| Tests | After prompt change, add or update a behavior test when working in the SDK. Builder has no tests — use Preview and listen. |

## Output (always)

### Audit
- bullets, or `none — new addendum`

### Voice-realism addendum (copy-paste)
Ready-to-paste markdown section only — not a full replacement prompt.

### TTS / tag check
- Which TTS is selected
- SSML / tags verified? yes/no/unknown
- Expressive Mode: on / off / not in Builder

### Why
- 3–5 short levers

### Next listen
1. Preview in Builder (or call) with the real TTS
2. If tags are spoken aloud → remove them, keep wording only
3. Banking / health / legal → strip almost all fillers

## Guardrails

- Do not replace Identity, Output rules, Goals, Tools, Guardrails, or `{{metadata.*}}`.
- Do not recommend Ultravox or other stacks.
- Do not claim SSML works without a docs check for the selected TTS.
- Professional domains: almost no fillers; calm, clear, short.
- Keep the addendum compact. If it rivals the rest of the prompt in length, cut pairs first.

## Templates

Paste-ready DE/EN blocks: [addendum.md](addendum.md)
