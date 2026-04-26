"""Finds the glyph with the most points in a certain font"""

from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansChinese = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Regular.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(notoSansChinese, loggingEnabled=True)

maxPoints = 0
mostComplexGlyph = -1
for i, glyph in enumerate(font.glyphs):
    if len(glyph.points) > maxPoints:
        maxPoints = len(glyph.points)
        mostComplexGlyph = i

mostComplexGlyphCodepoint = -1
for codepoint, glyph in font.cmap.mappings.items():
    if glyph == mostComplexGlyph:
        mostComplexGlyphCodepoint = codepoint

glyph = font.glyphs[mostComplexGlyph]
print(f"{chr(mostComplexGlyphCodepoint)} - {glyph.numberOfContours} contours:")
print(glyph)

