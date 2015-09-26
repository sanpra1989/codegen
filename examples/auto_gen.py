import sys
from codegen import *
import os
import clang.cindex

if len(sys.argv) != 2:
    print("Usage: translator.py [header file name]")
    sys.exit()

clang.cindex.Config.set_library_path(os.environ['LD_LIBRARY_PATH'])
index = clang.cindex.Index.create()
translation_unit = index.parse(sys.argv[1], ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])

translated = translate(translation_unit.cursor,sys.argv[1])

for cls in translated:
    for line in cls.generate():
        print line
