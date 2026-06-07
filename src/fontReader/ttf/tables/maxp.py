"""
The 'maxp' table contains maximum profiles, to establish the memory requirements, for a font

Functions to read 'maxp' table:

- readMaxpTable() -> MaxpTable
"""

from dataclasses import dataclass

from ...common.reader import Reader


@dataclass
class MaxpTable:
    """
    Contains 'maxp' table enteries

    - version: Always 0x00010000 (1.0)
    - numGlyphs: The number of glyphs in the font
    - maxPoints: Max points in non-compound glyph
    - maxContours: Max contours in non-compound glyph
    - maxComponentPoints: Max points in compound glyph
    - maxComponentContours: Max contours in compound glyph
    - maxZones: Set to 2
    - maxTwilightPoints: Max points used in Twilight Zone (Z0)
    - maxStorage: Max number of Storage Area locations
    - maxFunctionDefs: Max number of FDEFs
    - maxInstructionDefs: Max number of IDEFs
    - maxStackElements: Max maximum stack depth
    - maxSizeOfInstruction: Max byte count for glyph instructions
    - maxComponentElements: Max number of glyphs referenced at top level
    - maxComponentDepth: Max levels of recursion, set to 0 if font has only simple glyphs
    """

    version               :float
    numGlyphs             :int
    maxPoints             :int
    maxContours           :int
    maxComponentPoints    :int
    maxComponentContours  :int
    maxZones              :int
    maxTwilightPoints     :int
    maxStorage            :int
    maxFunctionDefs       :int
    maxInstructionDefs    :int
    maxStackElements      :int
    maxSizeOfInstructions :int
    maxComponentElements  :int
    maxComponentDepth     :int

    def __str__(self) -> str:
        """Human readable version of 'maxp" table"""

        lines = []
        lines.append("'maxp' table")
        lines.append("-" * 27)
        lines.append(f"version               {self.version:>5}")
        lines.append(f"numGlyphs             {self.numGlyphs:>5}")
        lines.append(f"maxPoints             {self.maxPoints:>5}")
        lines.append(f"maxContours           {self.maxContours:>5}")
        lines.append(f"maxComponentPoints    {self.maxComponentPoints:>5}")
        lines.append(f"maxComponentContours  {self.maxComponentContours:>5}")
        lines.append(f"maxZones              {self.maxZones:>5}")
        lines.append(f"maxTwilightPoints     {self.maxTwilightPoints:>5}")
        lines.append(f"maxStorage            {self.maxStorage:>5}")
        lines.append(f"maxFunctionDefs       {self.maxFunctionDefs:>5}")
        lines.append(f"maxInstructionDefs    {self.maxInstructionDefs:>5}")
        lines.append(f"maxStackElements      {self.maxStackElements:>5}")
        lines.append(f"maxSizeOfInstructions {self.maxSizeOfInstructions:>5}")
        lines.append(f"maxComponentElements  {self.maxComponentElements:>5}")
        lines.append(f"maxComponentDepth     {self.maxComponentDepth:>5}")

        return "\n".join(lines)


def readMaxpTable(reader: Reader) -> MaxpTable:
    """
    Reads the 'maxp' table
    
    The 'maxp' table establishes the memory requirements for a font
    """

    table: MaxpTable = MaxpTable(
        version               = reader.ReadFixedPoint16Dot16(),
        numGlyphs             = reader.ReadUInt16(),
        maxPoints             = reader.ReadUInt16(),
        maxContours           = reader.ReadUInt16(),
        maxComponentPoints    = reader.ReadUInt16(),
        maxComponentContours  = reader.ReadUInt16(),
        maxZones              = reader.ReadUInt16(),
        maxTwilightPoints     = reader.ReadUInt16(),
        maxStorage            = reader.ReadUInt16(),
        maxFunctionDefs       = reader.ReadUInt16(),
        maxInstructionDefs    = reader.ReadUInt16(),
        maxStackElements      = reader.ReadUInt16(),
        maxSizeOfInstructions = reader.ReadUInt16(),
        maxComponentElements  = reader.ReadUInt16(),
        maxComponentDepth     = reader.ReadUInt16()
    )

    return table
