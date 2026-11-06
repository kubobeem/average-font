#!/usr/bin/env python3
"""Download the 100-font manifest for the average-font project.
Sources: google/fonts (OFL 1.1) via raw.githubusercontent.com.
Variable fonts are downloaded once and rendered at multiple weights.
"""
import json, os, subprocess, sys, urllib.parse

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
OUT = os.path.expanduser("~/workspace/average-font/fonts")

# (family dir, filename, [weights or None for static], display name base)
MANIFEST = [
    ("notosansjp", "NotoSansJP[wght].ttf", [100,200,300,400,500,600,700,800,900], "Noto Sans JP"),
    ("notoserifjp", "NotoSerifJP[wght].ttf", [200,300,400,500,600,700,800,900], "Noto Serif JP"),
    ("mplus2", "MPLUS2[wght].ttf", [100,200,300,400,500,600,700,800,900], "M PLUS 2"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Light.ttf", None, "Zen Kaku Gothic New Light"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Regular.ttf", None, "Zen Kaku Gothic New Regular"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Medium.ttf", None, "Zen Kaku Gothic New Medium"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Bold.ttf", None, "Zen Kaku Gothic New Bold"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Black.ttf", None, "Zen Kaku Gothic New Black"),
    ("zenmarugothic", "ZenMaruGothic-Light.ttf", None, "Zen Maru Gothic Light"),
    ("zenmarugothic", "ZenMaruGothic-Regular.ttf", None, "Zen Maru Gothic Regular"),
    ("zenmarugothic", "ZenMaruGothic-Medium.ttf", None, "Zen Maru Gothic Medium"),
    ("zenmarugothic", "ZenMaruGothic-Bold.ttf", None, "Zen Maru Gothic Bold"),
    ("zenmarugothic", "ZenMaruGothic-Black.ttf", None, "Zen Maru Gothic Black"),
    ("zenoldmincho", "ZenOldMincho-Regular.ttf", None, "Zen Old Mincho Regular"),
    ("zenoldmincho", "ZenOldMincho-Bold.ttf", None, "Zen Old Mincho Bold"),
    ("zenoldmincho", "ZenOldMincho-Black.ttf", None, "Zen Old Mincho Black"),
    ("zenkakugothicantique", "ZenKakuGothicAntique-Light.ttf", None, "Zen Kaku Gothic Antique Light"),
    ("zenkakugothicantique", "ZenKakuGothicAntique-Regular.ttf", None, "Zen Kaku Gothic Antique Regular"),
    ("zenkakugothicantique", "ZenKakuGothicAntique-Medium.ttf", None, "Zen Kaku Gothic Antique Medium"),
    ("zenkakugothicantique", "ZenKakuGothicAntique-Bold.ttf", None, "Zen Kaku Gothic Antique Bold"),
    ("zenkakugothicantique", "ZenKakuGothicAntique-Black.ttf", None, "Zen Kaku Gothic Antique Black"),
    ("mplus1p", "MPLUS1p-Thin.ttf", None, "M PLUS 1p Thin"),
    ("mplus1p", "MPLUS1p-Light.ttf", None, "M PLUS 1p Light"),
    ("mplus1p", "MPLUS1p-Regular.ttf", None, "M PLUS 1p Regular"),
    ("mplus1p", "MPLUS1p-Medium.ttf", None, "M PLUS 1p Medium"),
    ("mplus1p", "MPLUS1p-Bold.ttf", None, "M PLUS 1p Bold"),
    ("mplus1p", "MPLUS1p-ExtraBold.ttf", None, "M PLUS 1p ExtraBold"),
    ("mplus1p", "MPLUS1p-Black.ttf", None, "M PLUS 1p Black"),
    ("mplusrounded1c", "MPLUSRounded1c-Thin.ttf", None, "M PLUS Rounded 1c Thin"),
    ("mplusrounded1c", "MPLUSRounded1c-Light.ttf", None, "M PLUS Rounded 1c Light"),
    ("mplusrounded1c", "MPLUSRounded1c-Regular.ttf", None, "M PLUS Rounded 1c Regular"),
    ("mplusrounded1c", "MPLUSRounded1c-Medium.ttf", None, "M PLUS Rounded 1c Medium"),
    ("mplusrounded1c", "MPLUSRounded1c-Bold.ttf", None, "M PLUS Rounded 1c Bold"),
    ("mplusrounded1c", "MPLUSRounded1c-ExtraBold.ttf", None, "M PLUS Rounded 1c ExtraBold"),
    ("mplusrounded1c", "MPLUSRounded1c-Black.ttf", None, "M PLUS Rounded 1c Black"),
    ("shipporimincho", "ShipporiMincho-Regular.ttf", None, "Shippori Mincho Regular"),
    ("shipporimincho", "ShipporiMincho-Medium.ttf", None, "Shippori Mincho Medium"),
    ("shipporimincho", "ShipporiMincho-SemiBold.ttf", None, "Shippori Mincho SemiBold"),
    ("shipporimincho", "ShipporiMincho-Bold.ttf", None, "Shippori Mincho Bold"),
    ("shipporimincho", "ShipporiMincho-ExtraBold.ttf", None, "Shippori Mincho ExtraBold"),
    ("shipporiminchob1", "ShipporiMinchoB1-Regular.ttf", None, "Shippori Mincho B1 Regular"),
    ("shipporiminchob1", "ShipporiMinchoB1-Medium.ttf", None, "Shippori Mincho B1 Medium"),
    ("shipporiminchob1", "ShipporiMinchoB1-Bold.ttf", None, "Shippori Mincho B1 Bold"),
    ("ibmplexsansjp", "IBMPlexSansJP-Thin.ttf", None, "IBM Plex Sans JP Thin"),
    ("ibmplexsansjp", "IBMPlexSansJP-ExtraLight.ttf", None, "IBM Plex Sans JP ExtraLight"),
    ("ibmplexsansjp", "IBMPlexSansJP-Light.ttf", None, "IBM Plex Sans JP Light"),
    ("ibmplexsansjp", "IBMPlexSansJP-Regular.ttf", None, "IBM Plex Sans JP Regular"),
    ("ibmplexsansjp", "IBMPlexSansJP-Medium.ttf", None, "IBM Plex Sans JP Medium"),
    ("ibmplexsansjp", "IBMPlexSansJP-SemiBold.ttf", None, "IBM Plex Sans JP SemiBold"),
    ("ibmplexsansjp", "IBMPlexSansJP-Bold.ttf", None, "IBM Plex Sans JP Bold"),
    ("kiwimaru", "KiwiMaru-Light.ttf", None, "Kiwi Maru Light"),
    ("kiwimaru", "KiwiMaru-Regular.ttf", None, "Kiwi Maru Regular"),
    ("kiwimaru", "KiwiMaru-Medium.ttf", None, "Kiwi Maru Medium"),
    ("kleeone", "KleeOne-Regular.ttf", None, "Klee One Regular"),
    ("kleeone", "KleeOne-SemiBold.ttf", None, "Klee One SemiBold"),
    ("bizudgothic", "BIZUDGothic-Regular.ttf", None, "BIZ UDGothic Regular"),
    ("bizudgothic", "BIZUDGothic-Bold.ttf", None, "BIZ UDGothic Bold"),
    ("bizudpmincho", "BIZUDPMincho-Regular.ttf", None, "BIZ UDPMincho Regular"),
    ("bizudpmincho", "BIZUDPMincho-Bold.ttf", None, "BIZ UDPMincho Bold"),
    ("bizudmincho", "BIZUDMincho-Regular.ttf", None, "BIZ UDMincho Regular"),
    ("bizudmincho", "BIZUDMincho-Bold.ttf", None, "BIZ UDMincho Bold"),
    ("kaiseidecol", "KaiseiDecol-Regular.ttf", None, "Kaisei Decol Regular"),
    ("kaiseidecol", "KaiseiDecol-Medium.ttf", None, "Kaisei Decol Medium"),
    ("kaiseidecol", "KaiseiDecol-Bold.ttf", None, "Kaisei Decol Bold"),
    ("kaiseitokumin", "KaiseiTokumin-Regular.ttf", None, "Kaisei Tokumin Regular"),
    ("kaiseitokumin", "KaiseiTokumin-Medium.ttf", None, "Kaisei Tokumin Medium"),
    ("kaiseitokumin", "KaiseiTokumin-Bold.ttf", None, "Kaisei Tokumin Bold"),
    ("kaiseitokumin", "KaiseiTokumin-ExtraBold.ttf", None, "Kaisei Tokumin ExtraBold"),
    ("kaiseiharunoumi", "KaiseiHarunoUmi-Regular.ttf", None, "Kaisei HarunoUmi Regular"),
    ("kaiseiharunoumi", "KaiseiHarunoUmi-Medium.ttf", None, "Kaisei HarunoUmi Medium"),
    ("kaiseiharunoumi", "KaiseiHarunoUmi-Bold.ttf", None, "Kaisei HarunoUmi Bold"),
    ("kaiseiopti", "KaiseiOpti-Regular.ttf", None, "Kaisei Opti Regular"),
    ("kaiseiopti", "KaiseiOpti-Medium.ttf", None, "Kaisei Opti Medium"),
    ("kaiseiopti", "KaiseiOpti-Bold.ttf", None, "Kaisei Opti Bold"),
    ("hinamincho", "HinaMincho-Regular.ttf", None, "Hina Mincho"),
    ("dotgothic16", "DotGothic16-Regular.ttf", None, "DotGothic16"),
    ("sawarabigothic", "SawarabiGothic-Regular.ttf", None, "さわらびゴシック"),
    ("sawarabimincho", "SawarabiMincho-Regular.ttf", None, "さわらび明朝"),
    ("yuseimagic", "YuseiMagic-Regular.ttf", None, "Yusei Magic"),
    ("zenkurenaido", "ZenKurenaido-Regular.ttf", None, "Zen Kurenaido"),
    ("zenantique", "ZenAntique-Regular.ttf", None, "Zen Antique"),
    ("zenantiquesoft", "ZenAntiqueSoft-Regular.ttf", None, "Zen Antique Soft"),
    ("stick", "Stick-Regular.ttf", None, "Stick"),

    # ---- v2 expansion (2026-11-05): +133 fonts -> 233 total ----
    # google/fonts, display/decorative/dot/retro (OFL 1.1)
    ("delagothicone", "DelaGothicOne-Regular.ttf", None, "Dela Gothic One"),
    ("rampartone", "RampartOne-Regular.ttf", None, "Rampart One"),
    ("reggaeone", "ReggaeOne-Regular.ttf", None, "Reggae One"),
    ("rocknrollone", "RocknRollOne-Regular.ttf", None, "RocknRoll One"),
    ("pottaone", "PottaOne-Regular.ttf", None, "Potta One"),
    ("mochiypopone", "MochiyPopOne-Regular.ttf", None, "Mochiy Pop One"),
    ("mochiypoppone", "MochiyPopPOne-Regular.ttf", None, "Mochiy Pop P One"),
    ("hachimarupop", "HachiMaruPop-Regular.ttf", None, "Hachi Maru Pop"),
    ("darumadropone", "DarumadropOne-Regular.ttf", None, "Darumadrop One"),
    ("zendots", "ZenDots-Regular.ttf", None, "Zen Dots"),
    ("yujisyuku", "YujiSyuku-Regular.ttf", None, "Yuji Syuku"),
    ("yujimai", "YujiMai-Regular.ttf", None, "Yuji Mai"),
    ("yujiboku", "YujiBoku-Regular.ttf", None, "Yuji Boku"),
    ("newtegomin", "NewTegomin-Regular.ttf", None, "New Tegomin"),
    ("shipporiantique", "ShipporiAntique-Regular.ttf", None, "Shippori Antique"),
    ("shipporiantiqueb1", "ShipporiAntiqueB1-Regular.ttf", None, "Shippori Antique B1"),
    ("yomogi", "Yomogi-Regular.ttf", None, "Yomogi"),
    ("murecho", "Murecho[wght].ttf", [100,200,300,400,500,600,700,800,900], "Murecho"),
    ("mplus1", "MPLUS1[wght].ttf", [100,200,300,400,500,600,700,800,900], "M PLUS 1"),
    ("bizudpgothic", "BIZUDPGothic-Regular.ttf", None, "BIZ UDPGothic Regular"),
    ("bizudpgothic", "BIZUDPGothic-Bold.ttf", None, "BIZ UDPGothic Bold"),
    ("shipporiminchob1", "ShipporiMinchoB1-SemiBold.ttf", None, "Shippori Mincho B1 SemiBold"),
    ("shipporiminchob1", "ShipporiMinchoB1-ExtraBold.ttf", None, "Shippori Mincho B1 ExtraBold"),
    # external: Adobe Source Han (OFL 1.1)
    (None, "SourceHanSansJP-ExtraLight.otf", None, "Source Han Sans JP ExtraLight"),
    (None, "SourceHanSansJP-Light.otf", None, "Source Han Sans JP Light"),
    (None, "SourceHanSansJP-Normal.otf", None, "Source Han Sans JP Normal"),
    (None, "SourceHanSansJP-Regular.otf", None, "Source Han Sans JP Regular"),
    (None, "SourceHanSansJP-Medium.otf", None, "Source Han Sans JP Medium"),
    (None, "SourceHanSansJP-Bold.otf", None, "Source Han Sans JP Bold"),
    (None, "SourceHanSansJP-Heavy.otf", None, "Source Han Sans JP Heavy"),
    (None, "SourceHanSerifJP-ExtraLight.otf", None, "Source Han Serif JP ExtraLight"),
    (None, "SourceHanSerifJP-Light.otf", None, "Source Han Serif JP Light"),
    (None, "SourceHanSerifJP-Regular.otf", None, "Source Han Serif JP Regular"),
    (None, "SourceHanSerifJP-Medium.otf", None, "Source Han Serif JP Medium"),
    (None, "SourceHanSerifJP-SemiBold.otf", None, "Source Han Serif JP SemiBold"),
    (None, "SourceHanSerifJP-Bold.otf", None, "Source Han Serif JP Bold"),
    (None, "SourceHanSerifJP-Heavy.otf", None, "Source Han Serif JP Heavy"),
    # external: Debian fonts packages (open licenses)
    (None, "IPAexGothic.ttf", None, "IPAexゴシック"),
    (None, "IPAexMincho.ttf", None, "IPAex明朝"),
    (None, "TakaoGothic.ttf", None, "Takaoゴシック"),
    (None, "TakaoPGothic.ttf", None, "Takao Pゴシック"),
    (None, "TakaoMincho.ttf", None, "Takao明朝"),
    (None, "TakaoPMincho.ttf", None, "Takao P明朝"),
    (None, "VLGothic-Regular.ttf", None, "VLゴシック"),
    (None, "VLPGothic-Regular.ttf", None, "VL Pゴシック"),
    (None, "MigMix-1P-Regular.ttf", None, "MigMix 1P Regular"),
    (None, "MigMix-1P-Bold.ttf", None, "MigMix 1P Bold"),
    (None, "MigMix-2P-Regular.ttf", None, "MigMix 2P Regular"),
    (None, "MigMix-2P-Bold.ttf", None, "MigMix 2P Bold"),
    (None, "MigMix-1M-Regular.ttf", None, "MigMix 1M Regular"),
    (None, "MigMix-1M-Bold.ttf", None, "MigMix 1M Bold"),
    (None, "MigMix-2M-Regular.ttf", None, "MigMix 2M Regular"),
    (None, "MigMix-2M-Bold.ttf", None, "MigMix 2M Bold"),
    (None, "Migu-1M-Regular.ttf", None, "Migu 1M Regular"),
    (None, "Migu-1M-Bold.ttf", None, "Migu 1M Bold"),
    (None, "Migu-1C-Regular.ttf", None, "Migu 1C Regular"),
    (None, "Migu-1C-Bold.ttf", None, "Migu 1C Bold"),
    (None, "Migu-1P-Regular.ttf", None, "Migu 1P Regular"),
    (None, "Migu-1P-Bold.ttf", None, "Migu 1P Bold"),
    (None, "Migu-2M-Regular.ttf", None, "Migu 2M Regular"),
    (None, "Migu-2M-Bold.ttf", None, "Migu 2M Bold"),
    (None, "UmePlus-Gothic.ttf", None, "UmePlusゴシック"),
    (None, "UmePlus-P-Gothic.ttf", None, "UmePlus Pゴシック"),
    # external: GitHub releases (OFL 1.1)
    (None, "Koruri-Regular.ttf", None, "Koruri Regular"),
    (None, "Koruri-Bold.ttf", None, "Koruri Bold"),
    (None, "Koruri-Semibold.ttf", None, "Koruri Semibold"),
    (None, "HackGen-Regular.ttf", None, "HackGen Regular"),
    (None, "HackGen-Bold.ttf", None, "HackGen Bold"),
    (None, "HackGenConsole-Regular.ttf", None, "HackGen Console Regular"),
    (None, "HackGenConsole-Bold.ttf", None, "HackGen Console Bold"),
    (None, "UDEVGothic-Regular.ttf", None, "UDEV Gothic Regular"),
    (None, "UDEVGothic-Bold.ttf", None, "UDEV Gothic Bold"),
    (None, "UDEVGothic35-Regular.ttf", None, "UDEV Gothic 35 Regular"),
    (None, "UDEVGothic35-Bold.ttf", None, "UDEV Gothic 35 Bold"),
    (None, "MoralerspaceNeon-Regular.ttf", None, "Moralerspace Neon Regular"),
    (None, "MoralerspaceNeon-Bold.ttf", None, "Moralerspace Neon Bold"),
    (None, "MoralerspaceArgon-Regular.ttf", None, "Moralerspace Argon Regular"),
    (None, "MoralerspaceArgon-Bold.ttf", None, "Moralerspace Argon Bold"),
    (None, "PlemolJP-Regular.ttf", None, "PlemolJP Regular"),
    (None, "PlemolJP-Bold.ttf", None, "PlemolJP Bold"),
    (None, "PlemolJPConsole-Regular.ttf", None, "PlemolJP Console Regular"),
    (None, "PlemolJPConsole-Bold.ttf", None, "PlemolJP Console Bold"),
    (None, "Cica-Regular.ttf", None, "Cica Regular"),
    (None, "Cica-Bold.ttf", None, "Cica Bold"),
    (None, "Cica-BoldItalic.ttf", None, "Cica Bold Italic"),
    (None, "Cica-RegularItalic.ttf", None, "Cica Regular Italic"),
    (None, "GenJyuuGothic-ExtraLight.ttf", None, "GenJyuuGothic ExtraLight"),
    (None, "GenJyuuGothic-Light.ttf", None, "GenJyuuGothic Light"),
    (None, "GenJyuuGothic-Normal.ttf", None, "GenJyuuGothic Normal"),
    (None, "GenJyuuGothic-Regular.ttf", None, "GenJyuuGothic Regular"),
    (None, "GenJyuuGothic-Medium.ttf", None, "GenJyuuGothic Medium"),
    (None, "GenJyuuGothic-Bold.ttf", None, "GenJyuuGothic Bold"),
    (None, "GenJyuuGothic-Heavy.ttf", None, "GenJyuuGothic Heavy"),
    (None, "GenShinGothic-ExtraLight.ttf", None, "GenShinGothic ExtraLight"),
    (None, "GenShinGothic-Light.ttf", None, "GenShinGothic Light"),
    (None, "GenShinGothic-Normal.ttf", None, "GenShinGothic Normal"),
    (None, "GenShinGothic-Regular.ttf", None, "GenShinGothic Regular"),
    (None, "GenShinGothic-Medium.ttf", None, "GenShinGothic Medium"),
    (None, "GenShinGothic-Bold.ttf", None, "GenShinGothic Bold"),
    (None, "GenShinGothic-Heavy.ttf", None, "GenShinGothic Heavy"),
    (None, "GenRyuMin2JP-ExtraLight.otf", None, "GenRyuMin JP ExtraLight"),
    (None, "GenRyuMin2JP-Light.otf", None, "GenRyuMin JP Light"),
    (None, "GenRyuMin2JP-Regular.otf", None, "GenRyuMin JP Regular"),
    (None, "GenRyuMin2JP-Medium.otf", None, "GenRyuMin JP Medium"),
    (None, "GenRyuMin2JP-SemiBold.otf", None, "GenRyuMin JP SemiBold"),
    (None, "GenRyuMin2JP-Bold.otf", None, "GenRyuMin JP Bold"),
    (None, "GenRyuMin2JP-Heavy.otf", None, "GenRyuMin JP Heavy"),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    # unique files to download
    files = {}
    for d, fn, weights, name in MANIFEST:
        files[(d, fn)] = True
    total_fonts = sum(len(w) if w else 1 for _, _, w, _ in MANIFEST)
    print(f"manifest fonts: {total_fonts} (files: {len(files)})")
    print(f"manifest fonts: {total_fonts} (files: {len(files)})")

    jobs = []
    for d, fn in files:
        url = BASE + d + "/" + urllib.parse.quote(fn)
        dest = os.path.join(OUT, fn)
        jobs.append((url, dest))

    # download in parallel with curl
    import concurrent.futures
    def dl(job):
        url, dest = job
        if os.path.exists(dest) and os.path.getsize(dest) > 100000:
            return (dest, "exists")
        r = subprocess.run(["curl", "-sL", "--retry", "2", "--connect-timeout", "20",
                            "-o", dest, url], capture_output=True, text=True)
        ok = os.path.exists(dest) and os.path.getsize(dest) > 100000
        if ok:
            with open(dest, "rb") as f:
                magic = f.read(4)
            if magic not in (b"\x00\x01\x00\x00", b"OTTO", b"true"):
                os.remove(dest)
                return (dest, "BAD MAGIC")
            return (dest, "ok")
        return (dest, f"FAIL {r.returncode}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for dest, st in ex.map(dl, jobs):
            print(os.path.basename(dest), st)
    # summary
    bad = [os.path.basename(d) for d, _ in jobs if not (os.path.exists(d) and os.path.getsize(d) > 100000)]
    print("missing/bad:", bad)
    total_mb = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e6
    print(f"total size: {total_mb:.1f} MB, files: {len(os.listdir(OUT))}")

if __name__ == "__main__":
    main()
