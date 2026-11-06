# 平均フォント — 229書体のピクセル平均

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
| 1 | Noto Sans JP 100 | `NotoSansJP[wght].ttf` |
| 2 | Noto Sans JP 200 | `NotoSansJP[wght].ttf` |
| 3 | Noto Sans JP 300 | `NotoSansJP[wght].ttf` |
| 4 | Noto Sans JP 400 | `NotoSansJP[wght].ttf` |
| 5 | Noto Sans JP 500 | `NotoSansJP[wght].ttf` |
| 6 | Noto Sans JP 600 | `NotoSansJP[wght].ttf` |
| 7 | Noto Sans JP 700 | `NotoSansJP[wght].ttf` |
| 8 | Noto Sans JP 800 | `NotoSansJP[wght].ttf` |
| 9 | Noto Sans JP 900 | `NotoSansJP[wght].ttf` |
| 10 | Noto Serif JP 200 | `NotoSerifJP[wght].ttf` |
| 11 | Noto Serif JP 300 | `NotoSerifJP[wght].ttf` |
| 12 | Noto Serif JP 400 | `NotoSerifJP[wght].ttf` |
| 13 | Noto Serif JP 500 | `NotoSerifJP[wght].ttf` |
| 14 | Noto Serif JP 600 | `NotoSerifJP[wght].ttf` |
| 15 | Noto Serif JP 700 | `NotoSerifJP[wght].ttf` |
| 16 | Noto Serif JP 800 | `NotoSerifJP[wght].ttf` |
| 17 | Noto Serif JP 900 | `NotoSerifJP[wght].ttf` |
| 18 | M PLUS 2 100 | `MPLUS2[wght].ttf` |
| 19 | M PLUS 2 200 | `MPLUS2[wght].ttf` |
| 20 | M PLUS 2 300 | `MPLUS2[wght].ttf` |
| 21 | M PLUS 2 400 | `MPLUS2[wght].ttf` |
| 22 | M PLUS 2 500 | `MPLUS2[wght].ttf` |
| 23 | M PLUS 2 600 | `MPLUS2[wght].ttf` |
| 24 | M PLUS 2 700 | `MPLUS2[wght].ttf` |
| 25 | M PLUS 2 800 | `MPLUS2[wght].ttf` |
| 26 | M PLUS 2 900 | `MPLUS2[wght].ttf` |
| 27 | Zen Kaku Gothic New Light | `ZenKakuGothicNew-Light.ttf` |
| 28 | Zen Kaku Gothic New Regular | `ZenKakuGothicNew-Regular.ttf` |
| 29 | Zen Kaku Gothic New Medium | `ZenKakuGothicNew-Medium.ttf` |
| 30 | Zen Kaku Gothic New Bold | `ZenKakuGothicNew-Bold.ttf` |
| 31 | Zen Kaku Gothic New Black | `ZenKakuGothicNew-Black.ttf` |
| 32 | Zen Maru Gothic Light | `ZenMaruGothic-Light.ttf` |
| 33 | Zen Maru Gothic Regular | `ZenMaruGothic-Regular.ttf` |
| 34 | Zen Maru Gothic Medium | `ZenMaruGothic-Medium.ttf` |
| 35 | Zen Maru Gothic Bold | `ZenMaruGothic-Bold.ttf` |
| 36 | Zen Maru Gothic Black | `ZenMaruGothic-Black.ttf` |
| 37 | Zen Old Mincho Regular | `ZenOldMincho-Regular.ttf` |
| 38 | Zen Old Mincho Bold | `ZenOldMincho-Bold.ttf` |
| 39 | Zen Old Mincho Black | `ZenOldMincho-Black.ttf` |
| 40 | Zen Kaku Gothic Antique Light | `ZenKakuGothicAntique-Light.ttf` |
| 41 | Zen Kaku Gothic Antique Regular | `ZenKakuGothicAntique-Regular.ttf` |
| 42 | Zen Kaku Gothic Antique Medium | `ZenKakuGothicAntique-Medium.ttf` |
| 43 | Zen Kaku Gothic Antique Bold | `ZenKakuGothicAntique-Bold.ttf` |
| 44 | Zen Kaku Gothic Antique Black | `ZenKakuGothicAntique-Black.ttf` |
| 45 | M PLUS 1p Thin | `MPLUS1p-Thin.ttf` |
| 46 | M PLUS 1p Light | `MPLUS1p-Light.ttf` |
| 47 | M PLUS 1p Regular | `MPLUS1p-Regular.ttf` |
| 48 | M PLUS 1p Medium | `MPLUS1p-Medium.ttf` |
| 49 | M PLUS 1p Bold | `MPLUS1p-Bold.ttf` |
| 50 | M PLUS 1p ExtraBold | `MPLUS1p-ExtraBold.ttf` |
| 51 | M PLUS 1p Black | `MPLUS1p-Black.ttf` |
| 52 | M PLUS Rounded 1c Thin | `MPLUSRounded1c-Thin.ttf` |
| 53 | M PLUS Rounded 1c Light | `MPLUSRounded1c-Light.ttf` |
| 54 | M PLUS Rounded 1c Regular | `MPLUSRounded1c-Regular.ttf` |
| 55 | M PLUS Rounded 1c Medium | `MPLUSRounded1c-Medium.ttf` |
| 56 | M PLUS Rounded 1c Bold | `MPLUSRounded1c-Bold.ttf` |
| 57 | M PLUS Rounded 1c ExtraBold | `MPLUSRounded1c-ExtraBold.ttf` |
| 58 | M PLUS Rounded 1c Black | `MPLUSRounded1c-Black.ttf` |
| 59 | Shippori Mincho Regular | `ShipporiMincho-Regular.ttf` |
| 60 | Shippori Mincho Medium | `ShipporiMincho-Medium.ttf` |
| 61 | Shippori Mincho SemiBold | `ShipporiMincho-SemiBold.ttf` |
| 62 | Shippori Mincho Bold | `ShipporiMincho-Bold.ttf` |
| 63 | Shippori Mincho ExtraBold | `ShipporiMincho-ExtraBold.ttf` |
| 64 | Shippori Mincho B1 Regular | `ShipporiMinchoB1-Regular.ttf` |
| 65 | Shippori Mincho B1 Medium | `ShipporiMinchoB1-Medium.ttf` |
| 66 | Shippori Mincho B1 Bold | `ShipporiMinchoB1-Bold.ttf` |
| 67 | IBM Plex Sans JP Thin | `IBMPlexSansJP-Thin.ttf` |
| 68 | IBM Plex Sans JP ExtraLight | `IBMPlexSansJP-ExtraLight.ttf` |
| 69 | IBM Plex Sans JP Light | `IBMPlexSansJP-Light.ttf` |
| 70 | IBM Plex Sans JP Regular | `IBMPlexSansJP-Regular.ttf` |
| 71 | IBM Plex Sans JP Medium | `IBMPlexSansJP-Medium.ttf` |
| 72 | IBM Plex Sans JP SemiBold | `IBMPlexSansJP-SemiBold.ttf` |
| 73 | IBM Plex Sans JP Bold | `IBMPlexSansJP-Bold.ttf` |
| 74 | Kiwi Maru Light | `KiwiMaru-Light.ttf` |
| 75 | Kiwi Maru Regular | `KiwiMaru-Regular.ttf` |
| 76 | Kiwi Maru Medium | `KiwiMaru-Medium.ttf` |
| 77 | Klee One Regular | `KleeOne-Regular.ttf` |
| 78 | Klee One SemiBold | `KleeOne-SemiBold.ttf` |
| 79 | BIZ UDGothic Regular | `BIZUDGothic-Regular.ttf` |
| 80 | BIZ UDGothic Bold | `BIZUDGothic-Bold.ttf` |
| 81 | BIZ UDPMincho Regular | `BIZUDPMincho-Regular.ttf` |
| 82 | BIZ UDPMincho Bold | `BIZUDPMincho-Bold.ttf` |
| 83 | BIZ UDMincho Regular | `BIZUDMincho-Regular.ttf` |
| 84 | BIZ UDMincho Bold | `BIZUDMincho-Bold.ttf` |
| 85 | Kaisei Decol Regular | `KaiseiDecol-Regular.ttf` |
| 86 | Kaisei Decol Medium | `KaiseiDecol-Medium.ttf` |
| 87 | Kaisei Decol Bold | `KaiseiDecol-Bold.ttf` |
| 88 | Kaisei Tokumin Regular | `KaiseiTokumin-Regular.ttf` |
| 89 | Kaisei Tokumin Medium | `KaiseiTokumin-Medium.ttf` |
| 90 | Kaisei Tokumin Bold | `KaiseiTokumin-Bold.ttf` |
| 91 | Kaisei Tokumin ExtraBold | `KaiseiTokumin-ExtraBold.ttf` |
| 92 | Kaisei HarunoUmi Regular | `KaiseiHarunoUmi-Regular.ttf` |
| 93 | Kaisei HarunoUmi Medium | `KaiseiHarunoUmi-Medium.ttf` |
| 94 | Kaisei HarunoUmi Bold | `KaiseiHarunoUmi-Bold.ttf` |
| 95 | Kaisei Opti Regular | `KaiseiOpti-Regular.ttf` |
| 96 | Kaisei Opti Medium | `KaiseiOpti-Medium.ttf` |
| 97 | Kaisei Opti Bold | `KaiseiOpti-Bold.ttf` |
| 98 | Hina Mincho | `HinaMincho-Regular.ttf` |
| 99 | DotGothic16 | `DotGothic16-Regular.ttf` |
| 100 | さわらびゴシック | `SawarabiGothic-Regular.ttf` |
| 101 | さわらび明朝 | `SawarabiMincho-Regular.ttf` |
| 102 | Yusei Magic | `YuseiMagic-Regular.ttf` |
| 103 | Zen Kurenaido | `ZenKurenaido-Regular.ttf` |
| 104 | Zen Antique | `ZenAntique-Regular.ttf` |
| 105 | Zen Antique Soft | `ZenAntiqueSoft-Regular.ttf` |
| 106 | Stick | `Stick-Regular.ttf` |
| 107 | Dela Gothic One | `DelaGothicOne-Regular.ttf` |
| 108 | Rampart One | `RampartOne-Regular.ttf` |
| 109 | Reggae One | `ReggaeOne-Regular.ttf` |
| 110 | RocknRoll One | `RocknRollOne-Regular.ttf` |
| 111 | Potta One | `PottaOne-Regular.ttf` |
| 112 | Mochiy Pop One | `MochiyPopOne-Regular.ttf` |
| 113 | Mochiy Pop P One | `MochiyPopPOne-Regular.ttf` |
| 114 | Hachi Maru Pop | `HachiMaruPop-Regular.ttf` |
| 115 | Darumadrop One | `DarumadropOne-Regular.ttf` |
| 116 | Zen Dots | `ZenDots-Regular.ttf` |
| 117 | Yuji Syuku | `YujiSyuku-Regular.ttf` |
| 118 | Yuji Mai | `YujiMai-Regular.ttf` |
| 119 | Yuji Boku | `YujiBoku-Regular.ttf` |
| 120 | New Tegomin | `NewTegomin-Regular.ttf` |
| 121 | Shippori Antique | `ShipporiAntique-Regular.ttf` |
| 122 | Shippori Antique B1 | `ShipporiAntiqueB1-Regular.ttf` |
| 123 | Yomogi | `Yomogi-Regular.ttf` |
| 124 | Murecho 100 | `Murecho[wght].ttf` |
| 125 | Murecho 200 | `Murecho[wght].ttf` |
| 126 | Murecho 300 | `Murecho[wght].ttf` |
| 127 | Murecho 400 | `Murecho[wght].ttf` |
| 128 | Murecho 500 | `Murecho[wght].ttf` |
| 129 | Murecho 600 | `Murecho[wght].ttf` |
| 130 | Murecho 700 | `Murecho[wght].ttf` |
| 131 | Murecho 800 | `Murecho[wght].ttf` |
| 132 | Murecho 900 | `Murecho[wght].ttf` |
| 133 | M PLUS 1 100 | `MPLUS1[wght].ttf` |
| 134 | M PLUS 1 200 | `MPLUS1[wght].ttf` |
| 135 | M PLUS 1 300 | `MPLUS1[wght].ttf` |
| 136 | M PLUS 1 400 | `MPLUS1[wght].ttf` |
| 137 | M PLUS 1 500 | `MPLUS1[wght].ttf` |
| 138 | M PLUS 1 600 | `MPLUS1[wght].ttf` |
| 139 | M PLUS 1 700 | `MPLUS1[wght].ttf` |
| 140 | M PLUS 1 800 | `MPLUS1[wght].ttf` |
| 141 | M PLUS 1 900 | `MPLUS1[wght].ttf` |
| 142 | BIZ UDPGothic Regular | `BIZUDPGothic-Regular.ttf` |
| 143 | BIZ UDPGothic Bold | `BIZUDPGothic-Bold.ttf` |
| 144 | Shippori Mincho B1 SemiBold | `ShipporiMinchoB1-SemiBold.ttf` |
| 145 | Shippori Mincho B1 ExtraBold | `ShipporiMinchoB1-ExtraBold.ttf` |
| 146 | Source Han Sans JP ExtraLight | `SourceHanSansJP-ExtraLight.otf` |
| 147 | Source Han Sans JP Light | `SourceHanSansJP-Light.otf` |
| 148 | Source Han Sans JP Normal | `SourceHanSansJP-Normal.otf` |
| 149 | Source Han Sans JP Regular | `SourceHanSansJP-Regular.otf` |
| 150 | Source Han Sans JP Medium | `SourceHanSansJP-Medium.otf` |
| 151 | Source Han Sans JP Bold | `SourceHanSansJP-Bold.otf` |
| 152 | Source Han Sans JP Heavy | `SourceHanSansJP-Heavy.otf` |
| 153 | Source Han Serif JP ExtraLight | `SourceHanSerifJP-ExtraLight.otf` |
| 154 | Source Han Serif JP Light | `SourceHanSerifJP-Light.otf` |
| 155 | Source Han Serif JP Regular | `SourceHanSerifJP-Regular.otf` |
| 156 | Source Han Serif JP Medium | `SourceHanSerifJP-Medium.otf` |
| 157 | Source Han Serif JP SemiBold | `SourceHanSerifJP-SemiBold.otf` |
| 158 | Source Han Serif JP Bold | `SourceHanSerifJP-Bold.otf` |
| 159 | Source Han Serif JP Heavy | `SourceHanSerifJP-Heavy.otf` |
| 160 | IPAexゴシック | `IPAexGothic.ttf` |
| 161 | IPAex明朝 | `IPAexMincho.ttf` |
| 162 | Takaoゴシック | `TakaoGothic.ttf` |
| 163 | Takao Pゴシック | `TakaoPGothic.ttf` |
| 164 | Takao明朝 | `TakaoMincho.ttf` |
| 165 | Takao P明朝 | `TakaoPMincho.ttf` |
| 166 | VLゴシック | `VLGothic-Regular.ttf` |
| 167 | VL Pゴシック | `VLPGothic-Regular.ttf` |
| 168 | MigMix 1P Regular | `MigMix-1P-Regular.ttf` |
| 169 | MigMix 1P Bold | `MigMix-1P-Bold.ttf` |
| 170 | MigMix 2P Regular | `MigMix-2P-Regular.ttf` |
| 171 | MigMix 2P Bold | `MigMix-2P-Bold.ttf` |
| 172 | MigMix 1M Regular | `MigMix-1M-Regular.ttf` |
| 173 | MigMix 1M Bold | `MigMix-1M-Bold.ttf` |
| 174 | MigMix 2M Regular | `MigMix-2M-Regular.ttf` |
| 175 | MigMix 2M Bold | `MigMix-2M-Bold.ttf` |
| 176 | Migu 1M Regular | `Migu-1M-Regular.ttf` |
| 177 | Migu 1M Bold | `Migu-1M-Bold.ttf` |
| 178 | Migu 1C Regular | `Migu-1C-Regular.ttf` |
| 179 | Migu 1C Bold | `Migu-1C-Bold.ttf` |
| 180 | Migu 1P Regular | `Migu-1P-Regular.ttf` |
| 181 | Migu 1P Bold | `Migu-1P-Bold.ttf` |
| 182 | Migu 2M Regular | `Migu-2M-Regular.ttf` |
| 183 | Migu 2M Bold | `Migu-2M-Bold.ttf` |
| 184 | UmePlusゴシック | `UmePlus-Gothic.ttf` |
| 185 | UmePlus Pゴシック | `UmePlus-P-Gothic.ttf` |
| 186 | Koruri Regular | `Koruri-Regular.ttf` |
| 187 | Koruri Bold | `Koruri-Bold.ttf` |
| 188 | Koruri Semibold | `Koruri-Semibold.ttf` |
| 189 | HackGen Regular | `HackGen-Regular.ttf` |
| 190 | HackGen Bold | `HackGen-Bold.ttf` |
| 191 | HackGen Console Regular | `HackGenConsole-Regular.ttf` |
| 192 | HackGen Console Bold | `HackGenConsole-Bold.ttf` |
| 193 | UDEV Gothic Regular | `UDEVGothic-Regular.ttf` |
| 194 | UDEV Gothic Bold | `UDEVGothic-Bold.ttf` |
| 195 | UDEV Gothic 35 Regular | `UDEVGothic35-Regular.ttf` |
| 196 | UDEV Gothic 35 Bold | `UDEVGothic35-Bold.ttf` |
| 197 | Moralerspace Neon Regular | `MoralerspaceNeon-Regular.ttf` |
| 198 | Moralerspace Neon Bold | `MoralerspaceNeon-Bold.ttf` |
| 199 | Moralerspace Argon Regular | `MoralerspaceArgon-Regular.ttf` |
| 200 | Moralerspace Argon Bold | `MoralerspaceArgon-Bold.ttf` |
| 201 | PlemolJP Regular | `PlemolJP-Regular.ttf` |
| 202 | PlemolJP Bold | `PlemolJP-Bold.ttf` |
| 203 | PlemolJP Console Regular | `PlemolJPConsole-Regular.ttf` |
| 204 | PlemolJP Console Bold | `PlemolJPConsole-Bold.ttf` |
| 205 | Cica Regular | `Cica-Regular.ttf` |
| 206 | Cica Bold | `Cica-Bold.ttf` |
| 207 | Cica Bold Italic | `Cica-BoldItalic.ttf` |
| 208 | Cica Regular Italic | `Cica-RegularItalic.ttf` |
| 209 | GenJyuuGothic ExtraLight | `GenJyuuGothic-ExtraLight.ttf` |
| 210 | GenJyuuGothic Light | `GenJyuuGothic-Light.ttf` |
| 211 | GenJyuuGothic Normal | `GenJyuuGothic-Normal.ttf` |
| 212 | GenJyuuGothic Regular | `GenJyuuGothic-Regular.ttf` |
| 213 | GenJyuuGothic Medium | `GenJyuuGothic-Medium.ttf` |
| 214 | GenJyuuGothic Bold | `GenJyuuGothic-Bold.ttf` |
| 215 | GenJyuuGothic Heavy | `GenJyuuGothic-Heavy.ttf` |
| 216 | GenShinGothic ExtraLight | `GenShinGothic-ExtraLight.ttf` |
| 217 | GenShinGothic Light | `GenShinGothic-Light.ttf` |
| 218 | GenShinGothic Normal | `GenShinGothic-Normal.ttf` |
| 219 | GenShinGothic Regular | `GenShinGothic-Regular.ttf` |
| 220 | GenShinGothic Medium | `GenShinGothic-Medium.ttf` |
| 221 | GenShinGothic Bold | `GenShinGothic-Bold.ttf` |
| 222 | GenShinGothic Heavy | `GenShinGothic-Heavy.ttf` |
| 223 | GenRyuMin JP ExtraLight | `GenRyuMin2JP-ExtraLight.otf` |
| 224 | GenRyuMin JP Light | `GenRyuMin2JP-Light.otf` |
| 225 | GenRyuMin JP Regular | `GenRyuMin2JP-Regular.otf` |
| 226 | GenRyuMin JP Medium | `GenRyuMin2JP-Medium.otf` |
| 227 | GenRyuMin JP SemiBold | `GenRyuMin2JP-SemiBold.otf` |
| 228 | GenRyuMin JP Bold | `GenRyuMin2JP-Bold.otf` |
| 229 | GenRyuMin JP Heavy | `GenRyuMin2JP-Heavy.otf` |

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
