#!/usr/bin/python

import sys
import binascii
from time import time
from multiprocessing.pool import ThreadPool
import itertools
# import des_wrapper as dw
pool = ThreadPool(50)

b = 8
minValHex = "808080BA80808080"
maxValHex = "808080BA7F7F7F7F"
minValBin = 1000000010000000100000001011101010000000100000001000000010000000
maxValBin = 1000000010000000100000001011101001111111011111110111111101111111

def removeParity(binVal):
    if len(str(binVal))%b == 0:
        strBinVal = str(binVal)
        noParStrBinVal = ''.join('' if i % b == 0 else char for i, char in enumerate(strBinVal))
        return noParStrBinVal

def enum_key(current):
    """Return the next key based on the current key as hex string.

    TODO: Implement the required functions.
    """
    valBin = bin(int(current, 16))[2:]
    noParValStr = str(removeParity(valBin))
    noParValDec = int(noParValStr,2)
    incValDec = noParValDec + 1
    paddedIncValBin = "0" * (7*b-len(bin(incValDec)[2:])%(7*b)) + bin(incValDec)[2:]
    paddedIncBlocksBin = [paddedIncValBin[i:(b-1+i)] for i in range(0, len(paddedIncValBin), b-1)]
    for i, block in enumerate(paddedIncBlocksBin):
        nOnes = 0
        for char in block:
            if char == "1":
                nOnes += 1
        if nOnes % 2:
            paddedIncBlocksBin[i] = "0" + paddedIncBlocksBin[i]
        else:
            paddedIncBlocksBin[i] = "1" + paddedIncBlocksBin[i]
    parIncValBin = "".join(str(block) for block in paddedIncBlocksBin)
    parIncValHex = hex(int(parIncValBin, 2))
    return str(parIncValHex[2:len(parIncValHex)-1])

def runCrack(val, msgBinList, cipher):
        incValDec = val + 1
        paddedIncValBin = "0" * (7*b-len(bin(incValDec)[2:])%(7*b)) + bin(incValDec)[2:]
        paddedIncBlocksBin = [paddedIncValBin[i:(b-1+i)] for i in range(0, len(paddedIncValBin), b-1)]
        for i, block in enumerate(paddedIncBlocksBin):
            nOnes = 0
            for char in block:
                if char == "1":
                    nOnes += 1
            if nOnes % 2:
                paddedIncBlocksBin[i] = "0" + paddedIncBlocksBin[i]
            else:
                paddedIncBlocksBin[i] = "1" + paddedIncBlocksBin[i]
        parIncValBin = "".join(str(block) for block in paddedIncBlocksBin)
        keyList = [int(x) for x in parIncValBin]
        cracked = bits2bytes(dw.des_encrypt(key, msgBinList))
        if cracked == cipher:
            print("Cracked: {0}".format(cracked))
            return cracked

def Range(start, stop):
   i = start
   while i < stop:
       yield i
       i += 1

def main(argv):
    if argv[0] == 'enum_key':
        pass
        print(enum_key(argv[1]))
    elif argv[0] == 'crack':
        message = open('plaintext', 'r').read()
        cipher = open('ciphertext', 'r').read()
        messageBin = '0' + bin(int(binascii.hexlify(message), 16))[2:]
        messageBinList = [int(x) for x in messageBin]
        noParMinValStr = str(removeParity(minValBin))
        noParMaxValStr = str(removeParity(maxValBin))        
        noParMinValDec = long(noParMinValStr,2)
        noParMaxValDec = long(noParMaxValStr,2)

        print("Beginning to crack..")
        t0 = time()
        for val in Range(noParMinValDec, noParMaxValDec):
            pool.apply_async(runCrack, (val, messageBinList, cipher))
        print("Time to crack: {0}".format(time() - t0))
        pool.close()
        pool.join()
        
    else:
        raise Exception("Wrong mode!")

    
if __name__=="__main__":
    main(sys.argv[1:])
