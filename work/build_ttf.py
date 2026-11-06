#!/usr/bin/env python3
"""Build a TTF from the averaged glyph bitmaps.

Method: threshold each averaged PNG at 50% ink, extract contours with
OpenCV (RETR_CCOMP so holes survive), simplify with approxPolyDP,
convert to font units and write glyphs (straight-line segments only)
into a copy of DotGothic16 (used only as a table template).
Vertical shift per group compensates for the anchor='mm' centered
rendering so glyphs sit on a plausible baseline.
"""
import json, os
import numpy as np
import cv2
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE = os.path.expanduser("~/workspace/average-font")
OUT = os.path.join(BASE, "out")
TEMPLATE = os.path.join(BASE, "fonts", "DotGothic16-Regular.ttf")

# vertical shift in font units (1000 upem), per group
SHIFT = {"hiragana": -60, "katakana": -60, "kanji": -60,
         "digits": -150, "latin_upper": -150, "latin_lower": -250}

def trace_glyph(png_path, upem, shift, eps=1.5):
    """Return list of contours; each contour is a list of (x, y) int points
    in font coordinates (y up, baseline 0). First contour(s) are outer."""
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    ink = (255 - img.astype(np.int16))
    mask = (ink >= 128).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return []
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
        # drop duplicate consecutive points
        pts = [p for j, p in enumerate(pts) if j == 0 or p != pts[j - 1]]
        if len(pts) >= 3:
            out.append((int(h[i][3]), pts))  # (parent, points)
    # outer contours first (parent == -1), then holes
    out.sort(key=lambda t: 0 if t[0] == -1 else 1)
    return [pts for _, pts in out]

def main():
    stats = json.load(open(os.path.join(OUT, "stats.json"), encoding="utf-8"))
    font = TTFont(TEMPLATE)
    upem = font["head"].unitsPerEm
    print("template upem:", upem)
    # force-decompile the tables we will edit BEFORE changing glyph order
    _glyf, _hmtx = font["glyf"], font["hmtx"]
    _name, _os2 = font["name"], font["OS/2"]
    _hhea, _head, _maxp = font["hhea"], font["head"], font["maxp"]
    glyph_order = [".notdef", "space"]
    for ch in stats["chars"]:
        glyph_order.append(f"uni{ord(ch):04X}")
    font.setGlyphOrder(glyph_order)

    # drop tables that reference the old glyph set / hinting
    for tag in ["GPOS", "GSUB", "GDEF", "BASE", "JSTF", "kern", "cvt ",
                "prep", "fpgm", "MATH", "COLR", "CBDT", "CBLC", "EBDT",
                "EBLC", "sbix", "VDMX", "LTSH", "hdmx", "DSIG", "STAT"]:
        if tag in font:
            del font[tag]

    glyf = font["glyf"]
    # remove old glyphs except .notdef
    for gname in list(glyf.glyphs.keys()):
        if gname != ".notdef":
            del glyf.glyphs[gname]
    hmtx = font["hmtx"]
    for gname in list(hmtx.metrics.keys()):
        if gname != ".notdef":
            del hmtx.metrics[gname]

    cmap_map = {}
    for ch, info in stats["chars"].items():
        gname = f"uni{ord(ch):04X}"
        png = os.path.join(OUT, "glyphs", info["file"])
        contours = trace_glyph(png, upem, SHIFT[info["group"]])
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
        hmtx.metrics[gname] = (adv, lsb)
        cmap_map[ord(ch)] = gname

    # space: empty glyph, advance 500 (not in the averaged set, but text
    # without a space glyph renders tofu between every word)
    glyf.glyphs["space"] = TTGlyphPen(None).glyph()
    hmtx.metrics["space"] = (500, 0)
    cmap_map[0x20] = "space"

    # rebuild cmap (format 4 only; all chars are BMP)
    cmap = newTable("cmap")
    cmap.tableVersion = 0
    sub = CmapSubtable.newSubtable(4)
    sub.platformID = 3
    sub.platEncID = 1
    sub.language = 0
    sub.cmap = cmap_map
    cmap.tables = [sub]
    font["cmap"] = cmap

    # names
    name = font["name"]
    for nid, val in [(1, "Average Font"), (2, "Regular"),
                     (4, "Average Font Regular"), (6, "AverageFont-Regular"),
                     (16, "Average Font"), (17, "Regular")]:
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)
    # metrics
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
    os2.fsSelection &= ~0x0080  # clear USE_TYPO_METRICS? keep simple
    head = font["head"]
    head.xMin, head.yMin, head.xMax, head.yMax = 0, -120, 1000, 900
    font["maxp"].numGlyphs = len(glyph_order)
    # recalculate each glyph's bounding box, then union -> head bounding box
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

    out_path = os.path.join(BASE, "AverageFont-Regular.ttf")
    font.save(out_path)
    print("saved", out_path, os.path.getsize(out_path), "bytes, glyphs:", len(glyph_order))

if __name__ == "__main__":
    main()
