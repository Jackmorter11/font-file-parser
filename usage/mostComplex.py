"""Finds the glyph with the most points in a certain font"""

from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(notoSans, loggingEnabled=True)

maxPoints = 0
mostComplexGlyph = -1
for i, glyph in enumerate(font.glyphs):
    if len(glyph.points) > maxPoints:
        maxPoints = len(glyph.points)
        mostComplexGlyph = i

print(font.glyphs[mostComplexGlyph])