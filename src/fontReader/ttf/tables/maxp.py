from dataclasses import dataclass

from ...common.reader import Reader


@dataclass
class maxpTable:
    version               :float # 0x00010000 (1.0)
    numGlyphs             :int   # the number of glyphs in the font
    maxPoints             :int   # points in non-compound glyph
    maxContours           :int   # contours in non-compound glyph
    maxComponentPoints    :int   # points in compound glyph
    maxComponentContours  :int   # contours in compound glyph
    maxZones              :int   # set to 2
    maxTwilightPoints     :int   # points used in Twilight Zone (Z0)
    maxStorage            :int   # number of Storage Area locations
    maxFunctionDefs       :int   # number of FDEFs
    maxInstructionDefs    :int   # number of IDEFs
    maxStackElements      :int   # maximum stack depth
    maxSizeOfInstructions :int   # byte count for glyph instructions
    maxComponentElements  :int   # number of glyphs referenced at top level
    maxComponentDepth     :int   # levels of recursion, set to 0 if font has only simple glyphs

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


def ReadMaxpTable(reader: Reader) -> maxpTable:
    """
    ### Reads the 'maxp' table from the current position
    
    ---
    The 'maxp' table establishes the memory requirements for a font
    """

    table: maxpTable = maxpTable(
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