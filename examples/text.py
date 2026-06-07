"""
Example to print the glyph data for every charicter in a sting
"""
from fontReader import ParseTTF


JETBRAINS_MONO = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
NOTO_SANS = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
NOTO_SANS_CHINESE = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
NOTO_SANS_SYMBOLS = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"


font = ParseTTF(NOTO_SANS_CHINESE, loggingEnabled=True)

TEXT = "⇌"

for char in TEXT:
    glyph = font.glyphs[font.cmap.charToGlyphIndex(char)]
    print(glyph)
