#!/usr/bin/env python3
"""Download v2 expansion fonts for the average-font project (target 233 total).

Sources:
- google/fonts (OFL 1.1) via raw.githubusercontent.com
- Adobe Source Han Sans/Serif JP (OFL 1.1) via GitHub releases
- Debian fonts packages (IPAex/Takao/VL/MigMix/Migu/UmePlus, open licenses)
- GitHub releases: Koruri (OFL), HackGen/UDEV/Moralerspace/PlemolJP (OFL),
  Cica (OFL), GenRyuMin JP OTF (OFL)
- OSDN mirror (ftp.iij.ad.jp): GenJyuuGothic / GenShinGothic (OFL)
All downloaded files are verified with fontTools (must have U+3042/U+65E5).
"""
import json, os, shutil, subprocess, sys, tarfile, urllib.parse, zipfile

BASE = os.path.expanduser("~/workspace/average-font")
FONTS = os.path.join(BASE, "fonts")
DL = os.path.join(BASE, "work", "downloads_v2")
os.makedirs(DL, exist_ok=True)
os.makedirs(FONTS, exist_ok=True)

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

# (dir, filename, weights, display name) — google/fonts, new in v2
GOOGLE_NEW = [
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
    ("murecho", "Murecho[wght].ttf", [100, 200, 300, 400, 500, 600, 700, 800, 900], "Murecho"),
    ("mplus1", "MPLUS1[wght].ttf", [100, 200, 300, 400, 500, 600, 700, 800, 900], "M PLUS 1"),
    ("bizudpgothic", "BIZUDPGothic-Regular.ttf", None, "BIZ UDPGothic Regular"),
    ("bizudpgothic", "BIZUDPGothic-Bold.ttf", None, "BIZ UDPGothic Bold"),
    ("shipporiminchob1", "ShipporiMinchoB1-SemiBold.ttf", None, "Shippori Mincho B1 SemiBold"),
    ("shipporiminchob1", "ShipporiMinchoB1-ExtraBold.ttf", None, "Shippori Mincho B1 ExtraBold"),
]

# apt-installed files: (source path, dest filename, display name)
APT = [
    ("/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf", "IPAexGothic.ttf", "IPAexゴシック"),
    ("/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf", "IPAexMincho.ttf", "IPAex明朝"),
    ("/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf", "TakaoGothic.ttf", "Takaoゴシック"),
    ("/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf", "TakaoPGothic.ttf", "Takao Pゴシック"),
    ("/usr/share/fonts/truetype/takao-mincho/TakaoMincho.ttf", "TakaoMincho.ttf", "Takao明朝"),
    ("/usr/share/fonts/truetype/takao-mincho/TakaoPMincho.ttf", "TakaoPMincho.ttf", "Takao P明朝"),
    ("/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf", "VLGothic-Regular.ttf", "VLゴシック"),
    ("/usr/share/fonts/truetype/vlgothic/VL-PGothic-Regular.ttf", "VLPGothic-Regular.ttf", "VL Pゴシック"),
    ("/usr/share/fonts/truetype/migmix/migmix-1p-regular.ttf", "MigMix-1P-Regular.ttf", "MigMix 1P Regular"),
    ("/usr/share/fonts/truetype/migmix/migmix-1p-bold.ttf", "MigMix-1P-Bold.ttf", "MigMix 1P Bold"),
    ("/usr/share/fonts/truetype/migmix/migmix-2p-regular.ttf", "MigMix-2P-Regular.ttf", "MigMix 2P Regular"),
    ("/usr/share/fonts/truetype/migmix/migmix-2p-bold.ttf", "MigMix-2P-Bold.ttf", "MigMix 2P Bold"),
    ("/usr/share/fonts/truetype/migmix/migmix-1m-regular.ttf", "MigMix-1M-Regular.ttf", "MigMix 1M Regular"),
    ("/usr/share/fonts/truetype/migmix/migmix-1m-bold.ttf", "MigMix-1M-Bold.ttf", "MigMix 1M Bold"),
    ("/usr/share/fonts/truetype/migmix/migmix-2m-regular.ttf", "MigMix-2M-Regular.ttf", "MigMix 2M Regular"),
    ("/usr/share/fonts/truetype/migmix/migmix-2m-bold.ttf", "MigMix-2M-Bold.ttf", "MigMix 2M Bold"),
    ("/usr/share/fonts/truetype/migmix/migu-1m-regular.ttf", "Migu-1M-Regular.ttf", "Migu 1M Regular"),
    ("/usr/share/fonts/truetype/migmix/migu-1m-bold.ttf", "Migu-1M-Bold.ttf", "Migu 1M Bold"),
    ("/usr/share/fonts/truetype/migmix/migu-1c-regular.ttf", "Migu-1C-Regular.ttf", "Migu 1C Regular"),
    ("/usr/share/fonts/truetype/migmix/migu-1c-bold.ttf", "Migu-1C-Bold.ttf", "Migu 1C Bold"),
    ("/usr/share/fonts/truetype/migmix/migu-1p-regular.ttf", "Migu-1P-Regular.ttf", "Migu 1P Regular"),
    ("/usr/share/fonts/truetype/migmix/migu-1p-bold.ttf", "Migu-1P-Bold.ttf", "Migu 1P Bold"),
    ("/usr/share/fonts/truetype/migmix/migu-2m-regular.ttf", "Migu-2M-Regular.ttf", "Migu 2M Regular"),
    ("/usr/share/fonts/truetype/migmix/migu-2m-bold.ttf", "Migu-2M-Bold.ttf", "Migu 2M Bold"),
    ("/usr/share/fonts/truetype/umeplus/umeplus-gothic.ttf", "UmePlus-Gothic.ttf", "UmePlusゴシック"),
    ("/usr/share/fonts/truetype/umeplus/umeplus-p-gothic.ttf", "UmePlus-P-Gothic.ttf", "UmePlus Pゴシック"),
]

# release zips: (url, archive name, {member suffix -> dest filename}, display prefix)
ZIPS = [
    ("https://github.com/adobe-fonts/source-han-sans/releases/download/2.005R/17_SourceHanSansJP.zip",
     "SourceHanSansJP.zip",
     {"SourceHanSansJP-ExtraLight.otf": "SourceHanSansJP-ExtraLight.otf",
      "SourceHanSansJP-Light.otf": "SourceHanSansJP-Light.otf",
      "SourceHanSansJP-Normal.otf": "SourceHanSansJP-Normal.otf",
      "SourceHanSansJP-Regular.otf": "SourceHanSansJP-Regular.otf",
      "SourceHanSansJP-Medium.otf": "SourceHanSansJP-Medium.otf",
      "SourceHanSansJP-Bold.otf": "SourceHanSansJP-Bold.otf",
      "SourceHanSansJP-Heavy.otf": "SourceHanSansJP-Heavy.otf"}, "Source Han Sans JP"),
    ("https://github.com/adobe-fonts/source-han-serif/releases/download/2.003R/12_SourceHanSerifJP.zip",
     "SourceHanSerifJP.zip",
     {"SourceHanSerifJP-ExtraLight.otf": "SourceHanSerifJP-ExtraLight.otf",
      "SourceHanSerifJP-Light.otf": "SourceHanSerifJP-Light.otf",
      "SourceHanSerifJP-Regular.otf": "SourceHanSerifJP-Regular.otf",
      "SourceHanSerifJP-Medium.otf": "SourceHanSerifJP-Medium.otf",
      "SourceHanSerifJP-SemiBold.otf": "SourceHanSerifJP-SemiBold.otf",
      "SourceHanSerifJP-Bold.otf": "SourceHanSerifJP-Bold.otf",
      "SourceHanSerifJP-Heavy.otf": "SourceHanSerifJP-Heavy.otf"}, "Source Han Serif JP"),
    ("https://github.com/Koruri/Koruri/releases/download/20210720/Koruri-20210720.tar.xz",
     "Koruri-20210720.tar.xz",
     {"Koruri-Regular.ttf": "Koruri-Regular.ttf",
      "Koruri-Bold.ttf": "Koruri-Bold.ttf",
      "Koruri-Semibold.ttf": "Koruri-Semibold.ttf"}, "Koruri"),
    ("https://github.com/yuru7/HackGen/releases/download/v2.10.0/HackGen_v2.10.0.zip",
     "HackGen_v2.10.0.zip",
     {"HackGen-Regular.ttf": "HackGen-Regular.ttf",
      "HackGen-Bold.ttf": "HackGen-Bold.ttf",
      "HackGenConsole-Regular.ttf": "HackGenConsole-Regular.ttf",
      "HackGenConsole-Bold.ttf": "HackGenConsole-Bold.ttf"}, "HackGen"),
    ("https://github.com/yuru7/udev-gothic/releases/download/v2.2.0/UDEVGothic_v2.2.0.zip",
     "UDEVGothic_v2.2.0.zip",
     {"UDEVGothic-Regular.ttf": "UDEVGothic-Regular.ttf",
      "UDEVGothic-Bold.ttf": "UDEVGothic-Bold.ttf",
      "UDEVGothic35-Regular.ttf": "UDEVGothic35-Regular.ttf",
      "UDEVGothic35-Bold.ttf": "UDEVGothic35-Bold.ttf"}, "UDEV Gothic"),
    ("https://github.com/yuru7/moralerspace/releases/download/v2.0.0/Moralerspace_v2.0.0.zip",
     "Moralerspace_v2.0.0.zip",
     {"MoralerspaceGothic-Regular.ttf": "MoralerspaceGothic-Regular.ttf",
      "MoralerspaceGothic-Bold.ttf": "MoralerspaceGothic-Bold.ttf",
      "MoralerspaceGothicHW-Regular.ttf": "MoralerspaceGothicHW-Regular.ttf",
      "MoralerspaceGothicHW-Bold.ttf": "MoralerspaceGothicHW-Bold.ttf"}, "Moralerspace"),
    ("https://github.com/yuru7/PlemolJP/releases/download/v3.1.0/PlemolJP_v3.1.0.zip",
     "PlemolJP_v3.1.0.zip",
     {"PlemolJP-Regular.ttf": "PlemolJP-Regular.ttf",
      "PlemolJP-Bold.ttf": "PlemolJP-Bold.ttf",
      "PlemolJPConsole-Regular.ttf": "PlemolJPConsole-Regular.ttf",
      "PlemolJPConsole-Bold.ttf": "PlemolJPConsole-Bold.ttf"}, "PlemolJP"),
    ("https://github.com/miiton/Cica/releases/download/v5.0.3/Cica_v5.0.3.zip",
     "Cica_v5.0.3.zip",
     {"Cica-Regular.ttf": "Cica-Regular.ttf",
      "Cica-Bold.ttf": "Cica-Bold.ttf",
      "Cica-Italic.ttf": "Cica-Italic.ttf",
      "Cica-BoldItalic.ttf": "Cica-BoldItalic.ttf"}, "Cica"),
    ("https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8642/genjyuugothic-20150607.zip",
     "genjyuugothic-20150607.zip",
     {"GenJyuuGothic-ExtraLight.ttf": "GenJyuuGothic-ExtraLight.ttf",
      "GenJyuuGothic-Light.ttf": "GenJyuuGothic-Light.ttf",
      "GenJyuuGothic-Normal.ttf": "GenJyuuGothic-Normal.ttf",
      "GenJyuuGothic-Regular.ttf": "GenJyuuGothic-Regular.ttf",
      "GenJyuuGothic-Medium.ttf": "GenJyuuGothic-Medium.ttf",
      "GenJyuuGothic-Bold.ttf": "GenJyuuGothic-Bold.ttf",
      "GenJyuuGothic-Heavy.ttf": "GenJyuuGothic-Heavy.ttf"}, "GenJyuuGothic"),
    ("https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8637/genshingothic-20150607.zip",
     "genshingothic-20150607.zip",
     {"GenShinGothic-ExtraLight.ttf": "GenShinGothic-ExtraLight.ttf",
      "GenShinGothic-Light.ttf": "GenShinGothic-Light.ttf",
      "GenShinGothic-Normal.ttf": "GenShinGothic-Normal.ttf",
      "GenShinGothic-Regular.ttf": "GenShinGothic-Regular.ttf",
      "GenShinGothic-Medium.ttf": "GenShinGothic-Medium.ttf",
      "GenShinGothic-Bold.ttf": "GenShinGothic-Bold.ttf",
      "GenShinGothic-Heavy.ttf": "GenShinGothic-Heavy.ttf"}, "GenShinGothic"),
    ("https://github.com/ButTaiwan/genryu-font/releases/download/v2.100/GenRyuMin2JP-otf.zip",
     "GenRyuMin2JP-otf.zip",
     {"GenRyuMin2JP-EL.otf": "GenRyuMin2JP-ExtraLight.otf",
      "GenRyuMin2JP-L.otf": "GenRyuMin2JP-Light.otf",
      "GenRyuMin2JP-R.otf": "GenRyuMin2JP-Regular.otf",
      "GenRyuMin2JP-M.otf": "GenRyuMin2JP-Medium.otf",
      "GenRyuMin2JP-SB.otf": "GenRyuMin2JP-SemiBold.otf",
      "GenRyuMin2JP-B.otf": "GenRyuMin2JP-Bold.otf",
      "GenRyuMin2JP-H.otf": "GenRyuMin2JP-Heavy.otf"}, "GenRyuMin JP"),
]


def dl(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "exists"
    r = subprocess.run(["curl", "-sL", "--retry", "2", "--connect-timeout", "30",
                        "-o", dest, url])
    if r.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        return f"FAIL rc={r.returncode}"
    return "ok"


def extract_members(archive, wanted, log):
    """wanted: {member basename -> dest filename}. Returns list of dest filenames extracted."""
    got = []
    if archive.endswith(".zip"):
        z = zipfile.ZipFile(archive)
        names = z.namelist()
        for base, dest in wanted.items():
            match = [n for n in names if n.endswith("/" + base) or n == base]
            if not match:
                log.append(f"MISSING in {os.path.basename(archive)}: {base}")
                continue
            with z.open(match[0]) as src, open(os.path.join(FONTS, dest), "wb") as out:
                shutil.copyfileobj(src, out)
            got.append(dest)
    else:  # tar.xz
        t = tarfile.open(archive)
        names = t.getnames()
        for base, dest in wanted.items():
            match = [n for n in names if n.endswith("/" + base) or n == base]
            if not match:
                log.append(f"MISSING in {os.path.basename(archive)}: {base}")
                continue
            src = t.extractfile(match[0])
            with open(os.path.join(FONTS, dest), "wb") as out:
                shutil.copyfileobj(src, out)
            got.append(dest)
    return got


def main():
    log = []
    new_entries = []  # (filename, weights, display name, source, license)
    # --- google/fonts ---
    import concurrent.futures
    jobs = []
    for d, fn, weights, name in GOOGLE_NEW:
        url = GF + d + "/" + urllib.parse.quote(fn)
        dest = os.path.join(FONTS, fn)
        jobs.append((url, dest, fn, weights, name))

    def do(job):
        url, dest, fn, weights, name = job
        return (fn, dl(url, dest), weights, name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for fn, st, weights, name in ex.map(do, jobs):
            print(f"google {fn}: {st}", flush=True)
            if st in ("ok", "exists"):
                new_entries.append((fn, weights, name, "google/fonts (OFL 1.1)", "OFL 1.1"))
            else:
                log.append(f"google FAIL: {fn}")

    # --- apt copies ---
    for src, dest, name in APT:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(FONTS, dest))
            new_entries.append((dest, None, name, "Debian fonts-* package", "open (IPA/M+/Ume)"))
            print(f"apt {dest}: ok", flush=True)
        else:
            log.append(f"apt MISSING source: {src}")

    # --- release zips ---
    for url, arc, wanted, prefix in ZIPS:
        path = os.path.join(DL, arc)
        st = dl(url, path)
        print(f"zip {arc}: {st} ({os.path.getsize(path)//1024//1024 if os.path.exists(path) else 0}MB)", flush=True)
        if st.startswith("FAIL"):
            log.append(f"zip FAIL: {arc}")
            continue
        try:
            got = extract_members(path, wanted, log)
        except Exception as e:
            log.append(f"zip extract FAIL {arc}: {e}")
            continue
        for dest in got:
            key = [k for k, v in wanted.items() if v == dest][0]
            nice = key.rsplit(".", 1)[0]
            new_entries.append((dest, None, nice, "release zip", "OFL 1.1"))
        print(f"  extracted {len(got)}/{len(wanted)} from {arc}", flush=True)

    # fix display names for zip entries (use wanted key without ext + prefix handled below)
    # verify all new files with fontTools
    from fontTools.ttLib import TTFont
    verified, failed = [], []
    for fn, weights, name, src, lic in new_entries:
        path = os.path.join(FONTS, fn)
        try:
            ft = TTFont(path, lazy=True)
            cmap = ft.getBestCmap()
            ft.close()
            if 0x3042 in cmap and 0x65E5 in cmap:
                verified.append((fn, weights, name, src, lic))
            else:
                failed.append((fn, "no kana/kanji cmap"))
        except Exception as e:
            failed.append((fn, str(e)[:100]))
    print(f"verified: {len(verified)}, failed: {len(failed)}", flush=True)
    for f in failed:
        print("  FAILED:", f, flush=True)
        log.append(f"verify FAIL: {f}")
    out = {"entries": [{"file": fn, "weights": w, "name": n, "source": s, "license": l}
                         for fn, w, n, s, l in verified],
           "failed": [list(f) for f in failed], "log": log}
    json.dump(out, open(os.path.join(BASE, "work", "v2_entries.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("DONE v2 download:", len(verified), "fonts verified")


if __name__ == "__main__":
    main()
