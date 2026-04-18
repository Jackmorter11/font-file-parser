from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(jetBrainsMono, loggingEnabled=True)

char = "i" # 我喜欢你

glyph = font.glyphs[font.cmap.CharToGlyphIndex(char)]
print(f"{char} - {glyph}")