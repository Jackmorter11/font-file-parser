from fontReader import ParseFont, ParseTTF

jetBrainsMono = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
notoSans = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
notoSansChinese = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
notoSansSymbols = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"

font = ParseTTF(notoSansChinese, loggingEnabled=True)

text = "苹果，这个我们一年四季都可以见到的水果，同样也是含有营养物质最多的水果之一。因此，往往有许多人会在早上会晚上吃苹果。那早上吃苹果好吗?早上吃苹果的好处又有哪些呢?今天萌主就来为大家一一解答一下。感兴趣的朋友就来看一下吧。"

font.logger.log("Starting loading string benchmark")
for char in text:
    glyph = font.glyphs[font.cmap.CharToGlyphIndex(char)]
    print(f"{char} - {glyph}\n")
font.logger.log("Finished loading string benchmark")
font.logger.log(f"Loaded {len(font.glyphs)} out of {font.maxp.numGlyphs} glyphs")