# Kevin Bower
# Assignment 2
# This python file generates psuedo-random numbers
# Sources:
# https://pynative.com/python-delete-lines-from-file/#h-delete-lines-from-a-file-by-line-numbers
# https://stackoverflow.com/questions/6648493/how-to-open-a-file-for-both-reading-and-writing
# https://www.programiz.com/python-programming/file-operation
# https://www.geeksforgeeks.org/sleep-in-python/
# https://www.cs.swarthmore.edu/~adanner/cs21/f09/randomlib.php#:~:text=To%20get%20access%20to%20the,get%20different%20(random)%20results.

# libraries for random range (images) and sleep
import random
import time
from datetime import datetime

random.seed(1)

while True:
    time.sleep(5)
    # open file, read line, and check if string is run
    # r+ -> read and write
    prngFile = open('prng-service.txt', 'r+')
    line = prngFile.readline()
    if line == 'run':
        # not inclusive on upper bound
        randNum = random.randint(1,1000)
        # move to beginning of file and delete line
        prngFile.seek(0)
        prngFile.truncate()
        # write random number to textfile
        prngFile.write(str(randNum))
    prngFile.close()
