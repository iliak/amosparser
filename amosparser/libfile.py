import io
import struct



class Token:
    Instruction = 0
    Function = 0
    Name = ''
    Param = ''
    Return = 0

class LibFile:

    def __init__(self, filename):
        """
        Loads an amos source code file
        :param filename: File to load
        """
        with open(filename, "rb") as stream:

            stream.read(32)     # Skip the Amiga header
            dummysize = struct.unpack(">I", stream.read(4))[0]
            tokensize = struct.unpack(">I", stream.read(4))[0]
            libsize = struct.unpack(">I", stream.read(4))[0]
            titlesize = struct.unpack(">I", stream.read(4))[0]
            stream.read(2)

            # AP20 present ?
            tag = struct.unpack("4s", stream.read(4))[0]
            if tag.decode("ascii") != "AP20":
                stream.seek(-4, 1)

            # Base offset of all above offsets
            base = stream.tell()

            # Read token
            stream.seek(base + dummysize)
            hash1, hash2, hash3, hash4 = struct.unpack(">HHBB", stream.read(6))
            if hash1 != 1 or hash3 != 0x80 or hash4 != 0xff:
                #hash2 =>   0x0110 AMOSPro.Lib
                #           0x0001 AMOSPro_Compiler.Lib
                print("Bad token header !!")
                return

            # The magic 3 bytes is dc.w 0 and dc.l 0
            while stream.tell() <= base + dummysize + tokensize:

                inst = struct.unpack(">h", stream.read(2))[0]
                func = struct.unpack(">h", stream.read(2))[0]
                if inst == 0 and func == 0:
                    break;

                token = Token()
                token.Instruction = inst
                token.Function = func

                # Token name
                c = 0
                while c < 0x80:
                    c = struct.unpack("B", stream.read(1))[0]
                    token.Name += chr(c & 0x7F)

                # Read Parameters
                while True:
                    c = struct.unpack("b", stream.read(1))[0]

                    if c > 0:
                        token.Param += chr(c)
                    else:
                        token.Return = c
                        break


                print("{}".format(token.Name))

                if stream.tell() % 2 == 1:
                    stream.read(1)

            return

    pass

