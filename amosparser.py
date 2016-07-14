import sys

from amosparser.amosfile import amosFile

if __name__ == '__main__':
    amos = amosFile(sys.argv[1])
    # amos.getsource()
    # amos.getbanks()
