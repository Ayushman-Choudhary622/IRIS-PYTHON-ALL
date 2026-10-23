# ⚡ IRIS // QUANTUM HOVER-LOCK & AUTO-CLICK SYSTEM v3.4

An ultra-futuristic, assistive hover-to-click & dwell targeting engine built with Python and native Windows Win32 API, featuring Ultra-HD Braille/ASCII branding art on startup.

---

## 🌟 Key Features

1. **Optional Cursor Circle / Sphere Overlay (Toggle On/Off)**:
   - **Press `F6`** anywhere in Windows to instantly **show or hide the circle/sphere** around your cursor!
   - Or click **`[🎯 CIRCLE ON (F6)]` / `[🚫 NO CIRCLE (F6)]`** in the top bar.
   - Or uncheck **`☑ Show Circle / Sphere around cursor`** in the settings.
   - **Clean Mode**: When turned off, the screen has **ZERO visual circles or rings** around your cursor — only the escalating radar alarm sounds, the GUI progress bar tracks the hold, and the hardware click fires at 2.0s!

2. **Ultra-HD IRIS ASCII / Braille Art Startup Banner**:
   - Automatically renders the glowing, 24-bit TrueColor Ultra-HD Braille & ASCII IRIS Logo from the `IRIS ASCII ART` folder with scanline reveal animation when starting!
   - In-app **`[👁 SHOW ASCII LOGO]`** button to view the ASCII logo directly inside a dedicated GUI modal at any time.

3. **Stationary Dwell Lock (Auto-Click on Hover)**:
   - Move your mouse cursor over **ANY button** or screen element.
   - Hold your cursor still on the target — the system immediately acquires lock!
   - Real-time **2.0-second countdown** (customizable from 0.5s to 4.0s).
   - Automatically executes a **Hardware Click** at the 2.0s mark.

4. **Audio Modes & Instant Silent / Mute Option**:
   - **`🔊 Full Beeps`**: Escalating multi-stage radar alarm (650Hz → 2400Hz) + click confirmation chime.
   - **`🔔 Click Only`**: Silent during hover countdown, sounds subtle chime when clicked.
   - **`🔇 Silent (Mute)`**: **100% silent stealth mode** with zero beeps and zero chimes.
   - **Global Mute Hotkey**: Press **`F7`** anywhere in Windows to instantly toggle between Sound and Silent Mode.
   - **Top-Bar Button**: Click **`[🔊 SOUND ON (F7)]` / `[🔇 SILENT (F7)]`** on the interface.

5. **Global Pause & Resume System**:
   - Press **`F8`** anywhere in Windows to instantly **PAUSE** or **RESUME** the auto-clicker.
   - Press **`F9`** for emergency target lock cancellation.

6. **Integrated Batch File Runner**:
   - Browse and select **ANY `.bat` file** from your computer.
   - Click **`⚡ RUN BATCH FILE NOW`** to launch the batch file alongside the auto-clicker.
   - Includes sample **`demo_target_app.bat`** for immediate testing!

7. **In-App Click Target Test Pad**:
   - Hover over `TEST BUTTON A` or `TEST BUTTON B` inside the application to see the real click counter in action!

---

## 🚀 Quick Start (1-Click Run)

Simply double-click:
```bat
RUN_IRIS_AUTOCLICKER.bat
```
Or run via terminal:
```bash
python iris_autoclicker.py
```

---

## ⌨️ Controls & Hotkeys

| Action | Control / Hotkey | Description |
| :--- | :--- | :--- |
| **Cursor Circle On/Off**| **`F6`** (Global) | Turn ON / OFF the circle / sphere overlay around mouse |
| **Mute / Silent Mode** | **`F7`** (Global) | Instantly mute all sounds / unmute anywhere in Windows |
| **Pause / Resume** | **`F8`** (Global) | Toggles the engine on/off anywhere in Windows |
| **Emergency Cancel**| **`F9`** (Global) | Discards current target lock immediately |
| **Hold Time** | **Slider (0.5s - 4.0s)** | Adjust the dwell hold duration (Default: 2.0s) |
| **Jitter Tolerance**| **Slider (12px - 60px)** | Adjust mouse tremor sensitivity (Default: 28px) |
| **Audio Alarm Mode**| **Radio Buttons** | Select between Full Beeps, Click Only, or Silent |
| **Click Mode** | **Radio Buttons** | Switch between Left Click, Double Click, Right Click |
| **Batch Runner** | **[Browse] + [Run]** | Launch any custom `.bat` application |
| **ASCII Art Viewer** | **[👁 SHOW ASCII LOGO]** | View Ultra-HD Braille branding logo in GUI |
