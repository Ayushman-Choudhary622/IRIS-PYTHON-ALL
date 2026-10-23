"""
Eye Blink Mouse Clicker (IRIS Finale)
=====================================
Custom-engineered blink-to-click accessibility software designed for:
- Single-eye blink detection (tracks anatomical Right Eye, ignores permanently closed Left Eye)
- Eyeglasses compatibility (supports clear lenses, blue-cut filters, and anti-glare coatings)
- Variable lighting resilience (handles dim rooms, strong backlights, monitor glare, and shadows)
- Instantaneous left-click trigger (zero perceptible lag via Windows ctypes user32 API)
- Intelligent debouncing & hysteresis (zero duplicate clicks, no clicks when resting closed)

Author: Antigravity AI (Pair Programming with Ayushman Choudhary)
"""

import sys
import os
import time
import json
import threading
import argparse
import ctypes
import numpy as np
import cv2
import mediapipe as mp

# Configure PyAutoGUI as fallback
try:
    import pyautogui
    pyautogui.PAUSE = 0.0
    pyautogui.FAILSAFE = False
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# Windows sound feedback
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iris_config.json")


class MouseController:
    """Handles ultra-low latency mouse clicking on Windows with safe toggle."""
    def __init__(self, enabled=True, sound_feedback=True):
        self.enabled = enabled
        self.sound_feedback = sound_feedback
        self.is_windows = sys.platform == "win32"

    def click(self):
        if not self.enabled:
            return False

        # Windows ctypes mouse_event (instantaneous execution: < 0.05ms)
        if self.is_windows:
            try:
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
            except Exception:
                if HAS_PYAUTOGUI:
                    pyautogui.click()
        elif HAS_PYAUTOGUI:
            pyautogui.click()

        if self.sound_feedback and HAS_WINSOUND:
            threading.Thread(target=self._play_sound, daemon=True).start()

        return True

    def _play_sound(self):
        try:
            winsound.Beep(1600, 25)  # 1600 Hz for 25ms (crisp click tick)
        except Exception:
            pass


class FrameEnhancer:
    """Preprocesses frames to pierce through lens glare, dim lighting, and harsh backlights."""
    _gamma_tables = {}

    @classmethod
    def get_gamma_lut(cls, gamma):
        if gamma not in cls._gamma_tables:
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            cls._gamma_tables[gamma] = table
        return cls._gamma_tables[gamma]

    @staticmethod
    def enhance_frame(frame, mode="auto"):
        """
        Enhances raw frame for robust face mesh landmark extraction.
        - 'auto': Dynamically analyzes face illumination and chooses best filter.
        - 'blue_cut': Suppresses intense cyan/blue monitor glare on lenses.
        - 'dim_backlit': Gamma 1.8 LUT + CLAHE on Y channel to expose shadowed faces.
        - 'normal': Direct unaltered passthrough.
        """
        if mode == "normal":
            return frame

        h, w = frame.shape[:2]

        if mode == "auto":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = float(np.mean(gray))

            # Sample center region where face is expected
            ch, cw = h // 4, w // 4
            center_crop = gray[ch:h - ch, cw:w - cw]
            center_brightness = float(np.mean(center_crop))

            if center_brightness < 100 or mean_brightness < 90:
                mode = "dim_backlit"
            else:
                b_mean = float(np.mean(frame[:, :, 0]))
                r_mean = float(np.mean(frame[:, :, 2]))
                if b_mean > r_mean * 1.12:
                    mode = "blue_cut"
                else:
                    return frame

        if mode == "blue_cut":
            # Suppress blue/cyan screen reflection spikes
            ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(ycrcb)
            clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
            y = clahe.apply(y)
            # Pull blue chroma towards neutral baseline to uncover pupil/eyelid edges
            cb = cv2.addWeighted(cb, 0.70, np.full_like(cb, 128), 0.30, 0)
            return cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2BGR)

        if mode == "dim_backlit":
            # Gamma boost expands deep shadows without clipping bright background lamps
            lut = FrameEnhancer.get_gamma_lut(1.8)
            gamma_frame = cv2.LUT(frame, lut)
            ycrcb = cv2.cvtColor(gamma_frame, cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(ycrcb)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            y = clahe.apply(y)
            return cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2BGR)

        return frame


class EyeTracker:
    """
    Computes Eye Aspect Ratio (EAR) using robust multi-point landmark geometry.
    Specifically tracks the user's open eye (anatomical Right Eye by default)
    and completely ignores the permanently closed Left Eye.
    """
    # MediaPipe landmark indices on UNFLIPPED raw camera frame:
    # Right Eye (User's anatomical right eye):
    # Outer corner: 33, Inner corner: 133
    # Upper eyelid: 160, 159, 158
    # Lower eyelid: 144, 145, 153
    # Iris center: 468
    RIGHT_EYE_LANDMARKS = {
        "width": (33, 133),
        "vertical_pairs": [(160, 144), (159, 145), (158, 153)],
        "iris": 468,
        "contour": [33, 160, 159, 158, 133, 153, 145, 144]
    }

    # Left Eye (User's anatomical left eye):
    # Inner corner: 362, Outer corner: 263
    # Upper eyelid: 385, 386, 387
    # Lower eyelid: 380, 374, 373
    # Iris center: 473
    LEFT_EYE_LANDMARKS = {
        "width": (362, 263),
        "vertical_pairs": [(385, 380), (386, 374), (387, 373)],
        "iris": 473,
        "contour": [362, 385, 386, 387, 263, 373, 374, 380]
    }

    def __init__(self, active_eye="right"):
        self.active_eye = active_eye  # "right", "left", or "auto"

    @staticmethod
    def calculate_ear(landmarks, eye_config, w, h):
        """Calculates multi-point Eye Aspect Ratio (EAR) using 3 vertical pairs."""
        w1_idx, w2_idx = eye_config["width"]
        p_w1 = np.array([landmarks[w1_idx].x * w, landmarks[w1_idx].y * h])
        p_w2 = np.array([landmarks[w2_idx].x * w, landmarks[w2_idx].y * h])
        h_dist = np.linalg.norm(p_w1 - p_w2)
        if h_dist < 1e-5:
            return 0.0

        v_dists = []
        for top_idx, bot_idx in eye_config["vertical_pairs"]:
            p_top = np.array([landmarks[top_idx].x * w, landmarks[top_idx].y * h])
            p_bot = np.array([landmarks[bot_idx].x * w, landmarks[bot_idx].y * h])
            v_dists.append(np.linalg.norm(p_top - p_bot))

        avg_v = sum(v_dists) / len(v_dists)
        return float(avg_v / h_dist)

    def get_eye_metrics(self, landmarks, w, h):
        """Extracts eye tracking metrics for current frame."""
        r_ear = self.calculate_ear(landmarks, self.RIGHT_EYE_LANDMARKS, w, h)
        l_ear = self.calculate_ear(landmarks, self.LEFT_EYE_LANDMARKS, w, h)

        if self.active_eye == "auto":
            # Auto-select whichever eye has higher openness
            target_eye = "right" if r_ear >= l_ear else "left"
        else:
            target_eye = self.active_eye

        config = self.RIGHT_EYE_LANDMARKS if target_eye == "right" else self.LEFT_EYE_LANDMARKS
        ear = r_ear if target_eye == "right" else l_ear

        iris_pt = (int(landmarks[config["iris"]].x * w), int(landmarks[config["iris"]].y * h))
        contour_pts = [
            (int(landmarks[idx].x * w), int(landmarks[idx].y * h))
            for idx in config["contour"]
        ]

        return ear, target_eye, iris_pt, contour_pts, r_ear, l_ear


class BlinkDetector:
    """
    Finite State Machine with:
    - Adaptive Baseline: Tracks natural open-eye EAR drift over time.
    - Dual-Threshold Hysteresis: Closes at close_thresh, recovers at open_thresh.
    - Zero-Latency Click: Fires the exact instant EAR drops below close_thresh.
    - Debounce Lockout / Cooldown: Prevents duplicate clicks during a single blink.
    - Rest/Squint Protection: Eye held closed for prolonged period never repeatedly clicks.
    """
    def __init__(self, drop_ratio=0.28, cooldown_sec=0.38, baseline_alpha=0.03):
        self.drop_ratio = drop_ratio          # Drop from baseline to trigger blink (28%)
        self.cooldown_sec = cooldown_sec      # Cooldown window to debounce (380ms)
        self.baseline_alpha = baseline_alpha  # EMA smoothing factor for baseline
        
        self.baseline = None
        self.state = "OPEN"                   # "OPEN", "COOLDOWN", "WAIT_RECOVERY"
        self.last_click_time = 0.0
        self.click_flash_until = 0.0          # UI visual indicator flash timer
        self.total_clicks = 0
        self.calibrated_threshold = None

    def update(self, ear):
        now = time.time()
        is_click = False

        if ear <= 0.01:
            return False, "NO_FACE", 0.0, self.baseline or 0.30

        # Initialize baseline on first valid frame
        if self.baseline is None:
            self.baseline = ear

        # Calculate active trigger and recovery thresholds
        if self.calibrated_threshold is not None:
            close_thresh = self.calibrated_threshold
            open_thresh = min(self.baseline * 0.95, self.calibrated_threshold * 1.15)
        else:
            close_thresh = self.baseline * (1.0 - self.drop_ratio)
            open_thresh = self.baseline * (1.0 - (self.drop_ratio * 0.45))

        # State Machine Transitions
        if self.state == "OPEN":
            # Smoothly update open-eye baseline only when eye is fully open and steady
            if ear > open_thresh:
                self.baseline = (1.0 - self.baseline_alpha) * self.baseline + self.baseline_alpha * ear

            # Instant Click Trigger
            if ear < close_thresh:
                is_click = True
                self.total_clicks += 1
                self.last_click_time = now
                self.click_flash_until = now + 0.35
                self.state = "COOLDOWN"

        elif self.state == "COOLDOWN":
            # In cooldown lockout: debounce multiple frames of the same blink
            if (now - self.last_click_time) > self.cooldown_sec:
                if ear >= open_thresh:
                    self.state = "OPEN"
                else:
                    self.state = "WAIT_RECOVERY"

        elif self.state == "WAIT_RECOVERY":
            # Prolonged closure protection: must open eye before re-arming
            if ear >= open_thresh:
                self.state = "OPEN"

        return is_click, self.state, close_thresh, self.baseline


class AutoCalibrator:
    """Guided 2-phase calibration to compute exact personal thresholds."""
    def __init__(self):
        self.is_calibrating = False
        self.phase = 0
        self.start_time = 0.0
        self.open_samples = []
        self.closed_samples = []

    def start(self):
        self.is_calibrating = True
        self.phase = 1
        self.start_time = time.time()
        self.open_samples = []
        self.closed_samples = []

    def update(self, ear):
        if not self.is_calibrating:
            return None

        elapsed = time.time() - self.start_time

        if self.phase == 1:
            # Phase 1: 2.0s open eye sampling
            self.open_samples.append(ear)
            if elapsed >= 2.0:
                self.phase = 2
                self.start_time = time.time()
                return "PHASE_2"
            return f"Keep eye OPEN naturally... ({2.0 - elapsed:.1f}s)"

        elif self.phase == 2:
            # Phase 2: 1.5s closed eye sampling
            self.closed_samples.append(ear)
            if elapsed >= 1.5:
                self.is_calibrating = False
                median_open = float(np.median(self.open_samples))
                median_closed = float(np.median(self.closed_samples))
                
                # Midpoint calculation
                threshold = (median_open * 0.45) + (median_closed * 0.55)
                drop_ratio = max(0.14, min(0.45, (median_open - threshold) / median_open))
                
                return {
                    "open_ear": median_open,
                    "closed_ear": median_closed,
                    "threshold": threshold,
                    "drop_ratio": drop_ratio
                }
            return f"Now BLINK / CLOSE eye... ({1.5 - elapsed:.1f}s)"

        return None


class HUDOverlay:
    """Renders a sleek, modern visual interface on the camera feed."""
    COLOR_BG_CARD = (25, 25, 30)
    COLOR_BORDER = (55, 55, 65)
    COLOR_TEXT = (245, 245, 250)
    COLOR_TEXT_DIM = (165, 165, 180)
    COLOR_GREEN = (45, 215, 85)
    COLOR_YELLOW = (0, 215, 255)
    COLOR_CYAN = (255, 225, 0)
    COLOR_RED = (60, 70, 245)

    @classmethod
    def draw_hud(cls, frame, ear, threshold, baseline, state, mode, active_eye, 
                 mouse_enabled, click_flash, clicks_count, calib_msg=None, 
                 iris_pt=None, contour_pts=None, show_landmarks=True):
        h, w = frame.shape[:2]

        # 1. Landmark Contour Overlay
        if show_landmarks and contour_pts is not None and len(contour_pts) > 0:
            pts = np.array(contour_pts, np.int32)
            cv2.polylines(frame, [pts], True, cls.COLOR_GREEN, 1, cv2.LINE_AA)
            for pt in contour_pts:
                cv2.circle(frame, pt, 2, cls.COLOR_CYAN, -1)
            if iris_pt is not None:
                cv2.circle(frame, iris_pt, 3, (0, 0, 255), -1)

        # 2. Click Trigger Flash Banner
        if click_flash:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 75), (0, 210, 255), -1)
            cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)
            cv2.putText(frame, "CLICK TRIGGERED!", (w // 2 - 165, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1.15, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(frame, "CLICK TRIGGERED!", (w // 2 - 165, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1.15, (255, 255, 255), 2, cv2.LINE_AA)

        # 3. Top Info Card
        card_h = 55
        cv2.rectangle(frame, (10, 10), (w - 10, 10 + card_h), cls.COLOR_BG_CARD, -1)
        cv2.rectangle(frame, (10, 10), (w - 10, 10 + card_h), cls.COLOR_BORDER, 1)

        # Mode Badge
        mode_text = f"MODE: [{mode.upper()}]"
        cv2.putText(frame, mode_text, (25, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cls.COLOR_CYAN, 2, cv2.LINE_AA)

        # Active Eye Badge
        eye_text = f"TRACKING: {active_eye.upper()} EYE (Left Ignored)"
        cv2.putText(frame, eye_text, (230, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, cls.COLOR_TEXT, 1, cv2.LINE_AA)

        # Mouse Status Badge
        mouse_color = cls.COLOR_GREEN if mouse_enabled else cls.COLOR_RED
        mouse_str = "MOUSE: ON" if mouse_enabled else "MOUSE: OFF"
        cv2.putText(frame, mouse_str, (w - 155, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, mouse_color, 2, cv2.LINE_AA)

        cv2.putText(frame, f"Clicks: {clicks_count}", (w - 155, 56),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, cls.COLOR_TEXT_DIM, 1, cv2.LINE_AA)

        # 4. EAR Gauge Bar (Bottom Card)
        gauge_y = h - 75
        cv2.rectangle(frame, (10, gauge_y), (w - 10, h - 15), cls.COLOR_BG_CARD, -1)
        cv2.rectangle(frame, (10, gauge_y), (w - 10, h - 15), cls.COLOR_BORDER, 1)

        ear_str = f"EAR: {ear:.3f}" if ear > 0 else "EAR: --"
        cv2.putText(frame, ear_str, (25, gauge_y + 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, cls.COLOR_TEXT, 2, cv2.LINE_AA)

        bar_x = 160
        bar_w = w - 340
        bar_h = 16
        bar_y = gauge_y + 14

        # Background track
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 60), -1)

        # Level fill
        max_ear_display = 0.42
        fill_ratio = max(0.0, min(1.0, ear / max_ear_display))
        fill_w = int(bar_w * fill_ratio)

        bar_color = cls.COLOR_GREEN if ear >= threshold else cls.COLOR_RED
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), bar_color, -1)

        # Threshold Cutoff Marker
        thresh_x = int(bar_x + bar_w * (threshold / max_ear_display))
        if bar_x <= thresh_x <= bar_x + bar_w:
            cv2.line(frame, (thresh_x, bar_y - 4), (thresh_x, bar_y + bar_h + 4), cls.COLOR_YELLOW, 2)
            cv2.putText(frame, f"Cut:{threshold:.2f}", (thresh_x - 22, bar_y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, cls.COLOR_YELLOW, 1, cv2.LINE_AA)

        state_color = cls.COLOR_GREEN if state == "OPEN" else cls.COLOR_YELLOW
        cv2.putText(frame, f"[{state}]", (w - 165, gauge_y + 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, state_color, 2, cv2.LINE_AA)

        # Guided Calibration Prompt
        if calib_msg:
            msg_overlay = frame.copy()
            cv2.rectangle(msg_overlay, (w // 6, h // 2 - 40), (5 * w // 6, h // 2 + 40), (20, 20, 25), -1)
            cv2.rectangle(msg_overlay, (w // 6, h // 2 - 40), (5 * w // 6, h // 2 + 40), cls.COLOR_CYAN, 2)
            cv2.addWeighted(msg_overlay, 0.88, frame, 0.12, 0, frame)
            cv2.putText(frame, calib_msg, (w // 6 + 25, h // 2 + 10),
                        cv2.FONT_HERSHEY_DUPLEX, 0.70, cls.COLOR_TEXT, 2, cv2.LINE_AA)

        # 5. Hotkey Legend Bar
        legend = "[1]Auto [2]BlueCut [3]Dim [4]Normal | [C]Calibrate | [M]Mouse | [E]Eye | [V]Mirror | [Q]Quit"
        cv2.putText(frame, legend, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, cls.COLOR_TEXT_DIM, 1, cv2.LINE_AA)

        return frame


def load_config():
    """Loads saved settings from disk."""
    defaults = {
        "mode": "auto",
        "active_eye": "right",
        "drop_ratio": 0.28,
        "cooldown_sec": 0.38,
        "calibrated_threshold": None,
        "mouse_enabled": True,
        "mirror_view": True,
        "sound_feedback": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_config(cfg):
    """Saves settings to disk."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"Notice: could not save config: {e}")


def run(camera_index=0, initial_mode=None, initial_eye=None):
    """Main execution loop for eye blink detection and clicking."""
    cfg = load_config()

    mode = initial_mode or cfg.get("mode", "auto")
    active_eye = initial_eye or cfg.get("active_eye", "right")
    drop_ratio = cfg.get("drop_ratio", 0.28)
    cooldown_sec = cfg.get("cooldown_sec", 0.38)
    mouse_enabled = cfg.get("mouse_enabled", True)
    mirror_view = cfg.get("mirror_view", True)
    sound_feedback = cfg.get("sound_feedback", True)

    mouse = MouseController(enabled=mouse_enabled, sound_feedback=sound_feedback)
    tracker = EyeTracker(active_eye=active_eye)
    detector = BlinkDetector(drop_ratio=drop_ratio, cooldown_sec=cooldown_sec)

    if cfg.get("calibrated_threshold"):
        detector.calibrated_threshold = cfg["calibrated_threshold"]
        print(f"Loaded calibrated cutoff threshold: {detector.calibrated_threshold:.3f}")

    calibrator = AutoCalibrator()

    print("=" * 68)
    print(" IRIS FINALE: Eye Blink Mouse Clicker")
    print("=" * 68)
    print(f" Active Tracking Eye : {active_eye.upper()} EYE (Left eye ignored)")
    print(f" Environment Mode    : {mode.upper()}")
    print(f" Mouse Click Trigger : {'ACTIVE' if mouse.enabled else 'DISABLED'}")
    print(f" Sound Feedback      : {'ACTIVE' if sound_feedback else 'OFF'}")
    print(f" Mirror Selfie View  : {'ON' if mirror_view else 'OFF'}")
    print(" Hotkeys:")
    print("   [1] Auto-Adaptive  [2] Blue-Cut Glasses  [3] Dim/Backlit  [4] Normal")
    print("   [C] Start Guided Calibration (takes 3.5 seconds)")
    print("   [M] Toggle Mouse Clicking ON / OFF")
    print("   [E] Switch Active Eye (Right / Left)")
    print("   [V] Toggle Mirror Selfie View")
    print("   [S] Toggle Sound Feedback")
    print("   [+] Increase Sensitivity (triggers easier)")
    print("   [-] Decrease Sensitivity (requires deeper blink)")
    print("   [L] Toggle Landmark Overlay")
    print("   [Q] / [ESC] Quit")
    print("=" * 68)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Unable to open camera index {camera_index}!")
        return

    # Minimize internal frame buffer for zero latency
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    show_landmarks = True
    calib_display_msg = None

    try:
        while True:
            ret, raw_frame = cap.read()
            if not ret:
                print("Warning: Failed to grab frame from camera.")
                break

            h, w = raw_frame.shape[:2]

            # 1. Image Enhancement on raw frame
            proc_frame = FrameEnhancer.enhance_frame(raw_frame, mode=mode)

            # 2. MediaPipe Face Mesh inference on raw frame
            # Processing raw un-flipped frame guarantees MediaPipe's anatomical
            # landmarks correspond strictly to Right Eye vs Left Eye!
            rgb = cv2.cvtColor(proc_frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            ear = 0.0
            iris_pt = None
            contour_pts = None

            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark
                ear, target_eye, iris_pt, contour_pts, r_ear, l_ear = tracker.get_eye_metrics(lm, w, h)

                # Guided Calibration
                if calibrator.is_calibrating:
                    calib_res = calibrator.update(ear)
                    if isinstance(calib_res, dict):
                        detector.calibrated_threshold = calib_res["threshold"]
                        detector.drop_ratio = calib_res["drop_ratio"]
                        detector.baseline = calib_res["open_ear"]
                        cfg["calibrated_threshold"] = calib_res["threshold"]
                        cfg["drop_ratio"] = calib_res["drop_ratio"]
                        save_config(cfg)
                        calib_display_msg = f"Calibrated! Cutoff: {calib_res['threshold']:.3f}"
                        threading.Timer(2.5, lambda: globals().update(calib_display_msg=None)).start()
                    elif isinstance(calib_res, str):
                        calib_display_msg = calib_res
                else:
                    # Blink Detection & Instant Click
                    is_click, state, thresh, baseline = detector.update(ear)
                    if is_click:
                        mouse.click()
            else:
                detector.update(0.0)

            # 3. Mirror transformation for natural selfie display
            display_frame = raw_frame.copy()
            if mirror_view:
                display_frame = cv2.flip(display_frame, 1)
                if iris_pt is not None:
                    iris_pt = (w - 1 - iris_pt[0], iris_pt[1])
                if contour_pts is not None:
                    contour_pts = [(w - 1 - pt[0], pt[1]) for pt in contour_pts]

            # 4. Render HUD Overlay
            now = time.time()
            click_flash = (now < detector.click_flash_until)
            active_thresh = detector.calibrated_threshold or (detector.baseline * (1.0 - detector.drop_ratio) if detector.baseline else 0.20)

            display_frame = HUDOverlay.draw_hud(
                frame=display_frame,
                ear=ear,
                threshold=active_thresh,
                baseline=detector.baseline or 0.30,
                state=detector.state,
                mode=mode,
                active_eye=tracker.active_eye,
                mouse_enabled=mouse.enabled,
                click_flash=click_flash,
                clicks_count=detector.total_clicks,
                calib_msg=calib_display_msg,
                iris_pt=iris_pt,
                contour_pts=contour_pts,
                show_landmarks=show_landmarks
            )

            cv2.imshow("IRIS FINALE - Eye Blink Mouse Clicker", display_frame)

            # 5. Handle Keyboard Controls
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), ord('Q'), 27]:
                break
            elif key == ord('1'):
                mode = "auto"
                cfg["mode"] = mode
                save_config(cfg)
                print("Mode set to: AUTO-ADAPTIVE")
            elif key == ord('2'):
                mode = "blue_cut"
                cfg["mode"] = mode
                save_config(cfg)
                print("Mode set to: BLUE-CUT LENS (Anti-glare)")
            elif key == ord('3'):
                mode = "dim_backlit"
                cfg["mode"] = mode
                save_config(cfg)
                print("Mode set to: DIM & BACKLIT")
            elif key == ord('4'):
                mode = "normal"
                cfg["mode"] = mode
                save_config(cfg)
                print("Mode set to: NORMAL")
            elif key in [ord('m'), ord('M'), 32]:  # Space or M
                mouse.enabled = not mouse.enabled
                cfg["mouse_enabled"] = mouse.enabled
                save_config(cfg)
                print(f"Mouse Click: {'ENABLED' if mouse.enabled else 'DISABLED'}")
            elif key in [ord('c'), ord('C')]:
                print("Starting Guided Calibration...")
                calibrator.start()
            elif key in [ord('e'), ord('E')]:
                tracker.active_eye = "left" if tracker.active_eye == "right" else "right"
                cfg["active_eye"] = tracker.active_eye
                save_config(cfg)
                print(f"Active tracking eye switched to: {tracker.active_eye.upper()}")
            elif key in [ord('v'), ord('V')]:
                mirror_view = not mirror_view
                cfg["mirror_view"] = mirror_view
                save_config(cfg)
                print(f"Mirror Selfie View: {'ON' if mirror_view else 'OFF'}")
            elif key in [ord('s'), ord('S')]:
                mouse.sound_feedback = not mouse.sound_feedback
                cfg["sound_feedback"] = mouse.sound_feedback
                save_config(cfg)
                print(f"Sound Feedback: {'ON' if mouse.sound_feedback else 'OFF'}")
            elif key in [ord('+'), ord('=')]:
                detector.drop_ratio = max(0.12, detector.drop_ratio - 0.03)
                cfg["drop_ratio"] = detector.drop_ratio
                save_config(cfg)
                print(f"Sensitivity increased (Drop ratio: {detector.drop_ratio:.2f})")
            elif key in [ord('-'), ord('_')]:
                detector.drop_ratio = min(0.48, detector.drop_ratio + 0.03)
                cfg["drop_ratio"] = detector.drop_ratio
                save_config(cfg)
                print(f"Sensitivity decreased (Drop ratio: {detector.drop_ratio:.2f})")
            elif key in [ord('l'), ord('L')]:
                show_landmarks = not show_landmarks

    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()
        print("Session complete. Settings safely saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRIS FINALE - Single Eye Blink Mouse Clicker")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index (default: 0)")
    parser.add_argument("--mode", type=str, choices=["auto", "blue_cut", "dim_backlit", "normal"],
                        default=None, help="Environment preset mode")
    parser.add_argument("--eye", type=str, choices=["right", "left", "auto"],
                        default=None, help="Eye to track (default: right)")
    parser.add_argument("--no-mouse", action="store_true", help="Start with mouse clicking disabled")
    args = parser.parse_args()

    init_mode = args.mode
    init_eye = args.eye
    if args.no_mouse:
        cfg = load_config()
        cfg["mouse_enabled"] = False
        save_config(cfg)

    run(camera_index=args.camera, initial_mode=init_mode, initial_eye=init_eye)
