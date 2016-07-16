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
            stream.seek(-4, 1)
            try:
                if tag.decode("ascii") != "AP20":
                    print("AMOS Pro extension")
            except:
                print("Not an AMOS Pro extension")


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
                previoustoken = ""
            while stream.tell() <= base + dummysize + tokensize:

                inst = struct.unpack(">H", stream.read(2))[0]
                func = struct.unpack(">H", stream.read(2))[0]
                if inst == 0 and func == 0:
                    break

                token = Token()
                token.Instruction = inst
                token.Function = func

                # Token name
                c = 0
                while c < 0x80:
                    c = struct.unpack("B", stream.read(1))[0]

                    if c == 0x80:
                        token.Name = previoustoken
                    else:
                        token.Name += chr(c & 0x7F)

                if token.Name[0] == "!":
                    token.Name = token.Name[1:]
                    previoustoken = token.Name


                # Read Parameters
                while True:
                    c = struct.unpack("b", stream.read(1))[0]

                    if c > 0:
                        token.Param += chr(c)
                    else:
                        break

                if stream.tell() % 2 == 1:
                    stream.read(1)

                if token.Instruction != 0xFFFF:
                    print("I [0x{:04}]: ".format(token.Instruction), end="")
                else:
                    print("F [0x{:04}]: ".format(token.Function), end="")

                if token.Param[0] == '0':
                    print("int = ", end="")
                elif token.Param[0] == '1':
                    print("float = ", end="")
                elif token.Param[0] == '2':
                    print("string = ", end="")

                print("{} ".format(token.Name), end="")

                if len(token.Param) > 1:
                    if token.Function != 0xFFFF:
                        print("(", end="")

                    for c in token.Param[1:]:
                        if c == "0":
                            print("int ", end="")
                        elif c == "1":
                            print("float ", end="")
                        elif c == "2":
                            print("string ", end="")
                        elif c == "3":
                            print("int/string ", end="")
                        elif c == "4":
                            print("int/float ", end="")
                        elif c == "5":
                            print("angle ", end="")
                        elif c in [",", 't']:
                            print("TO ", end="")

                    if token.Function != 0xFFFF:
                        print(")", end="")



                print()


                t = 0
            return

    pass

