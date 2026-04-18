from dataclasses import dataclass, field

from ...common.reader import Reader
from ..tables.tableDirectory import table


# Data structures

@dataclass
class point:
    x: float = 0
    y: float = 0
    onCurve: bool = False


@dataclass
class glyphData:
    numberOfContours: int = 0
    numPoints: int = 0
    endPtsOfContours: list[int] = field(default_factory=list)
    points: list[point] = field(default_factory=list)

    def __str__(self):
        string = ""
        startPoint = 0

        for endPoint in self.endPtsOfContours:
            contour = self.points[startPoint:endPoint + 1]
            contour.append(self.points[startPoint])  # close contour

            string += ", ".join(f"({p.x}, {p.y})" for p in contour) + "\n"
            startPoint = endPoint + 1

        return string


# Entry point
def ReadGlyfTable(reader: Reader, indexToLocFormat: int, tables: dict[str, table], numGlyphs: int) -> list[glyphData]:
    isShort = indexToLocFormat == 0

    locaStart = tables["loca"].offset
    glyfStart = tables["glyf"].offset

    glyphLocations: list[int] = []

    # Read loca table NOTE: Should be in tables/loca ?
    for i in range(numGlyphs):
        reader.goto(locaStart + i * (2 if isShort else 4))

        offset = reader.ReadUInt16() * 2 if isShort else reader.ReadUInt32()
        glyphLocations.append(glyfStart + offset)

    # Read glyphs
    glyphs: list[glyphData] = []

    for loc in glyphLocations:
        reader.goto(loc)
        glyphs.append(ReadGlyph(reader, indexToLocFormat, tables))

    return glyphs


# Glyph readers

def ReadGlyph(reader: Reader, indexToLocFormat: int, tables: dict[str, table]) -> glyphData:
    glyph = glyphData()

    glyph.numberOfContours = reader.ReadInt16()
    reader.SkipBytes(8)  # bbox

    if glyph.numberOfContours >= 0:
        return ReadSimpleGlyph(reader, glyph)
    else:
        return ReadCompoundGlyph(reader, glyph, indexToLocFormat, tables)


# Simple glyph

def ReadSimpleGlyph(reader: Reader, glyph: glyphData) -> glyphData:

    # Contours
    for _ in range(glyph.numberOfContours):
        glyph.endPtsOfContours.append(reader.ReadUInt16())

    # Instructions
    instructionLength = reader.ReadUInt16()
    reader.SkipBytes(instructionLength)

    glyph.numPoints = glyph.endPtsOfContours[-1] + 1 if glyph.endPtsOfContours else 0

    # Flags
    flags: list[int] = []
    i = 0

    while i < glyph.numPoints:
        flag = reader.ReadByte()[0]
        flags.append(flag)
        i += 1

        # repeat flag
        if flag & (1 << 3):
            repeatCount = reader.ReadByte()[0]
            for _ in range(min(repeatCount, glyph.numPoints - i)):
                flags.append(flag)
                i += 1

    # Coordinates
    xs, _ = ReadCoordinates(reader, flags, True)
    ys, onCurves = ReadCoordinates(reader, flags, False)

    for i in range(glyph.numPoints):
        glyph.points.append(point(xs[i], ys[i], onCurves[i]))

    return glyph

def ReadCoordinates(reader: Reader, flags: list[int], readingX: bool):
    coordinates = []
    onCurves = []

    current = 0

    sizeBit = 1 if readingX else 2
    sameBit = 4 if readingX else 5

    for flag in flags:
        onCurves.append(bool(flag & 1))

        if flag & (1 << sizeBit):
            val = reader.ReadByte()[0]
            if flag & (1 << sameBit):
                current += val
            else:
                current -= val
        else:
            if not (flag & (1 << sameBit)):
                current += reader.ReadInt16()
            # else: delta = 0

        coordinates.append(current)

    return coordinates, onCurves


# Compound glyph

def ReadCompoundGlyph(reader: Reader, glyph: glyphData, indexToLocFormat: int, tables: dict[str, table]) -> glyphData:

    allPoints: list[point] = []
    allEndPts: list[int] = []

    while True:
        component, isLast = ReadNextComponentGlyph(reader, indexToLocFormat, tables)

        offset = len(allPoints)

        allPoints.extend(component.points)

        for endPt in component.endPtsOfContours:
            allEndPts.append(endPt + offset)

        if isLast:
            break

    glyph.points = allPoints
    glyph.endPtsOfContours = allEndPts
    glyph.numPoints = len(allPoints)

    return glyph

def ReadNextComponentGlyph(reader: Reader, indexToLocFormat: int, tables: dict[str, table]):

    flags = reader.ReadUInt16()
    glyphIndex = reader.ReadUInt16()

    # Jump to component glyph
    currentPos = reader.file.tell()
    glyphLoc = GetGlyphLocation(reader, glyphIndex, indexToLocFormat, tables)

    reader.goto(glyphLoc)
    component = ReadGlyph(reader, indexToLocFormat, tables)
    reader.goto(currentPos)

    # Flags
    ARG_WORDS = 0
    ARGS_ARE_XY = 1
    MORE_COMPONENTS = 5

    if not (flags & (1 << ARGS_ARE_XY)):
        raise NotImplementedError("Point matching not supported")

    if flags & (1 << ARG_WORDS):
        dx = reader.ReadInt16()
        dy = reader.ReadInt16()
    else:
        dx = reader.ReadSByte()[0]
        dy = reader.ReadSByte()[0]

    # Scaling
    scaleX = 1.0
    scaleY = 1.0

    if flags & (1 << 3):
        scaleX = scaleY = reader.ReadFixedPoint2Dot14()
    elif flags & (1 << 6):
        scaleX = reader.ReadFixedPoint2Dot14()
        scaleY = reader.ReadFixedPoint2Dot14()
    elif flags & (1 << 7):
        raise NotImplementedError("2x2 transform not supported")

    # Transform
    for p in component.points:
        p.x = int(p.x * scaleX + dx)
        p.y = int(p.y * scaleY + dy)

    isLast = not (flags & (1 << MORE_COMPONENTS))

    return component, isLast


# Helpers

def GetGlyphLocation(reader: Reader, glyphIndex: int, indexToLocFormat: int, tables: dict[str, table]) -> int:
    locaStart = tables["loca"].offset
    glyfStart = tables["glyf"].offset

    if indexToLocFormat == 0:
        reader.goto(locaStart + glyphIndex * 2)
        offset = reader.ReadUInt16() * 2
    else:
        reader.goto(locaStart + glyphIndex * 4)
        offset = reader.ReadUInt32()

    return glyfStart + offset