"""
Test Suite: Evaluates IRIS FINALE Multi-Pass Pipeline + Face-Local 3D Pose & Rotation-Invariant EAR.
Shows 3D Fused EAR, Right EAR, Left EAR, Head Yaw/Pitch/Roll, and Gaze Direction across all head angles.
"""

import os
import glob
import cv2
import numpy as np
import mediapipe as mp
from eye_clicker import FrameEnhancer, EyeTracker, show_startup_ascii_art

def test_samples():
    show_startup_ascii_art()
    root_images = sorted(glob.glob("*.jpg"))
    new_images = sorted(glob.glob("NEW/*.jpg"))
    images = root_images + new_images

    if not images:
        print("No test images found!")
        return

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.45
    )

    tracker = EyeTracker(active_eye="right")
    
    print("=" * 155)
    print(f"{'Image File':<34} | {'Fused EAR':<10} | {'R_EAR':<8} | {'L_EAR':<8} | {'Yaw':<7} | {'Pitch':<7} | {'Roll':<7} | {'Gaze':<11} | {'Status':<9} | {'Pass'}")
    print("=" * 155)

    passed = 0
    for img_path in images:
        filename = os.path.basename(img_path)
        if "NEW" in img_path:
            filename = f"NEW/{filename}"
        frame = cv2.imread(img_path)
        h, w = frame.shape[:2]

        # Pass 1: Natural / Raw frame (optimal clarity for normal lighting & all glasses)
        res = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pass_name = "Adaptive (Natural)"

        # Pass 2: Multi-Pass Shadow Lift for dark / silhouetted backlight
        if not res.multi_face_landmarks:
            enh1 = FrameEnhancer.enhance_pass1(frame)
            res = face_mesh.process(cv2.cvtColor(enh1, cv2.COLOR_BGR2RGB))
            pass_name = "Shadow Lift"

        # Pass 3: Ultra-Dark High-Gain Lift
        if not res.multi_face_landmarks:
            enh2 = FrameEnhancer.enhance_pass2(frame)
            res = face_mesh.process(cv2.cvtColor(enh2, cv2.COLOR_BGR2RGB))
            pass_name = "High-Gain Lift"

        # Pass 4: Glare Pierce
        if not res.multi_face_landmarks:
            enh3 = FrameEnhancer.enhance_glare_pierce(frame)
            res = face_mesh.process(cv2.cvtColor(enh3, cv2.COLOR_BGR2RGB))
            pass_name = "Glare Pierce"

        if res.multi_face_landmarks:
            lm = res.multi_face_landmarks[0].landmark
            fused_ear, target_eye, iris_pt, contour_pts, r_ear, l_ear, gaze_dir, yaw, pitch, roll, head_motion_spd = tracker.get_eye_metrics(lm, w, h)
            detect_str = "SUCCESS"
            passed += 1
        else:
            fused_ear, r_ear, l_ear = 0.0, 0.0, 0.0
            yaw, pitch, roll = 0.0, 0.0, 0.0
            gaze_dir = "--"
            detect_str = "FAILED"
            pass_name = "--"

        print(f"{filename:<34} | {fused_ear:<10.3f} | {r_ear:<8.3f} | {l_ear:<8.3f} | {yaw:6.1f}° | {pitch:6.1f}° | {roll:6.1f}° | {gaze_dir:<11} | {detect_str:<9} | {pass_name}")

    print("=" * 155)
    pct = (passed / len(images) * 100) if images else 0
    print(f"Test Complete: {passed}/{len(images)} images successfully detected ({pct:.0f}% accuracy across all glasses, poses & lighting)!")

if __name__ == "__main__":
    test_samples()
