# difHash.py
import hashlib
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
import numpy as np
import struct


TOKENIZER = RegexpTokenizer(r'\w+')


def DifHash(input: str):
    input = input.lower()

    words = TOKENIZER.tokenize(input)

    hashed_words = [int.from_bytes(hashlib.new('md4', input.encode('utf-8')).digest()[:4],'little') for input in words]

    word_freq = defaultdict(int)
    for i in hashed_words:
        word_freq[i] += 1

    # Create numpy matrix

    bVMatrix = False
    weightsMatrix = False
    for k,v in word_freq.items():
        #print(k,v)
        if bVMatrix is False:
            bVMatrix = np.unpackbits(np.array([k], dtype='>i4').view(np.uint8))
            #print(bVMatrix)
            weightsMatrix = np.array([v])
            #print(bVMatrix.shape)
            #print(weightsMatrix.shape)
        else:
            bVMatrix = np.vstack((bVMatrix, np.unpackbits(np.array([k], dtype='>i4').view(np.uint8))))
            weightsMatrix = np.vstack((weightsMatrix, np.array([v])))

    #print(bVMatrix)
    #print(weightsMatrix)
    if bVMatrix is False:
        f = open(fail.txt,"w+")
        f.write(input)
        print(input)
        
    bVMatrix = bVMatrix.astype('int32')
    bVMatrix[bVMatrix == 0] = -1
    #print(bVMatrix)
    #print(bVMatrix.shape)
    #print(weightsMatrix.shape)

    if bVMatrix.shape != (32,):
        fingerPrint = (np.dot(bVMatrix.T,weightsMatrix)).T
        #print(fingerPrint)
        fingerPrint = np.where(fingerPrint > 0 , 1, 0)

        #print(fingerPrint[0])
        #print(fingerPrint.dot(2 ** np.arange(fingerPrint.size)[::-1]))
        return int((fingerPrint.dot(2 ** np.arange(fingerPrint.size)[::-1]))[0])
    else:

        pow2 = 2 ** np.arange(32, dtype='uint64')

        fingerPrint = 0
        for i in range(32):
            fingerPrint = fingerPrint + pow2[i] * bVMatrix[i]

        # Don't know why the
        return int(fingerPrint)

        #return bVMatrix.dot()
        #return (bVMatrix.dot(2 ** np.arange(bVMatrix.size)[::-1]))[0]

    # Do columnwise addition, if 1 give freq, else minus freq, sum down the columns


def simCheck(lhs, rhs):
    return bin(lhs ^ rhs).count("1") / 32

