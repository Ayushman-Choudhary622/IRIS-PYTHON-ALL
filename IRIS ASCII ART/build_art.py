import json

with open('braille_art.json', 'r', encoding='utf-8') as f:
    braille_dict = json.load(f)

with open('precomputed_art.json', 'r', encoding='utf-8') as f:
    legacy_dict = json.load(f)

script_content = '''# -*- coding: utf-8 -*-
"""
=============================================================================
 IRIS UNIVERSAL - ULTRA-HD CLAUDE CODE STYLE ASCII & BRAILLE ART
=============================================================================
High-definition, subpixel TrueColor (24-bit ANSI) ASCII Logo with
100% transparent background support for any terminal (Windows Terminal, CMD,
PowerShell, VS Code, Linux/macOS).

Uses 8x sub-pixel Braille vector rendering for ultra-sharp curves and zero
pixelation, exactly like modern developer CLI tools (Claude Code, Bun, Next.js).

HOW TO USE IN YOUR PYTHON PROGRAMS:
-----------------------------------
from iris_ascii import print_iris_logo, get_iris_logo

# 1. Print the default Ultra-HD Claude-Code-style glowing Iris logo:
print_iris_logo()

# 2. Print with specific theme ('iris', 'claude', 'cyberpunk', 'matrix', 'gold'):
print_iris_logo(theme='claude')

# 3. Choose size ('large', 'medium', 'compact', or 'auto' [default]):
print_iris_logo(size='large')

# 4. Animated scanline reveal effect:
from iris_ascii import stream_iris_logo
stream_iris_logo()
=============================================================================
"""

import os
import sys
import time
import argparse

# Enable UTF-8 & ANSI on Windows CMD / PowerShell
def init_terminal():
    """Initializes terminal for TrueColor ANSI and UTF-8 encoding."""
    if sys.platform == 'win32':
        os.system('')  # Activates VT100 / ANSI escape sequence parsing in Windows CMD
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

init_terminal()

# Precomputed Ultra-HD Sub-pixel Braille Art (8x pixel density, Zero pixelation!)
BRAILLE_ART = ''' + json.dumps(braille_dict, indent=4, ensure_ascii=False) + '''

# Precomputed Block & Classic ASCII (Fallback / Retro styles)
BLOCK_ART = ''' + json.dumps(legacy_dict, indent=4, ensure_ascii=False) + '''

SUBTITLES = {
    'iris':      "\\033[38;2;0;229;255m───\\033[0m \\033[1;38;2;240;248;255m[ IRIS UNIVERSAL \\033[38;2;0;229;255m•\\033[1;38;2;240;248;255m AI INTELLIGENCE SYSTEM ]\\033[0m \\033[38;2;0;229;255m───\\033[0m",
    'claude':    "\\033[38;2;249;115;22m───\\033[0m \\033[1;38;2;254;215;170m[ IRIS UNIVERSAL \\033[38;2;249;115;22m•\\033[1;38;2;254;215;170m CLAUDE CODE STYLE ]\\033[0m \\033[38;2;249;115;22m───\\033[0m",
    'cyberpunk': "\\033[38;2;0;245;255m───\\033[0m \\033[1;38;2;255;20;147m[ IRIS CYBERPUNK \\033[38;2;0;245;255m•\\033[1;38;2;255;20;147m NEON SYNTH EDITION ]\\033[0m \\033[38;2;0;245;255m───\\033[0m",
    'matrix':    "\\033[38;2;0;255;70m───\\033[0m \\033[1;38;2;160;255;180m[ IRIS MATRIX \\033[38;2;0;255;70m•\\033[1;38;2;160;255;180m NEURAL MAINFRAME ]\\033[0m \\033[38;2;0;255;70m───\\033[0m",
    'gold':      "\\033[38;2;255;215;0m───\\033[0m \\033[1;38;2;255;245;180m[ IRIS GOLD \\033[38;2;255;215;0m•\\033[1;38;2;255;245;180m CYBER LUXURY EDITION ]\\033[0m \\033[38;2;255;215;0m───\\033[0m",
    'original':  "\\033[38;2;0;180;216m───\\033[0m \\033[1;38;2;100;149;237m[ IRIS VECTOR \\033[38;2;0;180;216m•\\033[1;38;2;100;149;237m ORIGINAL PALETTE ]\\033[0m \\033[38;2;0;180;216m───\\033[0m",
    'ascii':     "\\033[38;2;0;229;255m───\\033[0m \\033[1;38;2;240;248;255m[ IRIS RETRO \\033[38;2;0;229;255m•\\033[1;38;2;240;248;255m CLASSIC ASCII ]\\033[0m \\033[38;2;0;229;255m───\\033[0m",
}

def get_terminal_width():
    """Returns current terminal width safely."""
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 100

def get_iris_logo(theme='iris', style='braille', size='auto', subtitle=True, center=False):
    """
    Returns the ANSI-colored IRIS logo string with full transparency.
    
    Args:
        theme (str): 'iris' (default neon cyan), 'claude' (coral gradient),
                     'cyberpunk' (cyan/magenta), 'matrix' (green),
                     'gold' (gold gradient), 'original' (navy/cyan), 'ascii'.
        style (str): 'braille' (Ultra-HD, default, non-pixelated),
                     'block' (retro half-block), 'ascii' (classic characters).
        size (str):  'auto' (adapts to terminal width), 'large' (110 chars),
                     'medium' (90 chars), 'compact' (74 chars).
        subtitle (bool): If True, appends a stylized subtitle banner.
        center (bool): If True, centers the logo based on terminal width.
        
    Returns:
        str: Ready-to-print string with ANSI TrueColor codes.
    """
    theme = theme.lower()
    style = style.lower()
    term_w = get_terminal_width()
    
    # Resolve size
    if size == 'auto':
        if term_w >= 115:
            resolved_size = 'large'
            art_w = 110
        elif term_w >= 95:
            resolved_size = 'medium'
            art_w = 90
        else:
            resolved_size = 'compact'
            art_w = 74
    else:
        resolved_size = size.lower()
        art_w = {'large': 110, 'medium': 90, 'compact': 74}.get(resolved_size, 90)

    if style == 'braille':
        size_dict = BRAILLE_ART.get(resolved_size, BRAILLE_ART['large'])
        raw_art = size_dict.get(theme, size_dict.get('iris'))
    elif style == 'ascii':
        raw_art = BLOCK_ART.get('ascii')
        art_w = 68
    else:  # block
        raw_art = BLOCK_ART.get(theme, BLOCK_ART['iris'])
        art_w = 68
        
    lines = raw_art.split('\\n')
    pad = max(0, (term_w - art_w) // 2) if center else 0
    pad_str = ' ' * pad
    
    formatted_lines = [f"{pad_str}{line}" for line in lines]
    
    if subtitle:
        sub = SUBTITLES.get(theme, SUBTITLES['iris'])
        sub_len = 54  # approximate visible length
        sub_pad = max(0, (art_w - sub_len) // 2) + pad
        formatted_lines.append('')
        formatted_lines.append(f"{' ' * sub_pad}{sub}")
        formatted_lines.append('')
        
    return '\\n'.join(formatted_lines)

def print_iris_logo(theme='iris', style='braille', size='auto', subtitle=True, center=False):
    """Prints the Ultra-HD IRIS logo directly to stdout."""
    init_terminal()
    print(get_iris_logo(theme=theme, style=style, size=size, subtitle=subtitle, center=center))

def stream_iris_logo(theme='iris', style='braille', size='auto', speed=0.03, subtitle=True, center=False):
    """Plays a smooth typewriter / scanline animation to reveal the logo."""
    init_terminal()
    logo_text = get_iris_logo(theme=theme, style=style, size=size, subtitle=subtitle, center=center)
    for line in logo_text.split('\\n'):
        print(line)
        time.sleep(speed)

def interactive_menu():
    """Interactive terminal menu to preview all sizes and themes."""
    themes = ['iris', 'claude', 'cyberpunk', 'matrix', 'gold', 'original']
    theme_names = {
        'iris': 'IRIS Electric Cyan & Pure White (Claude Code Inspired Default)',
        'claude': 'Claude Code Warm Coral Gradient',
        'cyberpunk': 'Cyberpunk Synthwave (Cyan & Neon Pink)',
        'matrix': 'Matrix Cyber Green',
        'gold': 'Cyber Luxury Gold',
        'original': 'Original PNG Vector Colors (Navy & Cyan)'
    }
    
    current_size = 'large'
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_iris_logo('iris', style='braille', size=current_size, subtitle=False)
        print("\\033[1;37m=======================================================================\\033[0m")
        print(f"\\033[1;36m       IRIS ULTRA-HD ASCII ART CONTROLLER  [Current Size: {current_size.upper()}]       \\033[0m")
        print("\\033[1;37m=======================================================================\\033[0m")
        print("  \\033[1;33m--- THEMES (Ultra-HD Sub-pixel Vector) ---\\033[0m")
        for idx, t in enumerate(themes, 1):
            print(f"  \\033[38;2;0;229;255m[{idx}]\\033[0m {theme_names[t]}")
        print("\\033[1;37m-----------------------------------------------------------------------\\033[0m")
        print("  \\033[1;33m--- SIZE / RESOLUTION TOGGLE ---\\033[0m")
        print("  \\033[38;2;0;229;255m[L]\\033[0m Switch to Large Ultra-HD (110 columns - Pristine Curves)")
        print("  \\033[38;2;0;229;255m[M]\\033[0m Switch to Medium (90 columns - Standard Terminal)")
        print("  \\033[38;2;0;229;255m[C]\\033[0m Switch to Compact (74 columns - Split Pane)")
        print("\\033[1;37m-----------------------------------------------------------------------\\033[0m")
        print("  \\033[38;2;0;229;255m[7]\\033[0m Retro Half-Block Mode")
        print("  \\033[38;2;0;229;255m[8]\\033[0m Retro Classic ASCII Character Mode (@%#*)")
        print("  \\033[38;2;0;229;255m[9]\\033[0m Animated Scanline Reveal")
        print("  \\033[38;2;0;229;255m[0]\\033[0m Exit")
        print("\\033[1;37m=======================================================================\\033[0m")
        
        try:
            choice = input("\\nSelect an option and press ENTER: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
            
        if choice in ['1', '2', '3', '4', '5', '6']:
            t = themes[int(choice) - 1]
            os.system('cls' if os.name == 'nt' else 'clear')
            print_iris_logo(t, style='braille', size=current_size, subtitle=True, center=True)
            input("\\nPress ENTER to return to menu...")
        elif choice == 'l':
            current_size = 'large'
        elif choice == 'm':
            current_size = 'medium'
        elif choice == 'c':
            current_size = 'compact'
        elif choice == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_iris_logo('iris', style='block', subtitle=True, center=True)
            input("\\nPress ENTER to return to menu...")
        elif choice == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_iris_logo('ascii', style='ascii', subtitle=True, center=True)
            input("\\nPress ENTER to return to menu...")
        elif choice == '9':
            os.system('cls' if os.name == 'nt' else 'clear')
            stream_iris_logo('iris', style='braille', size=current_size, speed=0.03, center=True)
            input("\\nPress ENTER to return to menu...")
        elif choice == '0' or choice == 'q':
            print("\\nExiting IRIS Art Viewer. Have a great day!")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display IRIS Logo in Ultra-HD Claude-Code-Style ASCII/Braille Art')
    parser.add_argument('--theme', '-t', choices=['iris', 'claude', 'cyberpunk', 'matrix', 'gold', 'original', 'ascii'],
                        default='iris', help='Color theme to display')
    parser.add_argument('--style', '-s', choices=['braille', 'block', 'ascii'],
                        default='braille', help='Rendering style: braille (Ultra-HD vector), block (half-blocks), or ascii (characters)')
    parser.add_argument('--size', choices=['auto', 'large', 'medium', 'compact'],
                        default='auto', help='Size / resolution: large (110 chars), medium (90 chars), compact (74 chars), auto')
    parser.add_argument('--all', '-a', action='store_true', help='Show gallery of all themes')
    parser.add_argument('--animate', action='store_true', help='Play animated reveal')
    parser.add_argument('--no-sub', action='store_true', help='Do not display subtitle banner')
    parser.add_argument('--center', '-c', action='store_true', help='Center horizontally in terminal')
    parser.add_argument('--interactive', '-i', action='store_true', help='Launch interactive menu')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_menu()
    elif args.all:
        for t in ['iris', 'claude', 'cyberpunk', 'matrix', 'gold', 'original']:
            print(f"\\n\\033[1;33m>>> THEME: {t.upper()} (Ultra-HD {args.size.upper()}) <<<\\033[0m")
            print_iris_logo(t, style=args.style, size=args.size, subtitle=not args.no_sub, center=args.center)
            print("-" * 90)
    elif args.animate:
        stream_iris_logo(args.theme, style=args.style, size=args.size, subtitle=not args.no_sub, center=args.center)
    else:
        print_iris_logo(args.theme, style=args.style, size=args.size, subtitle=not args.no_sub, center=args.center)
'''

with open('iris_ascii.py', 'w', encoding='utf-8') as f:
    f.write(script_content)

print('iris_ascii.py updated with Ultra-HD subpixel art successfully!')
