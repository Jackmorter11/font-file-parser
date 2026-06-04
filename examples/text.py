from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansChinese = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(jetBrainsMono, loggingEnabled=True)

text = "i"
font.logger.timeLog("Starting loading string benchmark")
for char in text:
    glyph = font.glyphs[font.cmap.CharToGlyphIndex(char)]
    print(f"{char} - {glyph}\n")
font.logger.timeLog("Finished loading string benchmark")
font.logger.timeLog(f"Loaded {len(font.glyphs)} out of {font.maxp.numGlyphs} glyphs")

print(font.name)