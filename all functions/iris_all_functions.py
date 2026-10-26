"""
================================================================================
  👁️ PROJECT IRIS // OVERLAY ON-SCREEN KEYBOARD & SCROLL CONTROLLER
  Lightweight Direct-Input Accessibility Overlay for Screen Placeholders & Inputs
  Optimized for Eye-Tracking, Head-Tracking, and Assistive Clickers
================================================================================
  Features:
    1. Direct-to-Screen Typing: No internal text box; keystrokes are typed directly
       into whatever placeholder, text field, search bar, or app is active on screen.
    2. Focus-Preserving Overlay (WS_EX_NOACTIVATE | WS_EX_TOPMOST):
       Clicking keys NEVER steals focus from your active document or web browser.
    3. Big & Customizable Key Tiles:
       Instantly adjust tile sizes (Normal, Large, X-Large, Massive) with live scaling.
    4. Dedicated Scroll Up & Scroll Down Buttons:
       Large, easily targetable buttons to scroll active web pages and documents.
    5. Always-On-Top Overlay:
       Floats cleanly on top of all windows and across multi-monitor setups.
    6. Optional Dwell Hover-to-Click:
       Works with existing eye clickers, or built-in dwell hover (toggleable).
================================================================================
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
import ctypes
from ctypes import wintypes

# Enable UTF-8 in console
if sys.platform == "win32":
    os.system("")
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Optional PyAutoGUI
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.005
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# Winsound for subtle click feedback
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Win32 API setup
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

GWL_EXSTYLE       = -20
WS_EX_TOPMOST     = 0x00000008
WS_EX_NOACTIVATE  = 0x08000000
WS_EX_TOOLWINDOW  = 0x00000080

MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000

# SendInput structures for flawless Unicode & Virtual Key typing
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t)
    ]

class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_i",)
    _fields_ = [("type", wintypes.DWORD), ("_i", _I)]

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

# Virtual key codes
VK_BACK    = 0x08
VK_TAB     = 0x09
VK_RETURN  = 0x0D
VK_ESCAPE  = 0x1B
VK_SPACE   = 0x20
VK_PRIOR   = 0x21  # Page Up
VK_NEXT    = 0x22  # Page Down
VK_END     = 0x23
VK_HOME    = 0x24
VK_LEFT    = 0x25
VK_UP      = 0x26
VK_RIGHT   = 0x27
VK_DOWN    = 0x28

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


# -----------------------------------------------------------------------------
# Color Palette & Styling
# -----------------------------------------------------------------------------
THEME = {
    "bg_root": "#0a0e17",
    "bg_bar": "#111827",
    "bg_key": "#1a243b",
    "bg_key_hover": "#2d3e63",
    "bg_key_special": "#202a45",
    "bg_scroll": "#0f2338",
    "bg_scroll_hover": "#173b5c",
    "border": "#273859",
    "accent_cyan": "#00f0ff",
    "accent_emerald": "#00ff88",
    "accent_violet": "#a78bfa",
    "accent_amber": "#f59e0b",
    "accent_rose": "#f43f5e",
    "text_main": "#ffffff",
    "text_sub": "#94a3b8",
    "text_dark": "#050811",
}

# Tile Size Profiles
SIZE_PROFILES = {
    "Normal": {
        "key_font": ("Segoe UI", 12, "bold"),
        "special_font": ("Segoe UI", 10, "bold"),
        "scroll_font": ("Segoe UI", 12, "bold"),
        "pad_y": 6,
        "pad_x": 4,
        "scroll_pady": 14,
        "win_w": 860,
        "win_h": 320
    },
    "Large": {
        "key_font": ("Segoe UI", 15, "bold"),
        "special_font": ("Segoe UI", 11, "bold"),
        "scroll_font": ("Segoe UI", 14, "bold"),
        "pad_y": 10,
        "pad_x": 6,
        "scroll_pady": 22,
        "win_w": 980,
        "win_h": 380
    },
    "X-Large": {
        "key_font": ("Segoe UI", 18, "bold"),
        "special_font": ("Segoe UI", 13, "bold"),
        "scroll_font": ("Segoe UI", 16, "bold"),
        "pad_y": 14,
        "pad_x": 8,
        "scroll_pady": 28,
        "win_w": 1120,
        "win_h": 460
    },
    "Massive": {
        "key_font": ("Segoe UI", 22, "bold"),
        "special_font": ("Segoe UI", 15, "bold"),
        "scroll_font": ("Segoe UI", 19, "bold"),
        "pad_y": 18,
        "pad_x": 10,
        "scroll_pady": 36,
        "win_w": 1280,
        "win_h": 540
    }
}


class IrisDirectOverlayKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("👁️ IRIS // Direct On-Screen Keyboard & Scroll Overlay")
        self.root.configure(bg=THEME["bg_root"])

        # State Variables
        self.size_presets = ["Normal", "Large", "X-Large", "Massive"]
        self.current_size_idx = 1  # Default: Large
        self.is_caps_lock = False
        self.is_shift = False
        self.is_symbols_mode = False
        self.dwell_enabled = False  # Default off so existing eye clicker script handles clicks
        self.dwell_time_seconds = 0.9
        self.audio_enabled = True
        self.is_auto_scrolling = False

        # Target background window tracking
        self.my_hwnd = None
        self.last_target_hwnd = None
        self.last_external_cursor_pos = (500, 500)

        # Dwell Tracker
        self.active_dwell_widget = None
        self.dwell_start_time = 0
        self.dwell_timer_id = None
        self.dwell_cooldown_widget = None

        # Key button widgets storage for live resizing
        self.all_key_widgets = []
        self.scroll_widgets = []

        # Setup Windows API & Non-activating styles
        self.setup_win32_attributes()

        # Build UI
        self.build_ui()

        # Apply initial size
        self.apply_size_profile(self.size_presets[self.current_size_idx], update_geometry=True)

        # Start background window tracker
        self.start_window_tracker()

    # -------------------------------------------------------------------------
    # Win32 Window Styles & Focus Management
    # -------------------------------------------------------------------------
    def setup_win32_attributes(self):
        """Sets Always-On-Top and WS_EX_NOACTIVATE so clicking NEVER steals focus."""
        try:
            self.root.attributes("-topmost", True)
        except Exception:
            pass

        self.root.update_idletasks()
        try:
            self.my_hwnd = user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()
            if self.my_hwnd and sys.platform == "win32":
                old_style = user32.GetWindowLongW(self.my_hwnd, GWL_EXSTYLE)
                # Apply WS_EX_NOACTIVATE (0x08000000) and WS_EX_TOPMOST (0x00000008)
                user32.SetWindowLongW(
                    self.my_hwnd,
                    GWL_EXSTYLE,
                    old_style | WS_EX_NOACTIVATE | WS_EX_TOPMOST
                )
        except Exception as e:
            print(f"[Notice] Win32 style adjustment: {e}")

    def start_window_tracker(self):
        """Continuously remembers the active placeholder window and cursor position."""
        def tracker_loop():
            while True:
                try:
                    fg = user32.GetForegroundWindow()
                    # If foreground is an external application, record it as active target
                    if fg and fg != self.my_hwnd and user32.IsWindow(fg):
                        self.last_target_hwnd = fg

                    pt = POINT()
                    user32.GetCursorPos(ctypes.byref(pt))
                    # Check if cursor is outside our keyboard window
                    rx = self.root.winfo_rootx()
                    ry = self.root.winfo_rooty()
                    rw = self.root.winfo_width()
                    rh = self.root.winfo_height()
                    if not (rx <= pt.x <= rx + rw and ry <= pt.y <= ry + rh):
                        self.last_external_cursor_pos = (int(pt.x), int(pt.y))
                except Exception:
                    pass
                time.sleep(0.06)

        t = threading.Thread(target=tracker_loop, daemon=True)
        t.start()

    def ensure_target_active(self):
        """Ensures the target placeholder/input field is active before keystroke."""
        current_fg = user32.GetForegroundWindow()
        if current_fg == self.my_hwnd:
            if self.last_target_hwnd and user32.IsWindow(self.last_target_hwnd):
                try:
                    user32.SetForegroundWindow(self.last_target_hwnd)
                    time.sleep(0.01)
                except Exception:
                    pass

    # -------------------------------------------------------------------------
    # Direct Screen Keystroke Dispatcher
    # -------------------------------------------------------------------------
    def send_direct_char(self, char):
        """Directly sends a Unicode character into whatever screen placeholder is active."""
        self.play_sound()
        self.ensure_target_active()

        # Handle Shift & Caps Lock
        actual_char = char
        if len(char) == 1 and char.isalpha():
            if self.is_caps_lock or self.is_shift:
                actual_char = char.upper()
            else:
                actual_char = char.lower()

        # 1. Primary method: Windows SendInput with KEYEVENTF_UNICODE
        try:
            code = ord(actual_char)
            inp_down = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, code, KEYEVENTF_UNICODE, 0, 0))
            inp_up   = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, 0))
            user32.SendInput(2, (INPUT * 2)(inp_down, inp_up), ctypes.sizeof(INPUT))
        except Exception:
            # 2. Fallback: PyAutoGUI write
            if HAS_PYAUTOGUI:
                try:
                    pyautogui.write(actual_char)
                except Exception:
                    pass

        # If Shift was active (one-shot), turn off shift
        if self.is_shift:
            self.is_shift = False
            self.refresh_key_labels()
            self.shift_btn.configure(bg=THEME["bg_key_special"], fg=THEME["text_main"])

    def send_direct_vk(self, vk_code):
        """Directly sends special virtual keys (Backspace, Enter, Space, Arrows, etc.)."""
        self.play_sound()
        self.ensure_target_active()

        try:
            inp_down = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(vk_code, 0, 0, 0, 0))
            inp_up   = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(vk_code, 0, KEYEVENTF_KEYUP, 0, 0))
            user32.SendInput(2, (INPUT * 2)(inp_down, inp_up), ctypes.sizeof(INPUT))
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Scroll Controls
    # -------------------------------------------------------------------------
    def scroll_screen(self, direction, clicks=3):
        """Directly scrolls the active screen / document."""
        self.play_sound()
        self.ensure_target_active()
        target_x, target_y = self.last_external_cursor_pos

        delta = 120 * clicks if direction in ["up", "pageup"] else -120 * clicks

        if direction in ["up", "down"]:
            # Send hardware mouse wheel
            user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
            if HAS_PYAUTOGUI:
                try:
                    pyautogui.scroll(delta, x=target_x, y=target_y)
                except Exception:
                    pass

        elif direction == "pageup":
            self.send_direct_vk(VK_PRIOR)
        elif direction == "pagedown":
            self.send_direct_vk(VK_NEXT)

    def toggle_auto_scroll(self):
        """Toggles continuous hands-free downward scrolling."""
        self.is_auto_scrolling = not self.is_auto_scrolling
        if self.is_auto_scrolling:
            self.auto_scroll_btn.configure(bg=THEME["accent_emerald"], fg=THEME["text_dark"], text="⏹ STOP SCROLL")
            self.play_sound()

            def _loop():
                while self.is_auto_scrolling:
                    try:
                        user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, -60, 0)
                    except Exception:
                        pass
                    time.sleep(0.08)

            threading.Thread(target=_loop, daemon=True).start()
        else:
            self.auto_scroll_btn.configure(bg=THEME["bg_scroll"], fg=THEME["text_main"], text="⬇ AUTO-SCROLL")
            self.play_sound()

    # -------------------------------------------------------------------------
    # Sound FX
    # -------------------------------------------------------------------------
    def play_sound(self):
        """Gentle non-blocking feedback beep."""
        if not self.audio_enabled or not HAS_WINSOUND:
            return
        threading.Thread(target=lambda: winsound.Beep(1200, 20), daemon=True).start()

    # -------------------------------------------------------------------------
    # Optional Dwell Hover Auto-Click
    # -------------------------------------------------------------------------
    def register_dwell(self, widget, command_func):
        """Optional hover dwell: auto-clicks button if cursor hovers over it."""
        orig_bg = widget.cget("bg")
        orig_fg = widget.cget("fg")

        def on_enter(event):
            if not self.dwell_enabled:
                widget.configure(bg=THEME["bg_key_hover"])
                return
            if self.dwell_cooldown_widget == widget:
                return

            self.active_dwell_widget = widget
            self.dwell_start_time = time.time()
            widget.configure(bg=THEME["bg_key_hover"], highlightbackground=THEME["accent_cyan"], highlightthickness=2)
            self._dwell_step(widget, command_func, orig_bg, orig_fg)

        def on_leave(event):
            if self.dwell_timer_id:
                self.root.after_cancel(self.dwell_timer_id)
                self.dwell_timer_id = None
            if self.active_dwell_widget == widget:
                self.active_dwell_widget = None
            self.dwell_cooldown_widget = None
            try:
                widget.configure(bg=orig_bg, fg=orig_fg, highlightbackground=THEME["border"], highlightthickness=1)
            except Exception:
                pass

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _dwell_step(self, widget, command_func, orig_bg, orig_fg):
        if self.active_dwell_widget != widget or not self.dwell_enabled:
            return
        elapsed = time.time() - self.dwell_start_time
        if elapsed >= self.dwell_time_seconds:
            self.dwell_cooldown_widget = widget
            self.active_dwell_widget = None
            widget.configure(bg=THEME["accent_emerald"], fg=THEME["text_dark"])
            self.root.after(120, lambda: self._reset_btn(widget, orig_bg, orig_fg))
            command_func()
            return
        self.dwell_timer_id = self.root.after(30, lambda: self._dwell_step(widget, command_func, orig_bg, orig_fg))

    def _reset_btn(self, widget, orig_bg, orig_fg):
        try:
            widget.configure(bg=orig_bg, fg=orig_fg, highlightbackground=THEME["border"], highlightthickness=1)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Tile Size Customization
    # -------------------------------------------------------------------------
    def cycle_tile_size(self, delta):
        """Increases or decreases key tile size."""
        new_idx = max(0, min(len(self.size_presets) - 1, self.current_size_idx + delta))
        if new_idx != self.current_size_idx:
            self.current_size_idx = new_idx
            self.apply_size_profile(self.size_presets[self.current_size_idx], update_geometry=True)

    def set_size_preset(self, size_name):
        """Selects specific tile size preset."""
        if size_name in self.size_presets:
            self.current_size_idx = self.size_presets.index(size_name)
            self.apply_size_profile(size_name, update_geometry=True)

    def apply_size_profile(self, size_name, update_geometry=True):
        """Applies typography, padding, and window dimensions."""
        cfg = SIZE_PROFILES.get(size_name, SIZE_PROFILES["Large"])

        self.size_label.configure(text=f"SIZE: {size_name.upper()}")

        # Update key buttons
        for btn, is_special in self.all_key_widgets:
            font = cfg["special_font"] if is_special else cfg["key_font"]
            btn.configure(font=font, pady=cfg["pad_y"], padx=cfg["pad_x"])

        # Update scroll buttons
        for s_btn in self.scroll_widgets:
            s_btn.configure(font=cfg["scroll_font"], pady=cfg["scroll_pady"])

        if update_geometry:
            # Resize window smoothly while maintaining screen position
            cur_x = self.root.winfo_x()
            cur_y = self.root.winfo_y()
            self.root.geometry(f"{cfg['win_w']}x{cfg['win_h']}+{max(0, cur_x)}+{max(0, cur_y)}")

    # -------------------------------------------------------------------------
    # Keyboard Key Actions
    # -------------------------------------------------------------------------
    def on_special_action(self, action):
        """Handles Shift, Caps, Symbols, Space, Backspace, Enter, Esc."""
        if action == "backspace":
            self.send_direct_vk(VK_BACK)
        elif action == "enter":
            self.send_direct_vk(VK_RETURN)
        elif action == "space":
            self.send_direct_vk(VK_SPACE)
        elif action == "tab":
            self.send_direct_vk(VK_TAB)
        elif action == "esc":
            self.send_direct_vk(VK_ESCAPE)
        elif action == "caps":
            self.is_caps_lock = not self.is_caps_lock
            self.refresh_key_labels()
            self.caps_btn.configure(
                bg=THEME["accent_cyan"] if self.is_caps_lock else THEME["bg_key_special"],
                fg=THEME["text_dark"] if self.is_caps_lock else THEME["text_main"]
            )
        elif action == "shift":
            self.is_shift = not self.is_shift
            self.refresh_key_labels()
            self.shift_btn.configure(
                bg=THEME["accent_violet"] if self.is_shift else THEME["bg_key_special"],
                fg=THEME["text_dark"] if self.is_shift else THEME["text_main"]
            )
        elif action == "symbols":
            self.is_symbols_mode = not self.is_symbols_mode
            self.rebuild_keyboard_grid()

    def refresh_key_labels(self):
        """Updates letter keys to uppercase or lowercase based on Shift / Caps."""
        for btn, is_special in self.all_key_widgets:
            txt = btn.cget("text")
            if len(txt) == 1 and txt.isalpha():
                if self.is_caps_lock or self.is_shift:
                    btn.configure(text=txt.upper())
                else:
                    btn.configure(text=txt.lower())

    # -------------------------------------------------------------------------
    # UI Builder
    # -------------------------------------------------------------------------
    def build_ui(self):
        """Constructs the clean, direct overlay interface."""

        # 1. Top Control Bar (Tile Size, Opacity, Dwell Toggle, Move Handle)
        self.build_top_control_bar()

        # 2. Main Content Area: Keyboard (Left) + Scroll Panel (Right)
        self.main_content = tk.Frame(self.root, bg=THEME["bg_root"])
        self.main_content.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Right Panel: Dedicated Big Scroll Controls
        self.scroll_panel = tk.Frame(self.main_content, bg=THEME["bg_bar"], highlightbackground=THEME["border"], highlightthickness=1)
        self.scroll_panel.pack(side="right", fill="y", padx=(6, 0))
        self.build_scroll_controls(self.scroll_panel)

        # Left Panel: On-Screen Virtual Keyboard
        self.keyboard_container = tk.Frame(self.main_content, bg=THEME["bg_root"])
        self.keyboard_container.pack(side="left", fill="both", expand=True)
        self.rebuild_keyboard_grid()

    def build_top_control_bar(self):
        """Constructs sleek top bar with tile size adjusters & overlay controls."""
        bar = tk.Frame(self.root, bg=THEME["bg_bar"], height=42, highlightbackground=THEME["border"], highlightthickness=1)
        bar.pack(fill="x", padx=8, pady=6)

        # Left: Branding / Drag Handle
        lbl_title = tk.Label(
            bar,
            text="👁️ IRIS OVERLAY KEYBOARD",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["bg_bar"],
            fg=THEME["accent_cyan"]
        )
        lbl_title.pack(side="left", padx=10, pady=4)

        # Tile Size Adjuster Controls
        size_frame = tk.Frame(bar, bg=THEME["bg_bar"])
        size_frame.pack(side="left", padx=15)

        btn_size_minus = tk.Button(
            size_frame,
            text="➖",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["text_main"],
            relief="flat",
            padx=6, pady=2,
            command=lambda: self.cycle_tile_size(-1)
        )
        btn_size_minus.pack(side="left", padx=2)
        self.register_dwell(btn_size_minus, lambda: self.cycle_tile_size(-1))

        self.size_label = tk.Label(
            size_frame,
            text="SIZE: LARGE",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["bg_bar"],
            fg=THEME["accent_emerald"],
            width=14
        )
        self.size_label.pack(side="left", padx=4)

        btn_size_plus = tk.Button(
            size_frame,
            text="➕",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["text_main"],
            relief="flat",
            padx=6, pady=2,
            command=lambda: self.cycle_tile_size(1)
        )
        btn_size_plus.pack(side="left", padx=2)
        self.register_dwell(btn_size_plus, lambda: self.cycle_tile_size(1))

        # Size Presets Buttons
        for sz in ["Normal", "Large", "XL", "Massive"]:
            full_name = "X-Large" if sz == "XL" else sz
            btn_sz = tk.Button(
                size_frame,
                text=sz,
                font=("Segoe UI", 8, "bold"),
                bg=THEME["bg_key_special"],
                fg=THEME["text_sub"],
                relief="flat",
                padx=6, pady=2,
                command=lambda s=full_name: self.set_size_preset(s)
            )
            btn_sz.pack(side="left", padx=2)
            self.register_dwell(btn_sz, lambda s=full_name: self.set_size_preset(s))

        # Right Controls: Dwell Toggle, Opacity, Close
        right_frame = tk.Frame(bar, bg=THEME["bg_bar"])
        right_frame.pack(side="right", padx=8)

        self.dwell_btn = tk.Button(
            right_frame,
            text="🎯 DWELL: OFF",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["text_sub"],
            relief="flat",
            padx=8, pady=2,
            command=self.toggle_dwell
        )
        self.dwell_btn.pack(side="left", padx=4)
        self.register_dwell(self.dwell_btn, self.toggle_dwell)

        # Opacity button toggle (100% -> 90% -> 80%)
        self.opacity_val = 0.98
        self.opacity_btn = tk.Button(
            right_frame,
            text="👁️ 100%",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["accent_cyan"],
            relief="flat",
            padx=6, pady=2,
            command=self.cycle_opacity
        )
        self.opacity_btn.pack(side="left", padx=4)
        self.register_dwell(self.opacity_btn, self.cycle_opacity)

        # Close
        btn_close = tk.Button(
            right_frame,
            text="✖",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["accent_rose"],
            relief="flat",
            padx=8, pady=2,
            command=self.root.destroy
        )
        btn_close.pack(side="left", padx=(4, 0))

    def toggle_dwell(self):
        """Toggles hover dwell click on/off."""
        self.dwell_enabled = not self.dwell_enabled
        if self.dwell_enabled:
            self.dwell_btn.configure(text="🎯 DWELL: ON", fg=THEME["accent_emerald"])
        else:
            self.dwell_btn.configure(text="🎯 DWELL: OFF", fg=THEME["text_sub"])
        self.play_sound()

    def cycle_opacity(self):
        """Cycles window transparency between 100%, 90%, 80%."""
        if self.opacity_val >= 0.95:
            self.opacity_val = 0.88
            lbl = "👁️ 90%"
        elif self.opacity_val >= 0.85:
            self.opacity_val = 0.78
            lbl = "👁️ 80%"
        else:
            self.opacity_val = 0.98
            lbl = "👁️ 100%"

        self.root.attributes("-alpha", self.opacity_val)
        self.opacity_btn.configure(text=lbl)
        self.play_sound()

    # -------------------------------------------------------------------------
    # Dedicated Scroll Panel
    # -------------------------------------------------------------------------
    def build_scroll_controls(self, parent):
        """Constructs prominent Scroll Up & Scroll Down buttons on the side."""
        self.scroll_widgets.clear()

        lbl_scroll = tk.Label(
            parent,
            text="📜 SCROLL",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["bg_bar"],
            fg=THEME["accent_cyan"]
        )
        lbl_scroll.pack(fill="x", padx=8, pady=(8, 4))

        # Huge Scroll Up Button
        btn_up = tk.Button(
            parent,
            text="▲▲\nSCROLL\nUP",
            font=("Segoe UI", 13, "bold"),
            bg=THEME["bg_scroll"],
            fg=THEME["text_main"],
            activebackground=THEME["accent_cyan"],
            activeforeground=THEME["text_dark"],
            relief="flat",
            padx=16, pady=20,
            command=lambda: self.scroll_screen("up", 4)
        )
        btn_up.pack(fill="both", expand=True, padx=6, pady=3)
        self.register_dwell(btn_up, lambda: self.scroll_screen("up", 4))
        self.scroll_widgets.append(btn_up)

        # Huge Scroll Down Button
        btn_down = tk.Button(
            parent,
            text="▼▼\nSCROLL\nDOWN",
            font=("Segoe UI", 13, "bold"),
            bg=THEME["bg_scroll"],
            fg=THEME["text_main"],
            activebackground=THEME["accent_cyan"],
            activeforeground=THEME["text_dark"],
            relief="flat",
            padx=16, pady=20,
            command=lambda: self.scroll_screen("down", 4)
        )
        btn_down.pack(fill="both", expand=True, padx=6, pady=3)
        self.register_dwell(btn_down, lambda: self.scroll_screen("down", 4))
        self.scroll_widgets.append(btn_down)

        # Page Up / Down Row
        p_row = tk.Frame(parent, bg=THEME["bg_bar"])
        p_row.pack(fill="x", padx=6, pady=2)

        btn_pup = tk.Button(
            p_row,
            text="⇞ PgUp",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["text_main"],
            relief="flat",
            pady=6,
            command=lambda: self.scroll_screen("pageup")
        )
        btn_pup.pack(side="left", fill="both", expand=True, padx=(0, 2))
        self.register_dwell(btn_pup, lambda: self.scroll_screen("pageup"))

        btn_pdn = tk.Button(
            p_row,
            text="⇟ PgDn",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["bg_key"],
            fg=THEME["text_main"],
            relief="flat",
            pady=6,
            command=lambda: self.scroll_screen("pagedown")
        )
        btn_pdn.pack(side="left", fill="both", expand=True, padx=(2, 0))
        self.register_dwell(btn_pdn, lambda: self.scroll_screen("pagedown"))

        # Hands-free Continuous Auto-Scroll Toggle
        self.auto_scroll_btn = tk.Button(
            parent,
            text="⬇ AUTO-SCROLL",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["bg_scroll"],
            fg=THEME["text_main"],
            relief="flat",
            padx=8, pady=8,
            command=self.toggle_auto_scroll
        )
        self.auto_scroll_btn.pack(fill="x", padx=6, pady=(3, 8))
        self.register_dwell(self.auto_scroll_btn, self.toggle_auto_scroll)

    # -------------------------------------------------------------------------
    # Virtual Keyboard Key Matrix
    # -------------------------------------------------------------------------
    def rebuild_keyboard_grid(self):
        """Constructs the virtual keyboard layout with direct-to-placeholder typing."""
        for w in self.keyboard_container.winfo_children():
            w.destroy()
        self.all_key_widgets.clear()

        if not self.is_symbols_mode:
            # Clean Standard QWERTY Layout
            rows = [
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACKSPACE"],
                ["TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
                ["CAPS", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
                ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "?123"],
                ["SPACE", "LEFT", "RIGHT", "UP", "DOWN", "ESC"]
            ]
        else:
            # Symbols & Punctuation Layout
            rows = [
                ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "BACKSPACE"],
                ["TAB", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "{", "}", "|"],
                ["ABC", ":", "\"", "<", ">", "?", "[", "]", "/", "\\", ";", "'", "ENTER"],
                ["SHIFT", "`", "=", "-", "+", "*", "%", "$", "#", "@", "!", "ABC"],
                ["SPACE", "LEFT", "RIGHT", "UP", "DOWN", "ESC"]
            ]

        for row_idx, key_row in enumerate(rows):
            row_frame = tk.Frame(self.keyboard_container, bg=THEME["bg_root"])
            row_frame.pack(fill="both", expand=True, pady=1)

            for key in key_row:
                is_special = key in ["BACKSPACE", "ENTER", "SPACE", "TAB", "CAPS", "SHIFT", "?123", "ABC", "ESC", "LEFT", "RIGHT", "UP", "DOWN"]

                # Tile background colors
                btn_bg = THEME["bg_key_special"] if is_special else THEME["bg_key"]
                btn_fg = THEME["text_main"]

                if key == "ENTER":
                    btn_bg = THEME["accent_cyan"]
                    btn_fg = THEME["text_dark"]
                elif key == "SPACE":
                    btn_bg = THEME["bg_key"]

                # Display text
                disp_text = key
                if key.isalpha() and not (self.is_caps_lock or self.is_shift):
                    disp_text = key.lower()
                elif key == "BACKSPACE":
                    disp_text = "⌫ BACK"
                elif key == "ENTER":
                    disp_text = "↵ ENTER"
                elif key == "SPACE":
                    disp_text = "␣  SPACEBAR  ␣"
                elif key == "TAB":
                    disp_text = "⇥ TAB"
                elif key == "CAPS":
                    disp_text = "⇪ CAPS"
                elif key == "SHIFT":
                    disp_text = "⇧ SHIFT"
                elif key == "LEFT":
                    disp_text = "◀"
                elif key == "RIGHT":
                    disp_text = "▶"
                elif key == "UP":
                    disp_text = "▲"
                elif key == "DOWN":
                    disp_text = "▼"

                btn = tk.Button(
                    row_frame,
                    text=disp_text,
                    font=("Segoe UI", 14, "bold"),
                    bg=btn_bg,
                    fg=btn_fg,
                    activebackground=THEME["accent_cyan"],
                    activeforeground=THEME["text_dark"],
                    relief="flat",
                    padx=4, pady=8
                )

                # Attach Direct Input Commands
                if key == "BACKSPACE":
                    btn.configure(command=lambda: self.on_special_action("backspace"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "ENTER":
                    btn.configure(command=lambda: self.on_special_action("enter"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "SPACE":
                    btn.configure(command=lambda: self.on_special_action("space"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "TAB":
                    btn.configure(command=lambda: self.on_special_action("tab"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "CAPS":
                    self.caps_btn = btn
                    btn.configure(command=lambda: self.on_special_action("caps"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "SHIFT":
                    self.shift_btn = btn
                    btn.configure(command=lambda: self.on_special_action("shift"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key in ["?123", "ABC"]:
                    btn.configure(command=lambda: self.on_special_action("symbols"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "ESC":
                    btn.configure(command=lambda: self.on_special_action("esc"))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "LEFT":
                    btn.configure(command=lambda: self.send_direct_vk(VK_LEFT))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "RIGHT":
                    btn.configure(command=lambda: self.send_direct_vk(VK_RIGHT))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "UP":
                    btn.configure(command=lambda: self.send_direct_vk(VK_UP))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                elif key == "DOWN":
                    btn.configure(command=lambda: self.send_direct_vk(VK_DOWN))
                    btn.pack(side="left", fill="both", expand=True, padx=2)
                else:
                    # Regular character key: Types directly into active placeholder!
                    btn.configure(command=lambda k=key: self.send_direct_char(k))
                    btn.pack(side="left", fill="both", expand=True, padx=2)

                self.register_dwell(btn, lambda b=btn: b.invoke())
                self.all_key_widgets.append((btn, is_special))

        # Re-apply active size profile to the rebuilt buttons
        self.apply_size_profile(self.size_presets[self.current_size_idx], update_geometry=False)


def main():
    root = tk.Tk()
    app = IrisDirectOverlayKeyboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
