# File: CacheSimulator.py
# Author: Jessica Li and Justin Lee
# Date: 04/30/2020
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
import random as ran

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

num_lines = int(associativity*S)

if (associativity == 4):
    cache = np.full((num_lines,(m+3)), "000")
else :
    cache = np.full((num_lines,(m+3)), "00")
#tag bit type is a string so it's not updating to the correct
for i in range (0, num_lines):
    #valid bit
    cache[i][0] = 0
    #dirty bit
    cache[i][1] = 0
    tagbit = "0" * t
    cache[i][2] = tagbit

# needed variables
cachehit = False
hitYN = ""
evict = -1
cachehitCount = 0 # need to do these for the write hit/misses
cachehitMiss = 0

#empty list to keep track of LRU cache line, pop after referenced~!
tracker =[]

# no change = -1 , change initiated to cache = 0
wrhit = False
wrhitYN = ""
dirty_bit = 0

print("cache successfully configured!")
# Configuring functions
def Replacement_policy(replace):
    if replace == 1:
        return "random_replacement"
    elif replace == 2:
        return "least_recently_used"

def Write_hit_policy(write_hit):
    if  write_hit == 1: #write the data in both the block in cache and block in RAM
        return "write_through" #no dirty bit!!
        coherency = True
        dirty_bit = 0
    elif write_hit == 2: #write the data only in the block in cache
        return "write_back"
        coherency = False
        dirty_bit = 1

def Write_miss_policy(write_miss):
    if write_miss == 1: #load block from RAM and write it in cache
        return  "write_allocate"
    elif write_miss == 2: #write the block in RAM and don't load in cache
        return  "no_write_allocate"

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
    if address == "":
        return 0
    else:
        return int(address, 2)

def Dec_to_Bin(address):
    return bin(int(address)).lstrip("0b").rstrip("L")

def Bin_to_Hex(address):
    if (address == tagbit):
        return (hex(int(address)))[2:] +"0"
    else :
        convert = hex(int(address, 2))
        return ("0" + convert.lstrip("0x").upper())
        
#****************************************************************************************************#
# Simulating Cache
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
    tag = Bin_to_Hex(str("".join(map(str, CT))))
    
    addressdec = int(Hex_to_Dec(address))
    '''
    print(cache[index*2][0] == '1')
    print(cache[index*2][2] == int(tag))
    print (type(tag))
    print (type(cache[index*2][2]))
    print(cache[index*2][0])
    print(cache[index*2][2])
    '''
    global cachehitCount
    global cachehitMiss
    # checking each line of index set in the cache for a hit
    '''
    elif (associativity == 2) :
        if (cache[index*2][0] == '0') and (cache[index*2+1][0] == '0') :
            cachehit = False
            cachehitMiss += 1
        elif (cache[index*2][2] == str(tag)) and (cache[index*2][0] == '1'):
            cachehit = True
            cachehitCount += 1
        elif (cache[index*2+1][0] == '0'):
            cachehit = False
            cachehitMiss += 1
        elif (cache[index*2+1][2] == str(tag)) and (cache[index*2+1][0] == '1'):
            cachehit = True
            cachehitCount += 1
    elif (associativity == 4) :
    '''
    if (associativity == 1):
        element = 0
        if (cache[index][0] == '0') :
            cachehit = False
            cachehitMiss += 1
        elif (cache[index][0] == '1') and (cache[index][2] == str(tag)):
            cachehit = True
            cachehitCount += 1
        else:
            cachehit =False
            cachehitMiss += 1
              
    if (associativity > 1):
        for element in range (0,len(cache)-2):
            print (element)
                #valid bit
            if (cache[index*associativity+element][0] == '0') and (cache[index*associativity+element][2] != str(tag)):
                cachehit = False
                cachehitMiss += 1
                
                break
            elif (cache[(index*associativity)+element][0] == '1') and (cache[index*associativity+element][2] == str(tag)):
                cachehit = True
                cachehitCount += 1
                break
            else:
                cachehit =False
                cachehitMiss += 1
        
    # cache hit false/true
    if cachehit == False :
        hitYN = "no"
        deeta = dataArray[addressdec]
        #load the ram line into the Cache
        #if line 1 of set is empty
        if cache[index*associativity+element][0] == '0':
            #change the valid bit
            cache[index*associativity+element][0] = 1
            #change the tag bit
            print(tag)
            cache[index*associativity+element][2] = tag
            #load data from RAM into cache
            bitupdate = 3
            evict = 0
            if (addressdec % 8 == 0):
                for curr in dataArray[addressdec:(addressdec+8)]:
                    cache[index*associativity+element][bitupdate] = curr
                    bitupdate +=1
                tracker.append(cache[index*2])
            else :
                displace = addressdec % 8
                for curr in dataArray[(addressdec-displace):(addressdec+(8-displace))]:
                    cache[index*associativity+element][bitupdate] = curr
                    bitupdate +=1
                tracker.append(cache[index*associativity+element])

        #replacement policies
        
        #random replacement
        elif (cache[index*2][0] == '1') and (cache[index*2+1][0] == '1') and (replace == 1) :
            #generate a random number line
            x = ran.randint(index*2,((index*2)+1))
            #print(f"rand int {x} selected")
            cache[x][0] = 1
            #change the tag bit
            cache[x][2] = tag
            #load data from RAM into cache
            bitupdate = 3
            evict = x
            #if the line's dirty bit = 1 and write allocate update the ram
            if (cache[x][1] == 1) and (write_hit == 1) :
                if (addressdec % 8 == 0):
                    for curr in dataArray[addressdec:(addressdec+8)]:
                        cache[x][bitupdate] = curr
                        bitupdate +=1
                    tracker.append(cache[x])
                else :
                    displace = addressdec % 8
                    for curr in dataArray[(addressdec-displace):(addressdec+(8-displace))]:
                        cache[x][bitupdate] = curr
                        bitupdate +=1
                    tracker.append(cache[x])
                    
        #least recently used
        elif (cache[index*2][0] == '1') and (cache[index*2+1][0] == '1') and (replace == 2) :
            #print(tracker[0])
            #print (cache[0])
            for line in range (0, len(cache)):
                if ((cache[line] == tracker[0]).all() == True):
                    cache[line][0] = 1
                    #change the tag bit
                    cache[line][2] = tag
                    #load data from RAM into cache
                    bitupdate = 3
                    evict = line
                    if (addressdec % 8 == 0):
                        for curr in dataArray[addressdec:(addressdec+8)]:
                            cache[line][bitupdate] = curr
                            bitupdate +=1
                        tracker.append(cache[line])
                    else :
                        displace = addressdec % 8
                        for curr in dataArray[(addressdec-displace):(addressdec+(8-displace))]:
                            cache[index*2+1][bitupdate] = curr
                            bitupdate +=1
                        tracker.append(cache[line])
            tracker.pop(0)
    elif cachehit == True :
        hitYN = "yes"
        evict = -1
        address = -1
        deeta = cache[index*2][offset+3]
    print(f"set:{index}")
    print(f"tag:{tag}")
    print(f"hit:{hitYN}")
    print(f"eviction_line: {evict}")
    print(f"ram_address:{address}")
    print(f"data:{deeta}")

def cache_write(address, data):
#convert hex to binary and then split binary bits to get offset, set, tag bits
    binary_bits = [int(d) for d in str(Hex_to_Bin(address))]
    #convert the set bits to decimal and assign them to variables for comparison
    CO = binary_bits[(len(binary_bits)-b):]
    offset = Bin_to_Dec(str("".join(map(str, CO))))
    
    CI = binary_bits[t:(len(binary_bits))-b]
    index = Bin_to_Dec(str("".join(map(str, CI))))
    
    CT = binary_bits[:(s+b)]
    tagbin = str("".join(map(str, CT)))
    tag = Bin_to_Hex(tagbin)
    
    addressdec = int(Hex_to_Dec(address))
    print()
    #test if its a hit
    if (cache[index*2][2] == str(tag)) and (cache[index*2][0] == '1'):
        wrhit = True
        line = index*2
    elif (cache[index*2+1][2] == str(tag)) and (cache[index*2+1][0] == '1'):
        wrhit = True
        line = index*2+1
    else:
        wrhit = False
    
    if (wrhit == False) : # do write miss policy
        wrhitYN = "no"
        evict = 0 # need to check what evict is for cache-write
        #write_allocating...
        if write_miss == 1 : # load block from RAM and write it in cache - in progress
            print("need to do lol")
            #load block from RAM to cache
            bitupdate = 3
            if (addressdec % 8 == 0):
                for curr in dataArray[addressdec:(addressdec+8)]:
                    cache[line][bitupdate] = curr
                    bitupdate +=1
                tracker.append(cache[line])#need to append to the tracker
                #could be problematic cause lines in appended wont match if cache-write *look at
            else :
                displace = addressdec % 8
                for curr in dataArray[(addressdec-displace):(addressdec+(8-displace))]:
                    cache[line][bitupdate] = curr
                    bitupdate +=1
                tracker.append(cache[line])
            # update the data bit
            cache[line][offset] = data.upper().lstrip("0X")
            #if write-back set dirty bit
            if (write-hit == 2):
                cache[line][1] = 1
            
        elif (write_miss == 2) : # only update RAM
            #print(dataArray[addressdec])
            dataArray[addressdec] = data.upper().lstrip("0X")
                
    elif (wrhit == True) : # do write hit policy - done
        wrhitYN = "yes"
        evict = -1
        if write_hit == 1: #write_through... write the data block in both in cache and RAM
            #update cache
            cache[line][offset] = data.upper().lstrip("0X")
            #update RAM
            dataArray[addressdec] = data.upper().lstrip("0X")
        elif write_hit == 2: # write_back...write the data only in the block in cache
            #update cache
            cache[line][offset+3] = data.upper().lstrip("0X")
            #set dirty bit to 1
            cache[line][1] = 1
            
    print(f"set:{index}")
    print(f"tag:{tag}")
    print(f"hit:{wrhitYN}")
    print(f"eviction_line: {evict}")
    print(f"ram_address:{address}")
    print(f"data:{data}")
    print("dirty_bit:") # what is this supposed to print the bit of?
    
def cache_flush():
    print("cache_cleared")
    # np.delete()
    # depends on write back/through policy
    # write back you have to update ram with cache lines that have dirty bit = 1
    
    # In case of cache flush, every line becomes valid bits all to 0 again

def cache_view():
    print(f"cache_size:{cache_size}")
    print(f"data_block_size:{data_size}")
    print(f"associativity:{associativity}")
    print(f"replacement_policy:{Replacement_policy(replace)}")
    print(f"write_hit_policy:{Write_hit_policy(write_hit)}")
    print(f"write_miss_policy:{Write_miss_policy(write_miss)}")
    print(f"number_of_cache_hits:{cachehitCount}")
    print(f"number_of_cache_misses:{cachehitMiss}")
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
            for i in row[3:]:
                cachefile.write(f"{i} ")
            cachefile.write("\n")
    cachefile.close()
    
def memory_dump():
    with open("ram.txt", "w+") as memfile:
        for i in range(len(x)):
            if (i == len(x)-1):
                memfile.write(dataArray[i])
            else:
                memfile.write(dataArray[i] + "\n")

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
    if "cache-read" in sim_input: #completed, testing
        #split input to get the address for passing into cache_read
        address = sim_input.split()
        address = address[1]
        cache_read(address)
    elif "cache-write" in sim_input: #in progress, write-hit completed
        #split input to get the address for passing into cache_write
        addressdata = sim_input.split()
        address = addressdata[1]
        data = addressdata[2]
        cache_write(address, data)
    elif sim_input == "cache-flush": #in progress
        cache_flush()
    elif sim_input == "cache-view": #done
        cache_view()
    elif sim_input == "memory-view": #done
        memory_view()
    elif sim_input == "cache-dump": #done
        cache_dump()
    elif sim_input == "memory-dump": #done
        memory_dump()
    elif sim_input == "quit": #done
        break
