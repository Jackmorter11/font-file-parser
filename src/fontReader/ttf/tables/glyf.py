"""
Funstions to read 'glyf' table:

- GlyphTable(): Class to interact with glyf table
- GlyphTable[glyphIndex]: Return glyph

NOTE: Currently, if reading compound glyph, _cache holds the components and then the combined and transformed glyph
"""

from dataclasses import dataclass, field

from ...common.reader import Reader
from .loca import LocaTable


@dataclass
class Point:
    """
    Holds data for a glyph point
    
    - x: x coordinate in font units
    - y: y coordinate in font units
    - onCurve: If the point is on or off the bezier
    """

    x: float = 0
    y: float = 0
    onCurve: bool = False

@dataclass
class Glyph:
    """
    Holds data for a glyph

    - numberOfContours: Number of contours in glyph
    - xMin: Minumum x cordinate (part of bounding box for glyph)
    - yMin: Minumum y cordinate (part of bounding box for glyph)
    - xMax: Maximum x cordinate (part of bounding box for glyph)
    - yMax: Maximum y cordinate (part of bounding box for glyph)
    - instructions: Byte array of instructions for glyph
    - flags: Byte array of flags for glyph (used for reading)
    - numPoints: Number of points in glyph
    - endPtsOfContours: Index of the last point in each contour
    - points: Flat list of points in glyph
    """

    numberOfContours: int = 0
    xMin: int = 0
    yMin: int = 0
    xMax: int = 0
    yMax: int = 0

    instructions: bytearray = field(default_factory=bytearray)
    flags:        bytearray = field(default_factory=bytearray)

    numPoints: int = 0

    endPtsOfContours:   list[int] = field(default_factory=list)
    points:           list[Point] = field(default_factory=list)

    def __str__(self):
        if not self.endPtsOfContours or not self.points:
            return "Glyph not loaded yet"

        string = ""
        startPoint = 0

        for endPoint in self.endPtsOfContours:
            contour = self.points[startPoint:endPoint + 1]
            contour.append(self.points[startPoint])  # close contour

            string += ", ".join(f"({p.x}, {p.y})" for p in contour) + "\n"
            startPoint = endPoint + 1

        return string

class GlyfTable:
    """
    Holds data for 'glyf' table:

    - _reader: Reader reference (to load glyphs on demand)
    - _locaTable: Loca table reference (to load glyphs on demand)
    - _glyfOffset: File offset of glyf table
    - _cache: Dict of loaded glyphs (glyphIndex -> Glyph)
    """

    def __init__(self, reader: Reader, locaTable: LocaTable):
        self._reader:          Reader = reader
        self._locaTable:    LocaTable = locaTable

        self._glyfOffset:         int = self._reader.file.tell()
        self._cache: dict[int, Glyph] = {} # Glyph index -> Glyph

    # Allow list indexing: 'font.glyphs[i]'
    def __getitem__(self, glyphIndex: int) -> Glyph:
        #if index not in self._cache:
        #    self._reader.goto(self._locaTable.offsets[index] + self._glyfOffset)
        #    self._cache[index] = self.readGlyph()

        return self.readGlyph(glyphIndex)

    def __len__(self):
        return len(self._cache)


    def readGlyph(self, glyphIndex: int) -> Glyph:
        """
        Read and return a Glyph based on glyphIndex, add to cache

        If the glyph is in cache it just returns that
        """

        if glyphIndex in self._cache:
            return self._cache[glyphIndex]

        self._reader.goto(self._locaTable.offsets[glyphIndex] + self._glyfOffset)

        glyph = Glyph()

        glyph.numberOfContours = self._reader.ReadInt16()

        glyph.xMin = self._reader.ReadInt16()
        glyph.yMin = self._reader.ReadInt16()
        glyph.xMax = self._reader.ReadInt16()
        glyph.yMax = self._reader.ReadInt16()

        if glyph.numberOfContours >= 0:
            self._cache[glyphIndex] = self.readSimpleGlyph(glyph)
        else:
            self._cache[glyphIndex] = self.readCompoundGlyph(glyph)

        return self._cache[glyphIndex]


    def readSimpleGlyph(self, glyph: Glyph) -> Glyph:
        """
        Called by readGlyph(), reads the rest of a simple glyph
        """

        # Read contours (each represented by the end point of the contour)
        for _ in range(glyph.numberOfContours):
            glyph.endPtsOfContours.append(self._reader.ReadUInt16())

        # Read instructions, TODO: Problem, bytearray has extra entrys, isnt cleared?
        instructionLength = self._reader.ReadUInt16()
        for _ in range(instructionLength):
            glyph.instructions.append(self._reader.ReadByte())

        # Number of points in glyph based on last point of last contour
        glyph.numPoints = glyph.endPtsOfContours[-1] + 1 if glyph.endPtsOfContours else 0

        # Read flags (1 byte for each point)
        i = 0
        while i < glyph.numPoints:
            flag = self._reader.ReadByte()
            glyph.flags.append(flag)
            i += 1

            # Repeat flag
            if flag & (1 << 3):
                repeatCount = self._reader.ReadByte()
                for _ in range(min(repeatCount, glyph.numPoints - i)):
                    glyph.flags.append(flag)
                    i += 1

        # Read coordinates
        xs, _ = self.readCoordinates(glyph.flags, True)
        ys, onCurves = self.readCoordinates(glyph.flags, False)
        for i in range(glyph.numPoints):
            glyph.points.append(Point(xs[i], ys[i], onCurves[i]))

        return glyph

    def readCoordinates(self, flags, readingX) -> tuple[list[int], list[bool]]:
        """
        Called by readGlyph() -> readSimpleGlyph()

        Reads cordinates for a simple glyph
        """

        coordinates = []
        onCurves = []

        current = 0

        xShort = 1 if readingX else 2
        sameBit = 4 if readingX else 5

        for flag in flags:
            # flag[0] == 1: Point onCurve
            onCurves.append(bool(flag & 1))

            # flag[1/2] == 1: Coorinate is 1 byte long
            if flag & (1 << xShort):
                val = self._reader.ReadByte()
                # flag[4/5] == 1: Positive coordinate
                if flag & (1 << sameBit):
                    current += val
                # flag[4/5] == 0: Negative coordainte
                else:
                    current -= val

            # flag[1/2] == 0: Coordinate is 2 bytes long
            else:
                # flag[4/5] == 0: Change in coordainte
                if not flag & (1 << sameBit):
                    current += self._reader.ReadInt16()
                # flag[4/5] == 1: No change

            coordinates.append(current)

        return coordinates, onCurves


    def readCompoundGlyph(self, glyph) -> Glyph:
        """
        Called by readGlyph(), reads the rest of a compound glyph

        Compresses all compenents into a single glyph
        
        NOTE: I should change this to cache components
        """

        allPoints: list[Point] = []
        allEndPts: list[int] = []

        while True:
            component, isLast = self.readNextComponentGlyph()

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

    def readNextComponentGlyph(self):
        """
        Called by readGlyph() -> ReadCompoundGlyph()

        Reads a component of a compound glyph and transforms it
        """

        flags = self._reader.ReadUInt16()
        glyphIndex = self._reader.ReadUInt16()

        # Jump to component glyph
        currentPos = self._reader.file.tell()
        component = self.readGlyph(glyphIndex)
        self._reader.goto(currentPos)

        # Flags
        argWords = 0
        argsAreXY = 1
        moreComponents = 5

        if not flags & (1 << argsAreXY):
            raise NotImplementedError("Point matching not supported")

        if flags & (1 << argWords):
            dx = self._reader.ReadInt16()
            dy = self._reader.ReadInt16()
        else:
            dx = self._reader.ReadSByte()
            dy = self._reader.ReadSByte()

        # NOTE: Perfect transform

        # Scaling
        scaleX = 1.0
        scaleY = 1.0

        if flags & (1 << 3):
            scaleX = scaleY = self._reader.ReadFixedPoint2Dot14()
        elif flags & (1 << 6):
            scaleX = self._reader.ReadFixedPoint2Dot14()
            scaleY = self._reader.ReadFixedPoint2Dot14()
        elif flags & (1 << 7):
            raise NotImplementedError("2x2 transform not supported")

        # Transform
        for p in component.points:
            p.x = int(p.x * scaleX + dx)
            p.y = int(p.y * scaleY + dy)

        isLast = not flags & (1 << moreComponents)

        return component, isLast
