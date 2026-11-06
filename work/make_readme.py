#!/usr/bin/env python3
"""Generate README.md for the average-font project."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST

BASE = os.path.expanduser("~/workspace/average-font")
stats = json.load(open(os.path.join(BASE, "out", "stats.json"), encoding="utf-8"))

rows = []
n = 0
for d, fn, weights, name in MANIFEST:
    if weights:
        for w in weights:
            n += 1
            rows.append(f"| {n} | {name} {w} | `{fn}` |")
    else:
        n += 1
        rows.append(f"| {n} | {name} | `{fn}` |")

readme = f"""# 平均フォント — 229書体のピクセル平均

日本語オープンライセンス書体 **229書体** のグリフをビットマップ描画して
ピクセル平均した「平均フォント」（v2。v1は100書体、旧TTFは `AverageFont-Regular-v1-100fonts.ttf` に保存）。

## 成果物

| ファイル | 内容 |
|---|---|
| `AverageFont-Regular.ttf` | 平均グリフをベクター化したTTF（174字＋スペース）。インストールして使える |
| `out/viewer.html` | 文字ごとの平均グリフを並べたビューワー（ブラウザで開く） |
| `out/glyphs/*.png` | 平均グリフ174枚（256×256px、グレースケール） |
| `out/contact_sheet.png` | 全174字のコンタクトシート |
| `out/contact_sheet_*.png` | グループ別コンタクトシート（ひらがな／カタカナ／数字／英字／漢字） |
| `out/ttf_test.png` | TTFで実際に組版したテスト画像 |
| `out/stats.json` | 各文字の寄与書体数などの集計 |
| `SOURCES.md` | 元書体229書体の出所URL・ライセンス一覧 |
| `fonts/` | 元フォント190ファイル・約1.1GB（可変フォント5ファイルをウェイト展開して229書体分） |
| `work/` | 再現用スクリプト（ダウンロード／平均化／シート／TTF化） |

## 手法

1. **収集**: v1は Google Fonts の `google/fonts` リポジトリから OFL の日本語フォントを
   ダウンロード（`work/download_fonts.py`）。v2（2026-11-05）は google/fonts 未収録の
   ディスプレイ系・ドット系・レトロ系（Dela Gothic One、Rampart One、Zen Dots、だるまドロップなど）と、
   Source Han Sans/Serif JP、IPAex、Takao、VLゴシック、MigMix、Migu、UmePlus、
   Koruri、HackGen、UDEV Gothic、Moralerspace、PlemolJP、Cica、源柔ゴシック、源真ゴシック、
   源流明朝を追加（`work/download_fonts_v2.py`）。可変フォントは1ファイルから
   複数ウェイトを描画し、ウェイト違いを別書体として数えた（内訳は下記）。
2. **描画**: 各書体で対象文字を 256×256px のグレースケール画像に描画
   （フォントサイズ 200px、文字をキャンバス中央に配置 `anchor="mm"`）。
   可変フォントは Pillow の `set_variation_by_axes` でウェイトを指定。
3. **平均**: 文字ごとに、全書体の画素値を合計して寄与書体数で割った。
   欠けているグリフがある書体はその文字の平均から除外する設計。
   v2では **かな・英数字は229書体、漢字は227書体が寄与**（だるまドロップは漢字なし、
   Zen Dotsはかな・漢字なしのため、その文字の平均からは除外）。
   平均画像は `255 - 平均インク量` で白地に黒字として保存。
4. **TTF化**: 平均ビットマップを50%の濃度で二値化し、OpenCV の輪郭抽出
   （`RETR_CCOMP`、穴も保持）＋ `approxPolyDP` で多角形化して、
   fontTools で TTF のグリフ（直線セグメントのみ）として書き込んだ。
   テンプレートは DotGothic16（表組みのみ流用、アウトラインは全て平均由来）。
   ベースラインはグループごとにシフトで調整（下記「制限」参照）。

## 文字セット（174字）

- ひらがな46字、 カタカナ46字、 数字0–9、 英字A–Z、 英字a–z、
  漢字20字（日本年時分前後大小上下中左右山川田人月火）
- TTFにはさらにスペース（U+0020、空グリフ・送り500）を追加。
  句読点・濁点つき仮名・その他の漢字は **未収録**（豆腐になる）。

## v2 で変わったこと（100書体 → 229書体）

- **きつい書体枠を追加**: Dela Gothic One、Rampart One、Reggae One、RocknRoll One、
  Potta One、Mochiy Pop One/P One、Hachi Maru Pop、だるまドロップ、Zen Dots、
  Yuji 系、New Tegomin、しっぽりアンティーク、Murecho、M PLUS 1 ほか、
  太い・デコラティブ・ドット・レトロ系をまとめて投入。
- **平均への影響**: 太字・ディスプレイ系の比率が上がり、v2の平均は全体的に
  インク量が増えて（平均グリフの濃度 27.35/255 ≒ 10.7%）少し太く・黒くなった。
  ただし平均化でクセは相殺されるため、ドットの粒や極太の角はぼんやりした滲みに留まる。
  漢字は227書体寄与（だるまドロップ・Zen Dotsは漢字グリフなし）。
- **旧版の保存**: v1のTTFは `AverageFont-Regular-v1-100fonts.ttf` として残してある。

## 元書体229書体の内訳

- 可変フォント（ウェイト展開）: Noto Sans JP 9、Noto Serif JP 8、M PLUS 2 9、
  Murecho 9、M PLUS 1 9 ＝ 44書体
- google/fonts スタティック（v1: 80 ＋ v2追加 21）: Zen 角ゴ New 5、Zen 丸ゴ 5、
  Zen Old 明朝 3、Zen 角ゴ Antique 5、M PLUS 1p 7、M PLUS Rounded 1c 7、
  しっぽり明朝 5、しっぽり明朝 B1 5、BIZ UDゴシック 2、BIZ UDP明朝 2、BIZ UD明朝 2、
  BIZ UDPゴシック 2、Kaisei Decol 3、Kaisei Tokumin 4、Kaisei HarunoUmi 3、Kaisei Opti 3、
  Hina 明朝 1、DotGothic16 1、さわらびゴシック 1、さわらび明朝 1、Yusei Magic 1、
  Zen Kurenaido 1、Zen Antique 1、Zen Antique Soft 1、Stick 1、
  Dela Gothic One 1、Rampart One 1、Reggae One 1、RocknRoll One 1、Potta One 1、
  Mochiy Pop One 1、Mochiy Pop P One 1、Hachi Maru Pop 1、だるまドロップ 1、Zen Dots 1、
  Yuji Syuku 1、Yuji Mai 1、Yuji Boku 1、New Tegomin 1、しっぽりアンティーク 1、
  しっぽりアンティーク B1 1、Yomogi 1、Kiwi 丸 3、Klee One 2、IBM Plex Sans JP 7 ＝ 101書体
- google/fonts以外: Source Han Sans JP 7、Source Han Serif JP 7、IPAexゴシック 1、
  IPAex明朝 1、Takaoゴシック 1、Takao Pゴシック 1、Takao明朝 1、Takao P明朝 1、
  VLゴシック 1、VL Pゴシック 1、MigMix 8、Migu 8、UmePlusゴシック 1、UmePlus Pゴシック 1、
  Koruri 3、HackGen 4、UDEV Gothic 4、Moralerspace（Neon/Argon）4、PlemolJP 4、
  Cica 4、源柔ゴシック 7、源真ゴシック 7、源流明朝 JP 7 ＝ 84書体
- 全一覧（出所URL・ライセンス付き）は `SOURCES.md` を参照。

| # | 書体 | ファイル |
|---:|---|---|
{chr(10).join(rows)}

## ライセンス

- 元書体の大半は **SIL Open Font License 1.1 (OFL)**。
  ただし IPAex／Takao は IPAフォントライセンス、VLゴシックは VLゴシックライセンス、
  MigMix／Migu は Migu・MigMixライセンス、UmePlus は梅フォント派生ライセンスと、
  OFL以外のオープンライセンスの書体も含む（詳細は `SOURCES.md` のライセンス欄）。
  各ライセンスの条件（ライセンス文の同梱・改変時の改名など）に従うこと。
- 平均グリフ画像・TTF は229書体の画素統計から生成した派生物。
  「Average Font」という名前で新規フォントとして配布する場合は、
  OFL の Reserved Font Name（例：「Noto」「M PLUS」など）を使っていないことを確認済み。
  商用利用の可否は最終的に利用者の責任で確認すること。

## 制限・正直なところ

- **滲み**: 平均化の当然の結果として、グリフはぼやける。特に筆画の多い漢字や
  明朝・ゴシックが混ざる文字は輪郭が二重に見える。これはバグではなく手法の特性。
- **ベースライン**: 描画時に文字を中央揃えしたため、TTF化の際にグループ別に
  シフトで補正した（かな・漢字 −60、数字・大文字 −150、小文字 −250 単位）。
  完全なベースライン一致ではないので、本文組版には向かない。見出し・実験用途向け。
- **TTFの輪郭**: ベジェ曲線ではなく直線の多角形近似（`approxPolyDP`、許容誤差1.5px）。
  拡大するとカクつきが見える。ヒンティング・カーニングなし。
- **ndot jp について**: 依頼の「ndot jp（DotGothic16系、GitHubのndotjp）」は
  GitHub 上に `ndotjp` ユーザー／組織が存在せず、配布元が特定できる
  オープンライセンスの「Ndot JP」も見つからなかったため、ドットフォント枠は
  同じドット系で OFL の **DotGothic16** で代替した（詳細は `SOURCES.md`）。
- **小杉フォント**: google/fonts に未収録で、配布元（GitHub）の公式リリースも
  特定できなかったため今回は含めていない。
- **さざなみフォント**: 配布元（OSDN）のダウンロードURLが特定できず今回は見送った。
- **Koku 明朝／Koku ゴシック**: GitHubリポジトリが見つからず今回は含めていない。
- **文字数**: 174字＋スペースのみ。常用漢字フルセットではない。

## 再現方法

```sh
cd work
python3 download_fonts.py   # v1: 83ファイルを fonts/ に取得（約390MB）
python3 download_fonts_v2.py  # v2: 追加107ファイルを fonts/ に取得（計190ファイル・約1.1GB）
python3 render_average.py   # 平均PNG174枚を out/glyphs/ に生成
python3 make_sheets.py      # コンタクトシート生成
python3 make_viewer.py      # out/viewer.html 生成
./venv/bin/python build_ttf.py  # TTF生成（work/venv に opencv＋fontTools が必要）
```

## 検証

- 平均化：229書体 × 174字、寄与数 min 227 / max 229
  （かな92字は228、英数字62字は229、漢字20字は227）。
- TTF：fontTools で再読込し、グリフ176個（.notdef＋space＋174字）、
  cmap 175エントリを確認。Pillow でテスト組版し、目視で文字が読めることを確認
  （`out/ttf_test.png`）。
"""
with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print("README.md written, rows:", n)
