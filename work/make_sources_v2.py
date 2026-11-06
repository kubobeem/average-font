#!/usr/bin/env python3
"""Regenerate SOURCES.md for the v2 (229-font) average font."""
import os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST

BASE = os.path.expanduser("~/workspace/average-font")
GF = "https://github.com/google/fonts/blob/main/ofl/"

# filename -> (source URL, license) for non-google/fonts entries
EXT = {
    "SourceHanSansJP": ("https://github.com/adobe-fonts/source-han-sans/releases/tag/2.005R", "OFL-1.1"),
    "SourceHanSerifJP": ("https://github.com/adobe-fonts/source-han-serif/releases/tag/2.003R", "OFL-1.1"),
    "IPAexGothic": ("https://moji.or.jp/ipafont/ipaex00401/ (Debian fonts-ipaexfont)", "IPA Font License"),
    "IPAexMincho": ("https://moji.or.jp/ipafont/ipaex00401/ (Debian fonts-ipaexfont)", "IPA Font License"),
    "TakaoGothic": ("https://launchpad.net/takao-fonts (Debian fonts-takao)", "IPA Font License"),
    "TakaoPGothic": ("https://launchpad.net/takao-fonts (Debian fonts-takao)", "IPA Font License"),
    "TakaoMincho": ("https://launchpad.net/takao-fonts (Debian fonts-takao)", "IPA Font License"),
    "TakaoPMincho": ("https://launchpad.net/takao-fonts (Debian fonts-takao)", "IPA Font License"),
    "VLGothic-Regular": ("https://ja.osdn.net/projects/vlgothic/ (Debian fonts-vlgothic)", "VL Gothic License"),
    "VLPGothic-Regular": ("https://ja.osdn.net/projects/vlgothic/ (Debian fonts-vlgothic)", "VL Gothic License"),
    "MigMix": ("https://mix-mplus-ipa.sourceforge.io/migu/ (Debian fonts-migmix)", "MigMix License (M+/IPA-based)"),
    "Migu": ("https://mix-mplus-ipa.sourceforge.io/migu/ (Debian fonts-migmix)", "Migu License (M+/IPA-based)"),
    "UmePlus": ("https://ja.osdn.net/projects/ume-font/ (Debian fonts-umeplus)", "UmePlus License (Ume Font-based)"),
    "Koruri": ("https://github.com/Koruri/Koruri/releases/tag/20210720", "OFL-1.1"),
    "HackGen": ("https://github.com/yuru7/HackGen/releases/tag/v2.10.0", "OFL-1.1"),
    "UDEVGothic": ("https://github.com/yuru7/udev-gothic/releases/tag/v2.2.0", "OFL-1.1"),
    "Moralerspace": ("https://github.com/yuru7/moralerspace/releases/tag/v2.0.0", "OFL-1.1"),
    "PlemolJP": ("https://github.com/yuru7/PlemolJP/releases/tag/v3.1.0", "OFL-1.1"),
    "Cica": ("https://github.com/miiton/Cica/releases/tag/v5.0.3", "OFL-1.1"),
    "GenJyuuGothic": ("http://jikasei.me/font/genjyuu/ (OSDN mirror ftp.iij.ad.jp)", "OFL-1.1"),
    "GenShinGothic": ("http://jikasei.me/font/genshin/ (OSDN mirror ftp.iij.ad.jp)", "OFL-1.1"),
    "GenRyuMin2JP": ("https://github.com/ButTaiwan/genryu-font/releases/tag/v2.100", "OFL-1.1"),
}


def ext_source(fn):
    base = fn.rsplit(".", 1)[0]
    for key, (url, lic) in EXT.items():
        if base.startswith(key):
            return url, lic
    return "?", "?"


rows = []
n = 0
for d, fn, weights, name in MANIFEST:
    wlist = weights if weights else [None]
    for w in wlist:
        n += 1
        label = f"{name} ({w})" if w else name
        if d:  # google/fonts
            url = GF + d + "/" + urllib.parse.quote(fn)
            lic = "OFL-1.1"
        else:
            url, lic = ext_source(fn)
        rows.append(f"| {n} | {label} | `{fn}` | {url} | {lic} |")

doc = f"""# SOURCES — 平均フォントの元書体 229書体

v1（100書体）はすべて SIL Open Font License 1.1 (OFL) の日本語フォントで、
出所は Google Fonts の google/fonts リポジトリ（`main` ブランチ、2026-11-05 時点）。
v2（2026-11-05）で129書体を追加し、合計229書体になった。
追加分には OFL 以外のオープンライセンス（IPAフォントライセンス、VLゴシックライセンス、
Migu/MigMixライセンス、UmePlusライセンス）も含む。ライセンス欄を参照のこと。

可変フォント（Noto Sans JP / Noto Serif JP / M PLUS 2 / Murecho / M PLUS 1）は
1ファイルから複数ウェイトを描画しており、ウェイト違いを別書体として数えている。

| # | 書体 | ファイル | 出所URL | ライセンス |
|---:|---|---|---|---|
{chr(10).join(rows)}

## 追加できなかった書体

- **小杉フォント**: google/fonts に未収録で、公式リリースの特定もできず見送り。
- **さざなみフォント**: 配布元（OSDN）のダウンロードURLが特定できず見送り。
- **Koku 明朝／Koku ゴシック**: GitHubリポジトリが見つからず見送り。
- **ndot jp**: v1と同様、GitHub 上に `ndotjp` ユーザー／組織が存在せず配布元不明のため、
  ドットフォント枠は OFL の DotGothic16（＋ v2で Zen Dots を追加）で代替。
"""
with open(os.path.join(BASE, "SOURCES.md"), "w", encoding="utf-8") as f:
    f.write(doc)
print("SOURCES.md written, rows:", n)
