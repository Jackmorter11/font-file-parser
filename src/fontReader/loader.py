from pathlib import Path

from .ttf.ttFont import ParseTTF
#from .common.font import Font - Might use for better types from ParseFont()

def ParseFont(fontPath: str, loggingEnabled: bool = False):
    ext = Path(fontPath).suffix.lower()

    if ext == ".ttf":
        return ParseTTF(fontPath, loggingEnabled=loggingEnabled)

    else:
        try:
            raise NotImplementedError(f"File type {ext} not supported yet")
        
        except NotImplementedError as e:
            # Display error in red
            print(f"\033[91m{e}\033[0m")