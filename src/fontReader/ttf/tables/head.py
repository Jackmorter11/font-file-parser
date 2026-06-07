"""
The 'head' table contains global information about the font

Functions to read 'head' table:

- readHeadTable(reader) -> HeadTable
"""

from dataclasses import dataclass
from datetime import datetime

from ...common.reader import Reader


@dataclass
class HeadTable:
    """
    Contains 'head' table enteries

    - version: Version of the head table, should always be 1.0
    - fontRevision: The font designer's version number for the font
    - _checkSumAdjustment: Checksum of whole file, used to verify integrity
    - _magicNumber: Always 0x5F0F3CF5
    - flags: Bit flags describing font properties NOTE: Add reference to bits
    - unitsPerEm: How many font units make up one em, used for scaling
    - created: When the font was created
    - modified: When the font was modified
    - xMin: Bounding box for all glyphs
    - yMin
    - xMax
    - yMax
    - macStyle: Bit flags for bold, italic, condensed, extended etc
    - lowestRecPPEM: Smallest readable pixel size untill the font becomes illegible
    - _fontDirectionHint: Deprecated since OpenType 1.4, always set to 2
    - _indexToLocFormat: Tells the parser whether the loca table uses short or long offsets
    - _glyphDataFormat: Always 0, reserved for future use
    """

    version             :float
    fontRevision        :float
    _checkSumAdjustment :int
    _magicNumber        :int
    flags               :int
    unitsPerEm          :int
    created             :datetime
    modified            :datetime
    xMin                :int
    yMin                :int
    xMax                :int
    yMax                :int
    macStyle            :int
    lowestRecPPEM       :int
    _fontDirectionHint  :int
    _indexToLocFormat   :int
    _glyphDataFormat    :int

    def __str__(self):
        """Human readable version of 'head' table"""

        lines = []
        lines.append("'head' table")
        lines.append("-----------------------------")
        lines.append(f"version            {self.version:>10}")
        lines.append(f"fontRevision       {round(self.fontRevision, 3):>10}")
        lines.append(f"checkSumAdjustment {self._checkSumAdjustment:>10}")
        lines.append(f"magicNumber        {f'{self._magicNumber:#010x}':>10}")
        lines.append(f"flags              {self.flags:>10}")
        lines.append(f"unitsPerEm         {self.unitsPerEm:>10}")
        lines.append(f"created            {self.created.strftime('%d/%m/%Y'):>10}")
        lines.append(f"modified           {self.modified.strftime('%d/%m/%Y'):>10}")
        lines.append(f"xMin               {self.xMin:>10}")
        lines.append(f"yMin               {self.yMin:>10}")
        lines.append(f"xMax               {self.xMax:>10}")
        lines.append(f"yMax               {self.yMax:>10}")
        lines.append(f"macStyle           {self.macStyle:>10}")
        lines.append(f"lowestRecPPEM      {self.lowestRecPPEM:>10}")
        lines.append(f"fontDirectionHint  {self._fontDirectionHint:>10}")
        lines.append(f"indexToLocFormat   {self._indexToLocFormat:>10}")
        lines.append(f"glyphDataFormat    {self._glyphDataFormat:>10}")
        return "\n".join(lines)


def readHeadTable(reader: Reader) -> HeadTable:
    """
    Reads the 'head' table

    The 'head' table contains global information about the font
    """

    version             = reader.ReadFixedPoint16Dot16()
    fontRevision        = reader.ReadFixedPoint16Dot16()
    _checkSumAdjustment = reader.ReadUInt32()
    _magicNumber        = reader.ReadUInt32()

    if _magicNumber != 0x5F0F3CF5:
        raise ValueError(f"Reading 'head' table - Invalid magic number: {_magicNumber:#010x}, expected 0x5f0f3cf5\n" +
              "            this could mean that there is an error in parsing")

    flags              = reader.ReadUInt16()
    unitsPerEm         = reader.ReadUInt16()
    created            = reader.ReadLongDateTime()
    modified           = reader.ReadLongDateTime()
    xMin               = reader.ReadFWord()
    yMin               = reader.ReadFWord()
    xMax               = reader.ReadFWord()
    yMax               = reader.ReadFWord()
    macStyle           = reader.ReadUInt16()
    lowestRecPPEM      = reader.ReadUInt16()
    _fontDirectionHint = reader.ReadInt16()
    _indexToLocFormat  = reader.ReadInt16()
    _glyphDataFormat   = reader.ReadInt16()

    return HeadTable(
        version             = version,
        fontRevision        = fontRevision,
        _checkSumAdjustment = _checkSumAdjustment,
        _magicNumber        = _magicNumber,
        flags               = flags,
        unitsPerEm          = unitsPerEm,
        created             = created,
        modified            = modified,
        xMin                = xMin,
        yMin                = yMin,
        xMax                = xMax,
        yMax                = yMax,
        macStyle            = macStyle,
        lowestRecPPEM       = lowestRecPPEM,
        _fontDirectionHint  = _fontDirectionHint,
        _indexToLocFormat   = _indexToLocFormat,
        _glyphDataFormat    = _glyphDataFormat
    )
