from typing import Callable
import time
import struct

from ..common.reader import Reader
from ..common.logger import Logger

from .tables.offsetSubTable import readOffsetSubTable
from .tables.tableDirectory import readTableDirectory, Table
#from .tables import cmap, glyf, head, hhea, hmtx, loca, maxp, name, post
from .tables import cmap, glyf, head, maxp, name, loca


TABLE_REGISTRY: list[tuple[str, str, Callable, Callable]] = [
#     tag | self.name |              read function              | extra variables
    ("head", "head",   lambda r, _:  head.readHeadTable(r),       lambda s: {}),
    ("maxp", "maxp",   lambda r, _:  maxp.readMaxpTable(r),       lambda s: {}),
    ("name", "name",   lambda r, _:  name.readNameTable(r),       lambda s: {}),
    ("loca", "loca",   lambda r, kw: loca.readLocaTable(r, **kw), lambda s: {"indexToLocFormat": s.head.indexToLocFormat, "numGlyphs": s.maxp.numGlyphs}),
    ("cmap", "cmap",   lambda r, kw: cmap.readCmapTable(r, **kw), lambda s: {"tables": s.tables}),
    ("glyf", "glyphs", lambda r, kw: glyf.GlyfTable(r, **kw), lambda s: {"locaTable": s.loca})
]


class ParseTTF:
    def __init__(self, fontPath: str, loggingEnabled: bool = False):
        # TODO: Does this overwrite the classes?
        # Set types for tables since they are loaded when available
        self.maxp:   maxp.MaxpTable
        self.head:   head.HeadTable
        self.glyphs: glyf.GlyfTable
        self.loca:   loca.LocaTable
        self.cmap:   cmap.CmapTable
        self.name:   name.NameTable


        self.fontPath = fontPath

        self.logger = Logger("logs/TTFParser.log", loggingEnabled=loggingEnabled)
        self.logger.timeLog(f"Font path: {self.fontPath}")

        self.reader = Reader(self.fontPath)
        self.logger.timeLog("Created reader object\n")


        self.offsetSubTable = readOffsetSubTable(self.reader)
        self.logger.timeLog("Read Sub Table")

        self.tables = readTableDirectory(self.reader, self.offsetSubTable.numTables)
        self.logger.timeLog("Read Table Directory\n")


        self.loadTables()


        parsingTimems = int((time.time() - self.logger.startTime) * 1000)
        self.logger.log(f"Parsing Complete in {parsingTimems} ms\n")


    def loadTables(self):
        implemented = {tag for tag, *_ in TABLE_REGISTRY}

        # Warn about tables in font that arnt implemented
        for tag in self.tables.tags():
            if tag not in implemented:
                self.logger.log(f"TODO: Implement '{tag}' table")
        self.logger.blankLine()

        # Read each table in order from the font
        for tag, tableName, readTableFunction, extraArgs in TABLE_REGISTRY:
            if tag in self.tables.tags():
                self.reader.goto(self.tables[tag].offset)

                setattr(self, tableName, readTableFunction(self.reader, extraArgs(self)))
                self.verifyCheckSum(self.tables[tag])

                self.logger.timeLog(f"Read '{tag}' table")
        self.logger.blankLine()


    def verifyCheckSum(self, table: Table):
        """
        Calculate the checksum of the given table,
        Compares it with set value
    
        If it isnt equal, throw error
        """

        savedPos = self.reader.file.tell()
        self.reader.goto(table.offset)
        data = self.reader.file.read(table.length)
        self.reader.goto(savedPos)

        # head table: zero out checkSumAdjustment (bytes 8-11)
        if table.tag == "head" and table.length >= 12:
            data = data[:8] + b'\x00\x00\x00\x00' + data[12:]

        padded = data + b'\x00' * ((4 - len(data) % 4) % 4)

        # Determine the struct format string based on endianness ('>' for big, '<' for little)
        # TTF standard is big endian ('>'), 'I' means Unsigned 32-bit Int
        endianFlag = ">" if self.reader.endian == "big" else "<"

        # Calculate how many 4-byte integers are in the padded data
        numIntegers = len(padded) // 4
        fmt = f"{endianFlag}{numIntegers}I"

        # Unpack the entire table into a Python tuple of numbers
        total = sum(struct.unpack(fmt, padded))

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
