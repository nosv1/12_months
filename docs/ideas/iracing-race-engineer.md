# iRacing race engineer (idea, 2026-10-10)

Brainstormed by phone on the drive to Omaha. Nothing built yet. A rewrite for fun, not a port of
the old ACC engineer (Python, untouched for ~6 months).

## The key idea (don't lose this)

**Log every question the engineer couldn't answer with a built-in function. The ones you keep
asking become proper built-in functions.**

The engineer gets two kinds of tools:

1. **Built-in functions** for known questions: gap to a car, gap trend, fuel to finish, pit-rejoin
   position. Fast and exact.
2. **A code fallback**: "run Python against the telemetry history." For a question with no
   function, the LLM writes a short query, runs it, reads the result, and answers.

Fallbacks are slow (several model round trips) and can be quietly wrong. Promoting the repeated
ones to built-ins means the engineer gets faster and more reliable on the questions you actually
ask. The replay recorder (below) lets you test this at a desk.

## What was wrong with the ACC version

- All behavior was pre-programmed triggers: catching the car ahead, car behind closing, pit gap
  open. Useful, but no intelligence.
- No good voice channel.
- No spotter.
- Python was **not** the problem. Easy to write and quick to test. Keep it.

## Wants

- Reacts to the race, tells you through audio (VR later, maybe).
- Understands real conversation, not fixed commands. DRE has some AI, but it falls down at
  understanding questions and answering them.
- **Local LLM only.** No paid usage.
- Hardware: Quest 3, RTX 5080 16 GB, Ryzen 7 9800X3D.

## Shape discussed (his to design)

Three layers:

1. **Deterministic detection.** Spotter (`CarLeftRight` gives left / right / three-wide directly),
   flags, gap trends, pit-rejoin math. Hard-coded: an LLM is too slow and too inconsistent for
   these calls.
2. **Race-state summary.** A compact, documented view of the race: a per-lap table for every car,
   recent detailed history, flags, fuel. **The quality of this data model and its descriptions
   decides how good the code fallback is**, more than the model does. Probably where DRE is weak
   (a guess, not checked).
3. **LLM engineer.** Decides whether something is worth saying, prioritizes, phrases it, and answers
   questions by calling tools. **It never does arithmetic itself.** It should say how it got an
   answer ("last five laps, sector 2") so wrong answers are visible.

Timing: hold non-urgent messages until a straight, using your lap-distance position. Never talk in
a braking zone.

## Voice pipeline

Push-to-talk on a wheel button → Whisper (speech to text) → LLM with tools → Piper or Kokoro (text
to speech). Set a latency target: button release to first spoken word.

## The real constraint: the GPU

iRacing in VR already loads the 5080. A local LLM competes with it for **memory** (a 4-bit model at
7–14B parameters needs ~5–9 GB) and for **compute** (generation steals frames, and dropped frames in
VR mean stutter). Options:

- Run Whisper and TTS on the CPU (the 9800X3D can handle it).
- Use a small model (~4–8B) and keep replies short.
- Ollama (wraps llama.cpp) is the easy way to download and serve weights locally.

**First experiment:** iRacing in VR, LLM requests firing in the background, watch frame times. That
one test tells you if the idea works.

## Suggested order

1. **Telemetry recorder + replay.** Read shared memory (`pyirsdk`), save a full race to file,
   replay it. Then you can develop at a desk without driving. Same idea as ROS bag files.
2. The GPU contention test above.
3. Deterministic layer: spotter, gaps, pit rejoin.
4. Voice in and out.
5. LLM with built-in functions, then the code fallback and the question log.
6. VR overlay last, if audio isn't enough. OpenKneeboard exists for OpenXR.

## Prior art to know

- iRacing's built-in spotter.
- Crew Chief (free; trigger-based calls and spotter for iRacing).
- DRE (some AI; weak on conversation, per his experience).

The part nobody does well yet is the conversational, judgment layer. That's where this one can be
different.
