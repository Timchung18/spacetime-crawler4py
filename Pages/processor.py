import os
import sys
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
import ast
import time

TOKENIZER = RegexpTokenizer(r'\w+')
# Maybe import NLTK for faster tokenization and word counting

save = open(os.path.join(sys.path[0], "freq.txt"), "r")
#save = open("./freq.txt", "r")
# TODO load the data into variables


#WORD_DICT = defaultdict(int)


line = save.readline()
lastLine = ""
while line:
    lastLine = line
    line = save.readline()


WORD_DICT = defaultdict(int, ast.literal_eval(lastLine))

save.close()


freq = open(os.path.join(sys.path[0], "freq.txt"), "w")

long = open(os.path.join(sys.path[0], "tkCount.txt"), "a")

EXCLUDE_SET = {"processor.py", "freq.txt", "tkCount.txt"}

i = 0
while True:
    try:
        #print(os.getcwd())
        #print(sys.path[0])


        # maybe save the files into a specific directory and then dont have to worry about filtering
        for file in os.listdir(sys.path[0]):

            if file not in EXCLUDE_SET:

                print(file)
                fp = open(os.path.join(sys.path[0], file),'r')

                totalWords = 0
                line = fp.readline()
                while line:
                    words = TOKENIZER.tokenize(line)
                    totalWords += len(words)
                    for w in words:
                        WORD_DICT[w] += 1

                    line = fp.readline()

                long.write(file + "," + str(totalWords) + "\n")

                # TODO uncomment this when deploying
                #os.remove(os.path.join(os.getcwd(), file))

        freq.write(str(dict(WORD_DICT))+"\n")



        assert i == 0
        time.sleep(15)
        i+= 1

    except KeyboardInterrupt:
        #print(WORD)
        freq.write(str(dict(WORD_DICT)))
        freq.close()
        break
