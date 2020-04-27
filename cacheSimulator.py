# File: CacheSimulator.py
# Author: Jessica Li and Justin Lee
# Date: 04/21/2020
# Section: 510
# E-mail: jml0400@tamu.edu and jlee232435@tamu.edu
# Description:
# e.g. The content of this file implements a cache simulation

#READ ME - to run type in the command line: python3 cacheSimulator.py input.txt
# use which ever input txt file
from cache import * #if we decide not to use just comment out
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

print("ram successfully initialized!")

#****************************************************************************************************#
# Configuring Cache

#printing the configuring menu and getting the integer inputs
print("configure the cache: ")

try:
    cache_size = int(input("cache size: ")) #aggregate size of all cache blocks <C>
    if (cache_size < 8) or (cache_size >256):
        print ("Invalid Cache Size.")
        sys.exit()
    data_size = int(input("data block size: ")) #number of bytes per block <B>
    if (data_size < 0):
        print ("Invalid Data Size.")
        sys.exit()
    associativity = int(input("associativity: ")) #n-way set associative cache holds n lines per set <E>
    replace = int(input("replacement policy: ")) #replaces a cache entry following a cache miss
    write_hit = int(input("write hit policy: ")) #where to write the data when an address is hit
    write_miss = int(input("write miss policy: ")) #where to write the data when an address is a miss
    
except:
    print("Error: Input invalid.")
    sys.exit()

m = 8 #number of address bits
S = int(cache_size / (data_size * associativity)) #number of sets
s = int(math.log(S, 2)) #number of set index bits
b = int(math.log(data_size, 2)) #number of block offset bits
t = m - (s + b) #number of tag bits

num_lines = int(cache_size/data_size)
additional_bits = (num_lines*3)
number_bits = int(cache_size + additional_bits)

cache = np.full((num_lines,(m+3)), "00")
tagbit = '0' * t
for i in range (0, num_lines):
    cache[i][2] = tagbit
    #valid bit
    cache[i][0] = 0
    #dirty bit
    cache[i][1] = 0

# needed variables
cachehit = False
hitYN = "no"
# no change = -1 , change initiated to cache = 0
evict = "-1"

print("cache successfully configured!")
# Configuring functions
def Replacement_policy(replace):
    if replace == 1:
        replace = "random_replacement"
    elif replace == 2:
        replace = "least_recently_used"

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

#Conversion Functions

def Hex_to_Bin(address):
    convert = "{0:08b}".format(int(address, 16))  
    return str(convert) 

def Hex_to_Dec(address):
    convert = int(address, 16)
    return str(convert)

def Dec_to_Hex(address):
    return hex(int(address)) #includes the 0x 
    #return hex(int(address)).lstrip("0x").rstrip("L") #- this version excludes the 0x if needed

def Bin_to_Dec(address):
    convert = int(address, 2)
    return convert

def Dec_to_Bin(address):
    return bin(int(address)).lstrip("0b").rstrip("L") 
        
#****************************************************************************************************#
# Simulating Cache

# Simulating Functions
def cache_read(address):
    #convert hex to binary and then split binary bits to get offset, set, tag bits
    #binary_bits = np.array(Hex_to_Bin(address))
    binary_bits = [int(d) for d in str(Hex_to_Bin(address))]
    #convert the set bits to decimal and assign them to variables for comparison
    
    CO = binary_bits[(len(binary_bits)-b):]
    offset = Bin_to_Dec(str("".join(map(str, CO))))
    
    CI = binary_bits[t:(len(binary_bits))-b]
    index = Bin_to_Dec(str("".join(map(str, CI))))
    
    CT = binary_bits[:(s+b)]
    tag = Bin_to_Dec(str("".join(map(str, CT))))
    
    count1 = 0
    count2 = 0
    # each line of set in the cache
    for i in cache[index*2] :
        if (i == 0) or (i == "00"):
            count1 +=1
        if (count1 > 3):
            cachehit = False
        
    for i in cache[index*2+1] :
        if (i == 0) or (i == "00"):
            count2 +=1
        if (count2 > 3):
            cachehit = False
    if cachehit == False :
        hitYN == "no"
        if (count1) > 3 :
            #change the valid bit
            cache[index*2][0] = 1
            #change the tag bit
            cache[index*2][2] = tag
            #load data from RAM into cache
            addressdec = int(Hex_to_Dec(address))
            bitupdate = 3
            if (addressdec % 8 == 0):
                for curr in dataArray[addressdec:(addressdec+8)]:
                    cache[index*2][bitupdate] = curr
                    bitupdate +=1
            else :
                displace = addressdec % 8
                for curr in dataArray[(addressdec-displace):(addressdec+(8-displace))]:
                    cache[index*2][bitupdate] = curr
                    bitupdate +=1
            #for i in dataArray[address]:
            print(cache)
            evict = 0
        else:
            cache[index*2+1][0] = 1
            print(cache[index*2+1])
            # load data from RAM into cache
            print(cache[index*2+1][1])
            evict = 0
    elif cachehit == True :
        hitYN == "yes"
        
    print(f"set:{s}")
    print(f"tag:{t}")
    print(f"hit:{hitYN}")
    print(f"eviction_line: {evict}")
    print(f"ram_address:{address}")
    print(f"data:{w[address]}")

    '''
    #if bounds meet then put it into cache array (the bounds are set by what you inputed in cache configuration)
    if (offset <= b & index <= s & tag <= t):
        for i in range (0, num_lines):
            cache[i][2] = tag
            cache[i][0] = offset
            cache[i][1] = index
    '''
def cache_write(address, data):
    print(f"set:{s}")
    print(f"tag:{t}")
    print(f"hit:{hitYN}")
    print("eviction_line:")
    print("ram_address:")
    print("data:")
    print("dirty_bit:")
    
    

def cache_flush():
    print("cache_cleared")

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
    for row in cache:
        for i in row:
            print (i, end=" ")
        print ("")
        

def memory_view():
    print(f"memory_size: {len(dataArray)}")
    print("memory_content:")
    print("Address:Data")
    for i in range(len(x)):
        if(i == 0):
          print(x[i].upper() + ":",end="")
        elif (i % 8 == 0):
          print("")
          print(x[i].upper() + ":",end="")
        print(dataArray[i], end=" ")

def cache_dump():
    print("cache dump...")
    with open("cache.txt", "w+") as cachefile:
        for row in cache:
            for i in row:
                cachefile.write(cache[x[i]] + "\n")

def memory_dump():
    with open("ram.txt", "w+") as memfile:
        for i in range(len(x)):
            if (i == len(x)-1):
                memfile.write(dataArray[x[i]])
            else:
                memfile.write(dataArray[x[i]] + "\n")

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
    if "cache-read" in sim_input: #in progress
        #split input to get the address for passing into cache_read
        address = sim_input.split()
        address = address[1]
        cache_read(address)
    elif "cache-write" in sim_input: #in progress
        #split input to get the address for passing into cache_write
        addressdata = sim_input.split()
        address = addressdata[1]
        data = addressdata[2]
        cache_write(address, data)
    elif sim_input == "cache-flush": #in progress
        cache_flush()
    elif sim_input == "cache-view": #almost done
        cache_view()
    elif sim_input == "memory-view": #done
        memory_view()
    elif sim_input == "cache-dump": #in progress
        cache_dump()
    elif sim_input == "memory-dump": #in progress
        memory_dump()
    elif sim_input == "quit":
        break
