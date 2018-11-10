############################################################################################################################################################
#Author:Adarsh Sawant ,University of North Carolina at Charlotte:                                                                                                                                                   
#The code implements a cache simulator with no pre-fetching or scheduling support.The code implements a cache simulatore by instantiating a class Mycache which
#consiste of array of sets which is the type cacheset.Cache set inturn instatiates object of type cacheline.Thus each of the cache set would consist obejct 
#Equivalent to the associativity of cache .For unified cache the cacheset would instatiate only one cache line.The entire cache structure would be instantiated by the 
#function create cache.                                                                          
#Reading the input: the code reads input from the trace file and for each of the line it seprates the address and the operation componet.After which the code would
#start parsing the address to determine the tag address,offset address and the line address.The code would then call search() function in order to whether the tag
#tag is already stored in the cache if yes the code would report hit by returning 1 to the calling function.If the tag is not present then the code would first check if there
#are empty slots in cache if there are empty slots then the new tag value would be written to the cache(compulsory miss)by using writeCache().If not it would check which is the candidate for 
#replacement by reading indRpl value.
#
#
#
#
#
#
#
#
#
import math
from collections import defaultdict
import math 

class Mycache:
    def __init__(self, blocksize, cachesize, asso):
        self.blocksize = blocksize
        self.cachesize = cachesize
        self.linesNos = cachesize / blocksize           
        self.cache = []
        self.set = []
        self.asso = asso

    def createCache(self):                                              #Cache class holds all sets together .The function creates a cache depending upon the input
        for i in range(self.linesNos):                                          # set number
            self.lineNo = i
            self.set = cacheset(self.asso)
            self.cache.append(self.set)
                                                                        # for k in range (self.asso):
                                                                        # print k,"TAG:",self.cache[i].cset[k].tag,"Hit count:",self.cache[i].cset[k].hitline

    def search(self, line, tag):
                                                                        #print"searching for:", tag, "Line", line
        stored = 0
        tarHit=0
        temp=0                                                              # print"line no",self.cache[line].lineNo,"data",self.cache[line].tag,"hit",self.cache[line].hitline
        for k in range(self.asso):
            indRpl = self.cache[line].repl                              #replacement candidate for this set 
            tarHit = self.cache[line].cset[indRpl].hitline              
                                                                        #print "replacement index:", indRpl,"with hit rate",tarHit
            stored = self.cache[line].cset[k].tag
            hit = self.cache[line].cset[k].hitline                      #temp variable
            if (stored != tag):
                if (stored == None):
                    #print"compulsory miss"
                    self.writeCache(line, tag, k)
                    return(0)
                else:
                    self.cache[line].cset[k].hitline = hit + 1                              #if value becomes greater than past candidate value store new candidate
                    if ((hit + 1) > indRpl):                                                        
                        self.cache[line].repl = k
                        temp=1                                                                             
                    if (k == (self.asso - 1)):                                          #We have come to the last line in the set so we should replace now 
                        #print"LRU starts to replace"                                                 # LRU would start here re
                        if(not(temp)):
                            self.writeCache(line,tag ,indRpl)
                        else:
                            self.writeCache(line,tag ,k)
                        #print"changing the hit line value for index",indRpl,"line:",line
                        return(0)
                        ###############################################################################################################################
                        # LRU implementation:we are keepin track of the index in the set which increment every time there is a miss and ths value is a line value indRpl
                        #we check this value every time we increment to the latest indexmvalue being missed in line 2
                        #when the value is replaced the algorithm takes care of it as one of the previous values must have got incremented
                        ###############################################################################################################################
                    else:
                        continue
                return

            elif(stored==tag):
                #print "hit"
                self.cache[line].cset[k].hitline = 0
                return(1)

    def writeCache(self, line, tag, num):
        #print "storing at line:", line, "num", num, "tag", tag
        self.cache[line].cset[num].tag = tag
        # print("storing at line",self.cache[line].lineNo);

    def displayCache(self):
        for i in range(self.linesNos):
            print "LINE:", i
            for k in range(self.asso):
                print k, "TAG:", self.cache[i].cset[k].tag, "Hit count:", self.cache[i].cset[k].hitline


class cacheset:                                                 #Cache set consist of array of lines depending upon the associativity.
    def __init__(self, asso):
        self.cset = []                                          #for unified cache set would have single line .                                
        # self.lineNo=lineNo
        self.line = 0
        self.tag = 0
        self.repl = 0                                           #This variable stores candidate which would be replaced at time of conflict .
        for i in range(asso):                                   #The algorithm stores the index of cache line with higest hitline 
            self.line = cacheline()
            self.cset.append(self.line)


class cacheline:                                                #cache line class :Each of it has tag and number of hits(hitline) counter for LRU
    def __init__(self):
        self.tag = None
        self.hitline = 0


def offsetCal(size, block):
    offs = math.log(block, 2)
    return offs


def lineNocal(size, bloc, asso):
    total = asso * bloc
    lineno = size / total
    return lineno

ldmiss=0                                                           #counter for the load instruction misses
dwmiss=0                                                           #counter for the data write misses misses
drmiss=0                                                           #counter for the data read misses misses
ay= []                                                             #iterator for the data read from the trace file
ldin=0                                                             #counts the ld instruction
rddat=0                                                            #counts the read instruction
strdat=0                                                           #counts the store instruction 
totalinst=0
hits =0
miss =0
with open("/home/adu/Desktop/Comparch/test/trace.txt", "r") as fobj:
    for line in fobj:
        stri = line.strip('\n')
        ay.append(stri)                                            # storing al the data in the buffer
k = 0

inp=int(1024*raw_input("Enter the cache size in KB"))
cachesize =1024*32      #hardcoded 
linesize = int(raw_input("Enter the line size in bytes "))
asso = int(raw_input("Enter the associativity"))
uni=int(raw_input("Enter 1 for unified cache or zero for the split cache "))#unified cache uni=1
if(uni):
        NoffBits = offsetCal(cachesize, linesize)
        lines = lineNocal(cachesize, linesize, asso)
        NlineBits = math.log(lines, 2)
        NtagBits = 32 - (NoffBits + NlineBits)
        print "offset:", NoffBits, "linebits:", NlineBits, "tagbits", NtagBits
        mycache = Mycache(linesize, cachesize, asso)
        mycache.createCache()
                                                                    # mycache.displayCache()
        while (k < len(ay)):
            oper, addr = ay[k].split(' ', 1)                        # spliting the address and the operation
            Baddr = '{:032b}'.format(int(addr, 16))                 #formating the address in 32 bit form 
            Baddrop = Baddr[::-1]                                   # fliping the adress to use the format as we habe to start from zero
                                                                    # print "adress",addr
                                                                    # print"adress",Baddr
                                                                    # print"adressflip",Baddrop
            lineBits = Baddrop[int(NoffBits):int(NoffBits + NlineBits)]
            line = int(lineBits, 2)
                                                                    # print "line bits",lineBits,"line no",int(lineBits,2)
            tagBits = Baddrop[int(NoffBits + NlineBits):32]
            tag = int(tagBits, 2)
                                                                    # print"tag adddres",tagBits,"address",int(tagBits,2)
                                                                    #print "address", addr
            if (oper == "0"):                                       #Data read operations
                rddat = rddat + 1
                hitmis=mycache.search(line, tag)        
                if(not(hitmis)):
                   drmiss=drmiss+1
            elif (oper == "1"):                                     #data store operations
                strdat = strdat + 1
                hitmis=mycache.search(line, tag)
                if(not(hitmis)):
                   dwmiss=dwmiss+1
            elif (oper == "2"):                                     #instruction store instructions 
                ldin = ldin + 1
                hitmis=mycache.search(line, tag)
                if(not(hitmis)):
                   ldmiss=ldmiss+1
            k = k + 1
        totalinst = ldin + strdat + rddat                           #toal instructions executed 
        totalmis=drmiss+dwmiss+ldmiss                               #total misses 
        inhit=ldin-ldmiss
        drhit=rddat-drmiss                                          #data read hits from the main code
        dshit=strdat-dwmiss                                         #data store hits from the main code
        dhit=drhit+dshit+inhit                                      #Total data hits from the main code
        print "*********************UNIFIED CACHE**********************************************************************"
        print"Fetches"
        print "total fetches:",totalinst
        print"\nTotal instrucntion fetches:",ldin,"Total Instruction miss:",ldmiss,"Total Instruction hits:",ldin-ldmiss
        print"\nTotal Data Read operations",rddat,"Total data read Miss",drmiss,"Total data read Hits",drhit,
        print"\nTotal Data Write operations",strdat,"Total Data Write Miss",dwmiss,"Total Data Write Misses",dshit
        print"Cache miss ",totalmis,"Miss rate:",float(totalmis)/(float(totalinst))
        print"Cache hits",dhit,"Hit rate:",float(dhit)/(float(totalinst))
        print"**************************************************************************************************************"
  # mycache.displayCache()
else:
    NoffBits = offsetCal(cachesize, linesize)
    lines = lineNocal(cachesize, linesize, asso)
    NlineBits = math.log(lines, 2)
        # print "lineBits",lineBits
    NtagBits = 32 - (NoffBits + NlineBits)
    print "offset:", NoffBits, "linebits:", NlineBits, "tagbits", NtagBits
    Datcache = Mycache(linesize, cachesize, asso)
    Datcache.createCache()
    Inscache = Mycache(linesize, cachesize, asso)
    Inscache.createCache()
        # mycache.displayCache()
    while (k < len(ay)):
        oper, addr = ay[k].split(' ', 1)                        # spliting the address and the operation
        Baddr = '{:032b}'.format(int(addr, 16))
        Baddrop = Baddr[::-1]                                   # fliping the adress to use the format as we habe to start from zero
                                                                # print "adress",addr
                                                                # print"adress",Baddr
                                                                # print"adressflip",Baddrop
        lineBits = Baddrop[int(NoffBits):int(NoffBits + NlineBits)]
        line = int(lineBits, 2)
                                                                # print "line bits",lineBits,"line no",int(lineBits,2)
        tagBits = Baddrop[int(NoffBits + NlineBits):32]
        tag = int(tagBits, 2)
                                                                # print"tag adddres",tagBits,"address",int(tagBits,2)
        #print "address", addr
        if (oper == "0"):
            rddat = rddat + 1
            hitmis=Datcache.search(line, tag)
            if(not(hitmis)):
                drmiss=drmiss+1
        elif (oper == "1"):
            strdat = strdat + 1
            hitmis=Datcache.search(line, tag)
            if(not(hitmis)):
                dwmiss=dwmiss+1
        elif (oper == "2"):
            ldin = ldin + 1
            hitmis=Inscache.search(line, tag)
            if(not(hitmis)):
                ldmiss=ldmiss+1
        k = k + 1
    totalDinst = strdat+ rddat
    totalmis=drmiss+dwmiss
    drhit=rddat-drmiss
    dshit=strdat-dwmiss
    dhit=drhit+dshit
    print "*********************INSTRUCTION CACHE**********************************************************************"
    print"\nFetches"
    print "\ntotal fetches:",ldin
    print"\nTotal instrucntion Misses:",ldmiss
    print"\nTotal Instruction Hits:",ldin-ldmiss
    print"\nInstruction cache Misses",ldmiss,"Miss rate:",float(ldmiss)/(float(ldin))
    print"\nInstruction cache hits",ldin-ldmiss,"Hit rate:",float(ldin-ldmiss)/(float(ldin))
    
    print "**************************************************************************************************************"
    print"***********************DATA CACHE******************************************************************************"
    print"\nTotal Data Instructions:",totalDinst
    print"\nTotal Data Read operations",rddat,"Total data read Miss",drmiss,"Total data read Hits",drhit,
    print"\nTotal Data Write operations",strdat,"Total Data Write Miss",dwmiss,"Total Data Write Misses",dshit
    print"\nData cache Misses",totalmis,"Miss rate:",float(totalmis)/(float(totalDinst))
    print"\nData cache hits",dhit,"Hit rate:",float(dhit)/(float(totalDinst))
    print"**************************************************************************************************************"
 
        

    
    


