import os
from shutil import move
from enum import Enum
import shutil


teststr = "D:\Libraries\Documents\Repositories\Personal\schoolFolderManager\CS 1331"
teststr1 = "D:\Libraries\Documents\Repositories\Personal\schoolFolderManager\Archive"
try:
    shutil.move(teststr,teststr1)
except shutil.Error as e:
    print(e)

