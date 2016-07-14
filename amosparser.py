import sys

from amosparser.amosfile import AmosFile

if __name__ == '__main__':
    amos = AmosFile(sys.argv[1])
    # amos.getsource()
    # amos.getbanks()
