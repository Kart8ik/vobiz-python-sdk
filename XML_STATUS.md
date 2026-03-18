# Vobiz XML Status (Current)

_Last updated: 2026-03-19_

## Quick Summary

The XML layer is now aligned to a strict spec-first model: `Gather` is the only input-collection verb, legacy `GetInput`/`GetDigits` have been removed, `AudioStream` is implemented, and core validations have been tightened (`Dial` nesting + `Record.action` requirement). The XML test suite currently passes (`46 passed`).

---

## Root + Top-Level Verbs

The root `Response` currently allows these top-level children:

- `Conference`
- `Dial`
- `DTMF`
- `AudioStream`
- `Gather`
- `Hangup`
- `Message`
- `Play`
- `PreAnswer`
- `Record`
- `Redirect`
- `Speak`
- `Wait`
- `MultiPartyCall`
- `Stream`

Source: `vobiz/xml/ResponseElement.py` (`_nestable`).

---

## Element Status Matrix

| Verb / Element | Status | Notes |
|---|---|---|
| `Response` | ✅ Implemented | Root element with no attributes. |
| `Speak` | ✅ Implemented | Supports SSML-style nested tags (`break`, `emphasis`, `lang`, `p`, `phoneme`, `prosody`, `s`, `say-as`, `sub`, `w`, `cont`). |
| `Play` | ✅ Implemented | `loop` supported. |
| `Dial` | ✅ Implemented | Core attrs + `Number`/`User` nesting; `confirmTimeout` wired; serialization requires at least one nested `Number` or `User`. |
| `Number` | ✅ Implemented | `sendDigits`, `sendOnPreanswer`, `sendDigitsMode`. |
| `User` | ✅ Implemented | `sendDigits`, `sendOnPreanswer`, `sipHeaders`. |
| `Gather` | ✅ Implemented | Official spec-style Gather is implemented with validations and `Speak`/`Play` nesting. |
| `Record` | ✅ Implemented | Action/callback/transcription fields implemented; `action` is required. |
| `Hangup` | ✅ Implemented | `reason`, `schedule`. |
| `Redirect` | ✅ Implemented | `method` + content URL. |
| `Wait` | ✅ Implemented | `length`, `silence`, `minSilence`, `beep`. |
| `Conference` | ✅ Implemented | Rich attribute set available. |
| `DTMF` | ✅ Implemented | `async` supported. |
| `PreAnswer` | ✅ Implemented | Supports nested `Speak`, `Play`, `Wait` only (strict spec). |
| `Stream` | ⚠️ Partial | Stream XML attrs implemented; no SDK-side WebSocket event engine (out of XML builder scope). |
| `MultiPartyCall` | ✅ Implemented | Rich attribute set with validation helpers. |
| `Message` | ✅ Implemented | Messaging verb available in XML tree. |
| `AudioStream` | ✅ Implemented | `AudioStreamElement` present and wired via `Response.add_audio_stream(...)`. |

---

## Gather (Current Behavior)

`GatherElement` is implemented with:

- Required `action` (must be fully-qualified URL)
- `method`: `GET` / `POST`
- `inputType`: `dtmf`, `speech`, `dtmf speech`
- `executionTimeout`: 5–60
- `digitEndTimeout`: `auto` or 2–10
- `speechEndTimeout`: `auto` or 2–10
- `finishOnKey`: `0-9`, `*`, `#`, `""`, `none`
- `numDigits`: 1–32
- `speechModel`: `default`, `command_and_search`, `phone_call`, `telephony`
- `hints` validation (non-empty, <= 10,000 chars)
- `language` allowlist (supported-language set)
- `interimSpeechResultsCallback` + method
- `log`, `redirect`, `profanityFilter`
- Nesting: `Speak`, `Play`

Source: `vobiz/xml/gatherElement.py`.

---

## Breaking Changes (Strict Refactor)

- `GetInputElement` and `GetDigitsElement` were removed.
- `ResponseElement.add_get_input(...)` and `ResponseElement.add_get_digits(...)` were removed.
- `RecordElement(action=...)` now requires `action` at construction.
- `ResponseElement.add_record(action=...)` now requires `action`.
- `Dial` now raises an XML error if serialized without a nested `Number`/`User`.

---

## Test Coverage Snapshot

`tests/xml` contains dedicated tests for:

- Core verbs (`Speak`, `Play`, `Dial`, `Record`, `Hangup`, `Redirect`, `Wait`, etc.)
- Gather + strict behavior coverage:
  - `test_gatherElement.py`
  - `test_responseElement.py` (builder-level wiring + Dial guard + AudioStream)
  - `test_preAnswerElement.py` (Speak/Play/Wait-only nesting)

Latest run:

- `pytest tests/xml -q`
- `46 passed`

---

## Known Gaps / Issues

1. **Runtime call-engine behavior is outside XML builder scope**
   - Things like “stop execution after Redirect”, webhook orchestration, and callback delivery/runtime semantics are not enforced inside these XML classes.

2. **`Stream` event protocol is not an SDK runtime engine**
   - XML attributes for `Stream` are present; handling WebSocket events (`playAudio`, `clearAudio`, `checkpoint`) is not implemented as a runtime component in this library.

---

## Recommended Current Usage

- Use `Gather` for new speech+DTMF flows.
- Do not use `GetInput`/`GetDigits` (removed).
- Treat `Stream` as XML declaration support; implement WebSocket event handling in your application service.
- Use `AudioStream` when your flow explicitly needs that tag.
