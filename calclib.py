# Library of methods used for determining a list of points from a function.
# Bradley King

import pandas as pd
import numpy as np

# Decompose a mathematical function into a python list
# The 'P' in PEMDAS
def decompose(str):
    # Split str using ) and ( as delimiters
    list = str.split(')')
    loop1 = len(list)
    for i in range(loop1 - 1):
        list[i] = list[i] + ')'
    temp = []
    for i in range(loop1):
        elements = list[i].split('(')
        loop2 = len(elements)
        for j in range(loop2 - 1):
            elements[j + 1] = '(' + elements[j + 1]
        for j in range(loop2):
            temp.append(elements[j])
    loop1 = len(temp)
    # Clean up list
    list = []
    for i in range(loop1):
        if (temp[i] != ''):
            list.append(temp[i])
    # Create list structure
    temp = []
    loop1 = len(list)
    open_count = 0
    closed_count = 0
    tempstr = ''
    for i in range(loop1):
        tempstr += list[i]
        open_count += list[i].count('(')
        closed_count += list[i].count(')')
        if (open_count == closed_count): # Verify parenthesis are balanced
            if (open_count == 1):
                tempstr = tempstr[1: -1]
                temp.append([tempstr])
            elif (open_count > 1):
                tempstr = tempstr[1: -1]
                templist = decompose(tempstr) # Break down remaining large chunks
                temp.append(templist)
            else:
                temp.append(tempstr)
            tempstr = ''
            open_count = 0
            closed_count = 0
    return temp

# Format the strings left in the list after decomposition
# Split operators from numbers and the X variables
# Pre-step before the EMDAS
def format(list):
    temp = []
    entry = ''
    loop1 = len(list)
    for i in range(loop1):
        if (type(list[i]) != type(list)): # Element is not a list
            tempstr = list[i]
            if (i == 0 and tempstr[0] == '-'):
                tempstr = '0' + tempstr
            loop2 = len(tempstr)
            for j in range(loop2):
                if (getType(tempstr[j]) == 0):
                    entry += tempstr[j]
                else:
                    if (entry != '' and getType(tempstr[j]) == 1):
                        temp.append(entry)
                        entry = ''
                    elif (entry != '' and getType(tempstr[j]) == 2):
                        temp.append(entry)
                        temp.append('*')
                        entry = ''
                    elif (entry == '' and getType(tempstr[j]) == 2):
                        if (temp != [] and (temp[-1] == 'x' or type(temp[-1]) == type(list))):
                            temp.append('*')
                    temp.append(tempstr[j])
            if (entry != ''):
                temp.append(entry)
                entry = ''
        elif(type(list[i]) == type(list)): # Element is a list
            list[i] = format(list[i]) # Format the inner list
            if (temp != [] and (temp[-1] == 'x' or type(temp[-1]) == type(list) or getType(temp[-1]) == 0)):
                temp.append('*')
            temp.append(list[i])
    return temp

# Returns an int representing the type of character
def getType(char):
    ops = '+-/*^'
    nums = '.0123456789'
    varbs = 'x'
    if (nums.count(char) > 0):
        return 0
    elif (ops.count(char) > 0):
        return 1
    elif (varbs.count(char) > 0):
        return 2
    else:
        return -1

# Evaluates a decomposed and formatted function at a point
# PEMDAS operations
def eval(list, point):
    listcopy = list.copy()
    temp = []
    while (listcopy.count('^') > 0):
        index = listcopy.index('^')
        element1 = parseElement(listcopy[index - 1], point)
        element2 = parseElement(listcopy[index + 1], point)
        out = element1 ** element2
        temp = listcopy[0: (index - 1)]
        temp.append(out)
        temp.extend(listcopy[(index + 2):])
        listcopy = temp.copy()
    # Evaluate multiplication
    while (listcopy.count('*')):
        index = listcopy.index('*')
        element1 = parseElement(listcopy[index - 1], point)
        element2 = parseElement(listcopy[index + 1], point)
        out = element1 * element2
        temp = listcopy[0: (index - 1)]
        temp.append(out)
        temp.extend(listcopy[(index + 2):])
        listcopy = temp.copy()
    # Evaluate division
    while (listcopy.count('/')):
        index = listcopy.index('/')
        element1 = parseElement(listcopy[index - 1], point)
        element2 = parseElement(listcopy[index + 1], point)
        out = 0
        if (element2 == 0): # Prevent division by 0
            lims = limit(listcopy, point, 7)
            if ((lims[0] > 0 and lims[1] > 0) and (lims[0] > 0 and lims[1] > 0)):
                out = lims[0] + lims[1]
            else:
                out = 0
        else:
            out = element1 / element2
        temp = listcopy[0: (index - 1)]
        temp.append(out)
        temp.extend(listcopy[(index + 2):])
        listcopy = temp.copy()
    # Evaluate addition
    while (listcopy.count('+')):
        index = listcopy.index('+')
        element1 = parseElement(listcopy[index - 1], point)
        element2 = parseElement(listcopy[index + 1], point)
        out = element1 + element2
        temp = listcopy[0: (index - 1)]
        temp.append(out)
        temp.extend(listcopy[(index + 2):])
        listcopy = temp.copy()
    # Evaluate subtraction
    while (listcopy.count('-')):
        index = listcopy.index('-')
        element1 = parseElement(listcopy[index - 1], point)
        element2 = parseElement(listcopy[index + 1], point)
        out = element1 - element2
        temp = listcopy[0: (index - 1)]
        temp.append(out)
        temp.extend(listcopy[(index + 2):])
        listcopy = temp.copy()
    if (len(listcopy) == 1 and (type(listcopy[0]) == type(1) or type(listcopy[0]) == type(1.0))):
        return listcopy[0]
    elif(type(listcopy) == type('string')):
        return float(listcopy[0])
    else:
        raise Exception('Bad leftovers for eval')

# Find the number value of a element in the list
# Helper function for eval
def parseElement(value, point):
    temp = []
    finalVal = 0
    if (type(value) == type(temp)):
        finalVal = eval(value, point)
    elif (type(value) == type('string')):
        if (value == 'x'):
            finalVal = point
        else:
            finalVal = float(value)
    elif (type(value) == type(1.0)):
        finalVal = value
    elif (type(value) == type(1)):
        finalVal = value
    else:
        return 'string'
    return finalVal

# Create a list of coordinates by evaluating many points
def evalRange(list, start, end, delta):
    coords = []
    input = start
    while (input < end):
        coord = []
        output = eval(list, input)
        coord.append(input)
        coord.append(output)
        coords.append(coord.copy())
        input += delta
    return coords

# Get the positive and negative limits at a certain accuracy
def limit(list, target, accuracy):
    delta = 10 ** (-1 * accuracy)
    pos = eval(list, target + delta)
    neg = eval(list, target - delta)
    limit = [pos, neg]
    return limit

# Use a set of points to approximate the derivative
# takes a list of points, and a function
# lim h -> x of (f(h) - f(x))/(h - x)
def getDerivative(list, func):
    coords = []
    delta = 10 ** -7
    loop1 = len(list)
    for i in range(loop1):
        x = list[i][0]
        h = x + delta
        fx = list[i][1]
        fh = eval(func, h)
        out = (fh - fx)/(h - x)
        coords.append([x, out])
    return coords

# def validate(list):


def main():
    # str = '2(5x+1)(-6(x+2)^2-(39x))+7'
    # str = '-2x+(3x-5)/x^2-7x(x+4)-349'
    # str = '5*x^2+6^3/4-49'
    # str = '-3(x+4)^2'
    # str = '234'
    # str = '-1/x^3'
    str = 'x^2'
    list = decompose(str)
    print(list)
    list2 = format(list)
    print(list2)
    # coord = eval(list2, 2)
    # print(coord)
    coords = evalRange(list2, -100, 100, 1)
    print(coords)
    # lim = limit(list2, 0, 5)
    # print(lim)

if __name__ == "__main__":
    main()