# CLI Alarm Clock & Countdown Timer

A lightweight, zero-dependency Python CLI alarm clock and countdown timer with real-time in-place progress tracking, non-blocking single-key pause/resume/stop controls, and sound/visual alerts.

Built strictly with the Python standard library using a spec-driven and test-driven development (TDD) approach.

---

## Quickstart

### 1. Requirements
- Python 3.8+ (macOS / Linux / POSIX compatible)
- Zero external dependencies required.

### 2. Running an Alarm

#### By Duration:
```bash
# 10-second countdown
python3 main.py 10s

# 5 minutes
python3 main.py 5m

# Combined duration (1 hour and 30 minutes)
python3 main.py 1h30m

# Raw seconds
python3 main.py 60
```

#### By Clock Time (24-Hour Format):
```bash
# Alarm for 14:30 (automatically rolls over to tomorrow if time has already passed)
python3 main.py 14:30
```

#### Interactive Prompt:
If launched without arguments, you will be prompted for input:
```bash
python3 main.py
```

---

## Interactive Controls

During countdown and alarm ringing:

| Key | Action |
| :--- | :--- |
| **`Space`** or **`p`** | **Pause / Resume** countdown |
| **`s`**, **`q`**, or **`Esc`** | **Stop / Cancel** alarm |
| **Any key / `Enter`** | **Dismiss ringing alert** when alarm goes off |
| **`Ctrl+C`** | Clean exit with terminal settings restored |

---

## Running Tests

Execute the full automated test suite:
```bash
python3 -m unittest discover tests
```

---

## Specifications & Documentation
- [`requirements.md`](requirements.md): Functional and non-functional requirements.
- [`design.md`](design.md): Architecture, state machine, and event loop design.
- [`task.md`](task.md): Phased implementation and TDD task breakdown.
