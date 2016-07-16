from enum import Enum
import struct

class Point:
    X = 0
    Y = 0


class Size:
    Width = 0
    Height = 0


# Memory types
class MemoryLocation(Enum):
    Chip = 0
    Fast = 1
    Unknown = 2


class Bank:
    Tag = None
    Memory = MemoryLocation.Unknown


class MemoryBank(Bank):
    Size = 0
    Name = ""
    Data = None
    Id = 0

    def load(self, stream):
        self.Id = struct.unpack(">H", stream.read(2))[0]
        self.Memory = MemoryLocation(struct.unpack(">H", stream.read(2))[0])
        self.Size = struct.unpack(">I", stream.read(4))[0] & 0x0FFFFFFF
        self.Name = struct.unpack("8s", stream.read(8))[0].decode("ascii")

        self.Data = stream.read(self.Size - 8)


class IconBank(Bank):
    Palette = None
    Sprites = []

    def load(self, stream):

        count = struct.unpack(">H", stream.read(2))[0]

        for id in range(0, count):
            sprite = Sprite()
            sprite.load(stream)

            self.Sprites.append(sprite)

        self.Palette = struct.unpack(">32H", stream.read(64))
        self.Memory = MemoryLocation.Chip


class Sprite:

    Size = Size()
    Depth = 0
    HotSpot = Point()
    Data = None
    Palette = None

    def load(self, stream):
        self.Size.Width, self.Size.Height = struct.unpack(">HH", stream.read(4))
        self.Depth = struct.unpack(">H", stream.read(2))[0]
        self.HotSpot.X, self.HotSpot.Y = struct.unpack(">HH", stream.read(4))

        size = self.Size.Width * self.Size.Height * self.Depth
        # self.Data = struct.unpack("{}H".format(size), stream.read(size * 2))
        self.Data = stream.read(size * 2)

        return

