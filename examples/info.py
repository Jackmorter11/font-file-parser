from fontReader import ParseTTF


JETBRAINS_MONO = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
NOTO_SANS = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
NOTO_SANS_CHINESE = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
NOTO_SANS_SYMBOLS = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"


font = ParseTTF(NOTO_SANS_CHINESE, loggingEnabled=True)

glyph = font.glyphs[font.cmap.CharToGlyphIndex("#")]
print(glyph)

#print(font)

#print(font.offsetSubTable)
#print(font.tableDirectory)

#print(font.loca)
#print(font.name)
#print(font.maxp)
#print(font.head)
