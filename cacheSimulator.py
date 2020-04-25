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
import math
import numpy as np

#****************************************************************************************************#
# Initializing the physical memory
print("*** Welcome to the cache simulator ***")
print("initialize the RAM:")
# some error catching for file reading
try:
    fileName = sys.argv[1]
    inputFile = open(fileName, 'r')
except:
    print("Error: File not found/selected.")
    sys.exit()
# placing the file into an array
with open(sys.argv[1]) as inputFile:
    dataArray = np.array (inputFile.read().splitlines())
    numAddresses = len(dataArray)
    
# hex addresses in an array
print("init-ram 0x00 0xFF")
x = np.empty((0, 255))

for address in range (0, 256):
    address = hex(address)
    if (len(address) == 3):
        address = ("0x0" + address[-1])
    x = np.append(x, address)
    
#Dictionary for the RAM
w = dict(zip(x, dataArray.T))
#print (f"{w[0x03]}")
print("ram successfully initialized!")
#sys.exit()
#****************************************************************************************************#
# Configuring Cache

#printing the configuring menu and getting the integer inputs
print("configure the cache: ")
cache_size = int(input("cache size: ")) #aggregate size of all cache blocks <C>
data_size = int(input("data block size: ")) #number of bytes per block <B>
associativity = int(input("associativity: ")) #n-way set associative cache holds n lines per set <E>
replace = int(input("replacement policy: ")) #replaces a cache entry following a cache miss
write_hit = int(input("write hit policy: ")) #where to write the data when an address is hit
write_miss = int(input("write miss policy: ")) #where to write the data when an address is a miss
print("cache successfully configured!")

m = 8 #number of address bits
S = cache_size / (data_size * associativity) #number of sets
s = int(math.log(S, 2)) #number of set index bits
b = int(math.log(data_size, 2)) #number of block offset bits
t = m - (s + b)  #number of tag bits

# Configuring functions
def Replacement_policy(replace):
    if replace == 1:
        replace = "random_replacement"
    elif replace == 2:
        replace = "least_recently_used"

Replacement_policy(replace)

def Write_hit_policy(write_hit):
    if  write_hit == 1: #write the data in both the block in cache and block in RAM
        write_hit = "write_through"
        coherency = True
        dirty_bit = 0
    elif write_hit == 2: #write the data only in the block in cache
        write_hit = "write_back"
        coherency = False
        dirty_bit = 1

Write_hit_policy(write_hit)

def Write_miss_policy(write_miss):
    if write_miss == 1: #load block from RAM and write it in cache
        write_miss = "write_allocate"
    elif write_miss == 2: #write the block in RAM and don't load in cache
        write_miss = "no_write_allocate"

Write_miss_policy(write_miss)
        
#****************************************************************************************************#
# Simulating Cache

# Simulating Functions
def cache_read():
    print(f"set:{s}")
    print(f"tag:{t}")
    print("hit:")
    print("eviction_line:")
    print("ram_address:")
    print("data:")

def cache_write():
    print(f"set:{s}")
    print(f"tag:{t}")
    print("hit:")
    print("eviction_line:")
    print("ram_address:")
    print("data:")
    print("dirty_bit:")

def cache_view():
    print(f"cache_size:{cache_size}")
    print(f"data_block_size:{data_size}")
    print(f"associativity:{associativity}")
    print(f"replacement_policy:{replace}")
    print(f"write_hit_policy:{write_hit}")
    print(f"write_miss_policy:{write_miss}")
    print("number_of_cache_hits:")
    print("number_of_cache_misses:")
    print("cache_content:")

def memory_view():
    print(f"memory_size: {len(dataArray)}")
    print("memory_content:")
    print("Address:Data")
    for i in range(len(x)):
        if(i == 0):
          print(x[i] + ":",end="")
        elif (i % 8 == 0):
          print("")
          print(x[i] + ":",end="")
        print(dataArray[i], end=" ")

def cache_dump():
    print("dumping cache...")

def memory_dump():
    print("dumping memory...")

#printing the simulating menu and getting the inputs
def printMenu():
    print("")
    print("*** Cache simulator menu ***")
    print("type one command: ")
    print("1. cache-read ")
    print("2. cache-write ")
    print("3. cache-flush ")
    print("4. cache-view ")
    print("5. memory-view ")
    print("6. cache-dump ")
    print("7. memory-dump ")
    print("8. quit ")
    print("****************************")

while True:
    printMenu()
    sim_input = input()
    if sim_input == "cache-read":
        cache_read()
    elif sim_input == "cache-write":
        cache_write()
    elif sim_input == "cache-flush":
        print("cache_cleared")
    elif sim_input == "cache-view":
        cache_view()
    elif sim_input == "memory-view":
        memory_view()
    elif sim_input == "cache-dump":
        cache_dump()
    elif sim_input == "memory-dump":
        memory_dump()
    elif sim_input == "quit":
        break

