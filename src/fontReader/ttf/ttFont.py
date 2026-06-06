from typing import Callable
import time

from ..common.reader import Reader
from ..common.logger import Logger

from .tables.offsetSubTable import ReadOffsetSubTable
from .tables.tableDirectory import readTableDirectory, Table
#from .tables import cmap, glyf, head, hhea, hmtx, loca, maxp, name, post
from .tables import cmap, glyf, head, maxp, name, loca


TABLE_REGISTRY: list[tuple[str, str, Callable, Callable]] = [
#     tag | self.name |              read function              | extra variables
    ("head", "head",   lambda r, _:  head.readHeadTable(r),       lambda s: {}),
    ("maxp", "maxp",   lambda r, _:  maxp.ReadMaxpTable(r),       lambda s: {}),
    ("name", "name",   lambda r, _:  name.readNameTable(r),       lambda s: {}),
    ("loca", "loca",   lambda r, kw: loca.readLocaTable(r, **kw), lambda s: {"indexToLocFormat": s.head._indexToLocFormat, "numGlyphs": s.maxp.numGlyphs}),
    ("cmap", "cmap",   lambda r, kw: cmap.ReadCmapTable(r, **kw), lambda s: {"tables": s._tables}),
    ("glyf", "glyphs", lambda r, kw: glyf.GlyfTable(r, **kw), lambda s: {"locaTable": s.loca})
]


class ParseTTF:
    # TODO: Does this overwrite the classes?
    # Set types for tables since they are loaded when available

    def __init__(self, fontPath: str, loggingEnabled: bool = False):
        self.maxp:   maxp.maxpTable
        self.head:   head.HeadTable
        self.glyphs: glyf.GlyfTable
        self.loca:   loca.LocaTable
        self.cmap:   cmap.cmapTable
        self.name:   name.NameTable


        self.fontPath = fontPath

        self.logger = Logger("logs/TTFParser.log", loggingEnabled=loggingEnabled)
        self.logger.timeLog(f"Font path: {self.fontPath}")

        self.reader = Reader(self.fontPath)
        self.logger.timeLog("Created reader object\n")


        self.offsetSubTable = ReadOffsetSubTable(self.reader)
        self.logger.timeLog("Read Sub Table")

        self.tableDirectory = readTableDirectory(self.reader, self.offsetSubTable.numTables)
        self._tables = self.tableDirectory.tables #TODO: Is it worth doing this?
        self.logger.timeLog("Read Table Directory\n")


        self.LoadTables()


        parsingTimems = int((time.time() - self.logger.startTime) * 1000)
        self.logger.log(f"Parsing Complete in {parsingTimems} ms\n")


    def LoadTables(self):
        implemented = {tag for tag, *_ in TABLE_REGISTRY}

        # Warn about tables in font that arnt implemented
        for tag in self._tables:
            if tag not in implemented:
                self.logger.log(f"TODO: Implement '{tag}' table")
        self.logger.blankLine()

        # Read each table in order from the font
        for tag, tableName, readTableFunction, extraArgs in TABLE_REGISTRY:
            if tag in self._tables:
                self.reader.goto(self._tables[tag].offset)

                setattr(self, tableName, readTableFunction(self.reader, extraArgs(self)))
                self.VerifyCheckSum(self._tables[tag])

                self.logger.timeLog(f"Read '{tag}' table")
        self.logger.blankLine()


    def VerifyCheckSum(self, table: Table):
        """
        Calculate the checksum of the given table,
        Compares it with set value

        ---
        If it isnt equal, throw
        """

        savedPos = self.reader.file.tell()
        self.reader.goto(table.offset)
        data = self.reader.file.read(table.length)
        self.reader.goto(savedPos)
        
        # head table: zero out checkSumAdjustment (bytes 8-11)
        if table.tag == "head" and table.length >= 12:
            data = data[:8] + b'\x00\x00\x00\x00' + data[12:]
        
        padded = data + b'\x00' * ((4 - len(data) % 4) % 4)
        total = 0
        for i in range(0, len(padded), 4):
            total += int.from_bytes(padded[i:i+4], byteorder=self.reader.endian)
        
        if (total & 0xFFFFFFFF) != table.checkSum:
            raise ValueError(f"{table.tag} table checksum mismatch, font possibly corrupted")


    def __str__(self) -> str:
        """Return info about font"""

        postScriptName = self.name.getName(6)
        version        = self.name.getName(5)
        description    = self.name.getName(10)
        trademark      = self.name.getName(7)
        fontCopyright  = self.name.getName(0)

        lines = []

        lines.append(f"{postScriptName} ({version})")
        lines.append(description)
        lines.append("")
        lines.append(f"Path: {self.fontPath}")
        lines.append("")
        lines.append(f"{trademark}")
        lines.append(f"{fontCopyright}")

        # Remove None values
        lines = [(line if line else '') for line in lines]

        return "\n".join(lines)
