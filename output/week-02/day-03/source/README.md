# Reproduction — Optional dependencies

Approved topic Optional dependencies; publication2026-11-25, proposed19:00Asia/Phnom_Penh. Actual tests: bash source/java/run.sh. Java21/ECJ3.40 targets17, Spring6.2.11/JUnit5.12.2/platform1.12.2; pinned JARs/checksums/licenses included. Configs.java contains the minimal configurations; OptionalTest asserts all startup outcomes and exact present reference, including the additional ambiguity guard. Negative-test warnings are expected. No standalone app/business/security behavior is claimed.

Voice: bash source/voice/setup.sh, then its .venv Python generate.py, qa.py --asr-model small.en and align.py. Setup must supply pinned Kokoro models/style bank and ASR cache; hashes/licenses retained. Use normal1.02 male80Puck20Fenrir. Source/voice/align.py maps known script words to observed ASR windows, preserving raw ASR/error score. No evenly divided captions or listening approval.

Install source/animation/requirements.txt, run audio_mix.py, render.py --render, then validate.py. Final packaging uses deliver.py after reports and source freeze. Keep model binaries, environments and caches excluded. Original music is synthesized locally. Inter cover104px/900; captions52px/700, dynamic rounded black82% backgrounds, 26/14padding, max840px. Do not publish automatically. Perceptual voice approval and actual browser/phone playback are unverified.
