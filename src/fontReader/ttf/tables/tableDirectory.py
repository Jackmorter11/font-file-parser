from dataclasses import dataclass

from ...common.reader import Reader

@dataclass
class table:
    checkSum :int = 0
    offset   :int = 0
    length   :int = 0
    
def ReadTableDirectory(reader: Reader, numTables: int) -> dict[str, table]:
    """  
    ## Reads the Table Directory

    ---
    Which contains a list of the tables, each one of this form

    ```
    Type      Name        Description
    uint32    tag         4-byte identifier
    uint32    checkSum    checksum for this table
    uint32    offset      offset from beginning of sfnt
    uint32    length      length of this table in byte (actual length not padded length)
    ```
    """

    tables: dict[str, table] = {}

    # Iterate through every table
    for _ in range(numTables):
        tag:    str = reader.ReadStr32()
        tables[tag] = table()

        tables[tag].checkSum = reader.ReadUInt32()
        tables[tag].offset   = reader.ReadUInt32()
        tables[tag].length   = reader.ReadUInt32()

    return tables