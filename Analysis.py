#Entering and Analyzing Equation

# To-do:
# - Make sure you cannot enter invalid characters into the equation.
# - Capitals/lower case shouldnt matter.
# - More error support (multiple '=', starting/ending with operation, etc).
# - Asymptote support (try & except)
# - Make dictionary of custom user-created variables
# - Line intersection points that you can click to toggle the label visibility

import math
radOrDeg = "deg"
operators = ["+","-","*","/","^",".","sin","cos","tan","sqrt"]
conversions = ["sin","cos","tan","sqrt"]
isError = True

#Replaces a list with one element, with that element. The list was pointless
def RemoveExtraBrackets(n):
    if type(n) is list and maxRecur > 0:
        return RemoveExtraBrackets(n)
    elif type(n) is float or type(n) is int or n == "x":
        return n
    return n

def Setup_1(e,i):
    while i < len(e):
        #initialize areas with brackets
        if e[i] == "(":
            b = 1
            #once an equal amount of begin/end brackets are found, that area is intialized
            for n,j in enumerate(e[i+1:]):
                if j == "(": b += 1
                elif j == ")": b -= 1
                if b == 0:
                    temp = e[i+1:i+n+1] #the area inside the set of brackets
                    del e[i:i+n+1]
                    e[i] = Initialize(temp) #initializes the bracketed area
                    if len(e[i]) == 1:
                        e[i] = RemoveExtraBrackets(e[i][0]) #If a list has one element, there's no need for the list
                    break
            if b != 0:
                print("Error: Unconsistent Brackets")
        #sets all possible integers into an integer
        if type(e[i]) is str:
            try: int(e[i])
            except ValueError: ''''''
            else: e[i] = int(e[i])
        i += 1
    while len(e) == 1 and type(e[0]) is list:
        e = e[0]
    return e
        
def Setup_2(e,i):
    #combines consecutive integers into one [1,2] --> [12]
    while i < len(e):
        if type(e[i]) is int and type(e[i-1]) is int:
            e[i-1] = int("".join([str(c) for c in e[i-1:i+1]]))
            del e[i]
        else: i += 1
    return e

def Setup_3(e,i):
    #combines integers with a decimal between them into a float [1,'.',2] --> [1.2]
    while i < len(e):
        if type(e[i]) is int and e[i-1] == "." and type(e[i-2]) is int:
            e[i-2] = e[i-2]+(e[i]/10**len(str(e[i])))
            del e[i-1:i+1]
        else: i += 1
    return e

def Setup_4(e,i):
    #combines letters for operations with lengths greater than one, like "sin" and "sqrt".
    while i < len(e):
        if type(e[i]) is list:
            e[i] = Setup_4(e[i],0) #repeats process in nested lists
        #If 3 consecutive letters equals an operation, merge them. ['s','q','r','t'] --> ['sqrt']
        elif len(e)-i >= 4 and "".join([str(c).lower() for c in e[i:i+4]]) in operators:
            e[i] = "".join([str(c).lower() for c in e[i:i+4]])
            del e[i+1:i+4]
        #If 3 consecutive letters equals an operation, merge them. ['s','i','n'] --> ['sin']
        elif len(e)-i >= 3 and "".join([str(c).lower() for c in e[i:i+3]]) in operators:
            e[i] = "".join([str(c).lower() for c in e[i:i+3]])
            del e[i+1:i+3]
        elif e[i] == " ":
            del e[i]
            i -= 1#counters the i+=1 below to stay on the same index next iteration
        i += 1
    return e

def Setup_5(e,i):
    #removes extra '+', changes subtracton to addition of a negative, and also changes 2 '-' to '+'
    while i < len(e)-1:
        if e[i] == "-" and (type(e[i+1]) is int or type(e[i+1]) is float):
            e[i] = "+"
            e[i+1] = -e[i+1]
        elif e[i] == "-" and e[i+1] == "-":
            e[i] = "+"
            del e[i+1]
        if e[i] == "+" and e[i+1] == "+":
            del e[i+1]
        i += 1
    return e

#Prepares the inputted equation to calculate
def Initialize(e):
    e = Setup_1(e,0)
    e = Setup_2(e,1)
    e = Setup_3(e,2)
    e = Setup_4(e,0)
    e = Setup_5(e,0)
    return e

def Postfix(e,i,opstack,output):
    #Sorts the equation into a format easy to calculate with, more info in link below
    #https://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    priority = {"^":3,"*":2,"/":2,"-":1,"+":1}
    while i < len(e):
        if type(e[i]) is list:
            temp = Postfix(e[i],0,[],[])
            for t in temp:
                output.append(t)
        elif type(e[i]) is int or type(e[i]) is float:
            output.append(e[i])
        elif e[i] in operators:
            if len(opstack) > 0 and priority[opstack[-1]] > priority[e[i]]:
                output.append(opstack[-1])
                del opstack[-1]
            opstack.append(e[i])
        i += 1
    for op in reversed(opstack):
        output.append(op)
    return output

#-------------------------------------------------- CALCULATIONS ------------------------------------------------------------

def PreCalc(e,i,xVal=None):
    global radOrDeg
    for n in range(len(e)):
        #If there is a list, repeat the process within it
        if type(e[n]) is list:
            e[n] = Calculate(e[n][:],[],0,xVal)
        elif e[n] == "x" and (type(xVal) is int or type(xVal) is float):
            e[n] = xVal
    #Pre-calculates all "conversion" operations like sine leaving only basic ones like adding
    while i < len(e)-1:
        if e[i] in conversions:
            if e[i].lower() == "sin":
                if radOrDeg == "deg":
                    e[i] = round(math.sin(math.radians(e[i+1])),10)
                    del e[i+1]
                elif radOrDeg == "rad":
                    e[i] = round(math.sin(e[i+1]),10)
                    del e[i+1]
            elif e[i].lower() == "cos":
                if radOrDeg == "deg":
                    e[i] = round(math.cos(math.radians(e[i+1])),10)
                    del e[i+1]
                elif radOrDeg == "rad":
                    e[i] = round(math.cos(e[i+1]),10)
                    del e[i+1]
            elif e[i].lower() == "tan":
                if radOrDeg == "deg":
                    e[i] = round(math.tan(math.radians(e[i+1])),10)
                    del e[i+1]
                elif radOrDeg == "rad":
                    e[i] = round(math.tan(e[i+1]),10)
                    del e[i+1]
            elif e[i].lower() == "sqrt":
                e[i] = math.sqrt(e[i+1])
                del e[i+1]
        i += 1
    return e

#Deals with the basic operations between 2 numbers
def Calc(a,b,op):
    if op == "+":
        return (a + b)
    elif op == "-":
        return (a - b)
    elif op == "*":
        return (a * b)
    elif op == "^":
        return (a ** b)
    elif op == "/":
        if b == 0:
            return None
        else:
            return (a / b)

def Calculate(e,temp,i,x):
    f = Postfix(PreCalc(e,0,x),0,[],[])
    #Uses a pre-sorted bedmas-friendly format to calculate with called "Postfix notation"
    while i < len(f):
        if type(f[i]) is int or type(f[i]) is float:
            temp.append(f[i])
        if f[i] in operators and len(temp) > 1:
            temp.append(Calc(temp[-2],temp[-1],f[i]))
            if temp[-1] == None: return None
            del temp[-3:-1]
        i += 1
    return temp[0]

equation = Initialize(list(''.join(input("Enter equation: y = ").split(" "))))
