from math import sqrt
from datetime import timedelta
from random import randint

# The United Kingdom keyboards have been used for this layout.
# Feel free to replace with your own layout.
# Remember: "\0" is a key to be ignored, and "\1" is the SHIFT key.

# uppercase QWERTY
QWERTY_UPPER = [
    "¬!\"£$%^&*()_+",
    "\0QWERTYUIOP{}",
    "\0ASDFGHJKL:@~",
    "\0ZXCVBNM<>?\0",
    "\0\0\0 \0\0\0\0\0\0\0\0\0"
]
# lowercase QWERTY
QWERTY_LOWER = [
    "`1234567890-=",
    "\tqwertyuiop[]\0",
    "\0asdfghjkl;'#\n",
    "\1zxcvbnm,./\0\1",
    "\0\0\0 \0\0\0\0\0\0\0\0\0\0"
]
# uppercase special QWERTY
QWERTY_S_UPPER = [
    "\0\0\0\0\0\0\0\0\0\0\0\0\0",
    "\0\0\0É\0\0\0ÚÍÓ\0",
    "\0Á\0\0\0\0\0\0\0\0\0\0|",
    "\0\0\0\0\0\0\0\0\0\0\0\0\0",
    "\0\0\0\0\0\0\0\0\0\0\0\0\0"
]
# lowercase special QWERTY
QWERTY_S_LOWER = [
    "\0\0\0\0\0\0\0\0\0\0\0\0\0",
    "\0\0\0é\0\0\0úíó\0",
    "\0á\0\0\0\0\0\0\0\0\0\0\\",
    "\0\0\0\0\0\0\0\0\0\0\0\0\0"
]

# all QWERTY keyboards
QWERTY = [QWERTY_LOWER, QWERTY_UPPER, QWERTY_S_LOWER, QWERTY_S_UPPER]

def keyCoords(key):
    """
        Finds the coordinates of the given key on one of the QWERTY keyboards.
        Returns (-1, 0, 0) if the key could not be found.
    """
    # for every keyboard
    for kbNum in range(len(QWERTY)):
        arr = QWERTY[kbNum]
        # for every row
        for row in range(len(arr)):
            line = arr[row]
            # for every key
            for col in range(len(arr[row])):
                # if the key is the one we're looking for...
                if line[col] == key:
                    # return (keyboard number, row, column)
                    return (kbNum, row, col)
    # no key was found:
    # print the missing key
    print(key)
    # return default value
    return -1, 0, 0
    
def distance(a, b):
    """
        Calculates the distance between two points, ignoring the first values
        of the tuples if their length is 3.
    """
    # if there are 3 values...
    if len(a) == 3:
        # ignore the first one
        _, xA, yA = a
    # otherwise...
    else:
        # use 2 first values
        xA, yA = a
    if len(b) == 3:
        _, xB, yB = b
    else:
        xB, yB = b
    
    # get absolute squared x & y difference
    xDiff = abs(xA - xB) ** 2
    yDiff = abs(yA - yB) ** 2
    
    # return square root of squared differences
    return sqrt(xDiff + yDiff)
    
def totalTime(text, rushed=False, retDelta=True):
    """
        Calculates the total amount of time it'd (theoretically) take to write
        the given text.
        
        If `retDelta` is True (default), a `timedelta` object is returned, a 
        float if False.
        
        If `rushed` is True or the text is in ALL CAPS, the base amount of time
        is multiplied by 0.63 and a random penalty is added. This is False
        by default.
    """
    # coordinates of the SHIFT key
    shiftCoords = keyCoords("\1")
    # the total travelled distance
    totalDistance = 0
    # last key pressed
    last = (0, 0, 0)
    # for every character
    for ch in text:
        # get the key's coordinates
        coords = keyCoords(ch)
        # if the key wasn't found...
        if coords[0] == -1:
            return -1
        # if we used a different keyboard for this character than the last...
        if coords[0] != last[0]:
            # add the distance between the last key and the shift key, twice
            totalDistance += distance(last, shiftCoords) * 2
        # add the distance from the last character to the current
        totalDistance += distance(last, coords)
    # divide the distance by 69 (nice) to get the time
    sec = totalDistance / 69
    # if the text is rushed...
    if rushed:
        # decrease total time and add randomized penalty
        sec *= 0.63 + (((randint(0, 166) - 0.37) * 1.3) / 300)
    # if we want a timedelta object....
    if retDelta:
        # return a timedelta object
        return timedelta(seconds=sec)
    # otherwise...
    else:
        # return the amount of seconds taken
        return sec