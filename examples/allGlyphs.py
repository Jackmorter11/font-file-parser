"""
Example to load every glyph for performance tests
"""
from fontReader import ParseTTF


JETBRAINS_MONO = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
NOTO_SANS = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
NOTO_SANS_CHINESE = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
NOTO_SANS_SYMBOLS = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"


font = ParseTTF(NOTO_SANS_CHINESE, loggingEnabled=True)

font.logger.blankLine()
font.logger.timeLog("Started loading all glyphs")

for i in range(font.maxp.numGlyphs):
    glyph = font.glyphs[i]

font.logger.timeLog("Finished loading all glyphs")
