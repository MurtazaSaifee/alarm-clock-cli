# Requirements Specification: CLI Alarm Clock

## 1. Overview
A lightweight Python command-line interface (CLI) alarm clock application built for quick setup, live progress tracking, and interactive controls (pause, resume, stop).

---

## 2. Scope & Target Constraints
- **Scope**: 30-minute MVP focused strictly on core functionality.
- **Interface**: Command-line interface only (no web UI, no database, no external services).
- **Runtime**: Python 3 (macOS compatible, standard library preferred).

---

## 3. Functional Requirements (FR)

### FR-1: Alarm Creation
- The user can set an alarm using either:
  - Duration countdown (e.g., `10s`, `5m`, or numeric seconds).
  - Target time (e.g., `HH:MM` / `HH:MM:SS` 24-hour format).
- Input validation to reject past target times or invalid duration formats with clear error messages.

### FR-2: Live Progress Display
- Display the ongoing countdown in the terminal:
  - Time remaining (formatted as `HH:MM:SS`).
  - Current status (`RUNNING`, `PAUSED`, `TRIGGERED`, `STOPPED`).
- Update display at 1-second intervals without spamming terminal scroll history (in-place line update).

### FR-3: Pause and Resume
- The user can pause an active running alarm at any time via a single keypress or command.
- The user can resume a paused alarm, resuming the countdown from where it stopped.

### FR-4: Stop / Cancel
- The user can stop/cancel an active alarm at any point before completion.
- Once the alarm triggers, the user can stop the alert ringing state.

### FR-5: Alarm Alert Notification
- When the countdown reaches zero:
  - Status changes to `TRIGGERED` / `RINGING`.
  - Trigger an audible notification (terminal bell `\a` and system alert).
  - Trigger a prominent visual alert in the terminal.
  - Ringing continues until stopped or dismissed by the user.

---

## 4. Non-Functional Requirements (NFR)

- **NFR-1: Simplicity**: Minimal code footprint (< 150 lines), zero heavy external dependencies.
- **NFR-2: Responsiveness**: Keypress detection (pause/stop) should be responsive without blocking countdown updates.
- **NFR-3: Graceful Exit**: Clean termination on `Ctrl+C` or quit command, ensuring terminal settings (raw mode, cursor visibility) are restored.
- **NFR-4: Testability**: Core timer/alarm logic decoupled from terminal I/O for straightforward unit testing.
