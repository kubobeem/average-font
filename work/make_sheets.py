#!/usr/bin/env python3
"""Contact sheet(s) from the averaged glyph PNGs."""
import json, os
from PIL import Image

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
stats = json.load(open(os.path.join(OUT, "stats.json"), encoding="utf-8"))
chars = list(stats["chars"].keys())

# one sheet: 174 glyphs, 18 cols x 10 rows, cell 128px
CELL = 128
COLS = 18
ROWS = (len(chars) + COLS - 1) // COLS
sheet = Image.new("L", (COLS * CELL, ROWS * CELL), 255)
for i, ch in enumerate(chars):
    info = stats["chars"][ch]
    im = Image.open(os.path.join(OUT, "glyphs", info["file"])).resize((CELL, CELL), Image.LANCZOS)
    x, y = (i % COLS) * CELL, (i // COLS) * CELL
    sheet.paste(im, (x, y))
sheet.save(os.path.join(OUT, "contact_sheet.png"))
print("saved contact_sheet.png", sheet.size)

# per-group sheets (smaller, for the viewer page sections)
from collections import defaultdict
groups = defaultdict(list)
for ch in chars:
    groups[stats["chars"][ch]["group"]].append(ch)
for g, cl in groups.items():
    cols = 12
    rows = (len(cl) + cols - 1) // cols
    s = Image.new("L", (cols * CELL, rows * CELL), 255)
    for i, ch in enumerate(cl):
        info = stats["chars"][ch]
        im = Image.open(os.path.join(OUT, "glyphs", info["file"])).resize((CELL, CELL), Image.LANCZOS)
        s.paste(im, ((i % cols) * CELL, (i // cols) * CELL))
    s.save(os.path.join(OUT, f"contact_sheet_{g}.png"))
    print("saved", g, s.size)
