# Kevin Bower
# Assignment 2
# This python file generates psuedo-random numbers
# Sources:
# https://pynative.com/python-random-seed/
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
# https://matthew-brett.github.io/teaching/string_formatting.html
# https://www.w3schools.com/python/ref_string_isdigit.asp

# library for sleep
import time

# set as constant so we can change if we remove or add images
NUMIMAGES = 9

while True:
    time.sleep(5)
    # open file so we can access random number
    imgFile = open('image-service.txt', 'r+')
    line = imgFile.readline()
    # check if the string is a valid number
    if line.isdigit():
        # mod randomNum by # of images so we get a valid . jpg
        modNum = (int(line) % NUMIMAGES) + 1
        path = '/d/Kevin/School - OSU/CS 361/Assignments/Assignment2/CS361-images/{}.jpg'.format(modNum)
        # write path to image File
        imgFile.seek(0)
        imgFile.truncate()
        imgFile.write(path)
    # close text file
    imgFile.close()
