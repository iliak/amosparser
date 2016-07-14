import struct

class Point:
    X = 0
    Y = 0


class Size:
    Width = 0
    Height = 0


class Bank:

    pass


class SpriteBank(Bank):

    pass


class IconBank(Bank):

    pass


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

