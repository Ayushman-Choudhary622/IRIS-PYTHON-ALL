"""
================================================================================
  IRIS // QUANTUM HOVER-LOCK & AUTO-CLICK SYSTEM v3.4
  Assistive Dwell-Lock, Escalating Audio Radar Alarm & Futuristic HUD Engine
  Features:
    - Hardware Auto-Click
    - Optional Cursor Circle / Sphere Overlay (Toggle On/Off with F6)
    - Full Audio Radar / Click Chime / Silent Mode (Toggle with F7)
    - Global Pause / Resume (Toggle with F8)
    - Emergency Lock Discard (F9)
    - Ultra-HD IRIS ASCII Art Branding on Startup
================================================================================
"""

import sys
import os
import re
import time
import math
import threading
import queue
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ctypes
from ctypes import wintypes

# Enable UTF-8 & ANSI parsing on Windows CMD / PowerShell
if sys.platform == "win32":
    os.system("")
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Import the IRIS ASCII ART module from folder
ascii_art_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IRIS ASCII ART")
if os.path.exists(ascii_art_dir) and ascii_art_dir not in sys.path:
    sys.path.insert(0, ascii_art_dir)

try:
    from iris_ascii import print_iris_logo, get_iris_logo, stream_iris_logo, BRAILLE_ART
    HAS_IRIS_ASCII = True
except Exception as e:
    HAS_IRIS_ASCII = False
    print(f"[Warning] IRIS ASCII Art module notice: {e}")

# Import PyAutoGUI for bulletproof OS-level mouse clicking
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.01
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# Windows Mouse Event Constants
MOUSEEVENTF_MOVE       = 0x0001
MOUSEEVENTF_LEFTDOWN   = 0x0002
MOUSEEVENTF_LEFTUP     = 0x0004
MOUSEEVENTF_RIGHTDOWN  = 0x0008
MOUSEEVENTF_RIGHTUP    = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP   = 0x0040
MOUSEEVENTF_ABSOLUTE   = 0x8000

# Extended Window Styles for Click-Through Transparency
GWL_EXSTYLE       = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED     = 0x00080000
WS_EX_NOACTIVATE  = 0x08000000
WS_EX_TOOLWINDOW  = 0x00000080

# Virtual Keys
VK_F6 = 0x75  # F6 key for Cursor Circle / Sphere HUD toggle
VK_F7 = 0x76  # F7 key for global Mute / Silent Mode toggle
VK_F8 = 0x77  # F8 key for global Pause/Resume toggle
VK_F9 = 0x78  # F9 key for emergency reset

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_mouse_pos():
    """Returns the current mouse coordinates (x, y) using Win32 API."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return int(pt.x), int(pt.y)


def trigger_hardware_click(x=None, y=None, click_type="left"):
    """
    Dispatches a real OS-level mouse click.
    Uses PyAutoGUI if available with fallback to Win32 normalized mouse_event.
    """
    if x is None or y is None:
        x, y = get_mouse_pos()

    # Strategy 1: PyAutoGUI (Most reliable across Windows 10/11)
    if HAS_PYAUTOGUI:
        try:
            if click_type == "left":
                pyautogui.click(x=x, y=y)
            elif click_type == "double":
                pyautogui.doubleClick(x=x, y=y)
            elif click_type == "right":
                pyautogui.rightClick(x=x, y=y)
            elif click_type == "middle":
                pyautogui.middleClick(x=x, y=y)
            return True
        except Exception as e:
            print("[PyAutoGUI fallback trigger]", e)

    # Strategy 2: Win32 Normalized Absolute Mouse Event
    try:
        screen_w = max(1, ctypes.windll.user32.GetSystemMetrics(0))
        screen_h = max(1, ctypes.windll.user32.GetSystemMetrics(1))
        norm_x = int(x * 65535 / (screen_w - 1))
        norm_y = int(y * 65535 / (screen_h - 1))

        # Position cursor firmly at target coordinates
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, norm_x, norm_y, 0, 0)
        time.sleep(0.02)

        if click_type == "left":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.04)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif click_type == "double":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.03)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.06)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.03)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif click_type == "right":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.04)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif click_type == "middle":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.04)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
        return True
    except Exception as e:
        print("[Win32 Click Error]", e)
        return False


class SoundRadarEngine:
    """Asynchronous escalating audio radar alarm thread with instant mute capability."""
    def __init__(self):
        self.queue = queue.Queue()
        self.enabled = True
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def play_beep(self, freq, duration_ms):
        if not self.enabled or not HAS_WINSOUND:
            return
        if self.queue.qsize() < 3:
            self.queue.put(("beep", int(freq), int(duration_ms)))

    def play_click_chime(self):
        if not self.enabled or not HAS_WINSOUND:
            return
        self.queue.put(("chime", 0, 0))

    def flush(self):
        """Immediately discard pending beeps when mouse moves away or when muted."""
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break

    def _worker(self):
        while self.running:
            try:
                item = self.queue.get(timeout=0.2)
                if not self.enabled:
                    self.queue.task_done()
                    continue
                if item[0] == "beep":
                    _, freq, duration = item
                    winsound.Beep(max(37, min(32767, freq)), max(10, duration))
                elif item[0] == "chime":
                    winsound.Beep(2600, 35)
                    winsound.Beep(3400, 70)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                pass


class ReticleHUD:
    """
    Futuristic circular sci-fi holographic reticle that floats
    with 100% click-through transparency over the cursor during dwell countdown.
    Can be completely disabled/hidden based on user preference.
    """
    SIZE = 120
    HALF_SIZE = 60
    TRANS_COLOR = "#000001"

    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.overrideredirect(True)
        self.top.attributes("-topmost", True)
        self.top.wm_attributes("-transparentcolor", self.TRANS_COLOR)
        self.top.withdraw()

        # Canvas for sci-fi HUD graphics
        self.canvas = tk.Canvas(
            self.top,
            width=self.SIZE,
            height=self.SIZE,
            bg=self.TRANS_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.visible = False

        # Apply Windows Click-Through Style so mouse clicks NEVER get blocked
        self.top.update_idletasks()
        self._apply_click_through()

    def _apply_click_through(self):
        """Applies WS_EX_TRANSPARENT so mouse clicks pass through completely to buttons underneath."""
        try:
            hwnd = self.top.winfo_id()
            parent = ctypes.windll.user32.GetParent(hwnd)
            target_hwnd = parent if parent else hwnd
            style = ctypes.windll.user32.GetWindowLongW(target_hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(
                target_hwnd,
                GWL_EXSTYLE,
                style | WS_EX_TRANSPARENT | WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW
            )
        except Exception as e:
            print("[Reticle Click-Through Warning]", e)

    def show(self, x, y, progress, time_left, is_silent=False):
        """Updates reticle position and draws holographic charging arc."""
        px = int(x - self.HALF_SIZE)
        py = int(y - self.HALF_SIZE)
        self.top.geometry(f"{self.SIZE}x{self.SIZE}+{px}+{py}")

        if not self.visible:
            self.top.deiconify()
            self._apply_click_through()
            self.visible = True

        self.canvas.delete("all")
        cx, cy = self.HALF_SIZE, self.HALF_SIZE

        # Dynamic color shift
        if is_silent:
            ring_color = "#38bdf8"
            glow_color = "#075985"
        elif progress < 0.4:
            ring_color = "#00f0ff"
            glow_color = "#004466"
        elif progress < 0.75:
            ring_color = "#00ff88"
            glow_color = "#006633"
        elif progress < 0.95:
            ring_color = "#ffdd00"
            glow_color = "#776600"
        else:
            ring_color = "#ff2266"
            glow_color = "#880022"

        # Outer sci-fi target bracket marks
        r_outer = 48
        bracket_len = 12
        for angle_deg in [45, 135, 225, 315]:
            rad = math.radians(angle_deg)
            bx = cx + r_outer * math.cos(rad)
            by = cy + r_outer * math.sin(rad)
            self.canvas.create_line(
                bx, by,
                bx - bracket_len * math.cos(rad),
                by - bracket_len * math.sin(rad),
                fill=ring_color, width=2
            )

        # Orbit guide circle
        self.canvas.create_oval(
            cx - 36, cy - 36, cx + 36, cy + 36,
            outline=glow_color, width=1, dash=(3, 3)
        )

        # Center target dot
        self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=ring_color, outline="")

        # Charging Radial Arc (0 to 359 degrees)
        extent = max(1, min(359, int(progress * 359)))
        self.canvas.create_arc(
            cx - 34, cy - 34, cx + 34, cy + 34,
            start=90,
            extent=-extent,
            outline=ring_color,
            width=4,
            style=tk.ARC
        )

        # Floating countdown tag
        suffix = " [MUTE]" if is_silent else ""
        status_txt = f"{time_left:0.1f}s{suffix}" if time_left > 0.05 else "CLICKING"
        self.canvas.create_text(
            cx, cy + 42,
            text=status_txt,
            fill=ring_color,
            font=("Consolas", 8, "bold")
        )

    def hide(self):
        """Instantly hides the reticle so the screen underneath is 100% unobstructed."""
        if self.visible:
            self.top.withdraw()
            self.visible = False


class IrisAutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IRIS // QUANTUM HOVER-LOCK & AUTO-CLICK SYSTEM v3.4")
        self.root.geometry("640x820")
        self.root.minsize(600, 750)
        self.root.configure(bg="#080b14")

        # System State
        self.is_running = True        # Master engine running switch
        self.is_paused = False        # Paused by user / hotkey
        self.dwell_time = 2.0         # Target hold time in seconds
        self.jitter_radius = 28       # Cursor movement sensitivity (28px)
        self.click_type = "left"      # left, double, right, middle
        self.total_clicks_count = 0   # Total clicks dispatched

        # Visual Reticle Display Option (User can turn off the circle/sphere around cursor)
        self.show_reticle_var = tk.BooleanVar(value=True)

        # Audio System State (full, chime_only, silent)
        self.sound_mode = "full"      # "full" = Radar beeps + click chime, "chime_only" = Click chime only, "silent" = Muted
        self.sound_enabled = True

        # Dwell Tracker Internals
        self.anchor_x = None
        self.anchor_y = None
        self.dwell_start_time = None
        self.last_beep_stage = -1
        self.click_cooldown_until = 0.0
        self.selected_batch_path = tk.StringVar(value="")

        # Setup Audio & Reticle HUD
        self.audio = SoundRadarEngine()
        self.reticle = ReticleHUD(self.root)

        # Style & Fonts
        self._setup_styles()
        self._build_gui()

        # Start Global Hotkey Listener (F6 = Circle On/Off, F7 = Mute/Silent, F8 = Pause/Resume, F9 = Reset)
        self.hotkey_thread = threading.Thread(target=self._hotkey_listener, daemon=True)
        self.hotkey_thread.start()

        # Start Main Engine Loop (runs at ~50 Hz inside Tkinter event loop)
        self.root.after(20, self._engine_tick)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar",
                        thickness=14,
                        troughcolor="#0f1526",
                        background="#00f0ff")

    def _build_gui(self):
        # ---------------- HEADER BANNER ----------------
        header_frame = tk.Frame(self.root, bg="#0d1322", highlightbackground="#00f0ff", highlightthickness=1)
        header_frame.pack(fill="x", padx=16, pady=(14, 6))

        h_top_row = tk.Frame(header_frame, bg="#0d1322")
        h_top_row.pack(fill="x", padx=14, pady=(8, 2))

        title_lbl = tk.Label(
            h_top_row,
            text="⚡ IRIS // QUANTUM AUTO-CLICK ENGINE v3.4",
            font=("Consolas", 13, "bold"),
            fg="#00f0ff",
            bg="#0d1322"
        )
        title_lbl.pack(side="left")

        # SHOW ASCII LOGO BUTTON IN HEADER
        ascii_btn = tk.Button(
            h_top_row,
            text="👁 SHOW ASCII LOGO",
            font=("Segoe UI", 8, "bold"),
            bg="#162035",
            fg="#38bdf8",
            activebackground="#0284c7",
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.open_ascii_viewer
        )
        ascii_btn.pack(side="right")

        sub_lbl = tk.Label(
            header_frame,
            text="Hover over ANY button → Escalating radar alarm → Real Hardware Click at 2.0s",
            font=("Segoe UI", 9),
            fg="#7aa2d6",
            bg="#0d1322"
        )
        sub_lbl.pack(anchor="w", padx=14, pady=(0, 8))

        # ---------------- STATUS & MASTER CONTROLS ----------------
        status_card = tk.Frame(self.root, bg="#0d1322", highlightbackground="#1b253d", highlightthickness=1)
        status_card.pack(fill="x", padx=16, pady=4)

        stat_row = tk.Frame(status_card, bg="#0d1322")
        stat_row.pack(fill="x", padx=14, pady=10)

        tk.Label(stat_row, text="STATUS:", font=("Consolas", 10, "bold"), fg="#8899bb", bg="#0d1322").pack(side="left")

        self.status_badge = tk.Label(
            stat_row,
            text="[ ● ARMED & ACTIVE ]",
            font=("Consolas", 11, "bold"),
            fg="#00ff88",
            bg="#0a2a1b",
            padx=8,
            pady=3,
            highlightbackground="#00ff88",
            highlightthickness=1
        )
        self.status_badge.pack(side="left", padx=8)

        # RETICLE CIRCLE TOGGLE BUTTON (USER REQUEST)
        self.reticle_btn = tk.Button(
            stat_row,
            text="🎯 CIRCLE ON (F6)",
            font=("Consolas", 9, "bold"),
            bg="#162035",
            fg="#00f0ff",
            activebackground="#0284c7",
            activeforeground="#ffffff",
            bd=0,
            padx=9,
            pady=4,
            cursor="hand2",
            highlightbackground="#00f0ff",
            highlightthickness=1,
            command=self.toggle_reticle
        )
        self.reticle_btn.pack(side="right", padx=(6, 0))

        # QUICK MUTE / SILENT TOGGLE BUTTON
        self.mute_btn = tk.Button(
            stat_row,
            text="🔊 SOUND ON (F7)",
            font=("Consolas", 9, "bold"),
            bg="#0d2818",
            fg="#00ff88",
            activebackground="#144226",
            activeforeground="#ffffff",
            bd=0,
            padx=9,
            pady=4,
            cursor="hand2",
            highlightbackground="#00ff88",
            highlightthickness=1,
            command=self.toggle_mute
        )
        self.mute_btn.pack(side="right", padx=(6, 0))

        # PAUSE / RESUME BUTTON
        self.pause_btn = tk.Button(
            stat_row,
            text="⏸ PAUSE (F8)",
            font=("Consolas", 9, "bold"),
            bg="#162035",
            fg="#ffdd00",
            activebackground="#2a3b5c",
            activeforeground="#ffffff",
            bd=0,
            padx=9,
            pady=4,
            cursor="hand2",
            highlightbackground="#ffdd00",
            highlightthickness=1,
            command=self.toggle_pause
        )
        self.pause_btn.pack(side="right")

        # ---------------- BATCH FILE LAUNCHER ----------------
        batch_card = tk.Frame(self.root, bg="#0d1322", highlightbackground="#8a2be2", highlightthickness=1)
        batch_card.pack(fill="x", padx=16, pady=4)

        b_hdr = tk.Frame(batch_card, bg="#0d1322")
        b_hdr.pack(fill="x", padx=14, pady=(8, 2))
        tk.Label(b_hdr, text="🚀 BATCH LAUNCHER // ONE-CLICK RUNNER", font=("Consolas", 10, "bold"), fg="#c084fc", bg="#0d1322").pack(side="left")
        tk.Label(b_hdr, text="Launch batch file with auto-clicker", font=("Segoe UI", 8), fg="#71717a", bg="#0d1322").pack(side="right")

        b_input_row = tk.Frame(batch_card, bg="#0d1322")
        b_input_row.pack(fill="x", padx=14, pady=4)

        self.batch_entry = tk.Entry(
            b_input_row,
            textvariable=self.selected_batch_path,
            font=("Consolas", 9),
            bg="#080b14",
            fg="#00f0ff",
            insertbackground="#00f0ff",
            bd=1,
            relief="solid"
        )
        self.batch_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=3)

        browse_btn = tk.Button(
            b_input_row,
            text="📁 Browse .bat",
            font=("Segoe UI", 9, "bold"),
            bg="#1e1b4b",
            fg="#c084fc",
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.browse_batch_file
        )
        browse_btn.pack(side="right")

        b_act_row = tk.Frame(batch_card, bg="#0d1322")
        b_act_row.pack(fill="x", padx=14, pady=(2, 8))

        run_bat_btn = tk.Button(
            b_act_row,
            text="⚡ RUN BATCH FILE NOW",
            font=("Consolas", 10, "bold"),
            bg="#4c1d95",
            fg="#ffffff",
            activebackground="#6d28d9",
            bd=0,
            padx=16,
            pady=5,
            cursor="hand2",
            highlightbackground="#a855f7",
            highlightthickness=1,
            command=self.run_selected_batch
        )
        run_bat_btn.pack(side="left")

        demo_bat_btn = tk.Button(
            b_act_row,
            text="🎯 Launch Demo Test App",
            font=("Segoe UI", 9),
            bg="#162035",
            fg="#7aa2d6",
            bd=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.launch_demo_app
        )
        demo_bat_btn.pack(side="right")

        # ---------------- RADAR & TELEMETRY DISPLAY ----------------
        telemetry_card = tk.Frame(self.root, bg="#0d1322", highlightbackground="#1b253d", highlightthickness=1)
        telemetry_card.pack(fill="x", padx=16, pady=4)

        t_row = tk.Frame(telemetry_card, bg="#0d1322")
        t_row.pack(fill="x", padx=14, pady=(8, 2))

        self.coords_lbl = tk.Label(
            t_row,
            text="CURSOR: X: 0000 | Y: 0000",
            font=("Consolas", 10, "bold"),
            fg="#00f0ff",
            bg="#0d1322"
        )
        self.coords_lbl.pack(side="left")

        self.clicks_counter_lbl = tk.Label(
            t_row,
            text="CLICKS DELIVERED: 0",
            font=("Consolas", 10, "bold"),
            fg="#00ff88",
            bg="#0d1322"
        )
        self.clicks_counter_lbl.pack(side="right")

        self.target_state_lbl = tk.Label(
            telemetry_card,
            text="STATE: IDLE SCANNING",
            font=("Consolas", 10, "bold"),
            fg="#7aa2d6",
            bg="#0d1322"
        )
        self.target_state_lbl.pack(anchor="w", padx=14, pady=(2, 2))

        # Progress bar representing dwell countdown (0 to 100%)
        self.progress_var = tk.DoubleVar(value=0.0)
        self.prog_bar = ttk.Progressbar(
            telemetry_card,
            variable=self.progress_var,
            maximum=100.0,
            style="TProgressbar"
        )
        self.prog_bar.pack(fill="x", padx=14, pady=(4, 2))

        self.prog_text_lbl = tk.Label(
            telemetry_card,
            text="Hold cursor still over any button for 2.0s to lock and trigger click",
            font=("Segoe UI", 8),
            fg="#5577aa",
            bg="#0d1322"
        )
        self.prog_text_lbl.pack(padx=14, pady=(0, 8))

        # ---------------- SETTINGS & CONFIGURATION ----------------
        settings_card = tk.Frame(self.root, bg="#0d1322", highlightbackground="#1b253d", highlightthickness=1)
        settings_card.pack(fill="x", padx=16, pady=4)

        tk.Label(
            settings_card,
            text="⚙️ ENGINE & DISPLAY CONFIGURATION",
            font=("Consolas", 10, "bold"),
            fg="#8899bb",
            bg="#0d1322"
        ).pack(anchor="w", padx=14, pady=(8, 2))

        # Dwell Time Slider (Default: 2.0s)
        dwell_row = tk.Frame(settings_card, bg="#0d1322")
        dwell_row.pack(fill="x", padx=14, pady=2)
        tk.Label(dwell_row, text="Dwell Hold Time:", font=("Segoe UI", 9), fg="#ccddee", bg="#0d1322").pack(side="left")
        self.dwell_val_lbl = tk.Label(dwell_row, text="2.00 s", font=("Consolas", 10, "bold"), fg="#00f0ff", bg="#0d1322")
        self.dwell_val_lbl.pack(side="right")

        self.dwell_slider = tk.Scale(
            settings_card,
            from_=0.5,
            to=4.0,
            resolution=0.1,
            orient="horizontal",
            bg="#0d1322",
            fg="#00f0ff",
            highlightthickness=0,
            troughcolor="#080b14",
            activebackground="#00f0ff",
            showvalue=False,
            command=self._on_dwell_slider_change
        )
        self.dwell_slider.set(2.0)
        self.dwell_slider.pack(fill="x", padx=14, pady=(0, 4))

        # Jitter Sensitivity Radius Slider (Default: 28px)
        jitter_row = tk.Frame(settings_card, bg="#0d1322")
        jitter_row.pack(fill="x", padx=14, pady=2)
        tk.Label(jitter_row, text="Mouse Jitter Tolerance:", font=("Segoe UI", 9), fg="#ccddee", bg="#0d1322").pack(side="left")
        self.jitter_val_lbl = tk.Label(jitter_row, text="28 px", font=("Consolas", 10, "bold"), fg="#00f0ff", bg="#0d1322")
        self.jitter_val_lbl.pack(side="right")

        self.jitter_slider = tk.Scale(
            settings_card,
            from_=12,
            to=60,
            resolution=2,
            orient="horizontal",
            bg="#0d1322",
            fg="#00f0ff",
            highlightthickness=0,
            troughcolor="#080b14",
            activebackground="#00f0ff",
            showvalue=False,
            command=self._on_jitter_slider_change
        )
        self.jitter_slider.set(28)
        self.jitter_slider.pack(fill="x", padx=14, pady=(0, 4))

        # CURSOR CIRCLE / SPHERE OVERLAY TOGGLE ROW (USER REQUEST)
        circle_row = tk.Frame(settings_card, bg="#0d1322")
        circle_row.pack(fill="x", padx=14, pady=3)

        tk.Label(circle_row, text="Visual Circle Overlay:", font=("Segoe UI", 9), fg="#ccddee", bg="#0d1322").pack(side="left")

        self.reticle_cb = tk.Checkbutton(
            circle_row,
            text="🎯 Show Circle / Sphere around cursor (F6)",
            variable=self.show_reticle_var,
            font=("Segoe UI", 9, "bold"),
            bg="#0d1322",
            fg="#00f0ff",
            selectcolor="#080b14",
            activebackground="#0d1322",
            activeforeground="#00f0ff",
            command=self._on_reticle_toggle
        )
        self.reticle_cb.pack(side="left", padx=8)

        # AUDIO PROFILE SELECTOR (FULL / CHIME ONLY / SILENT)
        sound_row = tk.Frame(settings_card, bg="#0d1322")
        sound_row.pack(fill="x", padx=14, pady=3)
        tk.Label(sound_row, text="Audio Alarm Mode:", font=("Segoe UI", 9), fg="#ccddee", bg="#0d1322").pack(side="left")

        self.sound_mode_var = tk.StringVar(value="full")
        for s_val, s_label in [("full", "🔊 Full Beeps"), ("chime_only", "🔔 Click Only"), ("silent", "🔇 Silent (Mute)")]:
            rb = tk.Radiobutton(
                sound_row,
                text=s_label,
                value=s_val,
                variable=self.sound_mode_var,
                font=("Segoe UI", 8),
                bg="#0d1322",
                fg="#ccddee",
                selectcolor="#080b14",
                activebackground="#0d1322",
                activeforeground="#00ff88",
                command=self._on_sound_mode_change
            )
            rb.pack(side="left", padx=4)

        # Click Type Selector
        opts_row = tk.Frame(settings_card, bg="#0d1322")
        opts_row.pack(fill="x", padx=14, pady=(2, 6))

        tk.Label(opts_row, text="Mouse Action:", font=("Segoe UI", 9), fg="#ccddee", bg="#0d1322").pack(side="left")
        self.click_type_var = tk.StringVar(value="left")
        for mode_val, mode_label in [("left", "Left Click"), ("double", "Double Click"), ("right", "Right Click")]:
            rb = tk.Radiobutton(
                opts_row,
                text=mode_label,
                value=mode_val,
                variable=self.click_type_var,
                font=("Segoe UI", 8),
                bg="#0d1322",
                fg="#ccddee",
                selectcolor="#080b14",
                activebackground="#0d1322",
                activeforeground="#00f0ff",
                command=self._on_click_type_change
            )
            rb.pack(side="left", padx=4)

        # ---------------- TEST CLICK TARGET PAD ----------------
        test_card = tk.Frame(self.root, bg="#0d1322", highlightbackground="#00f0ff", highlightthickness=1)
        test_card.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        tk.Label(
            test_card,
            text="🎯 TEST CLICK TARGET PAD (Hover your cursor over either button below to test!)",
            font=("Consolas", 9, "bold"),
            fg="#00f0ff",
            bg="#0d1322"
        ).pack(anchor="w", padx=14, pady=(8, 4))

        test_btns_row = tk.Frame(test_card, bg="#0d1322")
        test_btns_row.pack(fill="x", padx=14, pady=6)

        self.test_count_a = 0
        self.test_btn_a = tk.Button(
            test_btns_row,
            text="TEST BUTTON A [0 CLICKS]",
            font=("Consolas", 10, "bold"),
            bg="#111827",
            fg="#38bdf8",
            activebackground="#1e293b",
            bd=2,
            relief="raised",
            padx=12,
            pady=12,
            cursor="hand2",
            command=lambda: self._on_test_clicked("A")
        )
        self.test_btn_a.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.test_count_b = 0
        self.test_btn_b = tk.Button(
            test_btns_row,
            text="TEST BUTTON B [0 CLICKS]",
            font=("Consolas", 10, "bold"),
            bg="#111827",
            fg="#a855f7",
            activebackground="#1e293b",
            bd=2,
            relief="raised",
            padx=12,
            pady=12,
            cursor="hand2",
            command=lambda: self._on_test_clicked("B")
        )
        self.test_btn_b.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # Bottom Quick Guide Footnote
        foot_lbl = tk.Label(
            test_card,
            text="Hotkeys: [F6] Circle On/Off | [F7] Mute/Silent Toggle | [F8] Pause/Resume | [F9] Cancel",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0d1322"
        )
        foot_lbl.pack(pady=(2, 6))

    def toggle_reticle(self):
        """Toggles the visual circle / sphere HUD on/off (Hotkey: F6)."""
        new_val = not self.show_reticle_var.get()
        self.show_reticle_var.set(new_val)
        self._on_reticle_toggle()

    def _on_reticle_toggle(self):
        enabled = self.show_reticle_var.get()
        if not enabled:
            self.reticle.hide()
            self.reticle_btn.config(
                text="🚫 NO CIRCLE (F6)",
                bg="#261020",
                fg="#f472b6",
                highlightbackground="#f472b6"
            )
            self.prog_text_lbl.config(text="[⭕ CIRCLE DISABLED] Clean mode: Alarm and auto-click active with NO circle around cursor.")
        else:
            self.reticle_btn.config(
                text="🎯 CIRCLE ON (F6)",
                bg="#162035",
                fg="#00f0ff",
                highlightbackground="#00f0ff"
            )
            self.prog_text_lbl.config(text="[🎯 CIRCLE ENABLED] Floating holographic reticle active around cursor.")

    def open_ascii_viewer(self):
        """Displays the Ultra-HD IRIS ASCII / Braille art in a dedicated futuristic popup window."""
        viewer = tk.Toplevel(self.root)
        viewer.title("IRIS // ULTRA-HD ASCII LOGO VIEWER")
        viewer.geometry("780x520")
        viewer.configure(bg="#05070f")

        top_bar = tk.Frame(viewer, bg="#0c1122", highlightbackground="#00f0ff", highlightthickness=1)
        top_bar.pack(fill="x", padx=12, pady=10)

        tk.Label(
            top_bar,
            text="✨ IRIS UNIVERSAL // ULTRA-HD BRAILLE & ASCII LOGO",
            font=("Consolas", 11, "bold"),
            fg="#00f0ff",
            bg="#0c1122"
        ).pack(side="left", padx=12, pady=8)

        # Print in console button
        reprint_btn = tk.Button(
            top_bar,
            text="⚡ Print in Terminal",
            font=("Segoe UI", 8, "bold"),
            bg="#1e1b4b",
            fg="#c084fc",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self._reprint_ascii_terminal()
        )
        reprint_btn.pack(side="right", padx=12)

        # Scrolled Text Widget for ASCII art
        txt_frame = tk.Frame(viewer, bg="#05070f")
        txt_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        text_widget = tk.Text(
            txt_frame,
            font=("Consolas", 7, "bold"),
            bg="#070a14",
            fg="#38bdf8",
            insertbackground="#00f0ff",
            bd=1,
            relief="solid",
            highlightthickness=0,
            wrap="none"
        )
        text_widget.pack(fill="both", expand=True)

        # Fetch clean art without ANSI escapes
        clean_art = self._get_clean_ascii_art()
        text_widget.insert("1.0", clean_art)
        text_widget.config(state="disabled")

    def _reprint_ascii_terminal(self):
        if HAS_IRIS_ASCII:
            try:
                stream_iris_logo(theme="iris", style="braille", size="medium", speed=0.01, subtitle=True, center=True)
            except Exception:
                print_iris_logo(theme="iris", style="braille", size="medium", subtitle=True, center=True)

    def _get_clean_ascii_art(self):
        """Extracts Braille Art and strips ANSI color codes for Tkinter Text widget."""
        if HAS_IRIS_ASCII and "BRAILLE_ART" in globals():
            try:
                raw = BRAILLE_ART.get("medium", {}).get("iris", "")
                if not raw:
                    raw = BRAILLE_ART.get("compact", {}).get("iris", "")
                return re.sub(r"\x1b\[[0-9;]*m", "", raw)
            except Exception:
                pass
        return "IRIS UNIVERSAL SYSTEM ONLINE"

    def _on_test_clicked(self, which):
        """Visual verification triggered when a test button receives a real click."""
        if which == "A":
            self.test_count_a += 1
            self.test_btn_a.config(
                text=f"💥 CLICKED A! [{self.test_count_a}]",
                bg="#0284c7",
                fg="#ffffff"
            )
            self.root.after(500, lambda: self.test_btn_a.config(
                text=f"TEST BUTTON A [{self.test_count_a} CLICKS]",
                bg="#111827",
                fg="#38bdf8"
            ))
        else:
            self.test_count_b += 1
            self.test_btn_b.config(
                text=f"💥 CLICKED B! [{self.test_count_b}]",
                bg="#9333ea",
                fg="#ffffff"
            )
            self.root.after(500, lambda: self.test_btn_b.config(
                text=f"TEST BUTTON B [{self.test_count_b} CLICKS]",
                bg="#111827",
                fg="#a855f7"
            ))

    def _on_dwell_slider_change(self, val):
        self.dwell_time = float(val)
        self.dwell_val_lbl.config(text=f"{self.dwell_time:0.2f} s")

    def _on_jitter_slider_change(self, val):
        self.jitter_radius = int(float(val))
        self.jitter_val_lbl.config(text=f"{self.jitter_radius} px")

    def _on_click_type_change(self):
        self.click_type = self.click_type_var.get()

    def _on_sound_mode_change(self):
        mode = self.sound_mode_var.get()
        self.sound_mode = mode
        if mode == "silent":
            self.sound_enabled = False
            self.audio.enabled = False
            self.audio.flush()
            self.mute_btn.config(
                text="🔇 SILENT (F7)",
                bg="#2a0814",
                fg="#f43f5e",
                highlightbackground="#f43f5e"
            )
            self.prog_text_lbl.config(text="[🔇 SILENT MODE ACTIVE] All audio alarms muted.")
        else:
            self.sound_enabled = True
            self.audio.enabled = True
            btn_text = "🔔 CHIME ONLY (F7)" if mode == "chime_only" else "🔊 SOUND ON (F7)"
            self.mute_btn.config(
                text=btn_text,
                bg="#0d2818",
                fg="#00ff88",
                highlightbackground="#00ff88"
            )
            self.prog_text_lbl.config(text=f"[AUDIO: {mode.upper()}] Audio alarms active.")

    def toggle_mute(self):
        """Toggles between Full Audio and Completely Silent Mode (Hotkey: F7)."""
        current = self.sound_mode_var.get()
        if current == "silent":
            self.sound_mode_var.set("full")
        else:
            self.sound_mode_var.set("silent")
        self._on_sound_mode_change()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.status_badge.config(
                text="[ ⏸ SYSTEM PAUSED ]",
                fg="#ffbb00",
                bg="#2e2205",
                highlightbackground="#ffbb00"
            )
            self.pause_btn.config(text="▶ RESUME (F8)", fg="#00ff88", highlightbackground="#00ff88")
            self.reticle.hide()
            self.audio.flush()
            self.dwell_start_time = None
        else:
            self.status_badge.config(
                text="[ ● ARMED & ACTIVE ]",
                fg="#00ff88",
                bg="#0a2a1b",
                highlightbackground="#00ff88"
            )
            self.pause_btn.config(text="⏸ PAUSE (F8)", fg="#ffdd00", highlightbackground="#ffdd00")

    def browse_batch_file(self):
        f = filedialog.askopenfilename(
            title="Select Batch File to Run",
            filetypes=[("Batch Files", "*.bat;*.cmd"), ("All Files", "*.*")]
        )
        if f:
            self.selected_batch_path.set(f)

    def run_selected_batch(self):
        path = self.selected_batch_path.get().strip()
        if not path:
            messagebox.showinfo("Select Batch File", "Please select a .bat file first or click 'Browse .bat'.")
            return
        if not os.path.exists(path):
            messagebox.showerror("File Not Found", f"The specified file does not exist:\n{path}")
            return
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", "", path], shell=True)
            messagebox.showinfo("Batch File Started", f"Batch file launched successfully:\n{os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to start batch file:\n{str(e)}")

    def launch_demo_app(self):
        demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_target_app.bat")
        if os.path.exists(demo_path):
            subprocess.Popen(["cmd.exe", "/c", "start", "", demo_path], shell=True)
        else:
            messagebox.showinfo("Info", "demo_target_app.bat not found.")

    def _hotkey_listener(self):
        """Monitors global F6 (Circle On/Off), F7 (Mute/Silent), F8 (Pause), and F9 (Reset) keys anywhere in Windows."""
        f6_was_down = False
        f7_was_down = False
        f8_was_down = False
        f9_was_down = False
        while True:
            time.sleep(0.04)
            # Check F6 (Cursor Circle / Sphere Overlay Toggle)
            f6_state = bool(ctypes.windll.user32.GetAsyncKeyState(VK_F6) & 0x8000)
            if f6_state and not f6_was_down:
                self.root.after(0, self.toggle_reticle)
            f6_was_down = f6_state

            # Check F7 (Mute / Silent Mode Toggle)
            f7_state = bool(ctypes.windll.user32.GetAsyncKeyState(VK_F7) & 0x8000)
            if f7_state and not f7_was_down:
                self.root.after(0, self.toggle_mute)
            f7_was_down = f7_state

            # Check F8 (Pause / Resume)
            f8_state = bool(ctypes.windll.user32.GetAsyncKeyState(VK_F8) & 0x8000)
            if f8_state and not f8_was_down:
                self.root.after(0, self.toggle_pause)
            f8_was_down = f8_state

            # Check F9 (Reset / Emergency Discard)
            f9_state = bool(ctypes.windll.user32.GetAsyncKeyState(VK_F9) & 0x8000)
            if f9_state and not f9_was_down:
                self.dwell_start_time = None
                self.audio.flush()
                self.root.after(0, self.reticle.hide)
            f9_was_down = f9_state

    def _engine_tick(self):
        """
        Main high-frequency engine loop:
        1. Reads live mouse coordinates
        2. Detects dwell hover stability
        3. Fires escalating radar sound alarms (if not in silent mode)
        4. Animates futuristic reticle HUD over mouse cursor (ONLY if circle enabled)
        5. Executes real hardware click at 2.0s
        """
        now = time.time()
        mx, my = get_mouse_pos()
        is_silent = (self.sound_mode_var.get() == "silent")

        # Update telemetry GUI coordinates
        self.coords_lbl.config(text=f"CURSOR: X: {mx:04d} | Y: {my:04d}")

        if self.is_paused or not self.is_running:
            self.target_state_lbl.config(text="STATE: PAUSED", fg="#ffaa00")
            self.progress_var.set(0.0)
            self.reticle.hide()
            self.root.after(25, self._engine_tick)
            return

        # Cooldown guard after a click was triggered
        if now < self.click_cooldown_until:
            self.target_state_lbl.config(text="STATE: RE-ARMING SENSORS", fg="#a855f7")
            self.progress_var.set(0.0)
            self.reticle.hide()
            self.root.after(25, self._engine_tick)
            return

        # Check if cursor is stationary within jitter radius
        if self.anchor_x is None or self.anchor_y is None:
            self.anchor_x, self.anchor_y = mx, my
            self.dwell_start_time = now
            self.last_beep_stage = -1

        dist = math.hypot(mx - self.anchor_x, my - self.anchor_y)

        if dist > self.jitter_radius:
            # Cursor moved away -> Reset target lock and flush audio alarm
            self.anchor_x, self.anchor_y = mx, my
            self.dwell_start_time = now
            self.last_beep_stage = -1
            self.reticle.hide()
            self.audio.flush()
            self.target_state_lbl.config(text="STATE: SCANNING", fg="#7aa2d6")
            self.progress_var.set(0.0)
            mode_tag = " [MUTED]" if is_silent else ""
            self.prog_text_lbl.config(text=f"Hover stationary for {self.dwell_time:0.1f}s to lock target{mode_tag}")
        else:
            # Cursor is holding still on target!
            elapsed = now - self.dwell_start_time
            progress = min(1.0, elapsed / self.dwell_time)
            time_left = max(0.0, self.dwell_time - elapsed)

            status_tag = " (MUTED)" if is_silent else ""
            self.target_state_lbl.config(text=f"LOCKING TARGET: {time_left:0.2f}s{status_tag}", fg="#00f0ff")
            self.progress_var.set(progress * 100.0)
            self.prog_text_lbl.config(text=f"⚡ TARGET ACQUIRED! Holding lock... ({int(progress * 100)}%){status_tag}")

            # Escalating Beep Alarm Logic (Only if full audio mode is active):
            if self.sound_mode_var.get() == "full":
                stage = int(progress * 5)  # 0, 1, 2, 3, 4
                if stage > self.last_beep_stage and stage < 5:
                    self.last_beep_stage = stage
                    frequencies = [650, 950, 1350, 1850, 2400]
                    freq = frequencies[min(stage, len(frequencies) - 1)]
                    self.audio.play_beep(freq, 40)

            # Show Floating Reticle HUD during countdown ONLY if enabled by user
            if self.show_reticle_var.get():
                self.reticle.show(self.anchor_x, self.anchor_y, progress, time_left, is_silent=is_silent)
            else:
                self.reticle.hide()

            # Check if dwell time elapsed -> TRIGGER REAL HARDWARE CLICK!
            if elapsed >= self.dwell_time:
                target_x, target_y = self.anchor_x, self.anchor_y

                # STEP 1: HIDE RETICLE IMMEDIATELY so nothing obstructs the click target!
                self.reticle.hide()
                self.root.update_idletasks()

                # STEP 2: DISPATCH HARDWARE CLICK to the target button underneath
                trigger_hardware_click(target_x, target_y, self.click_type)

                # STEP 3: PLAY CONFIRMATION AUDIO CHIME (if not silent)
                if self.sound_mode_var.get() in ("full", "chime_only"):
                    self.audio.play_click_chime()

                # STEP 4: UPDATE TELEMETRY & STATS
                self.total_clicks_count += 1
                self.clicks_counter_lbl.config(text=f"CLICKS DELIVERED: {self.total_clicks_count}")
                self.target_state_lbl.config(text="💥 CLICK DELIVERED!", fg="#00ff88")
                self.prog_text_lbl.config(text=f"[SUCCESS] Hardware click dispatched at ({target_x}, {target_y})!")

                # STEP 5: ENTER COOLDOWN (1.2 seconds) to avoid spamming the same spot
                self.click_cooldown_until = now + 1.2
                self.dwell_start_time = None
                self.anchor_x, self.anchor_y = None, None
                self.last_beep_stage = -1

        self.root.after(20, self._engine_tick)


def main():
    # Print the Ultra-HD IRIS ASCII Art to terminal on startup
    if HAS_IRIS_ASCII:
        try:
            stream_iris_logo(theme="iris", style="braille", size="medium", speed=0.012, subtitle=True, center=True)
        except Exception:
            try:
                print_iris_logo(theme="iris", style="braille", size="medium", subtitle=True, center=True)
            except Exception:
                pass
    else:
        print("\n" + "=" * 80)
        print("          [ IRIS // QUANTUM AUTO-CLICK ENGINE ONLINE ]")
        print("=" * 80 + "\n")

    root = tk.Tk()
    app = IrisAutoClickerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
