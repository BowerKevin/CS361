# Kevin Bower
# Assignment 2
# This python file generates psuedo-random numbers
# Sources:
# https://pynative.com/python-delete-lines-from-file/#h-delete-lines-from-a-file-by-line-numbers
# https://stackoverflow.com/questions/6648493/how-to-open-a-file-for-both-reading-and-writing
# https://www.programiz.com/python-programming/file-operation
# https://www.geeksforgeeks.org/sleep-in-python/
# https://www.cs.swarthmore.edu/~adanner/cs21/f09/randomlib.php#:~:text=To%20get%20access%20to%20the,get%20different%20(random)%20results.

# library for sleep
import time

def fileWrites():
    # open file to write run, used by prng.py
    prngFile = open('prng-service.txt', 'w')
    prngFile.truncate()
    prngFile.write('run')
    time.sleep(2)
    prngFile.close()
    time.sleep(10)

    # line -> randomNumber
    # get randomNumber generated
    prngFile = open('prng-service.txt', 'r')
    prngFile.seek(0)
    line = prngFile.readline()
    prngFile.close()

    # write random number to image-service, used by imgsrv
    imgFile = open('image-service.txt', 'w')
    imgFile.truncate()
    imgFile.seek(0)
    imgFile.write(line)
    imgFile.close()
    time.sleep(5)

    # file now contains path of an img
    imgFile = open('image-service.txt', 'r')
    path = imgFile.readline()
    # display to user
    print(path)
    imgFile.close()

while True:
    userInput = input('\nEnter a number, 1 to generate a new image or 2 to exit: ')
    if userInput == '1':
        fileWrites()
    elif userInput == '2':
        break
    else:
        print('unknown option')