import sys

from amosparser.amosfile import AmosFile
from amosparser.libfile import LibFile

if __name__ == '__main__':
    # amos = AmosFile("/mnt/data/Emu/Amiga/Disk/dir/Work/Software/AMOS_Pro/test.amos")
    lib = LibFile(sys.argv[1])