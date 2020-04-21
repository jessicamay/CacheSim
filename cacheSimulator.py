# File: CacheSimulator.py
# Author: Jessica Li and Justin Lee
# Date: 04/21/2020
# Section: 510
# E-mail: jml0400@tamu.edu and jlee232435@tamu.edu
# Description:
# e.g. The content of this file implements a cache simulator

#READ ME - to run type in the command line: python3 cacheSimulator.py input.txt
# use which ever input txt file
import os
import sys

print("*** Welcome to the cache simulator ***")
print("initialize the RAM:")
print("init-ram 0x00 0xFF")
print("ram successfully initialized!")

# some error catching for file reading
try:
    fileName = sys.argv[1]
    inputFile = open(fileName, 'r')
except:
    print("Error: File not found/selected.")
    sys.exit()

#for line in inputFile:
#do something with it lol
#inputFile.close()






