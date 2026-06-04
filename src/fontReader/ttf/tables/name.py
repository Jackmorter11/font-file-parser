"""
Functions to read 'name' table:

- readNameTable(reader)
- NameTable.getName(nameID)
- NameTable.getRecords()
- NameTable.getCustomRecords()
- NameTable.getLangTag(languageID)
"""

from dataclasses import dataclass, field

from ...common.reader import Reader


NAME_ID_LABELS = {
    0:  "Copyright",
    1:  "Family",
    2:  "Subfamily",
    3:  "Unique ID",
    4:  "Full Name",
    5:  "Version",
    6:  "PostScript Name",
    7:  "Trademark",
    8:  "Manufacturer",
    9:  "Designer",
    10: "Description",
    11: "Vendor URL",
    12: "Designer URL",
    13: "License",
    14: "License URL",
#   15:  Reserved
    16: "Typographic Family",
    17: "Typographic Subfamily",
    18: "Compatible Full Name",
    19: "Sample Text"
#NOTE: 20-25 not listed, they take up too much space when printed and arnt used as much
#      If I find a need I should implement them
}


@dataclass
class _LangTagRecord:
    """
    Holds a language tag record (format 1 only)
    
    - length: Length (in bytes) of the language tag string
    - offset: Offset (in bytes) from start of shared string storage
    """

    length :int
    offset :int

@dataclass
class _NameRecord:
    """
    Holds a name record including metadata for the string and where to find it

    - platformID: Which platform the string is intended for (0 - Unicode, 1 - Mac, 3 - Windows)
    - platformSpecificID: Refines the platform (encoding depends on platformID)
    - languageID: What language the string is in (encoding depends on platformID)
    - nameID: What the string represents e.g. 0 - Copyright
    - length: The size (in bytes) of the string in shared string storage (at the end of table)
    - offset: Offset (in bytes) from the start of shared string storage (at the end of table)
    """

    platformID         :int
    platformSpecificID :int
    languageID         :int
    nameID             :int
    length             :int
    offset             :int

@dataclass
class NameTable:
    """
    Holds data for 'name' table

    - format: Verison of the 'name' table \
        (format 1 extends 0 by adding support for custom language tag records)
    - count: How many name records there are in the table
    - _stringOffset: Offset (in bytes) to start of shared string storage
    - _records: List of name records (each linking to a part of shared string storage)
    - _strings: A dict representing the shared string storage - \
        (nameID, platformID, languageID) -> string
    - _langTags: List of custom language tags (only for format 1)
    """

    format        :int
    count         :int
    _stringOffset :int
    _records      :list[_NameRecord]               = field(default_factory=list)
    _strings      :dict[tuple[int, int, int], str] = field(default_factory=dict)
    _langTags     :list[str]                       = field(default_factory=list)

    def __str__(self) -> str:
        """Human readable version of 'name' table"""

        lines = []
        lines.append(f"Name Table (format {self.format})")
        lines.append("-" * len(lines[-1]))

        seen = set()
        for nameID, label in NAME_ID_LABELS.items():
            value = self.getName(nameID)
            if value:
                lines.append(f"{label:<20} {value}")
                seen.add(nameID)

        # Any nameIDs not in records
        for (nameID, platformID, _), value in self._strings.items():
            if nameID not in seen and platformID == 3:
                lines.append(f"nameID {nameID:<13} {value}")
                seen.add(nameID)

        return "\n".join(lines)


    def getName(self, nameID: int) -> str | None:
        """
        Get a string by nameID (e.g. 0 for Copyright)
        
        Preferring Windows UTF-16 BE (platformID 3),
        falling back to Mac Roman (platformID 1)

        nameID Reference:
        - 0:  "Copyright"
        - 1:  "Family"
        - 2:  "Subfamily"
        - 3:  "Unique ID"
        - 4:  "Full Name"
        - 5:  "Version"
        - 6:  "PostScript Name"
        - 7:  "Trademark"
        - 8:  "Manufacturer"
        - 9:  "Designer"
        - 10: "Description"
        - 11: "Vendor URL"
        - 12: "Designer URL"
        - 13: "License"
        - 14: "License URL"
        - 16: "Typographic Family"
        - 17: "Typographic Subfamily"
        - 18: "Compatible Full Name"
        - 19: "Sample Text"
        """

        # Prefer Windows English
        result = self._strings.get((nameID, 3, 0x0409))
        if result:
            return result

        # Fall back to any Windows entry for this nameID
        for (nid, pid, _), value in self._strings.items():
            if nid == nameID and pid == 3:
                return value

        # Fall back to Mac
        for (nid, pid, _), value in self._strings.items():
            if nid == nameID and pid == 1:
                return value

        return None

    def getRecords(self) -> list[_NameRecord]:
        """
        Returns all records as
        
        list[NameRecord(platformID, platformSpecificID, languageID, nameID, length, offset)]

        Use getName(record.nameID) to get the decoded string for each record
        """

        return self._records

    def getCustomRecords(self) -> list[_NameRecord]:
        """
        Returns all records with a nameID >= 256 (font specific custom names) as

        list[NameRecord(platformID, platformSpecificID, languageID, nameID, length, offset)]

        Use getName(record.nameID) to get the decoded string for each record
        """

        return [record for record in self._records if record.nameID >= 256]

    def getLangTag(self, languageID: int) -> str | None:
        """
        Get a BCP 47 language tag string by languageID (format 1 only)

        Language IDs for format 1 lang tags start at 0x8000,
        e.g. 0x8000 -> langTags[0], 0x8001 -> langTags[1]

        Returns None if not format 1 or languageID is out of range
        """

        index = languageID - 0x8000
        if index < 0 or index >= len(self._langTags):
            return None

        return self._langTags[index]


def readNameTable(reader: Reader):
    """
    Reads the 'name' table
    
    The 'name' table contains human-readable names for features and settings,
    copyright notices, font names, style names, and other information
    """

    tableStart = reader.file.tell()

    nameFormat   = reader.ReadUInt16()
    count        = reader.ReadUInt16()
    stringOffset = reader.ReadUInt16()
    records      = []
    strings      = {}

    if nameFormat not in (0, 1):
        raise ValueError(f"Reading 'name' table - Unknown format: {nameFormat}, should be 0 or 1")

    # Read all name records
    for _ in range(count):
        records.append(_NameRecord(
            platformID         = reader.ReadUInt16(),
            platformSpecificID = reader.ReadUInt16(),
            languageID         = reader.ReadUInt16(),
            nameID             = reader.ReadUInt16(),
            length             = reader.ReadUInt16(),
            offset             = reader.ReadUInt16(),
        ))

    # Format 1: read language tag records
    langTagRecords = []
    langTags       = []
    if nameFormat == 1:
        langTagCount = reader.ReadUInt16()
        for _ in range(langTagCount):
            langTagRecords.append(_LangTagRecord(
                length = reader.ReadUInt16(),
                offset = reader.ReadUInt16(),
            ))

    # Resolve each record's string
    for record in records:
        stringPos = tableStart + stringOffset + record.offset
        reader.goto(stringPos)
        raw = reader.file.read(record.length)

        try:
            if record.platformID == 3:
                # Windows: UTF-16 BE
                text = raw.decode("utf-16-be")

            elif record.platformID == 1:
                # Mac: Mac Roman
                text = raw.decode("mac-roman")

            else:
                # Unicode platform: usually UTF-16 BE
                text = raw.decode("utf-16-be")

        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")

        strings[(record.nameID, record.platformID, record.languageID)] = text

    # Resolve language tag strings (format 1 only)
    for langTagRecord in langTagRecords:
        stringPos = tableStart + stringOffset + langTagRecord.offset
        reader.goto(stringPos)
        raw = reader.file.read(langTagRecord.length)
        langTags.append(raw.decode("utf-16-be"))

    return NameTable(
        format        = nameFormat,
        count         = count,
        _stringOffset = stringOffset,
        _records      = records,
        _strings      = strings,
        _langTags     = langTags,
    )
