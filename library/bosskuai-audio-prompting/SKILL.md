---
name: bosskuai-audio-prompting
description: "Use when you need instrumental focus or background music made with a generative audio model (Suno, Udio, Stable Audio) or a Web Audio tone generator: prompt recipes, negative tags, tempo, and loop-friendly structure."
---

# BosskuAI Audio Prompting

Use this skill to turn "I need music to concentrate to" into a tight prompt (or a small Web Audio script) for a purely instrumental, non-fatiguing track.

## How this differs from nearby skills

- **`bosskuai-fal-ai-media`**: calls a hosted media-generation API (image, video, audio). This skill is about what to write in the prompt and how to check the result.
- **`bosskuai-video-creative-direction`**: music-video and edit aesthetics. This skill is background audio for working, not picture-led direction.
- **`bosskuai-prompt-optimizer`**: rewrites prompts for BosskuAI agents, not for audio models.

## Method

1. Ask what the listener is doing: reading specs, deep coding, a fast sprint, or winding down. Ask if they want a beat or no rhythm at all.
2. Pick a profile and a tempo range from it. Slower and sparse for analysis (felt piano, ambient drone); mid tempo for steady work (lo-fi, downtempo); steadier pulse for execution (chillsynth, minimal house); noise beds for masking distraction.
3. Write the positive prompt in this order: marker tag (`[Instrumental]`), genre, tempo, 3-5 instruments, texture (tape, vinyl, room reverb), mood, then loop intent.
4. Add negative tags for vocals and harshness: no vocals, speech, choir, vocal chops; no sharp treble, no drops, no distortion.
5. Keep harmony simple: modal, 2-4 chord cycles, no key changes. Ask for gentle fade-in and an open ambient tail so it loops.
6. Generate a few takes, listen for stray vocals, harsh high end, and sudden dynamics. Reject, then tighten the negative tags before re-running.
7. For real-time audio in a browser, use the Web Audio API. Start the context from a user gesture and resume it if the browser suspended it; connections alone stay silent.

## Guardrails

- Model tag syntax and version behaviour change; check the current docs of the tool you use before relying on a tag.
- Benefits of specific frequencies (alpha waves, binaural beats) are not settled. Present them as an option the user can try, not as a proven effect.
- Keep volume and dynamic range moderate; warn about long listening on headphones.
- Do not imitate a named living artist or reuse copyrighted lyrics or melodies; check the tool's licence terms before commercial use.

## Output format

```text
Task profile: [what the listener does] / [beat or no beat]
Prompt: [ordered positive prompt]
Negative: [tags]
Structure: [intro / loop / tail markers]
Check: [vocal leak, harsh highs, loop seam]
```

Adapted from agency-agents/specialized/specialized-focus-music-architect.md (agency-agents, MIT).
