import logging
from reader import Reader
from fontClasses import Glyph

logging.basicConfig(
    filename="parseTTF.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class ParseTTF:
    def __init__(self, fontPath: str):
        logging.info("Starting Parser...")

        self.reader = Reader(fontPath)
        logging.info("Initiated Reader")

        self.ReadOffsetSubTable()
        logging.info("Read Sub Table")
        
        self.ReadTableDirectory()
        logging.info("Read Table Directory")

        self.reader.goto(self.tables["maxp"]["offset"])
        self.ReadMaxpTable()
        logging.info("Read maxp Table")

        self.reader.goto(self.tables["head"]["offset"])
        self.ReadHeadTable()
        logging.info("Read head Table")

        self.reader.goto(self.tables["glyf"]["offset"])
        self.ReadGlyfTable()
        logging.info("Read glyf Table")

        self.reader.goto(self.tables["cmap"]["offset"])
        self.ReadCmapTable()
        logging.info("Read cmap Table")
        


    def ReadOffsetSubTable(self):
        """
        TODO: The offset subtable keeps record of the tables in the font and provides offset information to access each table in the directory

        ```
        Type      Name             Description
        uint32    scalerType       A tag to indicate the OFA scaler to be used to rasterize this font
        uint16    numTables        Number of tables
        uint16    searchRange      (maximum power of 2 <= numTables) * 16
        uint16    entrySelector    log2(maximum power of 2 <= numTables)
        uint16    rangeShift       numTables * 16 - searchRange
        ```
        """
        
        self.scalerType:    int = self.reader.ReadUInt32()
        self.numTables:     int = self.reader.ReadUInt16()
        self.searchRange:   int = self.reader.ReadUInt16()
        self.entrySelector: int = self.reader.ReadUInt16()
        self.rangeShift:    int = self.reader.ReadUInt16()
        
    def ReadTableDirectory(self):
        """  
        The table directory comes right after the offset subtable. It stores data needed for finding each of the tables

        ```
        Type      Name        Description
        uint32    tag         4-byte identifier
        uint32    checkSum    checksum for this table
        uint32    offset      offset from beginning of sfnt
        uint32    length      length of this table in byte (actual length not padded length)
        ```
        """

        # Dictionary to store table data
        self.tables = {}

        # Iterate through every table
        for i in range(self.numTables):
            tag:      str = self.reader.ReadStr32()  # Name of table
            checkSum: int = self.reader.ReadUInt32()
            offset:   int = self.reader.ReadUInt32()
            length:   int = self.reader.ReadUInt32()

            self.tables[tag] = {"checkSum": checkSum, "offset": offset, "length": length}


    def ReadMaxpTable(self):
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

        self.reader.SkipBytes(4) # Version
        self.numGlyphs = self.reader.ReadUInt16()
    
    def ReadHeadTable(self):
        """
        ### **Reads the 'head' table from the current position**
        
        ---
        
        The 'head' table contains global information about the font
        
        ---  
        
        ### 'head' table structure:
        
        ```
        Type          Name                Description
        Fixed         version             0x00010000 if (version 1.0)
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

        self.reader.SkipBytes(50)
        self.indexToLocFormat = self.reader.ReadInt16()


    def ReadCmapTable(self):
        version = self.reader.ReadUInt16()
        numSubtables = self.reader.ReadUInt16() # Font can contain multiple charicter maps for different platforms

        cmapSubtableOffset = 0
        


    def ReadGlyfTable(self):
        isTwoByteEntery: bool = self.indexToLocFormat == 0
        locaTableStart = self.tables["loca"]["offset"]
        glyphTableStart = self.tables["glyf"]["offset"]
        self.allGlyphLocations = []

        for glyphIndex in range(self.numGlyphs):
            self.reader.goto(locaTableStart + glyphIndex * (2 if isTwoByteEntery else 4))
            # If 2-byte format is used, the stored location is half of actual location (so multiply by 2)
            glyphDataOffset = self.reader.ReadUInt16() * 2 if isTwoByteEntery else self.reader.ReadUInt32()
            self.allGlyphLocations.append(glyphTableStart + glyphDataOffset)
        
        self.glyphs = []
        for glyphLocation in self.allGlyphLocations:
            self.reader.goto(glyphLocation)
            glyph = self.ReadGlyph()
            self.glyphs.append(glyph)

    def ReadGlyph(self) -> Glyph:
        """
        **Read a single glyph table from the current position**.
        
        Below is the start of the Glyph Table; the rest depends on if it is a simple or compound glyph

        ```
        Type      Name              Description
        uint16    numberOfContours  If the number of contours is positive or zero, it is a single glyph
                                    If the number of contours less than zero, the glyph is compound
        FWord     xMin              Minimum x for coordinate data
        FWord     yMin              Minimum y for coordinate data
        FWord     xMax              Maximum x for coordinate data
        FWord     yMax              Maximum y for coordinate data
        ```
        """

        numberOfContours: int = self.reader.ReadInt16()
        self.reader.SkipBytes(8) # TODO: Read in bounding box

        if numberOfContours >= 0:
            return self.ReadSimpleGlyph(numberOfContours)
        else:
            return Glyph([], [], [])

    def ReadSimpleGlyph(self, numberOfContours: int) -> Glyph:
        """
        **Read the rest of a simple glyph table from the current position**.
        
        Below is the rest of a simple Glyph Table

        ```
        Type      Name                             Description
        uint16    endPtsOfContours[n]              Array of last points of each contour
                                                   n is the number of contours
                                                   array entries are point indices
        uint16    instructionLength                Total number of bytes needed for instructions
        uint8     instructions[instructionLength]  Array of instructions for this glyph
        uint8     flags[variable]                  Array of flags
        uint8/16  xCoordinates[]                   Array of x-coordinates; the first is relative to (0,0),
                                                   others are relative to previous point
        uint8/16  yCoordinates[]                   Array of y-coordinates; the first is relative to (0,0),
                                                   others are relative to previous point
        ```
        """

        # Read numberOfContours amount of UInt16 values
        # representing the contours and add to list of contours
        endPtsOfContours: list[int] = []
        for _ in range(numberOfContours):
            endPtsOfContours.append(self.reader.ReadUInt16())

        # TODO: Use instructions
        instructionLength = self.reader.ReadUInt16()
        self.reader.SkipBytes(instructionLength)
        
        # Find number of points in simple glyph from last endPoint + 1
        numPoints: int = endPtsOfContours[-1] + 1 if len(endPtsOfContours) else 0

        # List of flags, 1 byte for each point
        allFlags: list[bytes] = []
        # Read numPoints amount of Byte values
        # representing the flags for each point
        i = 0
        while i < numPoints:
            flag: bytes = self.reader.ReadByte()
            allFlags.append(flag)
            i += 1

            # If repeat bit (3rd bit) is set, read next byte to determine num copies
            # then add flag that many times
            if self.FlagBitIsSet(flag, 3):
                copies = self.reader.ReadByte()[0]
                # Only add up to remaining points
                remaining = numPoints - i
                actualCopies = min(copies, remaining)

                allFlags += [flag] * actualCopies
                i += actualCopies
            
        coordsX: list[int] = self.ReadCoordinates(allFlags, readingX=True)
        coordsY: list[int] = self.ReadCoordinates(allFlags, readingX=False)
        return Glyph(coordsX, coordsY, endPtsOfContours)
        
    def ReadCoordinates(self, allFlags: list[bytes], readingX: bool) -> list[int]:
        """
        Used in ReadSimpleGlyph(), reads the xCoordinates and yCoordinates arrays
        """

        offsetSizeFlagBit:   int = 1 if readingX else 2
        offsetSignOrSkipBit: int = 4 if readingX else 5

        coordinates:   list[int] = []
        current = 0

        # Iterate through each point, convert to absolute coordinate and add to list
        for i in range(len(allFlags)):
            # Coordinate is relative to previous value (0 for first coordinate)
            flag: bytes = allFlags[i]
            onCurve: bool = self.FlagBitIsSet(flag, 0) # TODO: Do something with this

            # 1 byte offset (unsigned)
            if self.FlagBitIsSet(flag, offsetSizeFlagBit):
                offset: int = self.reader.ReadByte()[0]
                if self.FlagBitIsSet(flag, offsetSignOrSkipBit):
                    current += offset   # positive
                else:
                    current -= offset   # negative
            
            # 2 byte offset (signed)
            # (Unless flag says to skip it and just kepp the coordinate the same)
            elif not self.FlagBitIsSet(flag, offsetSignOrSkipBit):
                current += self.reader.ReadInt16()

            coordinates.append(current)

        return coordinates


    def FlagBitIsSet(self, flag: bytes, bitIndex: int) -> bool:
        """
        **Test whether a particular bit in a byte is ON (1) or OFF (0)**

        * `flag`: The byte to check, has to be 1 byte long

        * `bitIndex`: The index in the byte to check
        """

        if len(flag) != 1:
            raise ValueError("FlagByteIsSet(): Flag must be a single byte if using bytes")
        
        flagInt: int = flag[0] # Convert single byte to int
        return ((flagInt >> bitIndex) & 1) == 1

        

if __name__ == "__main__":
    fontPath = "fonts/JetBrainsMono/fonts/ttf/JetBrainsMono-Bold.ttf"
    font = ParseTTF(fontPath)

    for i in range(0, 50):
        print(f"Glyph {i}:")
        print(font.glyphs[i])





"""
### **Reads the '' table from the current position**

---

The '' table...

---  

### '' table structure:

```
Type Name Description
```
"""