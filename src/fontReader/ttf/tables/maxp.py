from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class maxpTable:
    version               :int = 0 # 0x00010000 (1.0) TODO: Use custom 4dot4 class e.g 1.6 = 0001.0110
    numGlyphs             :int = 0 # the number of glyphs in the font
    maxPoints             :int = 0 # points in non-compound glyph
    maxContours           :int = 0 # contours in non-compound glyph
    maxComponentPoints    :int = 0 # points in compound glyph
    maxComponentContours  :int = 0 # contours in compound glyph
    maxZones              :int = 0 # set to 2
    maxTwilightPoints     :int = 0 # points used in Twilight Zone (Z0)
    maxStorage            :int = 0 # number of Storage Area locations
    maxFunctionDefs       :int = 0 # number of FDEFs
    maxInstructionDefs    :int = 0 # number of IDEFs
    maxStackElements      :int = 0 # maximum stack depth
    maxSizeOfInstructions :int = 0 # byte count for glyph instructions
    maxComponentElements  :int = 0 # number of glyphs referenced at top level
    maxComponentDepth     :int = 0 # levels of recursion, set to 0 if font has only simple glyphs

def ReadMaxpTable(reader: Reader) -> maxpTable:
    """
    ### Reads the 'maxp' table from the current position
    
    ---
    The 'maxp' table establishes the memory requirements for a font
    """

    table: maxpTable = maxpTable()

    reader.SkipBytes(4) # Version
    table.numGlyphs = reader.ReadUInt16()

    return table