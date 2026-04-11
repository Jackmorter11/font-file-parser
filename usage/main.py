from fontReader import ParseFont

fontPath = r"fonts\JetBrainsMono\fonts\ttf\JetBrainsMono-Bold.ttf"

font = ParseFont(fontPath, loggingEnabled=True)

for glyph in font.glyphs[75:80]:
    print(f"• {glyph}")