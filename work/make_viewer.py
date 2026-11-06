#!/usr/bin/env python3
"""Generate viewer.html for the average font."""
import json, os

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
stats = json.load(open(os.path.join(OUT, "stats.json"), encoding="utf-8"))

GROUPS = [
    ("hiragana", "ひらがな 46字"),
    ("katakana", "カタカナ 46字"),
    ("digits", "数字 0–9"),
    ("latin_upper", "英字 A–Z"),
    ("latin_lower", "英字 a–z"),
    ("kanji", "漢字 20字"),
]

cells = []
for g, title in GROUPS:
    items = [(ch, info) for ch, info in stats["chars"].items() if info["group"] == g]
    grid = "\n".join(
        f'      <figure><img src="glyphs/{info["file"]}" alt="{ch}" loading="lazy">'
        f'<figcaption>{ch} <span>{info["codepoint"]} · {info["contributors"]}書体</span></figcaption></figure>'
        for ch, info in items
    )
    cells.append(f'    <section><h2>{title}</h2><div class="grid">\n{grid}\n    </div></section>')

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>平均フォント — 100書体のピクセル平均</title>
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
<h1>平均フォント</h1>
<p class="lead">日本語オープンライセンス書体 <strong>100書体</strong> のグリフを 256×256px で描画し、
ピクセル単位で平均したもの。各文字は平均に寄与した書体数（100書体中）付き。
滲んで見えるのは平均化の結果で、バグじゃない。</p>
<p class="lead">手法の詳細と書体一覧は <a href="../README.md">README.md</a> / <a href="../SOURCES.md">SOURCES.md</a> を参照。
コンタクトシート: <a href="contact_sheet.png">全174字一覧</a></p>
{''.join(cells)}
<footer>
  平均フォント — 100 open-license Japanese fonts, pixel-averaged.
  全書体 SIL Open Font License 1.1 (OFL)。元フォントは <code>fonts/</code> に収録。
  平均グリフ画像は各フォントの著作物の派生物ではなく、画素統計の可視化として扱うこと。
  TTF版は <a href="../README.md">README</a> の「TTFについて」を参照。
</footer>
</body>
</html>
"""
with open(os.path.join(OUT, "viewer.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("viewer.html written")
