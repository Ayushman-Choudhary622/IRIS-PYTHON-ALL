"""
IRIS Auto Clicker - Ultimate Universal Auto Clicker
Features:
- Auto-click every 3 seconds (customizable to milliseconds or hours)
- Auto-start option (launches and immediately starts clicking)
- Global Hotkeys: F6 (Start/Stop), F7 (Pick Coordinates), ESC (Emergency Stop)
- Left, Right, Middle click support
- Single and Double click modes
- Fixed coordinates or dynamic cursor tracking
- Anti-detection humanized random jitter
- Audio feedback beeps
- Live click statistics and countdown timer
- 100% Zero-dependency (Pure Python standard library + Windows ctypes)
"""

import sys
import os
import re
import time
import random
import threading
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk, messagebox

# Locate and import IRIS ASCII ART module if available
ASCII_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IRIS ASCII ART")
if not os.path.exists(ASCII_DIR):
    # Try parent directory in case folder hierarchy varies
    ASCII_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "IRIS ASCII ART")

if os.path.exists(ASCII_DIR) and ASCII_DIR not in sys.path:
    sys.path.insert(0, ASCII_DIR)

try:
    from iris_ascii import print_iris_logo, get_iris_logo, init_terminal
    HAS_IRIS_ASCII = True
except Exception:
    HAS_IRIS_ASCII = False


def show_startup_ascii():
    """Prints the Ultra-HD IRIS ASCII Art banner at application launch."""
    if HAS_IRIS_ASCII:
        try:
            init_terminal()
            print_iris_logo(theme="iris", size="auto", subtitle=True)
            print("\033[38;2;148;163;184m" + "─" * 90 + "\033[0m")
            print("  ⚡ \033[1;38;2;6;182;212mIRIS 3-SEC AUTO CLICKER ENGINE INITIALIZED\033[0m")
            print("  ⌨️  Hotkeys: \033[1;38;2;167;139;250m[F6]\033[0m Start/Pause  |  \033[1;38;2;59;130;246m[F7]\033[0m Pick Coordinates  |  \033[1;38;2;244;63;94m[ESC]\033[0m Stop")
            print("\033[38;2;148;163;184m" + "─" * 90 + "\033[0m\n")
        except Exception as e:
            print(f"[*] IRIS Auto Clicker Initialized (Note on ASCII art: {e})")
    else:
        print("==================================================")
        print("         IRIS UNIVERSAL 3-SEC AUTO CLICKER        ")
        print("==================================================")


# Windows API Constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

VK_F6 = 0x75
VK_F7 = 0x76
VK_ESCAPE = 0x1B

user32 = ctypes.windll.user32

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class AutoClickerApp:
    def __init__(self, root, autostart=True):
        self.root = root
        self.root.title("IRIS 3-Sec Universal Auto Clicker")
        self.root.geometry("460x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f111a")

        # Set taskbar icon styling if available
        try:
            self.root.attributes("-topmost", True)
        except Exception:
            pass

        # State Variables
        self.is_running = False
        self.stop_event = threading.Event()
        self.click_thread = None
        self.hotkey_thread = None
        
        self.total_clicks = 0
        self.start_time = None
        self.next_click_time = 0
        
        # User Configuration Variables
        self.interval_sec = tk.DoubleVar(value=3.0)
        self.interval_ms = tk.IntVar(value=0)
        self.click_button = tk.StringVar(value="Left")
        self.click_type = tk.StringVar(value="Single")
        self.location_mode = tk.StringVar(value="cursor")  # 'cursor' or 'fixed'
        self.fixed_x = tk.IntVar(value=500)
        self.fixed_y = tk.IntVar(value=500)
        self.jitter_enabled = tk.BooleanVar(value=False)
        self.jitter_range = tk.DoubleVar(value=0.2)
        self.sound_enabled = tk.BooleanVar(value=True)
        self.always_on_top = tk.BooleanVar(value=True)
        self.repeat_unlimited = tk.BooleanVar(value=True)
        self.repeat_count = tk.IntVar(value=100)
        self.picking_coords = False

        self._build_ui()

        # Start Global Hotkey Listener
        self.hotkey_running = True
        self.hotkey_thread = threading.Thread(target=self._hotkey_listener, daemon=True)
        self.hotkey_thread.start()

        # Periodic GUI update
        self._update_gui_loop()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Auto-start if requested
        if autostart:
            self.root.after(500, self.start_clicking)

        # Automatically display Ultra-HD IRIS ASCII Art window at application launch
        self.root.after(200, self.open_ascii_modal)

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self.root, bg="#1a1c29", height=65)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header,
            text="⚡ IRIS AUTO CLICKER",
            font=("Segoe UI", 13, "bold"),
            fg="#a78bfa",
            bg="#1a1c29"
        )
        title_lbl.pack(side="left", padx=(14, 6), pady=8)

        # ASCII Art View Button
        btn_ascii = tk.Button(
            header,
            text="👁️ ASCII",
            font=("Segoe UI", 8, "bold"),
            bg="#2e1065",
            fg="#c084fc",
            activebackground="#581c87",
            activeforeground="#ffffff",
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.open_ascii_modal
        )
        btn_ascii.pack(side="left", padx=4, pady=16)

        self.status_pill = tk.Label(
            header,
            text="● STOPPED",
            font=("Segoe UI", 9, "bold"),
            fg="#f43f5e",
            bg="#271b26",
            padx=10,
            pady=4
        )
        self.status_pill.pack(side="right", padx=14, pady=16)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#0f111a")
        main_frame.pack(fill="both", expand=True, padx=16, pady=12)

        # Card 1: Click Interval
        c1 = self._create_card(main_frame, "⏱️ CLICK INTERVAL")
        row1 = tk.Frame(c1, bg="#161824")
        row1.pack(fill="x", pady=4)

        tk.Label(row1, text="Every:", font=("Segoe UI", 10), fg="#94a3b8", bg="#161824").pack(side="left", padx=4)
        
        sec_entry = tk.Spinbox(
            row1, from_=0.01, to=3600.0, increment=0.5, format="%.2f",
            textvariable=self.interval_sec, width=6, font=("Segoe UI", 10, "bold"),
            bg="#232738", fg="#f8fafc", insertbackground="#fff", bd=0, relief="flat"
        )
        sec_entry.pack(side="left", padx=4)
        tk.Label(row1, text="sec +", font=("Segoe UI", 10), fg="#94a3b8", bg="#161824").pack(side="left")

        ms_entry = tk.Spinbox(
            row1, from_=0, to=999, increment=50,
            textvariable=self.interval_ms, width=5, font=("Segoe UI", 10, "bold"),
            bg="#232738", fg="#f8fafc", insertbackground="#fff", bd=0, relief="flat"
        )
        ms_entry.pack(side="left", padx=4)
        tk.Label(row1, text="ms", font=("Segoe UI", 10), fg="#94a3b8", bg="#161824").pack(side="left")

        # Quick Preset Buttons
        p_frame = tk.Frame(c1, bg="#161824")
        p_frame.pack(fill="x", pady=(4, 0))
        tk.Label(p_frame, text="Presets:", font=("Segoe UI", 8), fg="#64748b", bg="#161824").pack(side="left")
        for preset, s, ms in [("100ms", 0.0, 100), ("1s", 1.0, 0), ("3s (Default)", 3.0, 0), ("5s", 5.0, 0), ("10s", 10.0, 0)]:
            btn = tk.Button(
                p_frame, text=preset, font=("Segoe UI", 8),
                bg="#232738", fg="#cbd5e1", activebackground="#7c3aed", activeforeground="#fff",
                bd=0, padx=6, pady=2, cursor="hand2",
                command=lambda s=s, ms=ms: self._set_preset(s, ms)
            )
            btn.pack(side="left", padx=3)

        # Card 2: Mouse Options
        c2 = self._create_card(main_frame, "🖱️ MOUSE SETTINGS")
        row2 = tk.Frame(c2, bg="#161824")
        row2.pack(fill="x", pady=2)

        tk.Label(row2, text="Button:", font=("Segoe UI", 9), fg="#94a3b8", bg="#161824").pack(side="left", padx=4)
        for btn_name in ["Left", "Right", "Middle"]:
            rb = tk.Radiobutton(
                row2, text=btn_name, value=btn_name, variable=self.click_button,
                font=("Segoe UI", 9), fg="#f1f5f9", bg="#161824", selectcolor="#7c3aed",
                activebackground="#161824", activeforeground="#fff"
            )
            rb.pack(side="left", padx=6)

        row2_sub = tk.Frame(c2, bg="#161824")
        row2_sub.pack(fill="x", pady=2)
        tk.Label(row2_sub, text="Type:", font=("Segoe UI", 9), fg="#94a3b8", bg="#161824").pack(side="left", padx=4)
        for t_name in ["Single", "Double"]:
            rb = tk.Radiobutton(
                row2_sub, text=t_name, value=t_name, variable=self.click_type,
                font=("Segoe UI", 9), fg="#f1f5f9", bg="#161824", selectcolor="#7c3aed",
                activebackground="#161824", activeforeground="#fff"
            )
            rb.pack(side="left", padx=6)

        # Card 3: Location Options
        c3 = self._create_card(main_frame, "📍 CLICK LOCATION")
        r3_1 = tk.Frame(c3, bg="#161824")
        r3_1.pack(fill="x", pady=2)

        rb_curr = tk.Radiobutton(
            r3_1, text="Current Mouse Position (Follow Cursor)", value="cursor",
            variable=self.location_mode, font=("Segoe UI", 9),
            fg="#f1f5f9", bg="#161824", selectcolor="#7c3aed",
            activebackground="#161824", activeforeground="#fff"
        )
        rb_curr.pack(anchor="w")

        r3_2 = tk.Frame(c3, bg="#161824")
        r3_2.pack(fill="x", pady=2)

        rb_fix = tk.Radiobutton(
            r3_2, text="Fixed Location: X:", value="fixed",
            variable=self.location_mode, font=("Segoe UI", 9),
            fg="#f1f5f9", bg="#161824", selectcolor="#7c3aed",
            activebackground="#161824", activeforeground="#fff"
        )
        rb_fix.pack(side="left")

        self.x_entry = tk.Entry(
            r3_2, textvariable=self.fixed_x, width=5, font=("Segoe UI", 9, "bold"),
            bg="#232738", fg="#f8fafc", insertbackground="#fff", bd=0
        )
        self.x_entry.pack(side="left", padx=2)

        tk.Label(r3_2, text="Y:", font=("Segoe UI", 9), fg="#94a3b8", bg="#161824").pack(side="left", padx=2)
        self.y_entry = tk.Entry(
            r3_2, textvariable=self.fixed_y, width=5, font=("Segoe UI", 9, "bold"),
            bg="#232738", fg="#f8fafc", insertbackground="#fff", bd=0
        )
        self.y_entry.pack(side="left", padx=2)

        self.pick_btn = tk.Button(
            r3_2, text="🎯 Pick (F7)", font=("Segoe UI", 8, "bold"),
            bg="#3b82f6", fg="#fff", activebackground="#2563eb",
            bd=0, padx=8, pady=2, cursor="hand2", command=self.pick_location
        )
        self.pick_btn.pack(side="left", padx=8)

        # Card 4: Extra Features (Anti-detection jitter, Sound, Always on Top)
        c4 = self._create_card(main_frame, "⚙️ ENHANCED FEATURES")
        r4 = tk.Frame(c4, bg="#161824")
        r4.pack(fill="x", pady=2)

        cb_jitter = tk.Checkbutton(
            r4, text="Random Jitter (±0.2s)", variable=self.jitter_enabled,
            font=("Segoe UI", 8), fg="#cbd5e1", bg="#161824", selectcolor="#7c3aed",
            activebackground="#161824", activeforeground="#fff"
        )
        cb_jitter.pack(side="left", padx=4)

        cb_sound = tk.Checkbutton(
            r4, text="Audio Beep", variable=self.sound_enabled,
            font=("Segoe UI", 8), fg="#cbd5e1", bg="#161824", selectcolor="#7c3aed",
            activebackground="#161824", activeforeground="#fff"
        )
        cb_sound.pack(side="left", padx=4)

        cb_top = tk.Checkbutton(
            r4, text="Stay On Top", variable=self.always_on_top,
            font=("Segoe UI", 8), fg="#cbd5e1", bg="#161824", selectcolor="#7c3aed",
            activebackground="#161824", activeforeground="#fff",
            command=self._toggle_always_on_top
        )
        cb_top.pack(side="left", padx=4)

        # Card 5: Statistics & Countdown
        c5 = self._create_card(main_frame, "📊 STATUS & STATISTICS")
        stat_row = tk.Frame(c5, bg="#161824")
        stat_row.pack(fill="x", pady=2)

        self.lbl_clicks = tk.Label(
            stat_row, text="Clicks: 0", font=("Segoe UI", 10, "bold"),
            fg="#38bdf8", bg="#161824"
        )
        self.lbl_clicks.pack(side="left", padx=6)

        self.lbl_timer = tk.Label(
            stat_row, text="Elapsed: 00:00", font=("Segoe UI", 9),
            fg="#94a3b8", bg="#161824"
        )
        self.lbl_timer.pack(side="left", padx=12)

        self.lbl_next = tk.Label(
            stat_row, text="Next: --", font=("Segoe UI", 9, "bold"),
            fg="#facc15", bg="#161824"
        )
        self.lbl_next.pack(side="right", padx=6)

        # Main Action Button (Toggle Start/Stop)
        self.btn_toggle = tk.Button(
            self.root,
            text="▶ START AUTO CLICKER (F6)",
            font=("Segoe UI", 12, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            height=2,
            cursor="hand2",
            command=self.toggle_clicking
        )
        self.btn_toggle.pack(fill="x", padx=16, pady=(0, 6))

        # Bottom Hotkeys legend
        legend = tk.Label(
            self.root,
            text="Hotkeys: [F6] Start/Stop   •   [F7] Pick Coordinate   •   [ESC] Emergency Stop",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f111a"
        )
        legend.pack(pady=(0, 8))

    def _create_card(self, parent, title):
        card = tk.Frame(parent, bg="#161824", bd=0, padx=10, pady=8)
        card.pack(fill="x", pady=4)
        lbl = tk.Label(
            card, text=title, font=("Segoe UI", 8, "bold"),
            fg="#818cf8", bg="#161824"
        )
        lbl.pack(anchor="w", pady=(0, 4))
        return card

    def _set_preset(self, sec, ms):
        self.interval_sec.set(sec)
        self.interval_ms.set(ms)

    def _toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())

    def toggle_clicking(self):
        if self.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if self.is_running:
            return
        
        # Calculate interval
        interval = self.interval_sec.get() + (self.interval_ms.get() / 1000.0)
        if interval <= 0.005:
            interval = 0.005  # minimum safety floor

        self.is_running = True
        self.stop_event.clear()
        self.start_time = time.time()
        self.next_click_time = time.time() + interval

        # UI updates
        self.status_pill.config(text="● RUNNING", fg="#10b981", bg="#064e3b")
        self.btn_toggle.config(
            text="⏸ STOP AUTO CLICKER (F6)",
            bg="#f43f5e",
            activebackground="#e11d48"
        )

        if self.sound_enabled.get():
            threading.Thread(target=self._play_beep, args=(880, 120), daemon=True).start()

        # Start clicking worker thread
        self.click_thread = threading.Thread(target=self._click_worker, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        if not self.is_running:
            return
        
        self.is_running = False
        self.stop_event.set()

        # UI updates
        self.status_pill.config(text="● STOPPED", fg="#f43f5e", bg="#271b26")
        self.btn_toggle.config(
            text="▶ START AUTO CLICKER (F6)",
            bg="#10b981",
            activebackground="#059669"
        )
        self.lbl_next.config(text="Next: --")

        if self.sound_enabled.get():
            threading.Thread(target=self._play_beep, args=(440, 150), daemon=True).start()

    def _play_beep(self, freq, duration):
        try:
            import winsound
            winsound.Beep(freq, duration)
        except Exception:
            pass

    def _do_click(self):
        btn = self.click_button.get()
        ctype = self.click_type.get()
        mode = self.location_mode.get()

        if mode == "fixed":
            user32.SetCursorPos(int(self.fixed_x.get()), int(self.fixed_y.get()))

        if btn == "Left":
            down_flag, up_flag = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
        elif btn == "Right":
            down_flag, up_flag = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
        else:
            down_flag, up_flag = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP

        # Execute Click(s)
        clicks_to_do = 2 if ctype == "Double" else 1
        for _ in range(clicks_to_do):
            user32.mouse_event(down_flag, 0, 0, 0, 0)
            time.sleep(0.01)
            user32.mouse_event(up_flag, 0, 0, 0, 0)
            if clicks_to_do > 1:
                time.sleep(0.05)

        self.total_clicks += clicks_to_do

    def _click_worker(self):
        while self.is_running and not self.stop_event.is_set():
            # Perform Click
            self._do_click()

            # Calculate next delay
            base_interval = self.interval_sec.get() + (self.interval_ms.get() / 1000.0)
            if self.jitter_enabled.get():
                # Add random fluctuation ± jitter
                jitter = random.uniform(-self.jitter_range.get(), self.jitter_range.get())
                actual_delay = max(0.01, base_interval + jitter)
            else:
                actual_delay = max(0.005, base_interval)

            self.next_click_time = time.time() + actual_delay

            # Sleep in tiny increments so stop is instant and responsive
            sleep_step = 0.05
            slept = 0.0
            while slept < actual_delay and not self.stop_event.is_set() and self.is_running:
                step = min(sleep_step, actual_delay - slept)
                time.sleep(step)
                slept += step

    def pick_location(self):
        """Allows user to press F7 anywhere or click button to lock current mouse coords"""
        self.pick_btn.config(text="Move & press F7!", bg="#f59e0b")
        self.picking_coords = True

    def _capture_current_mouse(self):
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        self.fixed_x.set(pt.x)
        self.fixed_y.set(pt.y)
        self.location_mode.set("fixed")
        self.pick_btn.config(text="🎯 Pick (F7)", bg="#3b82f6")
        self.picking_coords = False
        if self.sound_enabled.get():
            threading.Thread(target=self._play_beep, args=(1200, 100), daemon=True).start()

    def _hotkey_listener(self):
        """Polls F6, F7, and ESC asynchronously with debouncing"""
        last_f6 = False
        last_f7 = False
        last_esc = False

        while self.hotkey_running:
            # Check F6
            f6_state = (user32.GetAsyncKeyState(VK_F6) & 0x8000) != 0
            if f6_state and not last_f6:
                # Hotkey pressed
                self.root.after(0, self.toggle_clicking)
            last_f6 = f6_state

            # Check F7
            f7_state = (user32.GetAsyncKeyState(VK_F7) & 0x8000) != 0
            if f7_state and not last_f7:
                self.root.after(0, self._capture_current_mouse)
            last_f7 = f7_state

            # Check ESC (Emergency Stop)
            esc_state = (user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000) != 0
            if esc_state and not last_esc:
                if self.is_running:
                    self.root.after(0, self.stop_clicking)
            last_esc = esc_state

            time.sleep(0.04)

    def _update_gui_loop(self):
        if self.is_running:
            # Update clicks
            self.lbl_clicks.config(text=f"Clicks: {self.total_clicks:,}")

            # Update elapsed timer
            if self.start_time:
                elapsed = int(time.time() - self.start_time)
                mins, secs = divmod(elapsed, 60)
                self.lbl_timer.config(text=f"Elapsed: {mins:02d}:{secs:02d}")

            # Update next click countdown
            remaining = max(0.0, self.next_click_time - time.time())
            self.lbl_next.config(text=f"Next in: {remaining:.1f}s")
        else:
            self.lbl_clicks.config(text=f"Clicks: {self.total_clicks:,}")

        # Schedule next refresh
        self.root.after(100, self._update_gui_loop)

    def open_ascii_modal(self):
        """Displays the Ultra-HD IRIS ASCII art in a dedicated modal window with Sphere Toggle."""
        win = tk.Toplevel(self.root)
        win.title("IRIS Universal - Ultra-HD ASCII Logo")
        win.geometry("780x540")
        win.configure(bg="#0c0e17")
        win.attributes("-topmost", True)

        top_bar = tk.Frame(win, bg="#161824", height=45)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar,
            text="👁️ IRIS UNIVERSAL • ASCII & BRAILLE ART",
            font=("Segoe UI", 10, "bold"),
            fg="#38bdf8",
            bg="#161824"
        ).pack(side="left", padx=12, pady=10)

        # Container for text with scrollbars
        txt_frame = tk.Frame(win, bg="#0c0e17")
        txt_frame.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        txt = tk.Text(
            txt_frame,
            bg="#0f111a",
            fg="#00e6ff",
            insertbackground="#ffffff",
            font=("Consolas", 8),
            bd=0,
            wrap="none",
            padx=10,
            pady=10
        )
        scroll_y = tk.Scrollbar(txt_frame, orient="vertical", command=txt.yview)
        scroll_x = tk.Scrollbar(txt_frame, orient="horizontal", command=txt.xview)
        txt.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        txt.pack(fill="both", expand=True)

        if HAS_IRIS_ASCII:
            try:
                raw_art = get_iris_logo(theme="iris", size="compact", subtitle=True)
                clean_art = re.sub(r'\x1b\[[0-9;]*m', '', raw_art)
                txt.insert("1.0", clean_art)
            except Exception as e:
                txt.insert("1.0", f"Error loading IRIS ASCII art: {e}")
        else:
            txt.insert("1.0", "IRIS ASCII ART module not found.")
        txt.config(state="disabled")

    def _on_close(self):
        self.stop_clicking()
        self.hotkey_running = False
        self.root.destroy()


def main():
    # 1. Show Ultra-HD IRIS ASCII Art banner at startup in console
    show_startup_ascii()

    # Check for CLI arguments like --autostart or custom interval
    autostart = True
    if "--no-autostart" in sys.argv:
        autostart = False

    root = tk.Tk()
    app = AutoClickerApp(root, autostart=autostart)
    root.mainloop()


if __name__ == "__main__":
    main()
