#!/usr/bin/env python3
"""Render each of the 100 fonts' glyphs at 256px and pixel-average them.
Method: for each font, draw the glyph (size 200, centered via anchor='mm')
on a 256x256 grayscale canvas; accumulate float32 sums per character;
average = sum / contributor_count (fonts lacking the glyph are skipped).
"""
import json, os, sys, time, gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST

BASE = os.path.expanduser("~/workspace/average-font")
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "out", "glyphs")
SIZE = 256
FONT_SIZE = 200

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
KATAKANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
DIGITS = "0123456789"
LATIN_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_L = "abcdefghijklmnopqrstuvwxyz"
KANJI = "日本年時分前後大小上下中左右山川田人月火"
CHARS = list(HIRAGANA + KATAKANA + DIGITS + LATIN_U + LATIN_L + KANJI)

def group(ch):
    o = ord(ch)
    if 0x3040 <= o <= 0x309F: return "hiragana"
    if 0x30A0 <= o <= 0x30FF: return "katakana"
    if ch.isdigit(): return "digits"
    if ch.isupper(): return "latin_upper"
    if ch.islower(): return "latin_lower"
    return "kanji"

def main():
    assert len(CHARS) == 174, len(CHARS)
    os.makedirs(OUT, exist_ok=True)
    acc = {ch: np.zeros((SIZE, SIZE), dtype=np.float32) for ch in CHARS}
    cnt = {ch: 0 for ch in CHARS}
    missing = {}  # font display name -> [chars missing]
    t0 = time.time()
    n_fonts = 0
    for d, fn, weights, name in MANIFEST:
        path = os.path.join(FONTS, fn)
        try:
            ft = TTFont(path, lazy=True)
            cmap = ft.getBestCmap()
            ft.close()
        except Exception as e:
            print(f"SKIP {name}: cmap fail {e}", flush=True)
            continue
        wlist = weights if weights else [None]
        for w in wlist:
            label = f"{name}" + (f" wght={w}" if w else "")
            try:
                font = ImageFont.truetype(path, FONT_SIZE)
                if w is not None:
                    font.set_variation_by_axes([w])
            except Exception as e:
                print(f"SKIP {label}: load fail {e}", flush=True)
                continue
            miss = []
            img = Image.new("L", (SIZE, SIZE), 0)
            draw = ImageDraw.Draw(img)
            for ch in CHARS:
                if ord(ch) not in cmap:
                    miss.append(ch)
                    continue
                draw.rectangle([0, 0, SIZE, SIZE], fill=0)
                draw.text((SIZE // 2, SIZE // 2), ch, font=font, fill=255, anchor="mm")
                acc[ch] += np.asarray(img, dtype=np.float32)
                cnt[ch] += 1
            if miss:
                missing[label] = miss
            n_fonts += 1
            del font
            gc.collect()
        print(f"[{n_fonts}] {name} done ({time.time()-t0:.0f}s)", flush=True)

    stats = {"fonts_rendered": n_fonts, "chars": {}}
    for i, ch in enumerate(CHARS):
        n = cnt[ch]
        avg = acc[ch] / max(n, 1)  # 0..255, white = ink
        # black-on-white PNG
        out_img = Image.fromarray((255.0 - avg).astype(np.uint8), mode="L")
        fname = f"{i:03d}_U+{ord(ch):04X}_{group(ch)}.png"
        out_img.save(os.path.join(OUT, fname))
        stats["chars"][ch] = {"file": fname, "contributors": n,
                               "codepoint": f"U+{ord(ch):04X}", "group": group(ch)}
        del acc[ch]
    stats["missing"] = missing
    stats["total_fonts"] = n_fonts
    stats["elapsed_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(BASE, "out", "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"DONE: {n_fonts} fonts, {len(CHARS)} chars, {time.time()-t0:.0f}s")
    print("min contributors:", min(cnt.values()), "max:", max(cnt.values()))
    print("chars with <100 contributors:",
          [(ch, cnt[ch]) for ch in CHARS if cnt[ch] < 100])

if __name__ == "__main__":
    main()
