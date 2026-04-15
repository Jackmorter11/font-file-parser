from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class maxp:
    version               :int = 0 # TODO: Use custom 4dot4 class e.g 1.6 = 0001.0110
    numGlyphs             :int = 0
    maxPoints             :int = 0
    maxContours           :int = 0
    maxComponentPoints    :int = 0
    maxComponentContours  :int = 0
    maxZones              :int = 0
    maxTwilightPoints     :int = 0
    maxStorage            :int = 0
    maxFunctionDefs       :int = 0
    maxInstructionDefs    :int = 0
    maxStackElements      :int = 0
    maxSizeOfInstructions :int = 0
    maxComponentElements  :int = 0
    maxComponentDepth     :int = 0

def ReadMaxpTable(reader: Reader) -> maxp:
    """
    ### **Reads the 'maxp' table from the current position**
    
    ---

    The 'maxp' table establishes the memory requirements for a font

    ---

    ### 'maxp' table structure:

    ```
    Type    Name                   Description
    Fixed   version                0x00010000 (1.0)
    uint16  numGlyphs              the number of glyphs in the font
    uint16  maxPoints              points in non-compound glyph
    uint16  maxContours            contours in non-compound glyph
    uint16  maxComponentPoints     points in compound glyph
    uint16  maxComponentContours   contours in compound glyph
    uint16  maxZones               set to 2
    uint16  maxTwilightPoints      points used in Twilight Zone (Z0)
    uint16  maxStorage             number of Storage Area locations
    uint16  maxFunctionDefs        number of FDEFs
    uint16  maxInstructionDefs     number of IDEFs
    uint16  maxStackElements       maximum stack depth
    uint16  maxSizeOfInstructions  byte count for glyph instructions
    uint16  maxComponentElements   number of glyphs referenced at top level
    uint16  maxComponentDepth      levels of recursion, set to 0 if font has only simple glyphs
    ```
    """

    maxpTable: maxp = maxp()

    reader.SkipBytes(4) # Version
    maxpTable.numGlyphs = reader.ReadUInt16()

    return maxpTable