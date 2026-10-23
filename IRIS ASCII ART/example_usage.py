# -*- coding: utf-8 -*-
"""
Example showing how to use the Ultra-HD IRIS Logo in your own Python programs.
"""

from iris_ascii import print_iris_logo, get_iris_logo, stream_iris_logo

print("=== Example 1: Default Ultra-HD Glowing Iris Logo (Zero Pixelation) ===")
print_iris_logo()

print("\n=== Example 2: Ultra-HD Large Size in Claude Code Coral Theme ===")
print_iris_logo(theme="claude", size="large")

print("\n=== Example 3: Cyberpunk Synthwave Theme ===")
print_iris_logo(theme="cyberpunk", size="medium")

print("\n=== Example 4: Getting raw ANSI string for custom terminal headers ===")
banner_raw = get_iris_logo(theme="iris", size="large", subtitle=True)
print(f"Raw string length: {len(banner_raw)} characters with ANSI TrueColor & 100% transparency.")
