"""
Example to print general info about the font and summaries of the tables
"""

from fontReader import ParseTTF


JETBRAINS_MONO = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
NOTO_SANS = "fonts/Noto_Sans/static/NotoSans-Bold.ttf"
NOTO_SANS_CHINESE = "fonts/Noto_Sans_Chinese/static/NotoSansTC-Bold.ttf"
NOTO_SANS_SYMBOLS = "fonts/Noto_Sans_Symbols/static/NotoSansSymbols-Bold.ttf"


font = ParseTTF(NOTO_SANS_CHINESE, loggingEnabled=True)

print()
print(font)

print()
print(font.offsetSubTable)
print()
print(font.tables)

print()
print(font.head)
print()
print(font.cmap)
print()
print(font.loca)
print()
print(font.name)
print()
print(font.maxp)
