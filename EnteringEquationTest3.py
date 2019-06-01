#Graphing Calculator

# To-do:
# - Make sure you cannot enter invalid characters into the equation.
# - make sure the program knows which list (terms or ops) goes first.
# - Capitals/lower case shouldnt matter
# - more error support (multiple '=', starting/ending with operation, etc)

#test - 120+(sin4/66)   (x+3)^2-7

keyTerms = ["+","-","*","/","^",".","sin","cos","tan","log","sqrt"]
keyTerms2 = ["x","y","="]
terms = []
operations = []

def Initialize(e,i,maxIndex):
    while i <= maxIndex and i < len(e):
        if e[i] == "(":
            b = 1
            for n,j in enumerate(e[i+1:]):
                #print(n,j)
                if j == "(": b+=1
                elif j == ")": b -= 1
                if b == 0:
                    temp = e[i+1:i+n+1]
                    del e[i:i+n+1]
                    e[i] = Initialize(temp,0,len(temp)-1)#will initialize a nested list
                    break
            if b != 0:
                print("Error: Unconsistent Begin/End Brackets\n")
                return "error"
        #Changes strings with a number to an int
        if type(e[i]) is str:
            try: int(e[i])
            except ValueError: ''''''
            else: e[i] = int(e[i])
        #Combining 4-letter key words like "sqrt" into one item
        if len(e)-i >= 4 and "".join([str(c).lower() for c in e[i:i+4]]) in keyTerms:
            #if consecutive list elements are a key term, they combine to one and extra bits are deletd, lowering the maxIndex
            e[i] = "".join([str(c).lower() for c in e[i:i+4]])
            del e[i+1:i+4] 
            maxIndex -= 3
        #Combining 3-letter key words like "sin" into one item
        elif len(e)-i >= 3 and "".join([str(c).lower() for c in e[i:i+3]]) in keyTerms:
            #same as above but for sets of three
            e[i] = "".join([str(c).lower() for c in e[i:i+3]])
            del e[i+1:i+3]
            maxIndex -= 2
        #Combining consecutive numbers (checks previous instead next because next hasn't been changed to an integer yet
        if i > 0 and type(e[i]) is int and type(e[i-1]) is int:
            e[i-1] = int("".join([str(c) for c in e[i-1:i+1]]))
            del e[i]
            maxIndex -= 1
            i -= 1 #checked to the left not right, it must counter index+=1 to stay in the same index next iteration
        i += 1
    #Combines ints with a decimal between them into a float. [12,".",34] --> [12.34]
    i,maxIndex = 0,len(e)-1
    while i <= maxIndex:
        if i > 1 and type(e[i]) is int and e[i-1] == "." and type(e[i-2]) is int:
            e[i-2] = e[i-2]+(e[i]/10**len(str(e[i])))
            del e[i-1:i+1]
            maxIndex -= 2
        i += 1
    return e

def CreateData(e,t,op):
    #Sorts out terms and operations
    for i in e:
        if type(i) is list:
            temp = CreateData(i,[],[])#sorts nested lists
            t.append(temp[0])
            op.append(temp[1])
        elif type(i) is int or i == "x":
            t.append(i)
        elif i in keyTerms:
            op.append(i)
    return [t,op]

equation = "error"
while equation == "error":
    equation = list(input("Enter equation: y = "))
    equation = Initialize(equation,0,len(equation)-1)

data = CreateData(equation,terms,operations)
#print("Equation:",equation)
print(terms,operations)
