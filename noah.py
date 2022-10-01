# Project Backup Script ver 0.0.1
# Jeff Dickson Oct 1, 2022
# The intent is to create a script that will make copies of projects onto whatever medium you point it at

import os, sys, shutil, noahSources, logging
from shutil import SameFileError
from datetime import date

def _logpath(path, names):
    logging.info('Working in %s' % path)
    return []   # nothing will be ignored

arkName = "ARK"

print("Begining file backup process")

#Clear the path for the new backup
for root, dirs, files in os.walk(noahSources.arkLocation):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

for i in range(0,len(noahSources.directory)):
    print("Working on directory " + str(i))
    shutil.copytree(noahSources.directory[i], noahSources.arkLocation + arkName + " " + str(date.today()) + "/Animal " + str(i), ignore=_logpath)
    # try:
        # shutil.copytree(noahSources.directory[i], noahSources.arkLocation + arkName + str(date.today()))
    # except SameFileError:
        # print("Error copying " + str(noahSources.directory[i]) + "we are attempting to copy the same file")
    # except IsADirectoryError:
        # print("Error copying " + str(noahSources.directory[i]) + "the destination is a directory")

print("Process complete")
