import struct
from enum import Enum

from .iconbank import IconBank
from .sourcecode import SourceCode
from .spritebank import SpriteBank


class amosFile:

    # Valid headers
    HEADERS = [
        "AMOS Pro101V\0\0\0\0",
        "AMOS Basic V134 ",
        "AMOS Basic V1.3 ",
        "AMOS Basic V1.00",
        "AMOS Pro101v\0\0\0\0",
        "AMOS Basic v134 ",
        "AMOS Basic v1.3 ",
        "AMOS Basic v1.00",
    ]

    # Maximum number of banks
    MAX_BANK_COUNT = 27

    # Header version of the file
    Version = ""

    # Source code
    Source = SourceCode()

    # Sprite bank
    Sprites = SpriteBank()

    # Icon bank
    Icons = IconBank()

    def __init__(self, filename):
        """
        Loads an amos source code file
        :param filename: File to load
        """
        with open(filename, "rb") as stream:

            # Read the header
            if self.validateHeader(stream):
                print(self.Version)

                text = self.Source.load(stream)
                print(text)

                self.readBanks(stream)


    def validateHeader(self, stream) -> bool:
        """
        Validate source code header

        :param stream: stream data
        :return: True on success
        """
        self.Version = struct.unpack('16s', stream.read(16))[0].decode("ascii")

        if self.Version not in self.HEADERS:
            print("Bad amos source code header (got \"" + self.Version + ") !")
            return False

        return True

    def readBanks(self, stream):
        """
        Read banks from the source file
        :param stream:
        :return: True on success
        """

        return False

# Memory types
class MemoryLocation(Enum):
    Chip = 0
    Fast = 1
    unknown = 2