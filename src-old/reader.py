from typing import Literal

class Reader:
    def __init__(self, fontPath: str):
        self.fontPath = fontPath
        self.file = open(fontPath, "rb")

        # Order of bits, depends on font format, TTF: Big
        self.endian: Literal["little", "big"] = "big"
    

    def SkipBytes(self, offset: int) -> None:
        """
        ### **Move relative to the current position by `offset` bytes**

        ---
        * `offset`: Number of bytes to move file head
        """

        self.file.seek(offset, 1)

    def goto(self, offset: int) -> None:
        """
        **Move relative to the start of the file by `offset` bytes**
    
        * `offset`: Number of bytes to move
        """

        self.file.seek(offset, 0)


    def ReadByte(self) -> bytes:
        data = self.file.read(1)
        return data
    
    def ReadInt16(self) -> int:
        """
        **Read Int16 from current position and move pointer forward 2 bytes**
        
        Throws **EOFError**: If there are not enough bytes left in the file
        """

        # Read 2 bytes
        data = self.file.read(2)

        # If data isnt 2 bytes long it got cut off because of the end of file
        if len(data) != 2:
            raise EOFError(f"readInt16(): Unexpected end of file, expected 2 bytes, got {len(data)}")

        return int.from_bytes(data, byteorder=self.endian, signed=True)

    def ReadUInt16(self) -> int:
        """
        **Read UInt16 from current position and move pointer forward 2 bytes**
        
        Throws **EOFError**: If there are not enough bytes left in the file
        """

        # Read 2 bytes
        data = self.file.read(2)

        # If data isnt 2 bytes long it got cut off because of the end of file
        if len(data) != 2:
            raise EOFError(f"readUInt16(): Unexpected end of file, expected 2 bytes, got {len(data)}")

        return int.from_bytes(data, byteorder=self.endian)

    def ReadUInt32(self) -> int:
        """
        **Read UInt32 from current position and move pointer forward 4 bytes**
        
        Throws **EOFError**: If there are not enough bytes left in the file
        """

        # Read 4 bytes
        data = self.file.read(4)

        # If data isnt 4 bytes long it got cut off because of the end of file
        if len(data) != 4:
            raise EOFError(f"readUInt32(): Unexpected end of file, expected 4 bytes, got {len(data)}")

        return int.from_bytes(data, byteorder=self.endian)

    def ReadStr32(self, encoding: str = "ascii") -> str:
        """
        **Read 4 byte string from the file and move pointer forward 4 bytes**

        Throws **EOFError**: If there are not enough bytes left in the file
        """

        # Read 4 bytes
        data = self.file.read(4)

        # If data isnt 4 bytes long it got cut off because of the end of file
        if len(data) != 4:
            raise EOFError(f"readStr32(): Unexpected end of file, expected 4 bytes, got {len(data)}")
        
        # Reverse bytes if file is big endian
        # NOTE: Temporarily changed to little endian because tags where backwards
        # Why are they already the right way round?
        if self.endian == "little":
            data = data[::-1]
        
        return data.decode(encoding)
    






