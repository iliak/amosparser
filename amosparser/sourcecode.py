
import io
import struct
from .tokens import tokens

class SourceCode:

    # Source code length
    SourceLength = 0

    # Final source code
    Text = io.StringIO()

    # Unknown tokens
    MissingTokens = {}

    # Referenced extensions
    Extensions = {}

    # Unknown extensions
    MissingExtensions = {}

    def load(self, stream) -> str:
        """
        Decodes source code from file
        :param stream:
        :return: Decoded source code
        """
        self.SourceLength = struct.unpack('>I', stream.read(4))[0]
        start = stream.tell()

        # For each line
        while stream.tell() < start + self.SourceLength:
            linestart = stream.tell()
            linelength, indent = struct.unpack('BB', stream.read(2))
            linelength *= 2

            self.Text.write(" " * (indent - 1))

            # For each token
            while stream.tell() < linestart + linelength:

                tokenid = struct.unpack(">H", stream.read(2))[0]
                try:
                    sub = tokens[tokenid]

                    if type(sub) is str:
                        self.Text.write(sub)
                    else:
                        if sub[1]:
                            data = sub[1](stream)

                        self.Text.write(sub[0] + data)

                except KeyError:

                    pass

        return self.Text.getvalue()

    def decryptProcedure(self, stream) -> str:
        """
        Decrypt encrypted procedures

        :return: Decrypted source code
        """

        pass

