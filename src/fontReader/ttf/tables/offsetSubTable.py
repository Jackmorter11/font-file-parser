"""
The offsetSubTable keeps record of the tables in the font and provides
offset information to access each table in the directory

Functions to read the offset subtable

- readOffsetSubTable() -> OffsetSubTable
"""

from dataclasses import dataclass

from ...common.reader import Reader


@dataclass
class OffsetSubTable:
    """
    Contains offset subtable enteries
    """

    scalerType    :int = 0 # A tag to indicate the OFA scaler to be used to rasterize this font
    numTables     :int = 0 # Number of tables
    searchRange   :int = 0 # (maximum power of 2 <= numTables) * 16
    entrySelector :int = 0 # log2(maximum power of 2 <= numTables)
    rangeShift    :int = 0 # numTables * 16 - searchRange

    def __str__(self) -> str:
        """Human readable version of 'offset subtable'"""

        lines = []
        lines.append("offset subtable")
        lines.append( "------------------------")
        lines.append(f"scalerType    {self.scalerType:>10}")
        lines.append(f"numTables     {self.numTables:>10}")
        lines.append(f"searchRange   {self.searchRange:>10}")
        lines.append(f"entrySelector {self.entrySelector:>10}")
        lines.append(f"rangeShift    {self.rangeShift:>10}")
        return "\n".join(lines)


def readOffsetSubTable(reader: Reader) -> OffsetSubTable:
    """
    Reads the offsetSubTable

    The offsetSubTable keeps record of the tables in the font and provides
    offset information to access each table in the directory
    """

    table: OffsetSubTable = OffsetSubTable(
        scalerType    = reader.ReadUInt32(),
        numTables     = reader.ReadUInt16(),
        searchRange   = reader.ReadUInt16(),
        entrySelector = reader.ReadUInt16(),
        rangeShift    = reader.ReadUInt16()
    )

    return table
