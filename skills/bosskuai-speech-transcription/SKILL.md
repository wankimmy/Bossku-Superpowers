---
name: bosskuai-speech-transcription
description: "Use when building a speech-to-text pipeline: audio validation and ffmpeg prep, chunking long recordings, Whisper or cloud ASR choice, speaker diarization, SRT/VTT/JSON output, and privacy and retention controls."
---

# BosskuAI Speech Transcription

Use this skill to design or fix a pipeline that turns recordings (meetings, calls, podcasts, interviews) into time-stamped, speaker-attributed, usable text. Most bad transcripts come from bad input handling, not from the model.

## How this differs from nearby skills

- **`bosskuai-video-editing`** and **`bosskuai-videodb`**: editing and indexing video; this skill produces text from audio.
- **`bosskuai-audio-prompting`**: prompting generative audio models, the opposite direction.
- **`bosskuai-data-pipelines`**: general ETL and orchestration; combine for queue and storage design.
- **`bosskuai-healthcare-phi-compliance`**: PHI rules; this skill only flags that regulated audio constrains where it can be processed.
- **`bosskuai-redis-caching-queues`**: job queues and retries that back the async workers.

## Workflow

1. Requirements. Note audio type, languages, speakers, accuracy need, latency (batch versus near-real-time), privacy and residency rules, cost limits, and output consumers.
2. Choose local, cloud, or hybrid. Compare cost per audio hour, speed relative to real time, error rate on your own domain sample, diarization quality, language coverage, and whether audio may leave your environment. Sensitive audio may need local models only.
3. Validate input. Probe the real container with `ffprobe`; do not trust extensions. Check duration bounds, codec, sample rate, channels, size, and an audio stream exists. Extract the audio track explicitly from video files.
4. Preprocess with ffmpeg: resample and downmix to what the model documents (Whisper-style models commonly use 16 kHz mono; check the model card), normalise loudness, drop video, and optionally trim silence.
5. Chunk long audio with overlap so words are not split at boundaries, then trim the overlap when assembling. Do not rely on a model's maximum length silently.
6. Transcribe with timestamps (word-level if subtitles need them) and voice-activity filtering. Check the installed library version for option names.
7. Diarize if speakers matter: run a diarization model or the vendor's speaker labels and assign each transcript segment the speaker with the most time overlap. Flag overlapping speech.
8. Post-process: normalise whitespace and punctuation, flag likely noise segments instead of deleting them, keep confidence values, route low-confidence segments for human review.
9. Export: a versioned JSON schema (segments with start, end, speaker, text, confidence), SRT or VTT with validated cue times and line and reading-speed limits, and Markdown if needed. Validate that cue times are finite, positive, and ordered.
10. Deliver: REST or webhook with retries and signed requests, CMS or LLM hand-off with speaker labels and time anchors for citations.
11. Test with a curated set of audio and reference transcripts. Track word error rate on your domain and run it in CI when the model or preprocessing changes.

## Guardrails

- Never discard timestamps or speaker labels between stages.
- Never log raw audio or unredacted transcript text in monitoring. Make PII detection and redaction a named, configurable stage.
- Enforce tenant isolation and honour retention windows with automated deletion.
- Recording consent and call-recording laws vary by place. Medical, legal, or workplace audio needs a privacy decision and qualified review; this skill organises the pipeline and is not legal or compliance advice.
- Do not upload audio to a third-party service, or tokens to a model hub, without explicit user approval. Keep tokens out of code and logs.
- Treat model confidence as a review signal, not accuracy. Do not cite word-error or speed numbers from others; measure your own.

## Output format

```text
Requirements and constraints: [audio, privacy, latency]
Engine choice: [local / cloud / hybrid, reason]
Pipeline stages: [validate, preprocess, chunk, transcribe, diarize, post-process, export]
Output schema: [fields, formats]
Privacy controls: [redaction, retention, isolation]
Quality plan: [test set, WER measure, human review route]
Risks: [list]
```

Adapted from agency-agents/engineering/engineering-voice-ai-integration-engineer.md (agency-agents, MIT).
