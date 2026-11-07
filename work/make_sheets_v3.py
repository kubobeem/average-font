#!/usr/bin/env python3
"""v3 outputs: contact sheets, faint-kanji before/after sheet,
TTF typeset test image, and viewer_v3.html.

Files (v2 files untouched; everything v3 has a _v3 suffix):
- out/contact_sheet_v3.png, out/contact_sheet_v3_<group>.png
- out/faint_before_after_v3.png : 24 faintest kanji, 3 columns
  (average PNG | binary at fixed 128 = v2 method | binary at the
  v3 adaptive threshold). The visual proof that faint kanji survive.
- out/ttf_test_v3.png : real typesetting with the v3 TTF, including
  a line made only of the 24 faintest kanji.
- out/viewer_v3.html
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
GLYPHS = os.path.join(OUT, "glyphs_v3")
stats = json.load(open(os.path.join(OUT, "stats_v3.json"), encoding="utf-8"))
chars = list(stats["chars"].keys())
TTF = os.path.join(BASE, "AverageFont-Regular-v3-229fonts-2290chars.ttf")

# --- contact sheets ---
CELL = 48
COLS = 24
ROWS = (len(chars) + COLS - 1) // COLS
sheet = Image.new("L", (COLS * CELL, ROWS * CELL), 255)
for i, ch in enumerate(chars):
    info = stats["chars"][ch]
    im = Image.open(os.path.join(GLYPHS, info["file"])).resize((CELL, CELL), Image.LANCZOS)
    sheet.paste(im, ((i % COLS) * CELL, (i // COLS) * CELL))
sheet.save(os.path.join(OUT, "contact_sheet_v3.png"))
print("saved contact_sheet_v3.png", sheet.size)

groups = defaultdict(list)
for ch in chars:
    groups[stats["chars"][ch]["group"]].append(ch)
for g, cl in groups.items():
    rows = (len(cl) + COLS - 1) // COLS
    s = Image.new("L", (COLS * CELL, rows * CELL), 255)
    for i, ch in enumerate(cl):
        info = stats["chars"][ch]
        im = Image.open(os.path.join(GLYPHS, info["file"])).resize((CELL, CELL), Image.LANCZOS)
        s.paste(im, ((i % COLS) * CELL, (i // COLS) * CELL))
    s.save(os.path.join(OUT, f"contact_sheet_v3_{g}.png"))
    print("saved", g, len(cl), s.size)

# --- faint before/after sheet ---
kanji = [(ch, c) for ch, c in stats["chars"].items() if c["group"] == "kanji"]
faintest = sorted(kanji, key=lambda kv: kv[1]["max_ink"])[:24]
print("faintest 24:", [(ch, c["max_ink"], c["contributors"]) for ch, c in faintest])
CELL2 = 160
LABEL = 34
W = 3 * CELL2 + 8
H = len(faintest) * (CELL2 + LABEL) + 64
sheet2 = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(sheet2)
try:
    lab_font = ImageFont.truetype(TTF, 24)
    dejavu = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    small_font = ImageFont.truetype(dejavu, 16)
except Exception:
    lab_font = small_font = ImageFont.load_default()
d.text((8, 6), "left: average PNG   middle: binary fixed-128 (v2)",
       fill=0, font=small_font)
d.text((8, 26), "right: binary adaptive (v3)",
       fill=0, font=small_font)
for r, (ch, c) in enumerate(faintest):
    y0 = 64 + r * (CELL2 + LABEL)
    arr = np.asarray(Image.open(os.path.join(GLYPHS, c["file"])).convert("L"), dtype=np.int16)
    ink = 255 - arr
    avg_img = Image.fromarray((255 - ink).astype(np.uint8), mode="L").resize((CELL2, CELL2), Image.LANCZOS)
    bin128 = Image.fromarray(((ink < 128) * 255).astype(np.uint8), mode="L").resize((CELL2, CELL2), Image.LANCZOS)
    binad = Image.fromarray(((ink < c["threshold_v3"]) * 255).astype(np.uint8), mode="L").resize((CELL2, CELL2), Image.LANCZOS)
    sheet2.paste(avg_img, (4, y0))
    sheet2.paste(bin128, (4 + CELL2, y0))
    sheet2.paste(binad, (4 + 2 * CELL2, y0))
    d.text((8, y0 + CELL2 + 4), f"{ch} ", fill=0, font=lab_font)
    d.text((34, y0 + CELL2 + 6),
           f"U+{ord(ch):04X} max_ink={c['max_ink']} contrib={c['contributors']} "
           f"thr_v3={c['threshold_v3']} px128={c['ink_px_fixed128']} px_adapt={c['ink_px_adaptive']}",
           fill=0, font=small_font)
sheet2.save(os.path.join(OUT, "faint_before_after_v3.png"))
print("saved faint_before_after_v3.png", sheet2.size)

# --- TTF typeset test ---
W2, H2 = 1500, 900
test = Image.new("RGB", (W2, H2), "white")
d = ImageDraw.Draw(test)
f64 = ImageFont.truetype(TTF, 64)
f48 = ImageFont.truetype(TTF, 48)
y = 20
d.text((20, y), "平均文字 v3 229書体 2290字", fill=(0, 0, 0), font=f64); y += 90
d.text((20, y), "あいうえおかきくけこさしすせそたちつてと", fill=(0, 0, 0), font=f48); y += 70
d.text((20, y), "アイウエオカキクケコサシスセソタチツテト", fill=(0, 0, 0), font=f48); y += 70
d.text((20, y), "日本語の平均文字 常用漢字二千百三十六字", fill=(0, 0, 0), font=f48); y += 70
d.text((20, y), "平均化の結果 0123456789 ABCXYZ abcxyz", fill=(0, 0, 0), font=f48); y += 90
d.text((20, y), "見えにくい漢字24字", fill=(0, 0, 0), font=f48); y += 70
faint_str = "".join(ch for ch, _ in faintest)
d.text((20, y), faint_str, fill=(0, 0, 0), font=f64); y += 90
d.text((20, y), "鬱も読める", fill=(0, 0, 0), font=f48)
test.save(os.path.join(OUT, "ttf_test_v3.png"))
print("saved ttf_test_v3.png")

# --- viewer ---
GROUPS = [
    ("hiragana", "ひらがな 46字"),
    ("katakana", "カタカナ 46字"),
    ("digits", "数字 0–9"),
    ("latin_upper", "英字 A–Z"),
    ("latin_lower", "英字 a–z"),
    ("kanji", "漢字 2136字（常用漢字フルセット）"),
]
cells = []
for g, title in GROUPS:
    items = [(ch, info) for ch, info in stats["chars"].items() if info["group"] == g]
    grid = "\n".join(
        f'      <figure><img src="glyphs_v3/{info["file"]}" alt="{ch}" loading="lazy">'
        f'<figcaption>{ch} <span>{info["codepoint"]} · {info["contributors"]}書体 · '
        f'max_ink {info["max_ink"]}</span></figcaption></figure>'
        for ch, info in items
    )
    cells.append(f'    <section><h2>{title}</h2><div class="grid">\n{grid}\n    </div></section>')

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>平均フォント v3 — 229書体・2290字</title>
<style>
  body {{ font-family: sans-serif; margin: 0 auto; max-width: 1100px; padding: 24px;
         background: #fafafa; color: #111; }}
  h1 {{ font-size: 26px; margin: 0 0 4px; }}
  p.lead {{ color: #444; margin: 4px 0 20px; }}
  h2 {{ font-size: 18px; border-bottom: 2px solid #111; padding-bottom: 4px; margin: 28px 0 12px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; }}
  figure {{ margin: 0; background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 6px; text-align: center; }}
  figure img {{ width: 100%; height: auto; display: block; }}
  figcaption {{ font-size: 15px; margin-top: 4px; }}
  figcaption span {{ display: block; font-size: 10px; color: #777; }}
  footer {{ color: #666; font-size: 12px; margin-top: 32px; border-top: 1px solid #ccc; padding-top: 12px; }}
  a {{ color: #0645ad; }}
</style>
</head>
<body>
<h1>平均フォント v3</h1>
<p class="lead">日本語オープンライセンス書体 <strong>229書体</strong> のグリフを 256×256px で描画し、
ピクセル単位で平均したもの。v3では漢字を常用漢字2136字フルセットに拡張し、
全 <strong>2290字</strong>。各文字は平均に寄与した書体数と平均インクの最大値付き。
滲んで見えるのは平均化の結果で、バグじゃない。</p>
<p class="lead">見えづらい漢字の調整: TTF化の二値化しきい値をグリフごとに適応化
（しきい値 = 0.40 × そのグリフの平均インク最大値、8〜128にクランプ）。
調整の前後比較は <a href="faint_before_after_v3.png">faint_before_after_v3.png</a>、
コンタクトシートは <a href="contact_sheet_v3.png">全2290字一覧</a>。
手法の詳細は <a href="../README.md">README.md</a> を参照。</p>
{''.join(cells)}
<footer>
  平均フォント v3 — 229 open-license Japanese fonts, pixel-averaged, 2290 chars.
  TTF版は <a href="../README.md">README</a> を参照。
</footer>
</body>
</html>
"""
with open(os.path.join(OUT, "viewer_v3.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("viewer_v3.html written")
