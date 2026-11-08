#!/usr/bin/env python3
"""Build the v5 TTF from the averaged glyph bitmaps (out/glyphs_v5/).

Same method as v4 (build_ttf_v4.py): per-glyph ADAPTIVE binarization
threshold = clamp(0.40 * max_ink, 8, 128), OpenCV contour tracing
(RETR_CCOMP + approxPolyDP), fontTools TTF with straight-line polygons.
Template: DotGothic16 (tables only; outlines are all from averages).

v5 differences vs v4:
- 18414 chars (v4 10305 + new 8109, proper20 definition).
  Chars with 0 contributing fonts are DROPPED (recorded in stats as
  dropped_zero_contributors) instead of shipping empty glyphs.
- If the adaptive threshold yields no contour at all, retry at half
  threshold (floor 2); if still empty, drop the char (recorded as
  dropped_empty_after_trace). This guarantees 0 empty glyphs in the TTF.
- Non-BMP chars (371 new + 303 v4 = 674) need a format-12 cmap:
  the TTF carries BOTH a format-4 subtable (BMP chars) and a
  format-12 subtable (all chars).
- Baseline shift is computed per char (shift_for): -60 for kana/kanji/
  symbols/arrows/math/emoji/enclosed/scripts, -150 for digits/capitals/
  ascii/fullwidth/halfwidth, -250 for lowercase letters, and for
  latin1/latin_ext/greek/cyrillic/ipa groups -250 if lowercase else -150.
- Output filename carries the ACTUAL char count in the TTF
  (AverageFont-Regular-v5-229fonts-<N>chars.ttf), since drops can
  reduce it below 18414.
"""
import json, os
import numpy as np
import cv2
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
GLYPHS = os.path.join(OUT, "glyphs_v5")
TEMPLATE = os.path.join(BASE, "fonts", "DotGothic16-Regular.ttf")

SHIFT_MINUS60 = {"hiragana", "katakana", "kanji", "punct", "symbols",
                 "kana_ext", "arrows", "math", "emoji", "enclosed",
                 "scripts", "armenian", "hebrew", "arabic"}
SHIFT_MINUS150 = {"digits", "latin_upper", "ascii", "fullwidth",
                  "halfwidth"}
SHIFT_CASE = {"latin1", "latin_ext", "latin_ext_add", "greek",
              "greek_ext", "cyrillic", "ipa"}


def shift_for(ch, group):
    if group in SHIFT_MINUS60:
        return -60
    if group in SHIFT_MINUS150:
        return -150
    if group == "latin_lower":
        return -250
    if group in SHIFT_CASE:
        return -250 if ch.islower() else -150
    return -60


def adaptive_threshold(max_ink):
    return float(min(128.0, max(8.0, 0.40 * max_ink)))


def trace_glyph(png_path, upem, shift, threshold, eps=1.5):
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    ink = (255 - img.astype(np.int16))
    mask = (ink >= threshold).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return [], 0
    h = hierarchy[0]
    scale = upem / 256.0
    out = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 4:
            continue
        approx = cv2.approxPolyDP(c, eps, True).reshape(-1, 2)
        if len(approx) < 3:
            continue
        pts = []
        for (x, y) in approx:
            fx = int(round(x * scale))
            fy = int(round((255 - y) * scale)) + shift
            pts.append((fx, fy))
        pts = [p for j, p in enumerate(pts) if j == 0 or p != pts[j - 1]]
        if len(pts) >= 3:
            out.append((int(h[i][3]), pts))
    out.sort(key=lambda t: 0 if t[0] == -1 else 1)
    n_ink = int((ink >= threshold).sum())
    return [pts for _, pts in out], n_ink


def main():
    stats_path = os.path.join(OUT, "stats_v5.json")
    stats = json.load(open(stats_path, encoding="utf-8"))
    assert stats["total_chars"] == 18414, stats["total_chars"]
    assert len(stats["chars"]) == 18414, len(stats["chars"])
    font = TTFont(TEMPLATE)
    upem = font["head"].unitsPerEm
    print("template upem:", upem)
    _glyf, _hmtx = font["glyf"], font["hmtx"]
    _name, _os2 = font["name"], font["OS/2"]
    _hhea, _head, _maxp = font["hhea"], font["head"], font["maxp"]

    dropped_zero = [ch for ch, c in stats["chars"].items()
                    if c["contributors"] == 0]
    dropped_empty = []
    kept = [ch for ch, c in stats["chars"].items()
            if c["contributors"] > 0]
    print("zero-contributor chars (dropped):", len(dropped_zero),
          dropped_zero[:40])

    glyph_order = [".notdef", "space"]
    for ch in kept:
        glyph_order.append("uni%04X" % ord(ch))
    font.setGlyphOrder(glyph_order)

    for tag in ["GPOS", "GSUB", "GDEF", "BASE", "JSTF", "kern", "cvt ",
                "prep", "fpgm", "MATH", "COLR", "CBDT", "CBLC", "EBDT",
                "EBLC", "sbix", "VDMX", "LTSH", "hdmx", "DSIG", "STAT"]:
        if tag in font:
            del font[tag]

    glyf = font["glyf"]
    for gname in list(glyf.glyphs.keys()):
        if gname != ".notdef":
            del glyf.glyphs[gname]
    hmtx = font["hmtx"]
    for gname in list(hmtx.metrics.keys()):
        if gname != ".notdef":
            del hmtx.metrics[gname]

    cmap_map = {}
    n_empty = 0
    for ch in kept:
        info = stats["chars"][ch]
        gname = "uni%04X" % ord(ch)
        png = os.path.join(GLYPHS, info["file"])
        thr = adaptive_threshold(info["max_ink"])
        shift = shift_for(ch, info["group"])
        contours, n_ink = trace_glyph(png, upem, shift, thr)
        if not contours and thr > 2:
            thr2 = max(2.0, thr / 2)
            contours, n_ink = trace_glyph(png, upem, shift, thr2)
            if contours:
                thr = thr2
        img = cv2.imread(png, cv2.IMREAD_GRAYSCALE)
        ink = (255 - img.astype(np.int16))
        info["threshold_v5"] = round(thr, 1)
        info["ink_px_adaptive_v5"] = n_ink
        info["ink_px_fixed128_v5"] = int((ink >= 128).sum())
        info["ink_retention_fixed128_v5"] = round(
            info["ink_px_fixed128_v5"] / max(info["ink_px_ge64"], 1), 3)
        info["faint"] = bool(info["max_ink"] < 210)
        if not contours:
            dropped_empty.append(ch)
            n_empty += 1
            continue
        pen = TTGlyphPen(None)
        xs = []
        for pts in contours:
            pen.moveTo(pts[0])
            for p in pts[1:]:
                pen.lineTo(p)
            pen.closePath()
            xs.extend(p[0] for p in pts)
        glyph = pen.glyph()
        glyf.glyphs[gname] = glyph
        if xs:
            adv = min(1000, max(500, max(xs) - min(xs) + 200))
            lsb = min(xs)
        else:
            adv, lsb = 1000, 0
            n_empty += 1
        hmtx.metrics[gname] = (adv, lsb)
        cmap_map[ord(ch)] = gname

    for ch in dropped_empty:
        glyph_order.remove("uni%04X" % ord(ch))
    font.setGlyphOrder(glyph_order)

    glyf.glyphs["space"] = TTGlyphPen(None).glyph()
    hmtx.metrics["space"] = (500, 0)
    cmap_map[0x20] = "space"

    cmap = newTable("cmap")
    cmap.tableVersion = 0
    sub4 = CmapSubtable.newSubtable(4)
    sub4.platformID = 3
    sub4.platEncID = 1
    sub4.language = 0
    sub4.cmap = {cp: g for cp, g in cmap_map.items() if cp <= 0xFFFF}
    sub12 = CmapSubtable.newSubtable(12)
    sub12.platformID = 3
    sub12.platEncID = 10
    sub12.language = 0
    sub12.cmap = dict(cmap_map)
    cmap.tables = [sub4, sub12]
    font["cmap"] = cmap

    n_chars = len(glyph_order) - 2
    out_ttf = os.path.join(
        BASE, "AverageFont-Regular-v5-229fonts-%dchars.ttf" % n_chars)
    name = font["name"]
    for nid, val in [(1, "Average Font"), (2, "Regular"),
                     (4, "Average Font Regular"), (6, "AverageFont-Regular"),
                     (16, "Average Font"), (17, "Regular")]:
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)
    name.setName("Version 5.0; %d chars (proper20: visible chars in >=20 "
                 "of 229 fonts)" % n_chars, 5, 3, 1, 0x409)
    font["hhea"].ascent = 880
    font["hhea"].descent = -120
    font["hhea"].lineGap = 120
    font["hhea"].numberOfHMetrics = len(glyph_order)
    os2 = font["OS/2"]
    os2.sTypoAscender = 880
    os2.sTypoDescender = -120
    os2.sTypoLineGap = 120
    os2.usWinAscent = 900
    os2.usWinDescent = 300
    os2.fsSelection &= ~0x0080
    head = font["head"]
    head.xMin, head.yMin, head.xMax, head.yMax = 0, -120, 1000, 900
    font["maxp"].numGlyphs = len(glyph_order)
    for gname in glyph_order:
        g = font["glyf"][gname]
        if len(getattr(g, "coordinates", [])) > 0:
            g.recalcBounds(font["glyf"])
    xs_min, ys_min, xs_max, ys_max = [], [], [], []
    for gname in glyph_order:
        g = font["glyf"][gname]
        if hasattr(g, "xMin"):
            xs_min.append(g.xMin)
            ys_min.append(g.yMin)
            xs_max.append(g.xMax)
            ys_max.append(g.yMax)
    if xs_min:
        font["head"].xMin, font["head"].yMin = min(xs_min), min(ys_min)
        font["head"].xMax, font["head"].yMax = max(xs_max), max(ys_max)
    font["maxp"].recalc(font)

    font.save(out_ttf)
    print("saved", out_ttf, os.path.getsize(out_ttf), "bytes, glyphs:",
          len(glyph_order))
    print("empty glyphs (no contours):", n_empty)
    stats["dropped_zero_contributors"] = dropped_zero
    stats["dropped_empty_after_trace"] = dropped_empty
    stats["ttf_file"] = os.path.basename(out_ttf)
    stats["ttf_chars"] = n_chars
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    faint = [(ch, c["max_ink"], c["ink_px_fixed128_v5"],
             c["ink_px_adaptive_v5"])
            for ch, c in stats["chars"].items() if c.get("faint")]
    print("faint glyphs (max_ink<210):", len(faint))
    for row in sorted(faint, key=lambda r: r[1])[:15]:
        print("  faint:", row)
    print("dropped empty after trace:", dropped_empty[:40])


if __name__ == "__main__":
    main()
