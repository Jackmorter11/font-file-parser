from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansChinese = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Regular.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(notoSansChinese, loggingEnabled=True)

text = "我喜欢你"

for char in text:
    glyph = font.glyphs[font.cmap.CharToGlyphIndex(char)]
    print(f"{char} - {glyph}\n")