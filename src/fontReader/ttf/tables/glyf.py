from dataclasses import dataclass, field
from typing import Literal

from ...common.reader import Reader
from ..tables.tableDirectory import tableDirectory

@dataclass
class point:
    x       :float = None
    y       :float = None
    onCurve :bool  = None

@dataclass
class glyph:
    numberOfContours :int         = None
    numPoints        :int         = None
    endPtsOfContours :list[int]   = field(default_factory=list)
    points           :list[point] = field(default_factory=list)

    def __str__(self):
        string = ""

        startPoint = 0
        for endPoint in self.endPtsOfContours:
            string += ", ".join(f"({point.x}, {point.y})" for point in self.points[startPoint:endPoint+1] + [self.points[startPoint]]) + "\n"
            startPoint = endPoint+1
        
        return string

def ReadGlyfTable(reader: Reader, indexToLocFormat: int, tables: dict[str, tableDirectory], numGlyphs: int) -> list[glyph]:
    isTwoByteEntery: bool = indexToLocFormat == 0
    locaTableStart = tables["loca"].offset
    glyphTableStart = tables["glyf"].offset

    # Read glyph locations
    allGlyphLocations: list[int] = []
    for glyphIndex in range(numGlyphs):
        reader.goto(locaTableStart + glyphIndex * (2 if isTwoByteEntery else 4))

        # If 2-byte format is used, the stored location is half of actual location (so multiply by 2)
        glyphDataOffset: int = reader.ReadUInt16() * 2 if isTwoByteEntery else reader.ReadUInt32()
        allGlyphLocations.append(glyphTableStart + glyphDataOffset)
    
    # Read actual glyph data
    glyphs: list[glyph] = []
    for glyphLocation in allGlyphLocations:
        reader.goto(glyphLocation)
        glyphData = ReadGlyph(reader)
        glyphs.append(glyphData)
    
    return glyphs

def ReadGlyph(reader: Reader) -> glyph:
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

    glyphData: glyph = glyph()

    glyphData.numberOfContours = reader.ReadInt16()
    reader.SkipBytes(8) # Skip bounding box

    if glyphData.numberOfContours >= 0:
        return ReadSimpleGlyph(reader, glyphData)
    else:
        return glyph()

def ReadSimpleGlyph(reader: Reader, glyphData: glyph) -> glyph:
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
    # representing the contours and add them to list of contours
    for _ in range(glyphData.numberOfContours):
        glyphData.endPtsOfContours.append(reader.ReadUInt16())

    # TODO: Use instructions
    instructionLength = reader.ReadUInt16()
    reader.SkipBytes(instructionLength)
    
    # Find number of points in simple glyph from last endPoint + 1
    glyphData.numPoints = glyphData.endPtsOfContours[-1] + 1 if len(glyphData.endPtsOfContours) else 0

    # List of flags, 1 byte for each point
    allFlags: list[bytes] = []
    # Read numPoints amount of Byte values
    # representing the flags for each point
    i = 0
    while i < glyphData.numPoints:
        flag: bytes = reader.ReadByte()
        allFlags.append(flag)
        i += 1

        # If repeat bit (3rd bit) is set, read next byte to determine num copies
        # then add flag that many times
        if FlagBitIsSet(flag, 3):
            copies = reader.ReadByte()[0]
            # Only add up to remaining points
            remaining = glyphData.numPoints - i
            actualCopies = min(copies, remaining)

            allFlags += [flag] * actualCopies
            i += actualCopies
        
    # Read coordinates for glyph, onCurve is duplicated for both X and Y
    coordsX, _ = ReadCoordinates(reader, allFlags, readingX=True)
    coordsY, onCurve = ReadCoordinates(reader, allFlags, readingX=False)
    for i in range(glyphData.numPoints):
        glyphData.points.append(point(coordsX[i], coordsY[i], onCurve[i]))

    return glyphData
    
def ReadCoordinates(reader: Reader, allFlags: list[bytes], readingX: bool) -> tuple[list[int], list[bool]]:
    """
    Used in ReadSimpleGlyph(), reads the xCoordinates and yCoordinates arrays
    """

    offsetSizeFlagBit:   int = 1 if readingX else 2
    offsetSignOrSkipBit: int = 4 if readingX else 5

    coordinates: list[int]  = []
    onCurves:    list[bool] = []
    
    # Iterate through each point, convert to absolute coordinate and add to list
    current: int = 0
    for i in range(len(allFlags)):
        # Coordinate is relative to previous value (0 for first coordinate)
        flag: bytes = allFlags[i]
        onCurves.append(FlagBitIsSet(flag, 0))

        # 1 byte offset (unsigned)
        if FlagBitIsSet(flag, offsetSizeFlagBit):
            offset: int = reader.ReadByte()[0]
            if FlagBitIsSet(flag, offsetSignOrSkipBit):
                current += offset   # positive
            else:
                current -= offset   # negative
        
        # 2 byte offset (signed)
        # (Unless flag says to skip it and just kepp the coordinate the same)
        elif not FlagBitIsSet(flag, offsetSignOrSkipBit):
            current += reader.ReadInt16()

        coordinates.append(current)

    return coordinates, onCurves


def FlagBitIsSet(flag: bytes, bitIndex: int) -> bool:
    """
    **Test whether a particular bit in a byte is ON (1) or OFF (0)**

    * `flag`: The byte to check, has to be 1 byte long

    * `bitIndex`: The index in the byte to check
    """

    if len(flag) != 1:
        raise ValueError("FlagByteIsSet(): Flag must be a single byte if using bytes")
    
    flagInt: int = flag[0] # Convert single byte to int
    return ((flagInt >> bitIndex) & 1) == 1