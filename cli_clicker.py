"""
IRIS CLI 3-Second Auto Clicker (Pure Console Mode)
- Automatically starts clicking every 3.0 seconds
- Global F6 to Toggle Activate/Deactivate
- Global ESC or Ctrl+C to Exit
- Zero dependencies (Pure Python + Windows ctypes)
"""

import sys
import os
import time
import threading
import ctypes
import winsound

# Locate and import IRIS ASCII ART module if available
ASCII_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IRIS ASCII ART")
if not os.path.exists(ASCII_DIR):
    ASCII_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "IRIS ASCII ART")

if os.path.exists(ASCII_DIR) and ASCII_DIR not in sys.path:
    sys.path.insert(0, ASCII_DIR)

try:
    from iris_ascii import print_iris_logo, init_terminal
    HAS_IRIS_ASCII = True
except Exception:
    HAS_IRIS_ASCII = False


def show_startup_ascii():
    if HAS_IRIS_ASCII:
        try:
            init_terminal()
            print_iris_logo(theme="iris", size="auto", subtitle=True)
        except Exception:
            pass

# Win32 API
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
VK_F6 = 0x75
VK_ESCAPE = 0x1B

class CLIClicker:
    def __init__(self, interval=3.0):
        self.interval = interval
        self.active = True
        self.running = True
        self.total_clicks = 0

    def click(self):
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        self.total_clicks += 1

    def toggle(self):
        self.active = not self.active
        status = "ACTIVE [CLICKING]" if self.active else "PAUSED [STANDBY]"
        freq = 880 if self.active else 440
        try:
            winsound.Beep(freq, 120)
        except Exception:
            pass
        print(f"\n[*] Status changed: >>> {status} <<< (Press F6 to toggle)")

    def hotkey_thread_fn(self):
        last_f6 = False
        while self.running:
            f6 = (user32.GetAsyncKeyState(VK_F6) & 0x8000) != 0
            if f6 and not last_f6:
                self.toggle()
            last_f6 = f6

            esc = (user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000) != 0
            if esc:
                print("\n[!] ESC pressed. Exiting...")
                self.running = False
                break
            time.sleep(0.04)

    def run(self):
        show_startup_ascii()
        print("==================================================")
        print("     IRIS 3-SEC AUTO CLICKER (CLI MODE)")
        print("==================================================")
        print(f"[*] Interval: {self.interval:.1f} seconds")
        print("[*] State: ACTIVE (Auto-clicking started!)")
        print("[*] Hotkeys:")
        print("      [F6]  - Toggle Activate / Deactivate")
        print("      [ESC] - Stop and Exit")
        print("==================================================\n")

        t = threading.Thread(target=self.hotkey_thread_fn, daemon=True)
        t.start()

        try:
            while self.running:
                if self.active:
                    self.click()
                    print(f"\r[+] Click #{self.total_clicks} performed at {time.strftime('%H:%M:%S')}! Next in {self.interval}s...", end="", flush=True)
                    
                    # Sleep in small slices so toggle/pause is immediate
                    steps = int(self.interval / 0.1)
                    for _ in range(steps):
                        if not self.running or not self.active:
                            break
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[!] Ctrl+C detected. Exiting.")
        finally:
            self.running = False
            print(f"\n[+] Total clicks performed: {self.total_clicks}")

if __name__ == "__main__":
    interval = 3.0
    if len(sys.argv) > 1:
        try:
            interval = float(sys.argv[1])
        except ValueError:
            pass
    clicker = CLIClicker(interval=interval)
    clicker.run()
