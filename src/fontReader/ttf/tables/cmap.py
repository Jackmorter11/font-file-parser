from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class cmap:
    mappings: dict[str, int] = None

    reserved                          :int = None 
    subtableByteLengthIncludingHeader :int = None
    languageCode                      :int = None
    numGroups                         :int = None


    def CharToGlyphIndex(self, char):
        charCode = ord(char)
        return self.mappings[charCode]

def ReadCmapTable(reader: Reader) -> cmap:

    version = reader.ReadUInt16()
    numSubtables = reader.ReadUInt16() # Font can contain multiple charicter maps for different platforms

    # Read through metadata for each charicter map to find the one we want to use
    cmapSubtableOffset = 0xFFFFFFFF # Hopefuly equivilant to uint.MaxValue in C

    for _ in range(numSubtables):
        platformID = reader.ReadUInt16()
        platformSpecificID = reader.ReadUInt16()
        offset = reader.ReadUInt32()
 
        # PlatformID of 0 means Unicode, in which case platformSpecificID can be interpreted as Unicode version
        if platformID == 0:
            unicodeVersionInfo = platformSpecificID
 
            # Unicode 2.0 or later semantics (non-BMP charicters allowed)
            if unicodeVersionInfo == 4:
                cmapSubtableOffset = offset
 
            # Unicode 2.0 or later semantics (BMP only)
            if unicodeVersionInfo == 3 and cmapSubtableOffset == 0xFFFFFFFF:
                cmapSubtableOffset = offset
    
    if cmapSubtableOffset == 0:
        raise NotImplementedError("TODO: Font does not contain supported charicter map type")
    
    
    
    reader.goto(tables["cmap"]["offset"] + cmapSubtableOffset)
    format = reader.ReadUInt16()

    if format == 12:
        ReadCmapFormat12()
    
    else:
        raise NotImplementedError(f"TODO: Cmap format {format} not supported")
    
def ReadCmapFormat12(reader: Reader) -> dict[str, int]:
    """"""

    table: cmap = cmap()

    table.reserved = reader.ReadUInt16() # Set to 0
    table.subtableByteLengthIncludingHeader = reader.ReadUInt32()
    table.languageCode = reader.ReadUInt32() # Set to 0
    table.numGroups = reader.ReadUInt32()

    for _ in range(table.numGroups):
        startCharCode = reader.ReadUInt32()
        endCharCode = reader.ReadUInt32()
        startGlyphIndex = reader.ReadUInt32()

        numChars = endCharCode - startCharCode + 1

        for charCodeOffset in range(numChars):
            charCode = startCharCode + charCodeOffset
            glyphIndex = startGlyphIndex + charCodeOffset

            mappings[charCode] = glyphIndex
    
    return table