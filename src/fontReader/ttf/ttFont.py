from ..common.reader import Reader
from ..common.glyph  import Glyph
from ..common.logger import Logger

from .tables.offsetSubTable import offsetSubTable, ReadOffsetSubTable
from .tables.tableDirectory import tableDirectory, ReadTableDirectory
from .tables.maxp import maxp,  ReadMaxpTable
from .tables.head import head,  ReadHeadTable
from .tables.glyf import glyph, ReadGlyfTable
#from .tables.cmap import cmap, ReadCmapTable

class ParseTTF:
    def __init__(self, fontPath: str, loggingEnabled: bool = False):
        self.fontPath = fontPath

        self.reader = Reader(fontPath)
        self.logger = Logger("logs/TTFParser.log", loggingEnabled=True)
        
        self.logger.log("Created reader object\n")
        self.reader = Reader(self.fontPath)

        self.offsetSubTable: offsetSubTable = ReadOffsetSubTable(self.reader)
        self.logger.log("Read Sub Table")

        self.tables: dict[str, tableDirectory] = ReadTableDirectory(self.reader, self.offsetSubTable.numTables)
        self.logger.log("Read Table Directory\n")
    
        self.reader.goto(self.tables['maxp'].offset)
        self.maxp: maxp = ReadMaxpTable(self.reader)
        self.logger.log("Read 'maxp' table")

        self.reader.goto(self.tables["head"].offset)
        self.head: head = ReadHeadTable(self.reader)
        self.logger.log("Read 'head' table")

        self.reader.goto(self.tables["glyf"].offset)
        self.glyphs: list[glyph] = ReadGlyfTable(self.reader, self.head.indexToLocFormat, self.tables, self.maxp.numGlyphs)
        self.logger.log("Read 'glyf' Table")

        #self.reader.goto(self.tables["cmap"].offset)
        #self.cmap: cmap = ReadCmapTable(self.reader)
        #self.log("Read 'cmap' table")
        



    def __str__(self):
        string = f"True Type Font object..."
        return string
