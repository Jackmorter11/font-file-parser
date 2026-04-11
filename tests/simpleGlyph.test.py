from fontTools.ttLib import TTFont
from fontReader import ParseFont


def isComposite(font, glyphName):
    glyph = font["glyf"][glyphName]
    return glyph.isComposite()


def compareFonts(fontPath):
    ft = TTFont(fontPath)
    myFont = ParseFont(fontPath)

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


fontPath = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"

compareFonts(fontPath)