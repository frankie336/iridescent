import re
import time

with open('corpus/JULY10/gennady.korotkevich/LCM/JULY10_gennady.korotkevich_LCM.cpp') as f:
    test_file = f.readlines()

f ='corpus/JULY10/gennady.korotkevich/LCM/JULY10_gennady.korotkevich_LCM.cpp'


file_string = ''.join(test_file)

#p = re.compile( '(\()(.*)(\))'  )
#m = p.findall(file_string)
#print(m)

p = re.compile('( .*)(?<=\()(.*?)(?=\))')
all_params = p.findall(file_string)

import clang.cindex
from ctypes.util import find_library
import os.path





