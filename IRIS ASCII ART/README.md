# 🌌 IRIS UNIVERSAL - ULTRA-HD CLAUDE CODE STYLE ASCII ART

Ultra-high-definition, subpixel TrueColor (24-bit ANSI) ASCII Logo with **100% transparent background** support for all Python programs and Windows/Mac/Linux terminals.

Uses **8x subpixel Braille vector rendering** to eliminate pixelation and deliver silky smooth curves for the IRIS Eye icon and bold typography.

---

## ⚡ Quick Start (Double-Click)

- **[SHOW_LOGO.bat](file:///c:/Ayushman%20Choudhary/IRIS%20FINALE%20UNIVERSAL/IRIS%20ASCII%20ART/SHOW_LOGO.bat)** : Launches a 120-column terminal window and prints the Ultra-HD logo instantly.
- **[RUN_IRIS_ASCII.bat](file:///c:/Ayushman%20Choudhary/IRIS%20FINALE%20UNIVERSAL/IRIS%20ASCII%20ART/RUN_IRIS_ASCII.bat)** : Interactive controller to preview sizes (Large 110 cols, Medium 90 cols, Compact 74 cols), 6 color themes, and scanline animation.

---

## 🐍 How to Use in Your Python Programs

Copy [**`iris_ascii.py`**](file:///c:/Ayushman%20Choudhary/IRIS%20FINALE%20UNIVERSAL/IRIS%20ASCII%20ART/iris_ascii.py) into your project and import it:

```python
from iris_ascii import print_iris_logo, get_iris_logo, stream_iris_logo

# 1. Print default Ultra-HD glowing Cyan & White logo:
print_iris_logo()

# 2. Select specific size ('large', 'medium', 'compact', or 'auto'):
print_iris_logo(size="large")

# 3. Select theme ('iris', 'claude', 'cyberpunk', 'matrix', 'gold', 'original'):
print_iris_logo(theme="claude", size="large")     # Warm Coral / Terracotta gradient
print_iris_logo(theme="cyberpunk", size="large")  # Neon Cyan & Hot Pink
print_iris_logo(theme="gold", size="large")       # Cyber Luxury Gold

# 4. Get the raw string with ANSI codes (for loggers, Flask/FastAPI startup screens):
banner = get_iris_logo(theme="iris", size="large", subtitle=True)

# 5. Animated scanline reveal:
stream_iris_logo(speed=0.03)
```

---

## 🎨 Themes Available

| Theme | Description |
|---|---|
| `iris` *(Default)* | Radiant Electric Cyan Iris with Pure Diamond White / Ice-Blue text (Claude Code inspired) |
| `claude` | Iconic Claude Code warm terracotta / coral gradient (`#F97316` / `#FB923C` / `#FED7AA`) |
| `cyberpunk` | Synthwave Neon Cyan & Hot Magenta (`#00F5FF` & `#FF1493`) |
| `matrix` | Neural Mainframe Hacker Green gradient (`#00FF46` & `#A0FFB4`) |
| `gold` | Cyber Luxury Gold gradient (`#FFD700` & `#FFA500`) |
| `original` | Original PNG Vector colors (Deep Navy `#041A34` & Cyan) |

---

## 🌟 Why this version is not pixelated:
- **8 Subpixels per Terminal Cell**: We upgraded from coarse half-blocks (2 subpixels) to unicode Braille matrix (8 subpixels per character cell), delivering **400% higher resolution**.
- **Smooth Vector Contours**: Captures every concentric iris line, pupil aperture, and font serifs with crisp, anti-aliased curves.
- **100% Transparency**: Transparent pixels remain untouched so your terminal's dark theme remains uninterrupted.
- **Zero Dependencies**: Everything is pre-calculated and embedded directly into the code. No `Pillow` or `numpy` required at runtime.
