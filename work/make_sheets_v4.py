#!/usr/bin/env python3
"""v4 outputs: contact sheets, faint-kanji before/after sheet,
fewest-contributors sheet, TTF typeset test image, viewer_v4.html.

Files (v3 files untouched; everything v4 has a _v4 suffix):
- out/contact_sheet_v4.png, out/contact_sheet_v4_<group>.png
  (kanji split by JIS level: contact_sheet_v4_kanji_L1..L4)
- out/faint_before_after_v4.png : 24 faintest kanji, 3 columns
  (average PNG | binary fixed-128 (v2 method) | binary adaptive (v4))
- out/fewest_before_after_v4.png : 24 chars with fewest contributors
- out/ttf_test_v4.png : real typesetting with the v4 TTF. The test
  sentences deliberately use the NEW v4 chars (dakuten kana, small
  kana, long vowel, repetition marks, punctuation, L3/L4 kanji) --
  unlike v3, whose test text was restricted to already-covered chars.
  The script ASSERTS every test char is in the TTF cmap with a
  non-empty outline, so a tofu would fail loudly instead of being
  hidden by editing the test text.
- out/viewer_v4.html
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
from fontTools.ttLib import TTFont

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
GLYPHS = os.path.join(OUT, "glyphs_v4")
stats = json.load(open(os.path.join(OUT, "stats_v4.json"), encoding="utf-8"))
chars = list(stats["chars"].keys())
TTF = os.path.join(BASE, stats["ttf_file"])
print("TTF:", TTF)

tt = TTFont(TTF)
cmap = tt.getBestCmap()
glyf = tt["glyf"]
print("TTF glyphs:", len(tt.getGlyphOrder()), "cmap entries:", len(cmap))


def has_outline(ch):
    gname = cmap.get(ord(ch))
    if not gname:
        return False
    g = glyf[gname]
    return len(getattr(g, "coordinates", [])) > 0


# --- contact sheets ---
CELL = 48
COLS = 24
ROWS = (len(chars) + COLS - 1) // COLS
sheet = Image.new("L", (COLS * CELL, ROWS * CELL), 255)
for i, ch in enumerate(chars):
    info = stats["chars"][ch]
    im = Image.open(os.path.join(GLYPHS, info["file"])).resize(
        (CELL, CELL), Image.LANCZOS)
    sheet.paste(im, ((i % COLS) * CELL, (i // COLS) * CELL))
sheet.save(os.path.join(OUT, "contact_sheet_v4.png"))
print("saved contact_sheet_v4.png", sheet.size)

groups = defaultdict(list)
for ch in chars:
    info = stats["chars"][ch]
    if info["group"] == "kanji":
        groups["kanji_" + (info.get("jis_level") or "?")].append(ch)
    else:
        groups[info["group"]].append(ch)
for g, cl in sorted(groups.items()):
    rows = (len(cl) + COLS - 1) // COLS
    s = Image.new("L", (COLS * CELL, rows * CELL), 255)
    for i, ch in enumerate(cl):
        info = stats["chars"][ch]
        im = Image.open(os.path.join(GLYPHS, info["file"])).resize(
            (CELL, CELL), Image.LANCZOS)
        s.paste(im, ((i % COLS) * CELL, (i // COLS) * CELL))
    s.save(os.path.join(OUT, "contact_sheet_v4_%s.png" % g))
    print("saved", g, len(cl), s.size)


def before_after(rows24, path, title_lines):
    CELL2 = 160
    LABEL = 34
    W = 3 * CELL2 + 8
    H = len(rows24) * (CELL2 + LABEL) + 64
    sheet2 = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(sheet2)
    try:
        lab_font = ImageFont.truetype(TTF, 24)
        dejavu = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        small_font = ImageFont.truetype(dejavu, 16)
    except Exception:
        lab_font = small_font = ImageFont.load_default()
    d.text((8, 6), title_lines[0], fill=0, font=small_font)
    d.text((8, 26), title_lines[1], fill=0, font=small_font)
    for r, (ch, c) in enumerate(rows24):
        y0 = 64 + r * (CELL2 + LABEL)
        arr = np.asarray(Image.open(
            os.path.join(GLYPHS, c["file"])).convert("L"), dtype=np.int16)
        ink = 255 - arr
        avg_img = Image.fromarray(
            (255 - ink).astype(np.uint8), mode="L").resize(
                (CELL2, CELL2), Image.LANCZOS)
        bin128 = Image.fromarray(
            ((ink < 128) * 255).astype(np.uint8), mode="L").resize(
                (CELL2, CELL2), Image.LANCZOS)
        binad = Image.fromarray(
            ((ink < c["threshold_v4"]) * 255).astype(np.uint8),
            mode="L").resize((CELL2, CELL2), Image.LANCZOS)
        sheet2.paste(avg_img, (4, y0))
        sheet2.paste(bin128, (4 + CELL2, y0))
        sheet2.paste(binad, (4 + 2 * CELL2, y0))
        d.text((8, y0 + CELL2 + 4), "%s " % ch, fill=0, font=lab_font)
        d.text((34, y0 + CELL2 + 6),
               "U+%04X max_ink=%s contrib=%s thr_v4=%s px128=%s px_adapt=%s"
               % (ord(ch), c["max_ink"], c["contributors"],
                  c["threshold_v4"], c["ink_px_fixed128"],
                  c["ink_px_adaptive"]),
               fill=0, font=small_font)
    sheet2.save(path)
    print("saved", os.path.basename(path), sheet2.size)


# --- faint before/after sheet ---
kanji = [(ch, c) for ch, c in stats["chars"].items()
         if c["group"] == "kanji"]
faintest = sorted(kanji, key=lambda kv: kv[1]["max_ink"])[:24]
print("faintest 24:", [(ch, c["max_ink"], c["contributors"])
                       for ch, c in faintest])
before_after(faintest, os.path.join(OUT, "faint_before_after_v4.png"),
             ["left: average PNG   middle: binary fixed-128 (v2)",
              "right: binary adaptive (v4)"])

# --- fewest-contributors sheet ---
fewest = sorted(stats["chars"].items(),
                key=lambda kv: (kv[1]["contributors"], kv[1]["max_ink"]))[:24]
print("fewest 24:", [(ch, c["contributors"], c["max_ink"])
                     for ch, c in fewest])
before_after(fewest, os.path.join(OUT, "fewest_before_after_v4.png"),
             ["24 chars with fewest contributing fonts (v4)",
              "left: average PNG   middle: fixed-128   right: adaptive (v4)"])

# --- TTF typeset test (uses NEW v4 chars on purpose) ---
top_l3 = sorted(
    [(ch, c) for ch, c in stats["chars"].items()
     if c.get("jis_level") == "第3水準" and has_outline(ch)],
    key=lambda kv: -kv[1]["contributors"])[:8]
top_l4 = sorted(
    [(ch, c) for ch, c in stats["chars"].items()
     if c.get("jis_level") == "第4水準" and has_outline(ch)],
    key=lambda kv: -kv[1]["contributors"])[:8]
print("top L3:", "".join(ch for ch, _ in top_l3),
      [c["contributors"] for _, c in top_l3])
print("top L4:", "".join(ch for ch, _ in top_l4),
      [c["contributors"] for _, c in top_l4])
L3_STR = "".join(ch for ch, _ in top_l3)
L4_STR = "".join(ch for ch, _ in top_l4)

lines = [
    ("平均文字 v4 229書体 %d字" % stats["ttf_chars"], 64),
    ("がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉっゃゅょ", 48),
    ("ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポァィゥェォッャュョー", 48),
    ("じゅうようなじじつ：太陽は東から昇る。", 48),
    ("ウィークエンドにパーティーへ行く。ちょっと待って！", 48),
    ("『重要』なことは、もう一度言う。――太陽が昇る。", 48),
    ("くりかえし：ゝゞヽヾ", 48),
    ("第3水準：" + L3_STR, 48),
    ("第4水準：" + L4_STR, 48),
    ("人名用漢字：遙かなる琥珀の櫻、苺と蕾", 48),
    ("0123456789 ABCXYZ abcxyz 、。・（）〔〕【】！？…―〜：；－／＼＝＋×÷％", 40),
    ("見えにくい漢字：" + "".join(ch for ch, _ in faintest), 48),
]
# TOFU CHECK: every char in the test lines must be in the cmap
# with a non-empty outline. Fail loudly instead of editing the text.
missing = []
for text, _size in lines:
    for ch in text:
        if ch == " ":
            continue
        if not has_outline(ch):
            missing.append(ch)
print("TOFU CHECK missing chars:", missing)
assert not missing, "tofu in test lines: %s" % missing

W2, H2 = 1600, 1100
test = Image.new("RGB", (W2, H2), "white")
d = ImageDraw.Draw(test)
y = 20
for text, size in lines:
    f = ImageFont.truetype(TTF, size)
    d.text((20, y), text, fill=(0, 0, 0), font=f)
    y += size + 22
test.save(os.path.join(OUT, "ttf_test_v4.png"))
print("saved ttf_test_v4.png")

# --- viewer ---
SECTIONS = [
    ("hiragana", "ひらがな（清音＋濁音・半濁音・小さい仮名・繰り返し記号）"),
    ("katakana", "カタカナ（清音＋濁音・半濁音・小さい仮名・長音記号）"),
    ("punct", "句読点・記号"),
    ("digits", "数字 0–9"),
    ("latin_upper", "英字 A–Z"),
    ("latin_lower", "英字 a–z"),
    ("kanji_第1水準", "漢字 第1水準 2965字"),
    ("kanji_第2水準", "漢字 第2水準 3390字"),
    ("kanji_第3水準", "漢字 第3水準 1259字"),
    ("kanji_第4水準", "漢字 第4水準 2436字"),
]


def section_items(key):
    if key.startswith("kanji_"):
        lv = key.split("_", 1)[1]
        return [(ch, info) for ch, info in stats["chars"].items()
                if info["group"] == "kanji"
                and info.get("jis_level") == lv]
    return [(ch, info) for ch, info in stats["chars"].items()
            if info["group"] == key]


cells = []
for key, title in SECTIONS:
    items = section_items(key)
    grid = "\n".join(
        '      <figure><img src="glyphs_v4/%s" alt="%s" loading="lazy">'
        '<figcaption>%s <span>%s · %s書体 · max_ink %s</span></figcaption></figure>'
        % (info["file"], ch, ch, info["codepoint"], info["contributors"],
           info["max_ink"])
        for ch, info in items
    )
    cells.append('    <section><h2>%s（%d字）</h2><div class="grid">\n%s\n'
                 '    </div></section>' % (title, len(items), grid))

html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>平均フォント v4 — 229書体・%d字</title>
<style>
  body { font-family: sans-serif; margin: 0 auto; max-width: 1100px; padding: 24px;
         background: #fafafa; color: #111; }
  h1 { font-size: 26px; margin: 0 0 4px; }
  p.lead { color: #444; margin: 4px 0 20px; }
  h2 { font-size: 18px; border-bottom: 2px solid #111; padding-bottom: 4px; margin: 28px 0 12px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; }
  figure { margin: 0; background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 6px; text-align: center; }
  figure img { width: 100%%; height: auto; display: block; }
  figcaption { font-size: 15px; margin-top: 4px; }
  figcaption span { display: block; font-size: 10px; color: #777; }
  footer { color: #666; font-size: 12px; margin-top: 32px; border-top: 1px solid #ccc; padding-top: 12px; }
  a { color: #0645ad; }
</style>
</head>
<body>
<h1>平均フォント v4</h1>
<p class="lead">日本語オープンライセンス書体 <strong>229書体</strong> のグリフを 256×256px で描画し、
ピクセル単位で平均したもの。v4では漢字をJIS X 0213 全10050字（第1〜第4水準）に拡張し、
濁点つき仮名・小さい仮名・長音記号・句読点・記号も追加して全 <strong>%d字</strong>。
各文字は平均に寄与した書体数と平均インクの最大値付き。
滲んで見えるのは平均化の結果で、バグじゃない。</p>
<p class="lead">TTF化の二値化しきい値はグリフごとに適応化
（しきい値 = 0.40 × そのグリフの平均インク最大値、8〜128にクランプ）。
寄与書体が0の字はTTFから除外してある（空グリフ0を維持）。
調整の前後比較は <a href="faint_before_after_v4.png">faint_before_after_v4.png</a>、
寄与の少ない字は <a href="fewest_before_after_v4.png">fewest_before_after_v4.png</a>、
コンタクトシートは <a href="contact_sheet_v4.png">全%d字一覧</a>。
手法の詳細は <a href="../README.md">README.md</a> を参照。</p>
%s
<footer>
  平均フォント v4 — 229 open-license Japanese fonts, pixel-averaged, %d chars.
  TTF版は <a href="../README.md">README</a> を参照。
</footer>
</body>
</html>
""" % (stats["total_chars"], stats["ttf_chars"], stats["total_chars"],
       "".join(cells), stats["ttf_chars"])
with open(os.path.join(OUT, "viewer_v4.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("viewer_v4.html written")
