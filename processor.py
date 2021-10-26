import os
import sys

# Maybe import NLTK for faster tokenization and word counting

i= 0
while True:
    try:
        print(os.getcwd())
        print(sys.path[0])

        # maybe save the files into a specific directory and then dont have to worry about filtering
        for file in os.listdir(sys.path[0]):
            #if file not in {}
            #fp = os.path.join(os.getcwd(), file)
            #text = open(fp, 'r')
            print(file)
            #os.remove(fp)



        assert 1 == 0
    except KeyboardInterrupt:
        print(i)
        break


