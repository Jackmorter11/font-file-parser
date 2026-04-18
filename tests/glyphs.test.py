"""
Test each glyph in the font and see how many are read correctly
NOTE: Might not check each glyph e.g. noto sans has 3,741 glyphs - google fonts
but only prints Checked glyphs: 2642
Might be not full reading the cmap table
"""

from fontTools.ttLib import TTFont
from fontReader import ParseTTF


def isComposite(font, glyphName):
    glyph = font["glyf"][glyphName]
    return glyph.isComposite()


def compareFonts(fontPath):
    ft = TTFont(fontPath)
    myFont = ParseTTF(fontPath)

    glyfTable = ft["glyf"]
    glyphOrder = ft.getGlyphOrder()

    mismatches = []
    totalChecked = 0

    for gid, glyphName in enumerate(glyphOrder):
        glyph = glyfTable[glyphName]

        # skip composite glyphs
        if glyph.isComposite():
            continue

        # skip empty glyphs
        if glyph.numberOfContours == 0:
            continue

        ftGlyph = glyph
        myGlyph = myFont.glyphs[gid]

        totalChecked += 1

        # ---- NORMALISE DATA (IMPORTANT FIX) ----

        ftPoints = list(ftGlyph.coordinates)
        myPoints = [(p.x, p.y) for p in myGlyph.points]

        ftEndPts = ftGlyph.endPtsOfContours
        myEndPts = myGlyph.endPtsOfContours

        # ---- COMPARE ----

        if ftEndPts != myEndPts:
            mismatches.append((gid, "endPts mismatch"))
            continue

        if len(ftPoints) != len(myPoints):
            mismatches.append((gid, "coordinate count mismatch"))
            continue

        for i in range(len(ftPoints)):
            if ftPoints[i] != myPoints[i]:
                mismatches.append((gid, f"point mismatch at {i}"))
                break

    print(f"Checked glyphs: {totalChecked}")
    print(f"Mismatches: {len(mismatches)}")

    return mismatches


jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

compareFonts(notoSans)