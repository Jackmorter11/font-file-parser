from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class maxp:
    version               :int = None # NOTE: Might not be int, 4dot4 e.g 1.6 or 4.7
    numGlyphs             :int = None
    maxPoints             :int = None
    maxContours           :int = None
    maxComponentPoints    :int = None
    maxComponentContours  :int = None
    maxZones              :int = None
    maxTwilightPoints     :int = None
    maxStorage            :int = None
    maxFunctionDefs       :int = None
    maxInstructionDefs    :int = None
    maxStackElements      :int = None
    maxSizeOfInstructions :int = None
    maxComponentElements  :int = None
    maxComponentDepth     :int = None

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

    table: maxp = maxp()

    reader.SkipBytes(4) # Version
    table.numGlyphs = reader.ReadUInt16()

    return table