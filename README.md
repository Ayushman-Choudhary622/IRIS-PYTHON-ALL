# 👁️ Project IRIS // Universal Python & Assistive Wearable Suite

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-00f0ff?style=for-the-badge&logo=github)](https://ayushman-choudhary622.github.io/IRIS-PYTHON-ALL/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OS Windows](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-00ff88?style=for-the-badge)](LICENSE)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-478%20Landmarks-FF6F00?style=for-the-badge&logo=google)](https://mediapipe.dev)

> **Next-Generation Hands-Free Cursor Control, Computer Vision Eye Clicker, Quantum Dwell Hover-Lock Engine, and Assistive Wearable Ecosystem.**  
> *Engineered by Ayushman Choudhary for individuals with ALS, Locked-In Syndrome, and severe motor paralysis.*

---

## 🌐 Live Web Showcase & Deployments

- 🚀 **Master Ecosystem Portal (GitHub Pages)**: [https://ayushman-choudhary622.github.io/IRIS-PYTHON-ALL/](https://ayushman-choudhary622.github.io/IRIS-PYTHON-ALL/)
- 🌐 **Flagship 3D Motion Web App**: [Live 3D Motion Interface](https://ayushman-choudhary622.github.io/IRIS-PYTHON-ALL/IRIS%20WEBSITE%20FINALE/index.html)
- 📊 **Interactive Kiosk Slide Deck**: [Interactive Presentation Viewer](https://ayushman-choudhary622.github.io/IRIS-PYTHON-ALL/IRIS%20KIOSK%20PPT/preview_deck.html)

---

## 📁 Repository Directory Structure

```plaintext
IRIS-PYTHON-ALL/
├── index.html                   # Master GitHub Pages Ecosystem Portal & Interactive Showcase
├── README.md                    # Universal Repository Documentation & Guides
├── .gitignore                   # Optimized exclusions (.venv, node_modules, caches)
├── .github/workflows/pages.yml  # Automated GitHub Actions deployment to GitHub Pages
│
├── 📂 IRIS EYE PYTHON/          # Computer Vision Blink-to-Click Mouse Controller
│   ├── eye_clicker.py           # Multi-pass illumination & rotation-invariant blink engine
│   ├── run_eye_clicker.bat      # Instant UTF-8 one-click Windows launcher
│   ├── test_all_samples.py      # Automated benchmark suite against 20+ challenging lighting conditions
│   ├── iris_config.json         # Real-time sensitivity & calibration settings
│   └── IRIS ASCII ART/          # Bundled Ultra-HD console branding
│
├── 📂 IRIS AUTO BUTTON CLICK/   # Quantum Hover-Lock & Assistive Dwell Auto-Clicker v3.4
│   ├── iris_autoclicker.py      # Dwell-lock engine with escalating radar alarm & reticle HUD
│   ├── RUN_IRIS_AUTOCLICKER.bat # Automated launcher with UTF-8 console output
│   ├── demo_target_app.bat      # Built-in target test harness for validating clicks
│   └── README.md                # Dedicated user & hotkey manual
│
├── 📂 IRIS 3 SEC AUTO/          # Universal Background 3-Second Auto Clicker
│   ├── autoclicker.py           # Full-featured GUI auto-clicker (Win32 ctypes zero-dependency)
│   ├── cli_clicker.py           # Headless lightweight terminal clicker
│   ├── run.bat                  # One-click GUI runner
│   ├── run_cli.bat              # One-click CLI runner
│   └── README.md                # Quick-start configuration guide
│
├── 📂 IRIS ASCII ART/           # Ultra-HD Braille Vector Branding Studio
│   ├── iris_ascii.py            # 8x subpixel vector Braille TrueColor ANSI generator
│   ├── SHOW_LOGO.bat            # Instant large-format logo display
│   ├── RUN_IRIS_ASCII.bat       # Interactive multi-theme gallery browser
│   ├── braille_art.json         # Precomputed vector character matrices
│   └── example_usage.py         # Code snippets showing how to import into Python apps
│
├── 📂 IRIS KIOSK PPT/           # 3-Minute Morph Automated Presentation & Web Previewer
│   ├── generate_kiosk_ppt.py    # Automated PowerPoint deck generator via python-pptx
│   ├── preview_deck.html        # Interactive browser-based slide deck viewer
│   ├── IRIS_Kiosk_3Min_Morph.pptx # Primary kiosk deck for conferences & exhibitions
│   └── slide_previews/          # Pre-rendered slide preview assets
│
├── 📂 IRIS WEBSITE FINALE/      # Flagship 3D Motion Web Application
│   ├── index.html               # Dual-theme turntable web app
│   ├── styles.css               # Glassmorphic sci-fi stylesheet
│   ├── app.js                   # Scrubbing logic, Web Audio SFX & preloader
│   ├── frames_dark_opt/         # Optimized dark-mode turntable WebP frames
│   └── frames_light_opt/        # Optimized light-mode turntable WebP frames
│
├── 📂 IRIS UNIVERSAL/           # Next.js AI Assistive Universal Web App
├── 📂 IRIS ASSETS/              # Master branding, high-res logos & media
└── 📂 IRIS HEADBAND/            # Hardware headband 3D models & sensor schematics
```

---

## ⚡ Quick Start & Installation

### 1. Clone Repository
```bash
git clone https://github.com/Ayushman-Choudhary622/IRIS-PYTHON-ALL.git
cd IRIS-PYTHON-ALL
```

### 2. Install Python Dependencies
```bash
pip install opencv-python mediapipe pyautogui numpy python-pptx
```

---

## 🎮 Applications & Hotkey Reference

### 1. IRIS Eye Blink Clicker (`IRIS EYE PYTHON`)
```bash
cd "IRIS EYE PYTHON"
run_eye_clicker.bat
```
| Key | Action |
|:---:|:---|
| `W` | Toggle Camera Feed vs. Plain White Canvas Eye (Zero Distraction) |
| `E` | Cycle Eye Tracking Mode (Right Primary ➔ Binocular Mean ➔ Auto ➔ Left) |
| `1` | Multi-Pass Auto Lighting (Natural ➔ Shadow Lift ➔ High Gain ➔ Glare Pierce) |
| `2` | Force Glare Pierce (Blue-Cut lenses & intense reflections) |
| `3` | Force Backlight Max (Dark silhouette rooms) |
| `C` | Run 3.5-second Guided Calibration |
| `M` | Toggle Mouse Left Click dispatch ON / OFF |
| `+` / `-` | Increase / Decrease Blink Sensitivity Cutoff |
| `R` | Reset Baseline & Pose Normalization |
| `Q` | Exit Application |

---

### 2. Quantum Hover-Lock & Auto-Clicker (`IRIS AUTO BUTTON CLICK`)
```bash
cd "IRIS AUTO BUTTON CLICK"
RUN_IRIS_AUTOCLICKER.bat
```
| Key | Action |
|:---:|:---|
| `F6` | Toggle Sci-Fi Cursor Circle / Sphere HUD Overlay ON / OFF |
| `F7` | Toggle Audio Alarm Mode (Full Radar Beeps ➔ Click Chime Only ➔ Silent Mute) |
| `F8` | Global Pause / Resume Auto-Click Engine |
| `F9` | Emergency Discard / Clear Active Dwell Target |

---

### 3. Universal 3-Second Auto Clicker (`IRIS 3 SEC AUTO`)
```bash
cd "IRIS 3 SEC AUTO"
run.bat        # Launches Tkinter GUI mode
run_cli.bat    # Launches Minimalist Terminal CLI mode
```
- Custom interval from `0.01s` (10ms) up to `3600s` (1 hour)
- Anti-detection humanized cursor jitter
- Global `F6` Start/Pause, `F7` Coordinate Picker, `ESC` Emergency Stop

---

### 4. Ultra-HD Braille & ASCII Art Studio (`IRIS ASCII ART`)
```bash
cd "IRIS ASCII ART"
SHOW_LOGO.bat       # Displays full banner in current terminal
RUN_IRIS_ASCII.bat  # Launches interactive theme selector
```
- Available Themes: `iris` (Neon Cyan), `claude` (Warm Coral), `cyberpunk` (Cyan/Magenta), `matrix` (Green), `gold` (Cyber Luxury), `original` (Navy/Cyan).

---

## 🔬 Clinical & Engineering Innovations

1. **Multi-Pass Auto Shadow Lift**: Eliminates false blinks in extreme backlit environments and dimly lit rooms.
2. **Rotation-Invariant 3D Eye Aspect Ratio (EAR)**: Computes eye openness in head-local coordinates, eliminating tilt/yaw blink failures.
3. **5-Frame Anti-Jitter Smoothing**: Discards single-frame camera sensor noise spikes, preventing accidental click triggers.
4. **Click-Through Holographic HUD**: Reticle overlay utilizes Windows `WS_EX_TRANSPARENT` so clicks pass unobstructed to native application buttons.
5. **Ultra-Low Latency Dispatch**: Direct Windows kernel user32 ctypes invocation (< 0.05ms dispatch overhead).

---

## 👨‍💻 Author & Contact

**Ayushman Choudhary**  
Lead Developer & Inventor, Project IRIS  
- GitHub: [@Ayushman-Choudhary622](https://github.com/Ayushman-Choudhary622)  
- Repository: [IRIS-PYTHON-ALL](https://github.com/Ayushman-Choudhary622/IRIS-PYTHON-ALL)  

---

## 📄 License
This project is open-source under the [MIT License](LICENSE). Built for accessibility, human empowerment, and independence.
