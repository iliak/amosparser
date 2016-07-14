import io
import struct
from enum import Enum

from .tokens import tokens
from .bank import *

class AmosFile:

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
    Source = io.StringIO()

    # Banks
    Banks = {}

    def __init__(self, filename):
        """
        Loads an amos source code file
        :param filename: File to load
        """
        with open(filename, "rb") as stream:

            # Read the header
            if self.validateheader(stream):
                self.readsource(stream)
                self.readbanks(stream)

    def validateheader(self, stream) -> bool:
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

    def readsource(self, stream):
        """
        Decodes source code from file
        :param stream:
        """
        length = struct.unpack('>I', stream.read(4))[0]
        start = stream.tell()

        # For each line
        while stream.tell() < start + length:
            linestart = stream.tell()
            linelength, indent = struct.unpack('BB', stream.read(2))
            linelength *= 2

            self.Source.write(" " * (indent - 1))

            # For each token
            while stream.tell() < linestart + linelength:

                tokenid = struct.unpack(">H", stream.read(2))[0]
                try:
                    sub = tokens[tokenid]

                    if type(sub) is str:
                        self.Source.write(sub)
                    else:
                        if sub[1]:
                            data = sub[1](stream)

                        self.Source.write(sub[0] + data)

                except KeyError:

                    pass

        return

    def readbanks(self, stream):
        """
        Read banks from the source file
        :param stream:
        :return: True on success
        """
        header = struct.unpack('4s', stream.read(4))[0].decode("ascii")
        if header != "AmBs":
            return

        count = struct.unpack(">H", stream.read(2))[0]


        for i in range(0, count):
            tag = struct.unpack('4s', stream.read(4))[0]
            tag = tag.decode("ascii")

            # Sprite or Icon bank
            if tag in ("AmSp", "AmIc"):
                count = struct.unpack(">H", stream.read(2))[0]

                self.Banks[i] = []
                for id in range(0, count):
                    sprite = Sprite()
                    sprite.load(stream)

                    self.Banks[i].append(sprite)

                palette = struct.unpack(">32H", stream.read(64))

            elif tag == "AmBk":
                id = struct.unpack(">H", stream.read(2))[0]
                loc = struct.unpack(">H", stream.read(2))[0]
                length = struct.unpack(">i", stream.read(4))[0] & 0x0FFFFFFF
                name = struct.unpack("8s", stream.read(8))[0].decode("ascii")

                stream.read(length - 8)

            # Common
            else:
                self.readbank(stream)

        return False

    def readbank(self, stream):

        pass


    def readiconbank(self, stream):

        return


# Memory types
class MemoryLocation(Enum):
    Chip = 0
    Fast = 1
    unknown = 2