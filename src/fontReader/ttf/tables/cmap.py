from dataclasses import dataclass, field

from ...common.reader import Reader
from .tableDirectory import table

@dataclass
class cmapTable:
    mappings: dict[int, int] = field(default_factory=dict)

    reserved:                          int = 0 
    subtableByteLengthIncludingHeader: int = 0
    languageCode:                      int = 0
    numGroups:                         int = 0


    def CharToGlyphIndex(self, char: str) -> int:
        if len(char) != 1:
            raise ValueError(f"Expected string of length 1, not {len(char)}")
        
        # Unicode value of character
        charCode = ord(char)
        return self.mappings.get(charCode, 0)


def ReadCmapTable(reader: Reader, tables: dict[str, table]) -> cmapTable:
    cmapTableOffset: int = tables["cmap"].offset
    reader.goto(cmapTableOffset)

    version:      int = reader.ReadUInt16()
    numSubtables: int = reader.ReadUInt16()

    subtables: list[tuple[int, int, int]] = []

    # Collect all subtables
    for _ in range(numSubtables):
        platformID: int = reader.ReadUInt16()
        encodingID: int = reader.ReadUInt16()
        offset:     int = reader.ReadUInt32()

        subtables.append((platformID, encodingID, offset))

    bestOffset: int = -1 #None
    bestFormat: int = -1 #None
    bestScore:  int = -1

    # Evaluate all subtables
    for platformID, encodingID, offset in subtables:
        reader.goto(cmapTableOffset + offset)
        format: int = reader.ReadUInt16()
        score:  int = -1

        # Prefer full Unicode (format 12)
        if format == 12:
            if platformID == 0: score = 400
            elif platformID == 3 and encodingID == 10: score = 390
            else: score = 300

        # Fallback to BMP (format 4)
        elif format == 4:
            if platformID == 3 and encodingID == 1: score = 200
            elif platformID == 0: score = 190
            else: score = 100

        if score > bestScore:
            bestScore = score
            bestOffset = offset
            bestFormat = format

    if bestOffset is None or bestFormat is None:
        raise NotImplementedError("No supported cmap subtable found")

    # Jump to best subtable
    reader.goto(cmapTableOffset + bestOffset)

    if bestFormat == 12:
        return ReadCmapFormat12(reader)
    elif bestFormat == 4:
        return ReadCmapFormat4(reader)
    else:
        raise NotImplementedError(f"Cmap format {bestFormat} not implemented")


def ReadCmapFormat12(reader: Reader) -> cmapTable:
    format: int = reader.ReadUInt16()

    table: cmapTable = cmapTable()
    table.reserved                          = reader.ReadUInt16() # Set to 0
    table.subtableByteLengthIncludingHeader = reader.ReadUInt32()
    table.languageCode                      = reader.ReadUInt32() # Set to 0
    table.numGroups                         = reader.ReadUInt32()

    for _ in range(table.numGroups):
        startCharCode   = reader.ReadUInt32()
        endCharCode     = reader.ReadUInt32()
        startGlyphIndex = reader.ReadUInt32()

        numChars = endCharCode - startCharCode + 1

        for charCodeOffset in range(numChars): 
            charCode   = startCharCode   + charCodeOffset
            glyphIndex = startGlyphIndex + charCodeOffset

            table.mappings[charCode] = glyphIndex
    
    return table

def ReadCmapFormat4(reader: Reader) -> cmapTable:
    format = reader.ReadUInt16()

    length   = reader.ReadUInt16()
    language = reader.ReadUInt16()

    segCountX2 = reader.ReadUInt16()
    segCount   = segCountX2 // 2

    searchRange   = reader.ReadUInt16()
    entrySelector = reader.ReadUInt16()
    rangeShift    = reader.ReadUInt16()

    # Arrays
    endCode     = [reader.ReadUInt16() for _ in range(segCount)]
    reservedPad =  reader.ReadUInt16()
    startCode   = [reader.ReadUInt16() for _ in range(segCount)]
    idDelta     = [reader.ReadInt16()  for _ in range(segCount)]

    # Record position of idRangeOffset array start
    idRangeOffsetStart = reader.file.tell()
    idRangeOffset       = [reader.ReadUInt16() for _ in range(segCount)]

    # glyphIdArray starts here
    glyphArrayStart = reader.file.tell()

    result = cmapTable(
        reserved=reservedPad,
        subtableByteLengthIncludingHeader=length,
        languageCode=language,
        numGroups=segCount
    )

    # Build mappings
    for i in range(segCount):
        start = startCode[i]
        end = endCode[i]
        delta = idDelta[i]
        range_offset = idRangeOffset[i]

        for codepoint in range(start, end + 1):
            if codepoint == 0xFFFF:
                continue  # end-of-table marker segment

            if range_offset == 0:
                glyphID = (codepoint + delta) & 0xFFFF
            else:
                # Compute position inside glyphIdArray
                offset = (idRangeOffsetStart + (2 * i) + range_offset + 2 * (codepoint - start))
                currentPos = reader.file.tell()

                reader.goto(offset)
                glyphID = reader.ReadUInt16()
                reader.goto(currentPos)

                if glyphID != 0:
                    glyphID = (glyphID + delta) & 0xFFFF

            if glyphID != 0:
                result.mappings[codepoint] = glyphID

    return result