import os
import sys
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
import ast
import time

TOKENIZER = RegexpTokenizer(r'\w+')
# Maybe import NLTK for faster tokenization and word counting

save = open(os.path.join(sys.path[0], "tokenFreq.txt"), "r")
#save = open("./tokenFreq.txt", "r")
# TODO load the data into variables


#WORD_DICT = defaultdict(int)


line = save.readline()
lastLine = "{}"
while line:
    lastLine = line
    line = save.readline()


WORD_DICT = defaultdict(int, ast.literal_eval(lastLine))

save.close()


freq = open(os.path.join(sys.path[0], "tokenFreq.txt"), "w")

long = open(os.path.join(sys.path[0], "pageWordCount.txt"), "a")

EXCLUDE_SET = {"processor.py", "tokenFreq.txt", "pageWordCount.txt",".ipynb_checkpoints",".nfs00d0000000422d75000001bd", ".nfs001200000044b5b800000dcc",".nfs0092000000427f5000000dce",".nfs00c600000040a93e00000dcd"}

i = 0
while True:
    try:
        #print(os.getcwd())
        #print(sys.path[0])


        # maybe save the files into a specific directory and then dont have to worry about filtering
        for file in os.listdir(sys.path[0]):
            #print(file)
            if file not in EXCLUDE_SET and file[0] != ".":

                #print(file)
                fp = open(os.path.join(sys.path[0], file),'r')

                totalWords = 0
                line = fp.readline()
                while line:
                    words = TOKENIZER.tokenize(line.lower())
                    totalWords += len(words)
                    for w in words:
                        WORD_DICT[w] += 1

                    line = fp.readline()

                long.write(file + "," + str(totalWords) + "\n")

                # TODO uncomment this when deploying
                os.remove(os.path.join(os.getcwd(), file))

        freq.write(str(dict(WORD_DICT))+"\n")



        #assert i == 0
        time.sleep(3600)

    except KeyboardInterrupt:
        #print(WORD)
        freq.write(str(dict(WORD_DICT)))
        freq.close()
        break
