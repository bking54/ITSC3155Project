# Library of methods used for determining a list of points from a function.
# Bradley King

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
    nums = '0123456789'
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
# EMDAS operations
def eval(list, point):
    temp = []
    coords = []
    while (len(list) > 1 and type(list[0]) != type(list)):
        loop1 = len(list)
        # Evaluate exponents
        for i in range(loop1):
            if (list[i] == '^'):
                val1 = list[i - 1]
                val2 = list[i + 1]
                if (type(val1) == type(list)):
                            
        # Evaluate multiplication/division
        # Evaluate addition/subtraction
    return coords

def main():
    str = '2(5x+1)(-6(x+2)^2-(39x))+7'
    # str = '-2x+(3x-5)/x^2-7x(x+4)-349'
    list = decompose(str)
    print(list)
    list2 = format(list)
    print(list2)

if __name__ == "__main__":
    main()