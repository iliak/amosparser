import io
import struct



class Token:
    Instruction = 0         # Standalone instruction (e.g. Command)
    Function = 0            # Returns variables (e.g. X = Command)
    Name = ''
    Param = ''
    # Return = 0

class LibFile:

    def __init__(self, filename):
        """
        Loads an amos library file
        :param filename: File to load
        """
        with open(filename, "rb") as stream:

            stream.read(32)     # Skip the Amiga header
            commandsize = struct.unpack(">I", stream.read(4))[0]
            tokensize = struct.unpack(">I", stream.read(4))[0]
            libsize = struct.unpack(">I", stream.read(4))[0]
            titlesize = struct.unpack(">I", stream.read(4))[0]
            stream.read(2)

            # AP20 present ?
            tag = struct.unpack("4s", stream.read(4))[0]
            try:
                if tag.decode("ascii") == "AP20":
                    print("AMOS Pro extension")
            except UnicodeDecodeError:
                print("Not an AMOS Pro extension")
                stream.seek(-4, 1)

            # Base offset of all above sizes
            base = stream.tell()
            commandbase = base
            tokenbase = commandbase + commandsize
            libbase = tokenbase + tokensize
            titlebase = libbase + libsize

            # The title of the extension
            stream.seek(titlebase)
            name = ""
            while True:
                c = struct.unpack("B", stream.read(1))[0]
                if c == 0:
                    break
                name += chr(c)

            print("Name     \"{}\"".format(name))
            print("Start    Addresses Offset    : {:10} (0x{:04X})".format(32, 32))
            print("C_Off    Commands Offset     : {:10} (0x{:04X})".format(base, base))
            print("C_Tk     Tokens Offset       : {:10} (0x{:04X})".format(tokenbase, tokenbase))
            print("C_Lib    Library Offset      : {:10} (0x{:04X})".format(libbase, libbase))
            print("C_Title  Title Offset        : {:10} (0x{:04X})".format(titlebase, titlebase))

            # Read tokens
            stream.seek(tokenbase)
            hash1, hash2, hash3, hash4 = struct.unpack(">HHBB", stream.read(6))
            print("Token hash : 0x{:04X}:0x{:04X}:0x{:02X}:0x{:02X}".format(hash1, hash2, hash3, hash4))
            # if hash1 != 1 or hash3 != 0x80 or hash4 != 0xff:
                # hash2 =>   0x0110 AMOSPro.Lib
                #            0x0001 AMOSPro_Compiler.Lib
                # print("Bad token header !!")
                # return

            previoustoken = ""
            id = 1
            while True:

                inst = struct.unpack(">H", stream.read(2))[0]

                # End of the list
                if inst == 0:
                    break

                func = struct.unpack(">H", stream.read(2))[0]

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

                if len(token.Name) > 0 and token.Name[0] == "!":
                    token.Name = token.Name[1:]
                    previoustoken = token.Name

                # Read Parameters
                while True:
                    c = struct.unpack("b", stream.read(1))[0]

                    if c > 0:
                        token.Param += chr(c)
                    else:
                        break

                # Padding
                if stream.tell() % 2 == 1:
                    stream.read(1)

                print("{:04} [I: 0x{:04X} F: 0x{:04X}]: ".format(id, token.Instruction, token.Function), end="")
                id += 1

                if len(token.Param) > 0:
                    if token.Param[0] == '0':
                        print("int = ", end="")
                    elif token.Param[0] == '1':
                        print("float = ", end="")
                    elif token.Param[0] == '2':
                        print("string = ", end="")

                    print("{} ".format(token.Name), end="")

                    if len(token.Param) > 1:
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
                            elif c == ",":
                                print(", ", end="")
                            elif c == "t":
                                print("TO ", end="")

                print()

            # Offset table
            print("C_Off dump:")
            stream.seek(commandbase)
            base = libbase
            while stream.tell() < tokenbase:
                offset = stream.tell() - base
                data = struct.unpack(">H", stream.read(2))[0]

                base += data * 2
                print("L{} [0x{:04X}] = 0x{:04X} - Lib offset: 0x{:04X}"
                      .format(int(offset / 2), int(offset / 2), data * 2, base))

            return

    pass

