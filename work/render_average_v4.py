#!/usr/bin/env python3
"""v4 render: average all 229 fonts over the v3 2290 chars + new kana/
punct + all JIS X 0213 kanji (10050).

Char set (10305 total):
- v3's 2290 chars first, same order (joyo kanji 2136 + kana 92 + digits 10
  + latin 52) -- v3 is fully preserved.
- new kana 73: dakuten hiragana/katakana 40, handakuten 10, small kana 18,
  long vowel U+30FC 1, repetition marks U+309D/U+309E/U+30FD/U+30FE 4.
- punct/symbols 28: 、。・「」『』（）〔〕【】！？…―〜：；－／＼＝＋×÷％
- new kanji 7914: JIS X 0213 kanji (10050) minus joyo 2136 already in v3,
  ordered by level (L1, L2, L3, L4) then men-ku-ten order.
  Source: work/jisx0213_kanji.json (parsed from Wikipedia
  JIS X 0213 kanji lists, JIS X 0213:2004).
  Verified: L1 2965 / L2 3390 / L3 1259 / L4 2436, no duplicates.
  Jinmeiyo kanji (846字種, work/jinmeiyo_kanji.txt) are all inside this set.

Resumability (v4 is ~100 min for 10305 chars): rendering proceeds in
units (one font file x one weight) split into chunks of 512 chars.
Each chunk is rendered into a RAM buffer first, then added to the
memmap accumulator in one go and flushed; progress (completed chunks
per unit) is written to work/v4_progress.json after every chunk.
Killing the process mid-chunk loses at most that chunk; restarting
resumes from the last completed chunk. The memmap (work/v4_acc.dat,
~2.7 GB) and count file (work/v4_cnt.dat) persist across runs.

Outputs: out/glyphs_v4/*.png and out/stats_v4.json (per-glyph
contributors / max_ink / mean_ink / JIS level / jinmeiyo flag).
"""
import json, os, sys, time, gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_fonts import MANIFEST

BASE = os.path.expanduser("~/workspace/average-font")
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "out", "glyphs_v4")
SIZE = 256
FONT_SIZE = 200
CHUNK = 512
ACC_PATH = os.path.join(BASE, "work", "v4_acc.dat")
CNT_PATH = os.path.join(BASE, "work", "v4_cnt.dat")
PROG_PATH = os.path.join(BASE, "work", "v4_progress.json")

NEW_KANA = (
    "がぎぐげござじずぜぞだぢづでどばびぶべぼ"
    "ガギグゲゴザジズゼゾダヂヅデドバビブベボ"
    "ぱぴぷぺぽパピプペポ"
    "ぁぃぅぇぉっゃゅょァィゥェォッャュョ"
    "ー"
    "ゝゞヽヾ"
)
PUNCT = "、。・「」『』（）〔〕【】！？…―〜：；－／＼＝＋×÷％"
PUNCT_SET = set(PUNCT)


def group(ch):
    if ch in PUNCT_SET:
        return "punct"
    o = ord(ch)
    if 0x3040 <= o <= 0x309F:
        return "hiragana"
    if 0x30A0 <= o <= 0x30FF:
        return "katakana"
    if ch.isdigit():
        return "digits"
    if ch.isupper():
        return "latin_upper"
    if ch.islower():
        return "latin_lower"
    return "kanji"


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
    v3stats = json.load(open(os.path.join(BASE, "out", "stats_v3.json"),
                             encoding="utf-8"))
    v3chars = list(v3stats["chars"].keys())
    assert len(v3chars) == 2290, len(v3chars)
    jis = json.load(open(os.path.join(BASE, "work", "jisx0213_kanji.json"),
                         encoding="utf-8"))
    assert len(jis) == 10050, len(jis)
    level = {r["ch"]: r["level"] for r in jis}
    v3set = set(v3chars)
    assert len(NEW_KANA) == 73, len(NEW_KANA)
    assert len(set(NEW_KANA)) == 73
    assert len(PUNCT) == 28, len(PUNCT)
    assert len(set(PUNCT)) == 28
    assert not (set(NEW_KANA) & v3set), "new kana overlaps v3"
    assert not (PUNCT_SET & v3set), "punct overlaps v3"
    assert not (set(NEW_KANA) & PUNCT_SET)
    new_kanji = []
    for lv in ["第1水準", "第2水準", "第3水準", "第4水準"]:
        for r in jis:
            if r["level"] == lv and r["ch"] not in v3set:
                new_kanji.append(r["ch"])
    assert len(new_kanji) == 10050 - 2136 == 7914, len(new_kanji)
    chars = v3chars + list(NEW_KANA) + list(PUNCT) + new_kanji
    assert len(chars) == 10305, len(chars)
    assert len(set(chars)) == len(chars)
    return chars, level


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
    return {"version": 4, "total_chars": total_chars, "units_total": n_units,
            "units_done": {}, "started": time.time()}


def main():
    chars, level = build_chars()
    jinmeiyo = load_jinmeiyo()
    print("chars: %d (v3 2290 + kana %d + punct %d + new kanji 7914)"
          % (len(chars), len(NEW_KANA), len(PUNCT)), flush=True)
    print("jinmeiyo flag set: %d chars" % len(jinmeiyo), flush=True)
    os.makedirs(OUT, exist_ok=True)
    idx = {ch: i for i, ch in enumerate(chars)}

    units = []
    for d, fn, weights, name in MANIFEST:
        wlist = weights if weights else [None]
        for w in wlist:
            key = "%s|%s" % (name, w)
            label = "%s" % name + (" wght=%s" % w if w else "")
            units.append((key, os.path.join(FONTS, fn), w, label))
    print("units: %d" % len(units), flush=True)

    prog = load_progress(len(chars), len(units))
    if os.path.exists(ACC_PATH):
        acc = np.memmap(ACC_PATH, dtype=np.float32, mode="r+",
                        shape=(len(chars), SIZE, SIZE))
        cnt = np.memmap(CNT_PATH, dtype=np.int32, mode="r+",
                        shape=(len(chars),))
    else:
        acc = np.memmap(ACC_PATH, dtype=np.float32, mode="w+",
                        shape=(len(chars), SIZE, SIZE))
        acc[:] = 0
        cnt = np.memmap(CNT_PATH, dtype=np.int32, mode="w+",
                        shape=(len(chars),))
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
        present = [ch for ch in chars if ord(ch) in cmap]
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
        miss = [ch for ch in chars if ord(ch) not in cmap]
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

    n_fonts = len(units)
    stats = {"version": 4, "fonts_rendered": n_fonts, "chars": {},
             "total_chars": len(chars)}
    for i, ch in enumerate(chars):
        n = int(cnt[i])
        avg = acc[i] / max(n, 1)
        out_img = Image.fromarray((255.0 - avg).astype(np.uint8), mode="L")
        fname = "%04d_U+%04X_%s.png" % (i, ord(ch), group(ch))
        out_img.save(os.path.join(OUT, fname))
        info = {"file": fname, "contributors": n,
                "codepoint": "U+%04X" % ord(ch), "group": group(ch),
                "max_ink": round(float(avg.max()), 1),
                "mean_ink": round(float(avg.mean()), 2),
                "ink_px_ge64": int((avg >= 64).sum()),
                "ink_px_ge128": int((avg >= 128).sum())}
        if group(ch) == "kanji":
            info["jis_level"] = level.get(ch)
            info["jinmeiyo"] = bool(ch in jinmeiyo)
        stats["chars"][ch] = info
        if i % 500 == 0:
            print("saved %d/%d" % (i, len(chars)), flush=True)
    stats["missing"] = missing
    stats["total_fonts"] = n_fonts
    stats["elapsed_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(BASE, "out", "stats_v4.json"), "w",
              encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    zero = [ch for ch, c in stats["chars"].items()
            if c["contributors"] == 0]
    print("DONE: %d units, %d chars, %.0fs"
          % (n_fonts, len(chars), time.time() - t0))
    print("zero-contributor chars:", len(zero), zero[:30])
    for g in ["hiragana", "katakana", "punct", "kanji"]:
        cc = [c["contributors"] for c in stats["chars"].values()
              if c["group"] == g]
        if cc:
            print("%s: n=%d contrib min %d median %d max %d"
                  % (g, len(cc), min(cc), sorted(cc)[len(cc) // 2], max(cc)))
    for lv in ["第1水準", "第2水準", "第3水準", "第4水準"]:
        cc = [c["contributors"] for c in stats["chars"].values()
              if c.get("jis_level") == lv]
        if cc:
            print("%s: n=%d contrib min %d median %d max %d"
                  % (lv, len(cc), min(cc), sorted(cc)[len(cc) // 2], max(cc)))
    maxinks = sorted((c["max_ink"], ch) for ch, c in stats["chars"].items())
    print("faintest 15 by max_ink:", maxinks[:15])


if __name__ == "__main__":
    main()
