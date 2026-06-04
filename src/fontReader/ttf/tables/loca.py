"""
Functions to read 'loca' table:

- readLocaTable(reader)
"""

from ...common.reader import Reader


class LocaTable:
    """
    Holds data for the 'loca' table:

    - offsets: List of offsets to each glyph (realative to 'glyf' table)
    """

    def __init__(self, offsets: list[int]):
        self.offsets = offsets

    def __str__(self) -> str:
        lines = []

        lines.append(f"Loca table ({len(self.offsets)} entries)")
        lines.append("-" * len(lines[-1]))
        lines.append(f"First {min(10, len(self.offsets))} entries:")
        for i in range(0, min(10, len(self.offsets))):
            lines.append(f"{i}: {self.offsets[i]}")

        return "\n".join(lines)


def readLocaTable(reader: Reader, indexToLocFormat: int, numGlyphs: int) -> LocaTable:
    """
    Reads the 'loca' table
    
    The 'loca' table stores the offsets to the locations of the glyph entries in the font (relative to the 'glyf' table)
    """

    isShort: bool       = indexToLocFormat == 0
    offsets: list[int]  = []

    for _ in range(numGlyphs):
        locaOffset = reader.ReadUInt16() * 2 if isShort else reader.ReadUInt32()
        offsets.append(locaOffset)

    return LocaTable(offsets)
