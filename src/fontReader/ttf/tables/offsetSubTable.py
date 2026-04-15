from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class offsetSubTable:
    scalerType    :int = 0
    numTables     :int = 0
    searchRange   :int = 0
    entrySelector :int = 0
    rangeShift    :int = 0

def ReadOffsetSubTable(reader: Reader) -> offsetSubTable:
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

    table: offsetSubTable = offsetSubTable()

    table.scalerType    = reader.ReadUInt32()
    table.numTables     = reader.ReadUInt16()
    table.searchRange   = reader.ReadUInt16()
    table.entrySelector = reader.ReadUInt16()
    table.rangeShift    = reader.ReadUInt16()

    return table