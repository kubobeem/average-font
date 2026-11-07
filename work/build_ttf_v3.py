#!/usr/bin/env python3
"""Build the v3 TTF from the averaged glyph bitmaps (out/glyphs_v3/).

Difference from v2 (build_ttf.py): the binarization threshold is
ADAPTIVE per glyph instead of a fixed 50% (ink >= 128).

Why (measured on the v3 render, out/stats_v3.json): the cause is NOT
missing fonts — every joyo kanji has 200..227 contributing fonts and
every glyph's average-ink peak is >= 157 (median 251 for kanji). The
cause is ink SPREAD: each font puts the same stroke at a slightly
different pixel, so the average is a blurred halo around a core.
A fixed 128 cutoff keeps only the core: median 55% of the visible
ink (pixels >= 64) survives, and for the worst kanji (言・二・吉・士…)
only ~31%. Thin horizontal strokes (一・二・三) suffer most — their
peaks are only 180..195 and the fixed cutoff leaves them skeletal.

v3 rule (per glyph, max_ink = peak of the 0..255 average ink):
    threshold = clamp(0.40 * max_ink, 8, 128)
- dense glyphs (max_ink 255) -> 102, close to v2's 128 (same look);
- mid glyphs (max_ink 150) -> 60;
- faint glyphs (max_ink 80) -> 32, (max_ink 50) -> 20:
  the stroke core (where the contributing fonts agree) survives.
The 0.40 factor keeps the threshold at 40% of each glyph's own peak,
so the cut follows the glyph instead of an absolute level.
Floor 8 avoids turning pure background noise into a blob for
near-empty glyphs; cap 128 keeps v2 behaviour for dense glyphs.

Per-glyph threshold / ink-pixel counts (adaptive vs fixed-128) are
written back into out/stats_v3.json for the README and the
before/after sheet (work/make_sheets_v3.py).
"""
import json, os
import numpy as np
import cv2
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
GLYPHS = os.path.join(OUT, "glyphs_v3")
TEMPLATE = os.path.join(BASE, "fonts", "DotGothic16-Regular.ttf")
OUT_TTF = os.path.join(BASE, "AverageFont-Regular-v3-229fonts-2290chars.ttf")

SHIFT = {"hiragana": -60, "katakana": -60, "kanji": -60,
         "digits": -150, "latin_upper": -150, "latin_lower": -250}

def adaptive_threshold(max_ink):
    """v3 per-glyph binarization threshold (see module docstring)."""
    return float(min(128.0, max(8.0, 0.40 * max_ink)))

def trace_glyph(png_path, upem, shift, threshold, eps=1.5):
    """Return list of contours; each contour is a list of (x, y) int points
    in font coordinates (y up, baseline 0). First contour(s) are outer."""
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    ink = (255 - img.astype(np.int16))
    mask = (ink >= threshold).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return [], 0
    h = hierarchy[0]
    scale = upem / 256.0
    out = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 4:  # drop specks
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
    stats_path = os.path.join(OUT, "stats_v3.json")
    stats = json.load(open(stats_path, encoding="utf-8"))
    font = TTFont(TEMPLATE)
    upem = font["head"].unitsPerEm
    print("template upem:", upem)
    _glyf, _hmtx = font["glyf"], font["hmtx"]
    _name, _os2 = font["name"], font["OS/2"]
    _hhea, _head, _maxp = font["hhea"], font["head"], font["maxp"]
    glyph_order = [".notdef", "space"]
    for ch in stats["chars"]:
        glyph_order.append(f"uni{ord(ch):04X}")
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
    for ch, info in stats["chars"].items():
        gname = f"uni{ord(ch):04X}"
        png = os.path.join(GLYPHS, info["file"])
        thr = adaptive_threshold(info["max_ink"])
        contours, n_ink = trace_glyph(png, upem, SHIFT[info["group"]], thr)
        # fixed-128 pixel count, for the before/after comparison
        img = cv2.imread(png, cv2.IMREAD_GRAYSCALE)
        ink = (255 - img.astype(np.int16))
        info["threshold_v3"] = round(thr, 1)
        info["ink_px_adaptive"] = n_ink
        info["ink_px_fixed128"] = int((ink >= 128).sum())
        info["ink_retention_fixed128"] = round(
            info["ink_px_fixed128"] / max(info["ink_px_ge64"], 1), 3)
        # "faint" = low average-ink peak (thin / position-spread strokes)
        info["faint"] = bool(info["max_ink"] < 210)
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

    glyf.glyphs["space"] = TTGlyphPen(None).glyph()
    hmtx.metrics["space"] = (500, 0)
    cmap_map[0x20] = "space"

    cmap = newTable("cmap")
    cmap.tableVersion = 0
    sub = CmapSubtable.newSubtable(4)
    sub.platformID = 3
    sub.platEncID = 1
    sub.language = 0
    sub.cmap = cmap_map
    cmap.tables = [sub]
    font["cmap"] = cmap

    name = font["name"]
    for nid, val in [(1, "Average Font"), (2, "Regular"),
                     (4, "Average Font Regular"), (6, "AverageFont-Regular"),
                     (16, "Average Font"), (17, "Regular")]:
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)
    name.setName("Version 3.0; 2290 chars (joyo kanji 2136)", 5, 3, 1, 0x409)
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
            xs_min.append(g.xMin); ys_min.append(g.yMin)
            xs_max.append(g.xMax); ys_max.append(g.yMax)
    if xs_min:
        font["head"].xMin, font["head"].yMin = min(xs_min), min(ys_min)
        font["head"].xMax, font["head"].yMax = max(xs_max), max(ys_max)
    font["maxp"].recalc(font)

    font.save(OUT_TTF)
    print("saved", OUT_TTF, os.path.getsize(OUT_TTF), "bytes, glyphs:", len(glyph_order))
    print("empty glyphs (no contours):", n_empty)
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    faint = [(ch, c["max_ink"], c["ink_px_fixed128"], c["ink_px_adaptive"])
             for ch, c in stats["chars"].items() if c["faint"]]
    print("faint glyphs (max_ink<210):", len(faint))
    for row in sorted(faint, key=lambda r: r[1])[:15]:
        print("  faint:", row)

if __name__ == "__main__":
    main()
