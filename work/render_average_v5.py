#!/usr/bin/env python3
"""v5 render: average all 229 fonts over the NEW chars only (8109).

Char set (18414 total):
- v4's 10305 chars first, same order (out/stats_v4.json keys) -- preserved.
- new 8109 chars: proper20 minus v4, sorted by codepoint.
  proper20 = work/v5_proper_sets.json["proper20"]: every Unicode char
  that is a VISIBLE character (category NOT in Cc/Cf/Cs/Co/Cn/Zl/Zp/Zs/
  Mn/Me/Mc) and whose glyph exists in >=20 of the 229 font units.
  Verified: 18414 unique, v4 fully included, 0 bad-category chars.
  This includes all JIS X 0213 non-kanji + all JIS X 0212 (6067 chars,
  2743 already in v4, 3324 new incl. 3058 kanji).
  Excluded by definition (NOT a time limit): chars with <20 fonts
  (Ext B 42720 chars: only 354 have >=20; Ext A 6592: only 202;
  Hangul 11172: 0) -- mostly a single family (5-9 weights) carrying
  them, so averaging them would be a copy of one family, not a
  229-font average. The 10-19 band (1133 chars) is deferred to v6.

v4 glyphs are NOT re-rendered: out/glyphs_v4/*.png were copied to
out/glyphs_v5/ beforehand (indices 0000-10304, same filenames).
This script renders only the 8109 new chars (indices 10305-18413)
into out/glyphs_v5/ and writes out/stats_v5.json merging v4 stats.

Resumability: same as v4 (memmap acc/cnt for NEW chars only,
chunk 512, progress in work/v5_progress.json). ~70 min for 8109 chars.
"""
import json, os, sys, time, gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST

BASE = os.path.expanduser("~/workspace/average-font")
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "out", "glyphs_v5")
SIZE = 256
FONT_SIZE = 200
CHUNK = 512
ACC_PATH = os.path.join(BASE, "work", "v5_acc.dat")
CNT_PATH = os.path.join(BASE, "work", "v5_cnt.dat")
PROG_PATH = os.path.join(BASE, "work", "v5_progress.json")


def load_jis_levels():
    jis = json.load(open(os.path.join(BASE, "work", "jisx0213_kanji.json"),
                         encoding="utf-8"))
    level = {r["ch"]: r["level"] for r in jis}
    jis12 = set(json.load(open(os.path.join(BASE, "work",
                                           "jisx0212_chars.json"),
                              encoding="utf-8")))
    return level, jis12


JIS_LEVEL, JIS12 = load_jis_levels()


def kanji_level(ch):
    if ch in JIS_LEVEL:
        return JIS_LEVEL[ch]
    if ch in JIS12:
        return "JIS X 0212"
    o = ord(ch)
    if 0x3400 <= o <= 0x4DBF:
        return "CJK拡張A"
    if 0x20000 <= o <= 0x2A6DF:
        return "CJK拡張B"
    if 0x2A700 <= o <= 0x2B73F:
        return "CJK拡張C"
    if 0x2B740 <= o <= 0x2B81F:
        return "CJK拡張D"
    if 0x2B820 <= o <= 0x2CEAF:
        return "CJK拡張E"
    if 0x2CEB0 <= o <= 0x2EBEF:
        return "CJK拡張F"
    if 0xF900 <= o <= 0xFAFF or 0x2F800 <= o <= 0x2FA1F:
        return "CJK互換漢字"
    return "CJK統合漢字（JIS外）"


def group(ch):
    o = ord(ch)
    if 0x21 <= o <= 0x7E:
        return "ascii"
    if 0xA1 <= o <= 0xFF:
        return "latin1"
    if 0x100 <= o <= 0x24F:
        return "latin_ext"
    if 0x250 <= o <= 0x2FF:
        return "ipa"
    if 0x370 <= o <= 0x3FF:
        return "greek"
    if 0x1F00 <= o <= 0x1FFF:
        return "greek_ext"
    if 0x400 <= o <= 0x52F:
        return "cyrillic"
    if 0x530 <= o <= 0x58F:
        return "armenian"
    if 0x590 <= o <= 0x5FF:
        return "hebrew"
    if 0x600 <= o <= 0x6FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF:
        return "arabic"
    if 0x1D00 <= o <= 0x1DBF:
        return "ipa"
    if 0x1E00 <= o <= 0x1EFF:
        return "latin_ext_add"
    if 0x2190 <= o <= 0x21FF or 0x27F0 <= o <= 0x27FF or 0x2900 <= o <= 0x297F:
        return "arrows"
    if 0x2200 <= o <= 0x22FF or 0x27C0 <= o <= 0x27EF or 0x2A00 <= o <= 0x2AFF:
        return "math"
    if 0x2460 <= o <= 0x24FF or 0x3200 <= o <= 0x33FF or \
            0x1F100 <= o <= 0x1F2FF:
        return "enclosed"
    if 0x1D400 <= o <= 0x1D7FF:
        return "math"
    if 0x1F300 <= o <= 0x1F5FF or 0x1F900 <= o <= 0x1F9FF:
        return "emoji"
    if 0x2F00 <= o <= 0x2FDF:
        return "kanji"
    if 0x3000 <= o <= 0x303F:
        return "symbols"
    if 0x3040 <= o <= 0x309F:
        return "hiragana"
    if 0x30A0 <= o <= 0x30FF:
        return "katakana"
    if 0x31F0 <= o <= 0x31FF:
        return "kana_ext"
    if 0x3400 <= o <= 0x4DBF or 0x4E00 <= o <= 0x9FFF or \
            0x20000 <= o <= 0x2EBEF or 0xF900 <= o <= 0xFAFF or \
            0x2F800 <= o <= 0x2FA1F:
        return "kanji"
    if 0xFF01 <= o <= 0xFF60 or 0xFFE0 <= o <= 0xFFE6:
        return "fullwidth"
    if 0xFF61 <= o <= 0xFFDC or 0xFFE8 <= o <= 0xFFEE:
        return "halfwidth"
    if o == 0x0E3F:  # Thai baht sign (currency, not a script letter)
        return "symbols"
    if 0x900 <= o <= 0x1CFF or 0x2C00 <= o <= 0x2C5F or \
            0xA000 <= o <= 0xA4CF or 0xA700 <= o <= 0xA71F:
        return "scripts"
    if 0x2000 <= o <= 0x2BFF or 0x2C00 <= o <= 0x2FFF or \
            0xFE10 <= o <= 0xFE6F or 0x1F000 <= o <= 0x1FAFF:
        return "symbols"
    return "symbols"


def load_jinmeiyo():
    txt = open(os.path.join(BASE, "work", "jinmeiyo_kanji.txt"),
               encoding="utf-8").read()
    out = set()
    for line in txt.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        out.update(line.strip())
    return out


def build_chars():
    v4stats = json.load(open(os.path.join(BASE, "out", "stats_v4.json"),
                             encoding="utf-8"))
    v4chars = list(v4stats["chars"].keys())
    assert len(v4chars) == 10305, len(v4chars)
    sets = json.load(open(os.path.join(BASE, "work", "v5_proper_sets.json"),
                          encoding="utf-8"))
    proper = sets["proper20"]
    assert len(proper) == 18414, len(proper)
    assert len(set(proper)) == 18414
    v4set = set(v4chars)
    assert v4set <= set(proper), "v4 not fully inside proper20"
    new = sorted([c for c in proper if c not in v4set],
                 key=lambda c: ord(c))
    assert len(new) == 8109, len(new)
    chars = v4chars + new
    assert len(chars) == 18414, len(chars)
    assert len(set(chars)) == len(chars)
    return v4chars, new, chars


def load_progress(total_chars, n_units):
    if os.path.exists(ACC_PATH) and os.path.exists(CNT_PATH) \
            and os.path.exists(PROG_PATH):
        try:
            prog = json.load(open(PROG_PATH, encoding="utf-8"))
            if prog.get("total_chars") == total_chars \
                    and prog.get("units_total") == n_units:
                print("RESUME: progress found", flush=True)
                return prog
        except Exception as e:
            print("progress unreadable, starting fresh:", e, flush=True)
    for p in (ACC_PATH, CNT_PATH):
        if os.path.exists(p):
            os.remove(p)
    return {"version": 5, "total_chars": total_chars, "units_total": n_units,
            "units_done": {}, "started": time.time()}


def main():
    v4chars, new, chars = build_chars()
    jinmeiyo = load_jinmeiyo()
    print("chars: %d (v4 %d + new %d)" % (len(chars), len(v4chars), len(new)),
          flush=True)
    print("new groups:", {g: sum(1 for c in new if group(c) == g)
                          for g in sorted(set(group(c) for c in new))},
          flush=True)
    os.makedirs(OUT, exist_ok=True)
    idx = {ch: i for i, ch in enumerate(new)}

    units = []
    for d, fn, weights, name in MANIFEST:
        wlist = weights if weights else [None]
        for w in wlist:
            key = "%s|%s" % (name, w)
            label = "%s" % name + (" wght=%s" % w if w else "")
            units.append((key, os.path.join(FONTS, fn), w, label))
    print("units: %d" % len(units), flush=True)

    prog = load_progress(len(new), len(units))
    if os.path.exists(ACC_PATH):
        acc = np.memmap(ACC_PATH, dtype=np.float32, mode="r+",
                        shape=(len(new), SIZE, SIZE))
        cnt = np.memmap(CNT_PATH, dtype=np.int32, mode="r+",
                        shape=(len(new),))
    else:
        acc = np.memmap(ACC_PATH, dtype=np.float32, mode="w+",
                        shape=(len(new), SIZE, SIZE))
        acc[:] = 0
        cnt = np.memmap(CNT_PATH, dtype=np.int32, mode="w+",
                        shape=(len(new),))
        cnt[:] = 0
        acc.flush()
        cnt.flush()
    units_done = prog["units_done"]
    t0 = prog.get("started", time.time())
    missing = {}
    img = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(img)
    for ui, (key, path, w, label) in enumerate(units):
        try:
            ft = TTFont(path, lazy=True)
            cmap = ft.getBestCmap()
            ft.close()
        except Exception as e:
            print("SKIP %s: cmap fail %s" % (label, e), flush=True)
            continue
        present = [ch for ch in new if ord(ch) in cmap]
        n_chunks = (len(present) + CHUNK - 1) // CHUNK
        done = units_done.get(key, {})
        done_n = done.get("done", 0) if isinstance(done, dict) else 0
        if done_n >= n_chunks:
            continue
        try:
            font = ImageFont.truetype(path, FONT_SIZE)
            if w is not None:
                font.set_variation_by_axes([w])
        except Exception as e:
            print("SKIP %s: load fail %s" % (label, e), flush=True)
            continue
        miss = [ch for ch in new if ord(ch) not in cmap]
        if miss:
            missing[label] = miss
        for ci in range(done_n, n_chunks):
            chunk = present[ci * CHUNK:(ci + 1) * CHUNK]
            buf = np.zeros((len(chunk), SIZE, SIZE), dtype=np.float32)
            for j, ch in enumerate(chunk):
                draw.rectangle([0, 0, SIZE, SIZE], fill=0)
                draw.text((SIZE // 2, SIZE // 2), ch, font=font,
                          fill=255, anchor="mm")
                buf[j] = np.asarray(img, dtype=np.float32)
            ix = np.array([idx[ch] for ch in chunk], dtype=np.int64)
            acc[ix] += buf
            cnt[ix] += 1
            acc.flush()
            cnt.flush()
            units_done[key] = {"done": ci + 1, "total": n_chunks}
            prog["units_done"] = units_done
            prog["updated"] = time.time()
            prog["elapsed_sec"] = round(time.time() - t0, 1)
            with open(PROG_PATH, "w", encoding="utf-8") as f:
                json.dump(prog, f, ensure_ascii=False)
            del buf
        del font
        gc.collect()
        n_finished = sum(1 for u in units
                         if isinstance(units_done.get(u[0]), dict)
                         and units_done[u[0]].get("done", 0)
                         >= units_done[u[0]].get("total", 1))
        el = time.time() - t0
        eta = el / max(n_finished, 1) * (len(units) - n_finished)
        print("[%d/%d] %s done (%.0fs elapsed, ETA %.0fm, chars: %d)"
              % (ui + 1, len(units), label, el, eta / 60, len(present)),
              flush=True)

    # --- save new glyph PNGs + merge stats ---
    v4stats = json.load(open(os.path.join(BASE, "out", "stats_v4.json"),
                             encoding="utf-8"))
    stats = {"version": 5, "fonts_rendered": len(units),
             "chars": dict(v4stats["chars"]), "total_chars": len(chars),
             "v4_chars": len(v4chars), "new_chars": len(new),
             "definition": "proper20: visible Unicode chars (category not "
             "in Cc/Cf/Cs/Co/Cn/Zl/Zp/Zs/Mn/Me/Mc) with glyph in >=20 of "
             "229 font units (work/v5_proper_sets.json proper20)"}
    for i, ch in enumerate(new):
        n = int(cnt[i])
        avg = acc[i] / max(n, 1)
        gi = len(v4chars) + i
        g = group(ch)
        fname = "%04d_U+%04X_%s.png" % (gi, ord(ch), g)
        out_img = Image.fromarray((255.0 - avg).astype(np.uint8), mode="L")
        out_img.save(os.path.join(OUT, fname))
        info = {"file": fname, "contributors": n,
                "codepoint": "U+%04X" % ord(ch), "group": g,
                "max_ink": round(float(avg.max()), 1),
                "mean_ink": round(float(avg.mean()), 2),
                "ink_px_ge64": int((avg >= 64).sum()),
                "ink_px_ge128": int((avg >= 128).sum())}
        if g == "kanji":
            info["jis_level"] = kanji_level(ch)
            info["jinmeiyo"] = bool(ch in jinmeiyo)
        stats["chars"][ch] = info
        if i % 500 == 0:
            print("saved %d/%d" % (i, len(new)), flush=True)
    assert len(stats["chars"]) == 18414, len(stats["chars"])
    stats["missing_new"] = missing
    stats["missing_v4"] = v4stats.get("missing")
    stats["total_fonts"] = len(units)
    stats["elapsed_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(BASE, "out", "stats_v5.json"), "w",
              encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    zero = [ch for ch in new if stats["chars"][ch]["contributors"] == 0]
    print("DONE: %d units, %d new chars, %.0fs"
          % (len(units), len(new), time.time() - t0))
    print("zero-contributor new chars:", len(zero), zero[:30])
    for g in sorted(set(group(c) for c in new)):
        cc = [stats["chars"][c]["contributors"] for c in new
              if group(c) == g]
        print("%s: n=%d contrib min %d median %d max %d"
              % (g, len(cc), min(cc), sorted(cc)[len(cc) // 2], max(cc)))
    maxinks = sorted((stats["chars"][c]["max_ink"], c) for c in new)
    print("faintest 15 new by max_ink:", maxinks[:15])


if __name__ == "__main__":
    main()
