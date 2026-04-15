from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class head:
    version            :int = 0
    fontRevision       :int = 0
    checkSumAdjustment :int = 0
    magicNumber        :int = 0
    flags              :int = 0
    unitsPerEm         :int = 0
    created            :int = 0 # TODO: Use custom LongDateTime class
    modified           :int = 0 # TODO: Use custom LongDateTime class
    xMin               :int = 0 # TODO: Use custom FWord class
    yMin               :int = 0 # TODO: Use custom FWord class
    xMax               :int = 0 # TODO: Use custom FWord class
    yMax               :int = 0 # TODO: Use custom FWord class
    macStyle           :int = 0
    lowestRecPPEM      :int = 0
    fontDirectionHint  :int = 0
    indexToLocFormat   :int = 0
    glyphDataFormat    :int = 0

def ReadHeadTable(reader: Reader) -> head:
    """
    ### Reads the 'head' table from the current position
    
    ---
    
    The 'head' table contains global information about the font
    
    ---  
    
    ### 'head' table structure:
    
    ```
    Type          Name                Description
    Fixed         version             0x00010000 (version 1.0)
    Fixed         fontRevision        set by font manufacturer
    uint32        checkSumAdjustment  To compute: set it to 0, calculate the checksum for the 'head'
                                      table and put it in the table directory, sum the entire font
                                      as a uint32_t, then store 0xB1B0AFBA - sum. (The checksum for
                                      the 'head' table will be wrong as a result. That is OK; do not
                                      reset it.)
    uint32        magicNumber         set to 0x5F0F3CF5
    uint16        flags               bit 0 - y value of 0 specifies baseline
                                      bit 1 - x position of left most black bit is LSB
                                      bit 2 - scaled point size and actual point size will differ
                                      (i.e. 24 point glyph differs from 12 point glyph scaled by
                                      factor of 2)
                                      bit 3 - use integer scaling instead of fractional
                                      bit 4 - (used by the Microsoft implementation of the TrueType
                                      scaler)
                                      bit 5 - This bit should be set in fonts that are intended to be
                                      laid out vertically, and in which the glyphs have been drawn such
                                      that an x-coordinate of 0 corresponds to the desired vertical
                                      baseline.
                                      bit 6 - This bit must be set to zero.
                                      bit 7 - This bit should be set if the font requires layout for
                                      correct linguistic rendering (e.g. Arabic fonts).
                                      bit 8 - This bit should be set for an AAT font which has one or
                                      more metamorphosis effects designated as happening by default.
                                      bit 9 - This bit should be set if the font contains any strong
                                      right-to-left glyphs.
                                      bit 10 - This bit should be set if the font contains Indic-style
                                      rearrangement effects.
                                      bits 11-13 - Defined by Adobe.
                                      bit 14 - This bit should be set if the glyphs in the font are
                                      simply generic symbols for code point ranges, such as for a
                                      last resort font.
    uint16        unitsPerEm          range from 64 to 16384
    longDateTime  created             international date
    longDateTime  modified            international date
    FWord         xMin                for all glyph bounding boxes
    FWord         yMin                for all glyph bounding boxes
    FWord         xMax                for all glyph bounding boxes
    FWord         yMax                for all glyph bounding boxes
    uint16        macStyle            bit 0 bold
                                      bit 1 italic
                                      bit 2 underline
                                      bit 3 outline
                                      bit 4 shadow
                                      bit 5 condensed (narrow)
                                      bit 6 extended
    uint16        lowestRecPPEM       smallest readable size in pixels
    int16         fontDirectionHint   0 Mixed directional glyphs
                                      1 Only strongly left to right glyphs
                                      2 Like 1 but also contains neutrals
                                      -1 Only strongly right to left glyphs
                                      -2 Like -1 but also contains neutrals
    int16         indexToLocFormat    0 for short offsets, 1 for long
    int16         glyphDataFormat     0 for current format
    ```
    """

    headTable: head = head()

    reader.SkipBytes(50)
    headTable.indexToLocFormat = reader.ReadInt16()

    return headTable