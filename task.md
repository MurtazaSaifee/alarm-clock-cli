# Implementation Tasks: CLI Alarm Clock

## Phase 1: Core Logic & Unit Tests (PR #1: Engine & Parser)
*Goal: Implement decoupled, fully tested duration parsing and state engine using TDD.*

- [x] **Task 1.1: Unit tests for time & duration parser**
  - Commit: `test: add unit tests for duration and target time parsing`
  - File: `tests/test_parser.py`
  - Covers: relative durations (`10s`, `5m`, `1h`, `90`), target times (`HH:MM`), invalid format exceptions, past time handling.

- [x] **Task 1.2: Implement time & duration parser**
  - Commit: `feat: implement parse_target_seconds`
  - File: `alarm_clock/parser.py`
  - Verifies: `test_parser.py` passes.

- [x] **Task 1.3: Unit tests for AlarmEngine state machine**
  - Commit: `test: add unit tests for AlarmEngine state transitions`
  - File: `tests/test_engine.py`
  - Covers: `READY` -> `RUNNING` -> `PAUSED` -> `RUNNING` -> `RINGING` -> `STOPPED`, monotonic time delta calculation.

- [x] **Task 1.4: Implement AlarmEngine**
  - Commit: `feat: implement AlarmEngine state machine and monotonic clock ticker`
  - File: `alarm_clock/engine.py`
  - Verifies: `test_engine.py` passes.

---

## Phase 2: Terminal UI & Event Loop (PR #2: Interactive CLI)
*Goal: Integrate non-blocking keyboard listener, ANSI in-place renderer, and main event loop.*

- [x] **Task 2.1: Implement TerminalController**
  - Commit: `feat: add TerminalController with cbreak mode and ANSI rendering`
  - File: `alarm_clock/terminal.py`
  - Covers: `tty.setcbreak`, `termios` setup/restoration, `atexit` hook, formatting `HH:MM:SS`, bell sound `\a`.

- [x] **Task 2.2: Implement main event loop and CLI entrypoint**
  - Commit: `feat: implement main event loop and CLI entrypoint`
  - File: `main.py`
  - Connects: `parser.py`, `engine.py`, `terminal.py` via `select.select` non-blocking loop (0.1s tick).

- [x] **Task 2.3: Add integration tests for CLI loop & argument parsing**
  - Commit: `test: add integration tests for CLI lifecycle and keyboard actions`
  - File: `tests/test_integration.py`
  - Verifies: CLI starts, handles interactive actions, cleans up on completion.

---

## Phase 3: E2E Verification & Delivery (PR #3: Verification & Polish)
*Goal: End-to-end verification, all tests passing, ready to use.*

- [ ] **Task 3.1: Execute full test suite**
  - Commit: `chore: verify test suite passes 100%`
  - Command: `python3 -m unittest discover tests`

- [ ] **Task 3.2: E2E verification & Quickstart documentation**
  - Commit: `docs: add quickstart guide to README.md`
  - File: `README.md`
  - Verifies: Live run with `python3 main.py 3s` to verify countdown, ringing, and dismissal.
