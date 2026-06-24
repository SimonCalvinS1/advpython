try:
    import math
    print(math.exp(1000))

    d = {1: "SS", 2: "CC"}
    d.append("2w")
except OverflowError as o:
    print("Error occurred: ", o)
except AttributeError as a:
    print("Error occurred: ", a)

try:
    import abc1
    print(x)
except ModuleNotFoundError as mod:
    print("Error occurred: ", mod)
except NameError as n:
    print("Error occurred: ", n)

try:
    mark = 100/0
    s = ["SS", "FF"]
    print(s[3])
except ZeroDivisionError as z:
    print("Error occurred: ", z)
except IndexError as i:
    print("Error occurred: ", i)

try:
    d = {1: "SS", 2: "CC"}
    print(d[44])

    open("file.txt")
except KeyError as k:
    print("Error occurred: ", k)
except FileNotFoundError as f:
    print("Error occurred: ", f)

try:
    s = int("abc")
    result = "Age: " + 25 
except ValueError as val:
    print("Error occurred: ", val)
except TypeError as t:
    print("Error occurred: ", t)

# name, value, attribute, type, zero division, index, module not found, file not found, key, overflow