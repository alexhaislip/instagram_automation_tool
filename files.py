import datetime
import os
import settings

def fileContains(filename, value):
    with open(filename) as myfile:
        if value in myfile.read():
            return True
        else:
            return False


def appendToFile(filename, value, addDate):

    unfollowDate = datetime.datetime.now() + datetime.timedelta(minutes=settings.timeTillUnfollow)

    dateStr = unfollowDate.strftime("%Y %m %d %H %M %S")

    with open(filename, 'a') as myFile:
        if(addDate == True):
            myFile.write(value + " " + dateStr + "\n")
        else:
            myFile.write(value + "\n")
            print("gathered " + str(value))

def appendListToFile(filename, list):
    for value in list:
        appendToFile(filename, value, False)


def removeAndReturn(filename):
    user = ""
    with open("pending.txt", "r+") as file:
        fileLines = file.readlines()
        user = fileLines[-1]
        if(user.endswith("\n")):
            user = user[:-1]
        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()

        if(len(file.readlines()) == 1):
            file.truncate(0)
    return user