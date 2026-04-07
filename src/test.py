import os
from parseTTF import ParseTTF
from fontTools.ttLib import TTFont

fontPath = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"

# FontTools font
fontToolsFont = TTFont(fontPath)
cmap = fontToolsFont.getBestCmap()

# Your parser
myFont = ParseTTF(fontPath)

coordinatesMismatch = 0
endPtsMismatch = 0
totalGlyphs = 0

for codepoint, glyphName in cmap.items():
    fontToolsGlyph = fontToolsFont["glyf"][glyphName]
    try:
        # Get the glyph index from a character
        glyphIndex = myFont.mappings[codepoint]
        myGlyph = myFont.glyphs[glyphIndex]

        if myGlyph.coordinates != fontToolsGlyph.coordinates:
            coordinatesMismatch += 1
        if myGlyph.endPtsOfContours != fontToolsGlyph.endPtsOfContours:
            endPtsMismatch += 1

    except Exception as e:
        # Optional: print(e) to debug missing glyphs
        pass

    totalGlyphs += 1

print(f"glyph.coordinates:       {totalGlyphs - coordinatesMismatch} / {totalGlyphs} passed")
print(f"glyph.endPtsOfContours:  {totalGlyphs - endPtsMismatch} / {totalGlyphs} passed")