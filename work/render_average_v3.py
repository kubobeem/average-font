#!/usr/bin/env python3
"""v3 render: average all 229 fonts over the v2 174 chars + full joyo kanji.

Char set: v2's 174 chars (same order) + the 2116 joyo kanji not already
in that set = 2290 chars total. Joyo list (2136) in work/joyo_kanji.txt,
extracted from Wikipedia's 常用漢字一覧 (Bunka-cho table): the 5 kanji
deleted in 2010 (勺錘銑脹匁) excluded, and the variant row 𠮟 replaced
with the official joyo form 叱 (U+53F1, BMP).

Memory: 2290 float32 256x256 accumulators = ~600 MB, so the sums live
in a numpy memmap file (work/v3_acc.dat) instead of RAM (this VM has
~8 GB RAM, mostly used). Same draw settings as v2: size 200, anchor mm.

Outputs: out/glyphs_v3/*.png (black-on-white averages) and
out/stats_v3.json, which additionally records per-glyph max_ink /
mean_ink / faintness stats used by the v3 adaptive threshold.
"""
import json, os, sys, time, gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST
from render_average import CHARS as V2_CHARS, group

BASE = os.path.expanduser("~/workspace/average-font")
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "out", "glyphs_v3")
SIZE = 256
FONT_SIZE = 200
ACC_PATH = os.path.join(BASE, "work", "v3_acc.dat")

def load_joyo():
    txt = open(os.path.join(BASE, "work", "joyo_kanji.txt"), encoding="utf-8").read().strip()
    assert len(txt) == 2136, len(txt)
    assert len(set(txt)) == 2136
    return txt

def main():
    joyo = load_joyo()
    v2set = set(V2_CHARS)
    new_kanji = [c for c in joyo if c not in v2set]
    chars = list(V2_CHARS) + new_kanji
    assert len(chars) == 174 + 2116 == 2290, len(chars)
    print(f"chars: {len(chars)} (v2 174 + new kanji {len(new_kanji)})", flush=True)
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(ACC_PATH):
        os.remove(ACC_PATH)
    acc = np.memmap(ACC_PATH, dtype=np.float32, mode="w+",
                    shape=(len(chars), SIZE, SIZE))
    acc[:] = 0
    cnt = np.zeros(len(chars), dtype=np.int32)
    idx = {ch: i for i, ch in enumerate(chars)}
    missing = {}
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
            for ch in chars:
                if ord(ch) not in cmap:
                    miss.append(ch)
                    continue
                draw.rectangle([0, 0, SIZE, SIZE], fill=0)
                draw.text((SIZE // 2, SIZE // 2), ch, font=font, fill=255, anchor="mm")
                acc[idx[ch]] += np.asarray(img, dtype=np.float32)
                cnt[idx[ch]] += 1
            if miss:
                missing[label] = miss
            n_fonts += 1
            del font
            gc.collect()
        acc.flush()
        print(f"[{n_fonts}] {name} done ({time.time()-t0:.0f}s)", flush=True)

    stats = {"version": 3, "fonts_rendered": n_fonts, "chars": {},
             "total_chars": len(chars)}
    for i, ch in enumerate(chars):
        n = int(cnt[i])
        avg = acc[i] / max(n, 1)  # 0..255 ink
        out_img = Image.fromarray((255.0 - avg).astype(np.uint8), mode="L")
        fname = f"{i:03d}_U+{ord(ch):04X}_{group(ch)}.png"
        out_img.save(os.path.join(OUT, fname))
        stats["chars"][ch] = {
            "file": fname, "contributors": n,
            "codepoint": f"U+{ord(ch):04X}", "group": group(ch),
            "max_ink": round(float(avg.max()), 1),
            "mean_ink": round(float(avg.mean()), 2),
            "ink_px_ge64": int((avg >= 64).sum()),
            "ink_px_ge128": int((avg >= 128).sum()),
        }
        if i % 200 == 0:
            print(f"saved {i}/{len(chars)}", flush=True)
    stats["missing"] = missing
    stats["total_fonts"] = n_fonts
    stats["elapsed_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(BASE, "out", "stats_v3.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    kanji_cnt = [c["contributors"] for c in stats["chars"].values()
                 if c["group"] == "kanji"]
    print(f"DONE: {n_fonts} fonts, {len(chars)} chars, {time.time()-t0:.0f}s")
    print("kanji contributors: min", min(kanji_cnt), "max", max(kanji_cnt))
    print("chars with <100 contributors:",
          [(ch, stats['chars'][ch]['contributors']) for ch in chars
           if stats['chars'][ch]['contributors'] < 100][:20])
    maxinks = sorted((c["max_ink"], ch) for ch, c in stats["chars"].items())
    print("faintest 15 by max_ink:", maxinks[:15])

if __name__ == "__main__":
    main()
