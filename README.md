# CAutoGUI (by danckard)

High-performance GUI automation library. A C++ powered drop-in replacement for PyAutoGUI.

## Goal
To provide the same API as PyAutoGUI but with near-zero latency by executing the core logic in native C++ and (eventually) x86_64 Assembly.

## Features (In progress)
- [ ] Native Screen Capture (Win32/X11)
- [ ] C++ Template Matching
- [ ] Zero-copy memory buffer handling
- [ ] No third-party dependencies

## How to use
```python
import cautogui as pyautogui
# Use it exactly like PyAutoGUI