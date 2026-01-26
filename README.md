# CAutoGUI 🚀
**A Native High-Performance Multi-Monitor UI Automation Library.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-windows-blue)](https://www.microsoft.com/windows)
[![Language: C++](https://img.shields.io/badge/language-C++-red)](src/core.cpp)
[![Donate with USDT](https://img.shields.io/badge/Donate-USDT-green.svg?style=flat-square&logo=tether)](#-support-this-project)

CAutoGUI is a UI automation engine built for speed. Unlike other libraries that rely purely on Python, CAutoGUI uses a **custom-built C++ core** to interact directly with the Windows API and GDI, bypassing high-latency bottlenecks.

## 🌟 Key Features
- **Ultra-Fast Vision:** Image searching takes **0.09s** on average, up to 20x faster than traditional libraries.
- **DPI-Aware Captures:** Pixel-perfect accuracy even on screens with Windows scaling enabled.
- **Native Multi-Monitor Support:** Seamlessly control multiple displays using a unified coordinate system.
- **Advanced Tweening:** Professional easing functions (Bounce, Elastic, Exponential) for human-like mouse movement.
- **Compiled Efficiency:** Zero heavy dependencies like OpenCV; runs light and fast.

## 📊 Performance Benchmark (Full Screen Scan)
| Library | Search Time (Avg) | Technology |
| :--- | :--- | :--- |
| PyAutoGUI | ~1.50s - 2.10s | Pure Python / MSS |
| **CAutoGUI** | **0.09s** ⚡ | **C++ Native / GDI** |



## 🛠️ Installation

### Using Pre-compiled Wheels (Recommended)
import cautogui as pyautogui
# Use it exactly like PyAutoGUI
---

## ☕ Support this project
If CAutoGUI saved you time and improved your automation speed, consider supporting its development!

**USDT (TRC20):** `TZ9idiUf39JmSYCapp6wZEDdnpm5yJz5HX`

**USDT (ERC20):** `0x97246ff700f1504755eb329b619ebb6a6889c50d`

---