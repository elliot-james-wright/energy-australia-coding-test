# Author: Elliot Wright
# Last update: 19/08/2021

def getData():
    f = open("testcase.txt", "r")
    data = f.read()
    return data

def sortData(data):
    return data

def outputData(data):
    print(data)

if __name__ == '__main__':
    data = getData()
    data = sortData(data)
    outputData(data)
