"""
Functions to read 'table directory':

- readTableDirectory(reader, numTables)
"""

from dataclasses import dataclass

from ...common.reader import Reader


@dataclass
class Table:
    """
    Holds data for a table

    - **tag**: 4-byte identifier of the table
    - **checkSum**: Checksum for the table, to check integrity
    - **offset**: Offset (in bytes) from begginning of file
    - **length**: Length (in bytes) of the table
    """

    tag      :str
    checkSum :int
    offset   :int
    length   :int

@dataclass
class TableDirectory:
    """
    List of table enteries in font
    """

    tables: dict[str, Table]

    def __str__(self) -> str:
        """Human readable version of 'table directory'"""

        lines = []
        lines.append("Table Directory")
        lines.append("-" * 43)
        lines.append(" tag     checkSum       offset       length")

        for table in self.tables.values():
            lines.append(f"{table.tag}   {table.checkSum:>10}   {table.offset:>10}   {table.length:>10}")

        return "\n".join(lines)


def readTableDirectory(reader: Reader, numTables: int) -> TableDirectory:
    """  
    Reads the 'table directory'

    The table directory contains a list of the table tags, checksum, offset and length
    """

    tables: dict[str, Table] = {}

    # Iterate through every table
    for _ in range(numTables):
        tag = reader.ReadStr32()

        tables[tag] = Table(
            tag      = tag,
            checkSum = reader.ReadUInt32(),
            offset   = reader.ReadUInt32(),
            length   = reader.ReadUInt32()
        )

    return TableDirectory(tables)
