from ..common.reader import Reader
from ..common.glyph  import Glyph
from ..common.logger import Logger

from .tables.offsetSubTable import offsetSubTable, ReadOffsetSubTable
from .tables.tableDirectory import table         , ReadTableDirectory
from .tables.glyf import glyphData, ReadGlyfTable
from .tables.maxp import maxp,      ReadMaxpTable
from .tables.head import head,      ReadHeadTable
from .tables.cmap import cmap,      ReadCmapTable

class ParseTTF:
    def __init__(self, fontPath: str, loggingEnabled: bool = False):
        self.fontPath = fontPath

        self.logger = Logger("logs/TTFParser.log", loggingEnabled=loggingEnabled)
        self.logger.log(f"Font path: {self.fontPath}")

        self.reader = Reader(self.fontPath)
        self.logger.log("Created reader object\n")


        self.offsetSubTable: offsetSubTable = ReadOffsetSubTable(self.reader)
        self.logger.log("Read Sub Table")

        self.tables: dict[str, table] = ReadTableDirectory(self.reader, self.offsetSubTable.numTables)
        self.logger.log("Read Table Directory\n")
    

        self.reader.goto(self.tables['maxp'].offset)
        self.maxp: maxp = ReadMaxpTable(self.reader)
        self.logger.log("Read 'maxp' table")

        self.reader.goto(self.tables["head"].offset)
        self.head: head = ReadHeadTable(self.reader)
        self.logger.log("Read 'head' table")

        self.reader.goto(self.tables["glyf"].offset)
        self.glyphs: list[glyphData] = ReadGlyfTable(self.reader, self.head.indexToLocFormat, self.tables, self.maxp.numGlyphs)
        self.logger.log("Read 'glyf' Table")

        self.reader.goto(self.tables["cmap"].offset)
        self.cmap: cmap = ReadCmapTable(self.reader, self.tables)
        self.logger.log("Read 'cmap' table")
        



    def __str__(self):
        string = f"True Type Font object... TODO: Name this"
        return string
