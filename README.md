# ACE Python — Multilingual AI Computer Agent

A Python-first Windows computer-use agent inspired by the UI-TARS Desktop action model. It accepts text or English/Hindi/Telugu/mixed speech, sends the current screenshot plus the task to an OpenAI-compatible multimodal VLM, parses UI-TARS-style actions, validates them, executes them locally, and loops until completion.

## Features
- AI decides actions from the goal + screenshot; no website-specific command dictionary.
- UI-TARS-style action grammar: click, double click, right click, drag, hotkey, type, scroll, wait, finished, call_user.
- Windows screenshots and local mouse/keyboard control.
- English/Hindi/Telugu and code-switching speech via faster-whisper.
- Optional multilingual TTS via edge-tts.
- Screen reading / describing through the same VLM.
- Pause/resume/stop and safety confirmation for destructive actions.
- PySide6 desktop UI, with CLI fallback.
- OpenAI-compatible multimodal endpoint configuration, suitable for providers that expose the required vision API.
- Mock mode and unit tests.

## Install on Windows
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

For microphone transcription, `faster-whisper` downloads a model the first time. For TTS, Edge TTS requires network access. The VLM endpoint is configured independently.

## Run
```powershell
python -m ace_agent
```

or:
```powershell
python -m ace_agent --cli
```

## Environment
See `.env.example`.

`MODEL`, `BASE_URL`, and `API_KEY` point to an OpenAI-compatible multimodal model. The model must accept an image in the request and return the UI-TARS-style action format.

## Safety
The agent never executes model-generated shell/code. It only executes a fixed validated computer action schema. Delete/overwrite/send/post/purchase/shutdown/restart style actions require confirmation when they can be detected from the task/action context.

## UI-TARS relationship
The supplied UI-TARS Desktop repository was inspected as the reference for its GUI-agent loop, action grammar, parsing concepts, and operator separation. This project intentionally implements the same computer-use contract in Python rather than shipping Electron/TypeScript. The upstream repository remains the canonical reference for additional operators and model adapters.
