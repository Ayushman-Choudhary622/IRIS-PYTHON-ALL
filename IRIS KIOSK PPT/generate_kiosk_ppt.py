"""
Generate High-Impact Animated Kiosk Presentation for Project IRIS
Vivo Ignite National Finale at Bharat Mandapam, New Delhi
Presenter: Ayushman Choudhary
14 Slides - 16:9 Widescreen - Hyper-Realistic Dark Cyber-Medical Aesthetic
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

MEDIA_DIR = "extracted_ppt_media"
LOGO_IMG = os.path.join("IRIS UNIVERSAL", "images", "iris-logo-original-clean.png")

# --- COLOR PALETTE ---
BG_DARK = RGBColor(10, 13, 20)           # #0A0D14
CARD_BG = RGBColor(18, 24, 38)           # #121826
CARD_BORDER = RGBColor(36, 48, 72)       # #243048
CARD_BG_ELEVATED = RGBColor(24, 32, 50)  # #182032
CARD_BG_HIGHLIGHT = RGBColor(15, 30, 55) # #0F1E37

CYAN_ACCENT = RGBColor(0, 242, 254)      # #00F2FE
CYAN_DIM = RGBColor(0, 160, 180)         # #00A0B4
BLUE_GLOW = RGBColor(0, 114, 255)        # #0072FF
TEXT_WHITE = RGBColor(255, 255, 255)     # #FFFFFF
TEXT_MUTED = RGBColor(148, 163, 184)     # #94A3B8
TEXT_DIM = RGBColor(100, 116, 139)       # #64748B
GREEN_WIN = RGBColor(0, 230, 118)        # #00E676
RED_ALERT = RGBColor(255, 59, 92)        # #FF3B5C
AMBER_WARN = RGBColor(255, 179, 0)       # #FFB300

FONT_HEAD = "Arial Black"
FONT_SUB = "Segoe UI Semibold"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def apply_kiosk_transition(slide, auto_advance_ms=6500):
    """Injects slide transition and auto-advance timing for Kiosk Mode."""
    try:
        xml_str = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" advTm="{auto_advance_ms}"><p:morph/></p:transition>'
        slide._element.append(parse_xml(xml_str))
    except Exception as e:
        print(f"Warning: could not inject transition: {e}")

def create_base_slide():
    """Creates a blank slide with obsidian dark background and subtle cyan header line."""
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()

    # Top ambient glow line
    glow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CYAN_ACCENT
    glow.line.fill.background()

    apply_kiosk_transition(slide)
    return slide

def add_header(slide, eyebrow, title, category="PROJECT IRIS v2.0 · KIOSK DISPLAY"):
    """Adds standard cinematic header."""
    # Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.8), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG_ELEVATED
    badge.line.color.rgb = CARD_BORDER
    badge.line.width = Pt(1)
    tf = badge.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = category.upper()
    p.font.name = FONT_SUB
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # Top right event branding
    tx_r = slide.shapes.add_textbox(Inches(8.5), Inches(0.35), Inches(4.0), Inches(0.35))
    p_r = tx_r.text_frame.paragraphs[0]
    p_r.text = "VIVO IGNITE NATIONAL FINALE · BHARAT MANDAPAM"
    p_r.font.name = FONT_SUB
    p_r.font.size = Pt(9.5)
    p_r.font.bold = True
    p_r.font.color.rgb = TEXT_MUTED
    p_r.alignment = PP_ALIGN.RIGHT

    # Eyebrow
    tx_eye = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.3))
    p_eye = tx_eye.text_frame.paragraphs[0]
    p_eye.text = eyebrow.upper()
    p_eye.font.name = FONT_SUB
    p_eye.font.size = Pt(11)
    p_eye.font.bold = True
    p_eye.font.color.rgb = CYAN_ACCENT

    # Title
    tx_t = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.65))
    p_t = tx_t.text_frame.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEAD
    p_t.font.size = Pt(23)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

def create_card(slide, left, top, width, height, border_color=CARD_BORDER, bg_color=CARD_BG):
    """Creates rounded rectangular card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    return card

def add_image_safely(slide, img_path, left, top, width, height, frame=True):
    """Adds an image safely if exists, with optional glass frame."""
    if os.path.exists(img_path):
        if frame:
            # Outer frame
            create_card(slide, left - Inches(0.06), top - Inches(0.06), width + Inches(0.12), height + Inches(0.12), border_color=CYAN_DIM, bg_color=CARD_BG_ELEVATED)
        slide.shapes.add_picture(img_path, left, top, width, height)
        return True
    return False

# ==========================================
# SLIDE 1: CINEMATIC HERO COVER
# ==========================================
s1 = create_base_slide()

# Left Column (Hero Content)
badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(5.6), Inches(0.38))
badge1.fill.solid()
badge1.fill.fore_color.rgb = CARD_BG_ELEVATED
badge1.line.color.rgb = CYAN_ACCENT
badge1.line.width = Pt(1)
p = badge1.text_frame.paragraphs[0]
p.text = "VIVO IGNITE NATIONAL FINALE · BHARAT MANDAPAM, NEW DELHI"
p.font.name = FONT_SUB
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p.alignment = PP_ALIGN.CENTER

# Main Title
t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.8), Inches(1.1))
p = t1.text_frame.paragraphs[0]
p.text = "PROJECT IRIS · v2.0"
p.font.name = FONT_HEAD
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

# Subtitle / Hook
sub1 = s1.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(6.8), Inches(1.2))
tf = sub1.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "A Blink Becomes a Click. A Tilt Becomes a Cursor."
p0.font.name = FONT_HEAD
p0.font.size = Pt(20)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT

p1 = tf.add_paragraph()
p1.text = "An ₹800 open-source assistive wearable restoring full digital agency and voice communication to patients with Locked-In Syndrome, ALS & severe paralysis."
p1.font.name = FONT_BODY
p1.font.size = Pt(13)
p1.font.color.rgb = TEXT_MUTED
p1.space_before = Pt(8)

# 4 Core Innovation Badges
badges = [
    ("950nm Optical Reflectance", "Digital eye open/close"),
    ("6-DOF Inertial Steering", "Smooth MPU6050 head tilt"),
    ("BLE 5.0 + Wi-Fi Telemetry", "Thumb-sized ESP32-C3"),
    ("₹800 vs ₹25,00,000", "99.96% price disruption")
]
for i, (b_title, b_sub) in enumerate(badges):
    bx = Inches(0.8) + (i % 2) * Inches(3.3)
    by = Inches(3.8) + (i // 2) * Inches(1.1)
    b_card = create_card(s1, bx, by, Inches(3.1), Inches(0.95), border_color=CARD_BORDER, bg_color=CARD_BG)
    tb = s1.shapes.add_textbox(bx + Inches(0.12), by + Inches(0.08), Inches(2.86), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = b_title
    p.font.name = FONT_SUB
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p2 = tf.add_paragraph()
    p2.text = b_sub
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_MUTED

# Presenter Card
pres_card = create_card(s1, Inches(0.8), Inches(6.15), Inches(6.4), Inches(0.9), border_color=CARD_BORDER, bg_color=CARD_BG_ELEVATED)
tb_pres = s1.shapes.add_textbox(Inches(0.95), Inches(6.2), Inches(6.1), Inches(0.8))
tf = tb_pres.text_frame
p0 = tf.paragraphs[0]
p0.text = "Ayushman Choudhary  ·  Class 10th"
p0.font.name = FONT_SUB
p0.font.size = Pt(13)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT

p1 = tf.add_paragraph()
p1.text = "Bhavan’s B.P. Vidya Mandir Ashti, Nagpur, Maharashtra"
p1.font.name = FONT_BODY
p1.font.size = Pt(10.5)
p1.font.color.rgb = TEXT_WHITE

# Right Column - Real Prototype Photo
hero_img = os.path.join(MEDIA_DIR, "image1.jpg")
add_image_safely(s1, hero_img, Inches(7.8), Inches(0.7), Inches(4.7), Inches(6.35), frame=True)

# Overlay tag on image
live_tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(6.5), Inches(4.3), Inches(0.42))
live_tag.fill.solid()
live_tag.fill.fore_color.rgb = RGBColor(10, 13, 20)
live_tag.line.color.rgb = GREEN_WIN
p = live_tag.text_frame.paragraphs[0]
p.text = "● LIVE HARDWARE PROTOTYPE · READY FOR DEMO"
p.font.name = FONT_SUB
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = GREEN_WIN
p.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 2: THE TRAGEDY & THE UNREACHABLE WALL
# ==========================================
s2 = create_base_slide()
add_header(s2, "THE CRISIS · LOCKED-IN SYNDROME & ALS", "Trapped Inside a Conscious Mind.")

# 3 Stat Cards
stat_data = [
    ("240K+", "Paralyzed Indians", "Living with locked-in syndrome, ALS, stroke & severe spinal injuries with fully intact cognitive minds.", CYAN_ACCENT),
    ("₹25L+", "Commercial Monopoly", "Imported optical eye-trackers (Tobii Dynavox) cost as much as a luxury car—financially impossible for Indian families.", RED_ALERT),
    ("0", "Affordable Options", "Zero reliable, high-accuracy sub-₹2,000 assistive cursor devices exist in the healthcare market today.", AMBER_WARN)
]

for i, (val, lbl, desc, col) in enumerate(stat_data):
    cx = Inches(0.8) + i * Inches(3.95)
    card = create_card(s2, cx, Inches(1.8), Inches(3.8), Inches(3.2))
    tx = s2.shapes.add_textbox(cx + Inches(0.25), Inches(1.95), Inches(3.3), Inches(2.9))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = val
    p.font.name = FONT_HEAD
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = col
    
    p2 = tf.add_paragraph()
    p2.text = lbl.upper()
    p2.font.name = FONT_SUB
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(10)

# Bottom Callout Banner
bot_card = create_card(s2, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.8), border_color=CYAN_DIM, bg_color=CARD_BG_HIGHLIGHT)
tx_bot = s2.shapes.add_textbox(Inches(1.0), Inches(5.35), Inches(11.3), Inches(1.6))
tf = tx_bot.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THE CLINICAL REALITY:"
p.font.name = FONT_SUB
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p2 = tf.add_paragraph()
p2.text = "Paralyzed individuals lose peripheral limb movement, but in over 95% of cases, two voluntary motor signals remain intact: micro head rotation and deliberate eye blinks. IRIS bridges these exact two biological channels into a high-precision computer mouse for ₹800."
p2.font.name = FONT_BODY
p2.font.size = Pt(12.5)
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)


# ==========================================
# SLIDE 3: THE DISRUPTIVE BREAKTHROUGH
# ==========================================
s3 = create_base_slide()
add_header(s3, "DISRUPTIVE INNOVATION", "The ₹800 Breakthrough: 99.96% Cheaper.")

# Left Card: Commercial Monopoly
c_left = create_card(s3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.0), border_color=RED_ALERT, bg_color=CARD_BG)
t_left = s3.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(3.7))
tf = t_left.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "COMMERCIAL STATUS QUO"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RED_ALERT

p2 = tf.add_paragraph()
p2.text = "Tobii Dynavox I-Series: ₹25,00,000+"
p2.font.name = FONT_HEAD
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)

tobii_points = [
    "High-speed binocular cameras that fail under sunlight or lens glare",
    "Forces purchase of proprietary locked 4kg tablets",
    "Requires 30+ minutes tedious calibration by clinical specialists",
    "Closed patent monopoly with 40-60% Indian import customs duty",
    "Result: Completely inaccessible to 99.9% of Indian patients"
]
for pt in tobii_points:
    p = tf.add_paragraph()
    p.text = f"•  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

# Right Card: Project IRIS
c_right = create_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.0), border_color=CYAN_ACCENT, bg_color=CARD_BG_HIGHLIGHT)
t_right = s3.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(3.7))
tf = t_right.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PROJECT IRIS DISRUPTION"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_WIN

p2 = tf.add_paragraph()
p2.text = "Total Prototype BOM: ₹800"
p2.font.name = FONT_HEAD
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = CYAN_ACCENT
p2.space_before = Pt(4)

iris_points = [
    "950nm Optical Reflectance: Works in total darkness or direct sunlight",
    "Works on any existing family laptop, PC, Android, or tablet",
    "Self-calibrating in 2–3 seconds with saved returning user profiles",
    "Built using locally available off-the-shelf micro-electronics",
    "100% Free & Open-Source (CERN-OHL & GPL): Reproducible anywhere"
]
for pt in iris_points:
    p = tf.add_paragraph()
    p.text = f"✔  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)

# Bottom Stat Ribbon
bot_rib = create_card(s3, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.0), border_color=CARD_BORDER, bg_color=CARD_BG_ELEVATED)
tx_rib = s3.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.8))
tf = tx_rib.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "PRICE DISRUPTION: 99.96% CHEAPER  |  CALIBRATION: 2–3 SECONDS  |  BATTERY RUNTIME: 12+ HOURS"
p.font.name = FONT_HEAD
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GREEN_WIN
p.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 4: DUAL-RIG ERGONOMIC HARDWARE ARCHITECTURE
# ==========================================
s4 = create_base_slide()
add_header(s4, "HARDWARE ERGONOMICS & THERMAL DESIGN", "Two Detached Systems. Zero Scalp Heating.")

# Left Card: Headband
c1 = create_card(s4, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.2))
tx1 = s4.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(3.3), Inches(4.9))
tf1 = tx1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "RIG 1: AIRFLOW HEADBAND"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p2 = tf1.add_paragraph()
p2.text = "Perforated Mesh Belt"
p2.font.name = FONT_HEAD
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)

hb_points = [
    "Houses Seeed XIAO ESP32-C3, MPU6050 IMU, Li-Po & safety fuses",
    "Continuous Scalp Airflow: Breathable anti-sweat mesh prevents heating",
    "Zero Rigid Plastics: Eliminates pressure ulcers on bedridden patients",
    "Featherweight: Entire headband rig weighs less than 58 grams",
    "Soft Velcro cinch adjusts to any adult or pediatric head circumference"
]
for pt in hb_points:
    p = tf1.add_paragraph()
    p.text = f"•  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

# Middle Card: Magnetic Eyewear
c2 = create_card(s4, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.2))
tx2 = s4.shapes.add_textbox(Inches(5.0), Inches(1.95), Inches(3.3), Inches(4.9))
tf2 = tx2.text_frame
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "RIG 2: MAGNETIC EYEWEAR"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_WIN

p2 = tf2.add_paragraph()
p2.text = "N52 Quick-Snap Pivot"
p2.font.name = FONT_HEAD
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)

eye_points = [
    "Glasses carry ONLY the ultra-light 950nm IR sensor (zero electronics)",
    "N52 Neodymium Snap: Put glasses on first, snap sensor on in 1 second",
    "Universal Rx Support: Fits any frame and up to ±7.0D prescription lenses",
    "Friction Nut-Bolt Pivot: Easy angle adjustment without bending wires",
    "Overcomes Camera Glare: Positions optical beam below lens reflection lines"
]
for pt in eye_points:
    p = tf2.add_paragraph()
    p.text = f"•  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

# Right: Real Prototype Image
add_image_safely(s4, os.path.join(MEDIA_DIR, "image8.jpg"), Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.2), frame=True)


# ==========================================
# SLIDE 5: TRANSPARENT BOM TEARDOWN (₹800)
# ==========================================
s5 = create_base_slide()
add_header(s5, "TRANSPARENT ENGINEERING", "Every Rupee Engineered for Maximum Accessibility.")

bom_items = [
    ("Seeed Studio XIAO ESP32-C3", "₹250", "RISC-V 32-bit @ 160MHz, BLE 5.0 + Wi-Fi, integrated Li-Po charge circuit eliminates bulky external power shields."),
    ("MPU6050 6-DOF IMU Sensor", "₹120", "Fast I2C @ 400kHz, 3-axis gyro + accel, streams 50Hz continuous pitch/roll for smooth cursor steering."),
    ("950nm Multi-Beam IR Module", "₹100", "Safe diffused infrared (<0.5 mW/cm²), onboard LM393 analog comparator gives instantaneous hardware digitalRead."),
    ("3.7V 1000mAh Li-Po Battery", "₹125", "Direct charging via XIAO pads, 12+ hours continuous runtime with Deep Sleep firmware and 2A safety fuse protection."),
    ("N52 Magnetic Pivot Mount", "₹75", "Quick-release neodymium magnetic mount + friction pivot; zero lens scratching; fits custom prescription frames."),
    ("Medical Ventilated Headband", "₹130", "Perforated airflow fabric, soft Velcro closure, zero pressure points, total rig weight under 58 grams.")
]

for i, (title, cost, desc) in enumerate(bom_items):
    col = i % 3
    row = i // 3
    cx = Inches(0.8) + col * Inches(3.95)
    cy = Inches(1.8) + row * Inches(2.25)
    
    card = create_card(s5, cx, cy, Inches(3.8), Inches(2.1))
    tx = s5.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), Inches(3.4), Inches(1.8))
    tf = tx.text_frame
    tf.word_wrap = True
    
    # Title & Cost on top
    p = tf.paragraphs[0]
    p.text = f"{title.upper()}"
    p.font.name = FONT_SUB
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    
    p_cost = tf.add_paragraph()
    p_cost.text = f"BOM COST: {cost}"
    p_cost.font.name = FONT_HEAD
    p_cost.font.size = Pt(14)
    p_cost.font.bold = True
    p_cost.font.color.rgb = CYAN_ACCENT
    p_cost.space_before = Pt(2)
    
    p_desc = tf.add_paragraph()
    p_desc.text = desc
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(4)

# Bottom Highlight
bot_bom = create_card(s5, Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.7), border_color=GREEN_WIN, bg_color=CARD_BG_HIGHLIGHT)
tx_b = s5.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.55))
p = tx_b.text_frame.paragraphs[0]
p.text = "TOTAL SYSTEM BUILD COST: ₹800  |  COMMERCIAL TOBII: ₹25,00,000+  |  SAVINGS: 99.96%"
p.font.name = FONT_HEAD
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = GREEN_WIN
p.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 6: SENSING PHYSICS & ZERO-LAG SENSING
# ==========================================
s6 = create_base_slide()
add_header(s6, "PHYSICAL SENSING ENGINE", "How Light Reads the Eye in Darkness & Sunlight.")

phys_cards = [
    ("OPEN EYE · CURSOR ACTIVE", "High Reflectance (94%)", [
        "950nm diffused infrared beam directed at outer canthus of the eye",
        "White sclera tissue reflects optical energy strongly back to phototransistor",
        "Sensor outputs steady HIGH voltage state (~94% reflectance)",
        "Microcontroller interprets state as ACTIVE EYE: cursor steers smoothly"
    ], CYAN_ACCENT),
    ("CLOSED EYE · CLICK TRIGGER", "Low Reflectance (<20%)", [
        "When patient closes eyelid, skin absorbs and deflects the 950nm beam",
        "Immediate sharp drop in optical energy reaching phototransistor",
        "Sensor outputs LOW voltage state (<20% reflectance)",
        "Firmware timer initiates blink duration measurement for click classification"
    ], AMBER_WARN),
    ("LM393 HARDWARE COMPARATOR", "Zero MCU Lag / Analog Silicon", [
        "Onboard LM393 comparator compares reflectance against calibrated threshold",
        "Decides open vs. closed in pure analog silicon in less than 1 microsecond",
        "Firmware uses digitalRead() instead of analogRead()—zero ADC compute waste",
        "Immune to ambient light: works identically in pitch darkness or direct sunlight"
    ], GREEN_WIN)
]

for i, (title, sub, pts, col) in enumerate(phys_cards):
    cx = Inches(0.8) + i * Inches(3.95)
    card = create_card(s6, cx, Inches(1.8), Inches(3.8), Inches(5.2), border_color=col)
    tx = s6.shapes.add_textbox(cx + Inches(0.25), Inches(1.95), Inches(3.3), Inches(4.9))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SUB
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = col
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)
    
    for pt in pts:
        p3 = tf.add_paragraph()
        p3.text = f"•  {pt}"
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(8)


# ==========================================
# SLIDE 7: CLICK LOGIC & NEURAL DENOISING
# ==========================================
s7 = create_base_slide()
add_header(s7, "GESTURE & TIMING LOGIC", "Separating Conscious Intent from Involuntary Reflex.")

click_cards = [
    ("NATURAL REFLEX BLINK", "< 200 ms", "Completely Ignored", "Fast involuntary corneal hydration blink. Filtered out before any click event is generated. Cursor never twitches or misfires.", TEXT_MUTED),
    ("SINGLE DELIBERATE BLINK", "200 – 500 ms", "Left Click (LC)", "Deliberately held blink beyond reflex threshold. Emits a clean Left Click to select menu tiles, emergency alarms, or trigger speech.", CYAN_ACCENT),
    ("DOUBLE DELIBERATE BLINK", "2x < 600 ms", "Right Click (RC)", "Two held blinks in quick succession within a 600ms timing window. Emits an instant Right Click for secondary context options.", GREEN_WIN),
    ("ERGONOMIC CLUTCH", "> 1000 ms", "Re-Zero Horizon", "Holding eye closed for over 1 second acts as a digital clutch, instantly resetting cursor center point to eliminate patient neck fatigue.", AMBER_WARN)
]

for i, (name, timing, action, desc, col) in enumerate(click_cards):
    cx = Inches(0.8) + i * Inches(2.96)
    card = create_card(s7, cx, Inches(1.8), Inches(2.82), Inches(3.4), border_color=CARD_BORDER)
    tx = s7.shapes.add_textbox(cx + Inches(0.18), Inches(1.95), Inches(2.46), Inches(3.1))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name
    p.font.name = FONT_SUB
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = col
    
    p2 = tf.add_paragraph()
    p2.text = timing
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = f"ACTION: {action}"
    p3.font.name = FONT_SUB
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = col
    p3.space_before = Pt(4)
    
    p4 = tf.add_paragraph()
    p4.text = desc
    p4.font.name = FONT_BODY
    p4.font.size = Pt(9.5)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(8)

# Bottom Card: TensorFlow Denoising Filter
tf_card = create_card(s7, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.7), border_color=CYAN_DIM, bg_color=CARD_BG_ELEVATED)
tx_tf = s7.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.5))
tf = tx_tf.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "TENSORFLOW EMBEDDED NOISE FILTER & TREMOR SUPPRESSION"
p.font.name = FONT_SUB
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p2 = tf.add_paragraph()
p2.text = "Patients with ALS and severe motor disorders suffer from involuntary neck spasms and micro-tremors. The IRIS Python pipeline applies an adaptive moving-average Kalman filter and lightweight TensorFlow neural model to suppress physiological noise, delivering rock-steady cursor telemetry."
p2.font.name = FONT_BODY
p2.font.size = Pt(11.5)
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)


# ==========================================
# SLIDE 8: 2-3 SECOND LIGHTNING CALIBRATION
# ==========================================
s8 = create_base_slide()
add_header(s8, "CLINICAL SIMPLICITY", "Calibrates in 2–3 Seconds. Zero Specialists Needed.")

steps = [
    ("1", "CONNECT", "Launch Python app. Advertises BLE 5.0 at 2Hz. Instant wireless handshake with PC or phone."),
    ("2", "USER CHECK", "Detects new vs. returning patient. Returning users load profile in <1s, skipping calibration."),
    ("3", "GESTURE LOCK", "Gentle nod up/down & tilt left/right. Learns patient's comfortable neck range & sets dead-zones."),
    ("4", "BLINK LOCK", "2 deliberate blinks (takes 2–3 seconds). Locks optical reflectance threshold & syncs eye twin."),
    ("5", "CURSOR READY", "Cursor goes live immediately. Fully drives OS, universal assistive apps, or games.")
]

for i, (num, title, desc) in enumerate(steps):
    cx = Inches(0.8) + i * Inches(2.36)
    card = create_card(s8, cx, Inches(1.8), Inches(2.24), Inches(3.6), border_color=CARD_BORDER)
    tx = s8.shapes.add_textbox(cx + Inches(0.15), Inches(1.95), Inches(1.94), Inches(3.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"STEP {num}"
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.name = FONT_SUB
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(8)

# Bottom Comparison Callout
c_comp = create_card(s8, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.5), border_color=GREEN_WIN, bg_color=CARD_BG_HIGHLIGHT)
tx_c = s8.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.3))
tf = tx_c.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "THE CALIBRATION DISRUPTION:"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_WIN

p2 = tf.add_paragraph()
p2.text = "Commercial eye trackers demand 30–45 minutes of painful 9-point screen staring with a trained clinical technician present. If the patient shifts slightly in bed, tracking is lost and the 30-minute test must restart. IRIS auto-calibrates in 2–3 seconds and stores personalized profiles permanently."
p2.font.name = FONT_BODY
p2.font.size = Pt(11.5)
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(4)


# ==========================================
# SLIDE 9: UNIVERSAL COMPANION APP
# ==========================================
s9 = create_base_slide()
add_header(s9, "PATIENT SOFTWARE ECOSYSTEM", "One Streamlined Screen. Everything They Need.")

# Left Column: 4 Assistive Pillars
c_app = create_card(s9, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.2))
tx_a = s9.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.4), Inches(4.9))
tf = tx_a.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "4 CORE ACCESSIBLE TILES"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p2 = tf.add_paragraph()
p2.text = "Engineered for Bedridden Independence"
p2.font.name = FONT_HEAD
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(2)

pillars = [
    ("COMMUNICATION HUB", "High-contrast tiles for Water, Rest, Call & AI Speech. Patients express essential daily needs in a single deliberate blink."),
    ("EMERGENCY SOS SIREN", "Instant one-blink caregiver alarm. Dispatches push notifications via ntfy.sh and sounds an acoustic alarm in under 145ms."),
    ("HEALTH & VITALS TRACKER", "Daily pain rating scale, posture comfort log, and medication reminders accessible to caregivers and visiting nurses."),
    ("SMART ROOM IoT RELAY", "Direct local Wi-Fi control: toggle room lights, ceiling fans, and adjust motorized bed tilt without speaking a word.")
]

for title, desc in pillars:
    p = tf.add_paragraph()
    p.text = f"●  {title}"
    p.font.name = FONT_SUB
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_WIN
    p.space_before = Pt(8)
    
    p_desc = tf.add_paragraph()
    p_desc.text = desc
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = TEXT_MUTED

# Right Column: Screenshot of the App
app_img = os.path.join(MEDIA_DIR, "image13.png")
add_image_safely(s9, app_img, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.2), frame=True)


# ==========================================
# SLIDE 10: GEMINI AI CONTEXT EXPANSION
# ==========================================
s10 = create_base_slide()
add_header(s10, "ARTIFICIAL INTELLIGENCE", "Telegraphic Words In. Articulate Speech Out.")

# Left Column: The Problem & Pipeline
c_ai = create_card(s10, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.2))
tx_ai = s10.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.4), Inches(4.9))
tf = tx_ai.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "THE FATIGUE PROBLEM"
p.font.name = FONT_SUB
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RED_ALERT

p2 = tf.add_paragraph()
p2.text = "Motor Fatigue Halts Typing"
p2.font.name = FONT_HEAD
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(2)

p3 = tf.add_paragraph()
p3.text = "Typing a 15-word sentence with an eye cursor requires over 60 deliberate saccades and blinks. Paralyzed patients exhaust their energy within minutes."
p3.font.name = FONT_BODY
p3.font.size = Pt(10.5)
p3.font.color.rgb = TEXT_MUTED
p3.space_before = Pt(4)

# AI Flow Box
p4 = tf.add_paragraph()
p4.text = "THE GEMINI AI EXPANSION ENGINE:"
p4.font.name = FONT_SUB
p4.font.size = Pt(11)
p4.font.bold = True
p4.font.color.rgb = CYAN_ACCENT
p4.space_before = Pt(10)

p5 = tf.add_paragraph()
p5.text = "1. Patient Selects 3 Words: [ Pain ]  [ Left Shoulder ]  [ Sharp ]"
p5.font.name = FONT_MONO
p5.font.size = Pt(10)
p5.font.color.rgb = TEXT_WHITE
p5.space_before = Pt(4)

p6 = tf.add_paragraph()
p6.text = "2. Gemini Multimodal Context Model Ingests: Time of day, posture logs, clinical history."
p6.font.name = FONT_BODY
p6.font.size = Pt(10)
p6.font.color.rgb = TEXT_MUTED

p7 = tf.add_paragraph()
p7.text = "3. Expanded Output: 'I am experiencing a sharp pain in my left shoulder; could you please help me readjust my pillows?'"
p7.font.name = FONT_BODY
p7.font.size = Pt(10.5)
p7.font.bold = True
p7.font.color.rgb = GREEN_WIN
p7.space_before = Pt(4)

p8 = tf.add_paragraph()
p8.text = "4. Patient Agency Safeguard: Patient confirms preview before Web Speech speaks aloud!"
p8.font.name = FONT_BODY
p8.font.size = Pt(10)
p8.font.color.rgb = TEXT_MUTED
p8.space_before = Pt(4)

# Right Column: Screenshot of AI Expansion UI
ai_img = os.path.join(MEDIA_DIR, "image15.png")
add_image_safely(s10, ai_img, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.2), frame=True)


# ==========================================
# SLIDE 11: HEAD-TO-HEAD BENCHMARK (TOBII VS IRIS)
# ==========================================
s11 = create_base_slide()
add_header(s11, "MARKET BENCHMARK", "Commercial Monopoly vs. Open-Source Breakthrough.")

# Comparison Table
table_shape = s11.shapes.add_table(8, 3, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
tbl = table_shape.table
tbl.columns[0].width = Inches(3.2)
tbl.columns[1].width = Inches(4.2)
tbl.columns[2].width = Inches(4.3)

headers = ["FEATURE / METRIC", "COMMERCIAL TOBII DYNAVOX", "PROJECT IRIS (v2.0)"]
for col_idx, h_text in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = CARD_BG_ELEVATED
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT if col_idx == 2 else TEXT_WHITE

rows_data = [
    ("Retail Price in India", "₹25,00,000+ (Extreme cost barrier)", "₹800 (99.96% Cheaper!)", RED_ALERT, GREEN_WIN),
    ("Sensing Technology", "Binocular high-speed optical cameras", "950nm Reflectance + 6-DOF IMU", TEXT_MUTED, CYAN_ACCENT),
    ("Ambient Light Immunity", "Fails in direct sun or dark rooms", "Works in pitch black darkness or daylight", RED_ALERT, GREEN_WIN),
    ("Calibration Time", "30–45 mins (Trained clinical specialist)", "2–3 seconds (Fully self-calibrating)", RED_ALERT, GREEN_WIN),
    ("Prescription Eyewear", "Lens reflections cause severe tracking loss", "Fits any frame & up to ±7.0D lenses", TEXT_MUTED, GREEN_WIN),
    ("Hardware Portability", "Forced proprietary locked 4kg tablet", "Runs on family's existing PC/laptop/phone", TEXT_MUTED, GREEN_WIN),
    ("Open Source / Replicable", "Closed commercial patent monopoly", "100% Free & Open-Source (CERN-OHL)", RED_ALERT, GREEN_WIN)
]

for row_idx, (feat, tobii, iris, t_col, i_col) in enumerate(rows_data, start=1):
    c0 = tbl.cell(row_idx, 0)
    c0.fill.solid()
    c0.fill.fore_color.rgb = CARD_BG
    p = c0.text_frame.paragraphs[0]
    p.text = feat
    p.font.name = FONT_SUB
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    
    c1 = tbl.cell(row_idx, 1)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    p = c1.text_frame.paragraphs[0]
    p.text = tobii
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = t_col
    
    c2 = tbl.cell(row_idx, 2)
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG_HIGHLIGHT
    p = c2.text_frame.paragraphs[0]
    p.text = iris
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = i_col


# ==========================================
# SLIDE 12: DIGITAL THERAPEUTICS & BEYOND HEALTHCARE
# ==========================================
s12 = create_base_slide()
add_header(s12, "REHABILITATION & GAMING DIVERSIFICATION", "Restoring Joy, Play, and Future Market Scale.")

# Left Column: Stacked Pillar Cards
# Pillar 1
c_th = create_card(s12, Inches(0.8), Inches(1.8), Inches(5.8), Inches(2.05))
tx_th = s12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.4), Inches(1.85))
tf = tx_th.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PILLAR 1: DIGITAL THERAPEUTICS & REHAB"
p.font.name = FONT_SUB
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p2 = tf.add_paragraph()
p2.text = "Combatting Sensory Deprivation in ALS"
p2.font.name = FONT_HEAD
p2.font.size = Pt(14)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE

th_pts = [
    "Bedridden isolation causes cognitive decline and severe clinical depression",
    "Gaze Dino Runner: Playable browser game rehabilitates ocular motor control",
    "360° Cockpit Flight Simulator: Paralyzed patients explore skies via head motion"
]
for pt in th_pts:
    p = tf.add_paragraph()
    p.text = f"•  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(3)

# Pillar 2
c_gm = create_card(s12, Inches(0.8), Inches(4.0), Inches(5.8), Inches(2.1))
tx_gm = s12.shapes.add_textbox(Inches(1.0), Inches(4.1), Inches(5.4), Inches(1.9))
tf = tx_gm.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PILLAR 2: HANDS-FREE CONSUMER GAMING"
p.font.name = FONT_SUB
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = GREEN_WIN

p2 = tf.add_paragraph()
p2.text = "Cross-Subsidizing Free Medical Units"
p2.font.name = FONT_HEAD
p2.font.size = Pt(14)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE

gm_pts = [
    "Enables amputees, injured soldiers, and mobility-impaired players to game",
    "MPU6050 head tilt maps to 360° crosshair aiming; blinks act as fire triggers",
    "Mass-Market Scale: High-volume consumer gaming adoption subsidizes free medical units"
]
for pt in gm_pts:
    p = tf.add_paragraph()
    p.text = f"✔  {pt}"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(3)

# Right Column: Real Simulator Screenshot
sim_img = os.path.join(MEDIA_DIR, "image17.png")
add_image_safely(s12, sim_img, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.3), frame=True)

# Bottom Highlight Ribbon
bot_th = create_card(s12, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.9), border_color=CARD_BORDER, bg_color=CARD_BG_ELEVATED)
tx_bth = s12.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.7))
p = tx_bth.text_frame.paragraphs[0]
p.text = "INNOVATION MODEL: Accessible consumer gaming profits fund free medical distribution to rural hospitals across India."
p.font.name = FONT_HEAD
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 13: UN GLOBAL GOALS (SDGs)
# ==========================================
s13 = create_base_slide()
add_header(s13, "ETHICAL RESPONSIBILITY & SCALING", "Engineered for the United Nations Global Goals.")

sdg_cards = [
    ("SDG 3", "GOOD HEALTH & WELL-BEING", "Restoring voice, communication, and emotional agency to paralyzed and locked-in individuals.", "image26.png"),
    ("SDG 9", "INDUSTRY, INNOVATION & INFRASTRUCTURE", "Frugal, open-source hardware engineering replacing costly multi-lakh monopolies.", "image27.png"),
    ("SDG 10", "REDUCED INEQUALITIES", "Demolishing financial walls so rural and lower-income families receive equal healthcare access.", "image30.png"),
    ("SDG 17", "PARTNERSHIPS FOR THE GOALS", "Open-source schematics and firmware empowering NGOs, neurology wards, and makers worldwide.", "image32.png")
]

for i, (sdg_num, sdg_title, sdg_desc, img_name) in enumerate(sdg_cards):
    cx = Inches(0.8) + i * Inches(2.96)
    card = create_card(s13, cx, Inches(1.8), Inches(2.82), Inches(5.2), border_color=CARD_BORDER)
    
    # Image Icon
    img_p = os.path.join(MEDIA_DIR, img_name)
    if os.path.exists(img_p):
        s13.shapes.add_picture(img_p, cx + Inches(0.76), Inches(2.0), Inches(1.3), Inches(1.3))
    
    tx = s13.shapes.add_textbox(cx + Inches(0.18), Inches(3.5), Inches(2.46), Inches(3.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = sdg_num
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = sdg_title
    p2.font.name = FONT_SUB
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = sdg_desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)


# ==========================================
# SLIDE 14: CONCLUSION & THE NATIONAL VISION
# ==========================================
s14 = create_base_slide()
add_header(s14, "VIVO IGNITE NATIONAL FINALE · BHARAT MANDAPAM", "Technology Should Be a Bridge, Not a Wall.")

# Central Closing Quote Card
c_quote = create_card(s14, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.4), border_color=CYAN_ACCENT, bg_color=CARD_BG_HIGHLIGHT)
tx_q = s14.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(10.9), Inches(2.0))
tf = tx_q.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "“For a paralyzed human trapped inside their own mind, technology should be an immediate bridge of communication — never an unreachable multi-lakh financial wall.”"
p.font.name = FONT_HEAD
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "— Ayushman Choudhary, Creator of Project IRIS"
p2.font.name = FONT_SUB
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = CYAN_ACCENT
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(10)

# 3 National Scale Pillars
pillars_fin = [
    ("MAKE IN INDIA", "100% locally sourceable components, zero imported monopolies, manufactured for ₹800."),
    ("HOSPITAL & HOME READY", "Plug-and-play wireless telemetry ready for neurology ICUs, rural clinics, and home care."),
    ("OPEN HARDWARE MOVEMENT", "Full circuit schematics, firmware code, and AI models freely published to empower global makers.")
]

for i, (p_title, p_desc) in enumerate(pillars_fin):
    cx = Inches(0.8) + i * Inches(3.95)
    card = create_card(s14, cx, Inches(4.4), Inches(3.8), Inches(1.8))
    tx = s14.shapes.add_textbox(cx + Inches(0.2), Inches(4.5), Inches(3.4), Inches(1.6))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = p_title
    p.font.name = FONT_SUB
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_WIN
    
    p2 = tf.add_paragraph()
    p2.text = p_desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(4)

# Presenter Signature Bar
sig_bar = create_card(s14, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.8), border_color=CARD_BORDER, bg_color=CARD_BG_ELEVATED)
tx_sig = s14.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.3), Inches(0.65))
tf = tx_sig.text_frame
p = tf.paragraphs[0]
p.text = "Ayushman Choudhary  ·  Class 10th  ·  Bhavan's B.P. Vidya Mandir Ashti, Nagpur, Maharashtra"
p.font.name = FONT_HEAD
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "PROJECT IRIS  |  INFRARED REFLECTIVE INTERFACE SYSTEM  |  VIVO IGNITE NATIONAL FINALE"
p2.font.name = FONT_SUB
p2.font.size = Pt(10)
p2.font.bold = True
p2.font.color.rgb = CYAN_ACCENT
p2.alignment = PP_ALIGN.CENTER

# Configure Kiosk loop mode in presentation XML
try:
    kiosk_xml = '<p:showPr xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" loop="1"><p:kiosk/></p:showPr>'
    prs._element.append(parse_xml(kiosk_xml))
    print("Configured native Kiosk show mode with infinite loop!")
except Exception as e:
    print(f"Warning setting kiosk show mode: {e}")

# Save presentation
output_pptx = "IRIS_Kiosk_Bharat_Mandapam.pptx"
prs.save(output_pptx)
print(f"SUCCESS: Generated {output_pptx} with 14 slides!")
