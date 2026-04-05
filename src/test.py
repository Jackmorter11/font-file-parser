import os
import random
from parseTTF import ParseTTF
from fontTools.ttLib import TTFont


fontPath = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"

fontToolsFont = TTFont(fontPath)
cmap = fontToolsFont.getBestCmap()

myFont = ParseTTF(fontPath)

coordiantesMismatch = 0
endPtsMismatch = 0
totalGlyphs = 0

for codepoint, glyphName in cmap.items():
    fontToolsGlyph = fontToolsFont["glyf"][glyphName]
    try:
        myGlyph = myFont.glyphs[glyphName]
    
        if myGlyph.coordinates == fontToolsGlyph.coordinates: coordiantesMismatch += 1
        if myGlyph.endPtsOfContours == myGlyph.endPtsOfContours: endPtsMismatch += 1
    
    except:
        pass

    totalGlyphs += 1


print(f"glyph.coordaintes:       {coordiantesMismatch} / {totalGlyphs} passed")
print(f"glyph.endPtsOfContours:  {endPtsMismatch} / {totalGlyphs} passed")