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

#****************************************************************************************************#
# Initializing the physical memory
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
s = math.log(S) #number of set index bits
b = math.log(data_size) #number of block offset bits
t = m - (s + b)  #number of tag btis

if replace == 1:
    replace = "random_replacement"
elif replace == 2:
    replace = "least_recently_used"

if  write_hit == 1: #write the data in both the block in cache and block in RAM
    write_hit = "write_through"
elif write_hit == 2: #write the data only in the block in cache
    write_hit = "write_back"

if write_miss == 1: #load block from RAM and write it in cache
    write_miss = "write_allocate"
elif write_miss == 2: #write the block in RAM and don't load in cache
    write_miss = "no_write_allocate"

    
#****************************************************************************************************#
# Simulating Cache

#printing the simulating menu and getting the inputs
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
    sim_input = input()
    if sim_input == "cache-read":
        print("set:" + s)
        print("tag:" + t)
        print("hit:")
        print("eviction_line:")
        print("ram_address:")
        print("data:")
    elif sim_input == "cache-write":
        print("set:" + s)
        print("tag:" + t)
        print("hit:")
        print("eviction_line:")
        print("ram_address:")
        print("data:")
        print("dirty_bit:")
    elif sim_input == "cache-flush":
        print("cache_cleared")    
    elif sim_input == "cache-view":
        print("cache_size:" + cache_size)
        print("data_block_size:" + data_size)
        print("associativity:" + associativity)
        print("replacement_policy:" + replace)
        print("write_hit_policy:" + write_hit)
        print("write_miss_policy:" + write_miss)
        print("number_of_cache_hits:")
        print("number_of_cache_misses:")
        print("cache_content:")
    elif sim_input == "memory-view":
        print("memory_size:")
        print("memory_used:")
        print("memory_content:")
        print("Address:Data")
    elif sim_input == "cache-dump":
        print()
    elif sim_input == "memory-dump":
        print()
    elif sim_input == "quit":
        break

