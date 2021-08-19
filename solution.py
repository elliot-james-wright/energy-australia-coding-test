# Author: Elliot Wright
# Last update: 19/08/2021

import json
import requests

def getData():
    '''
    This function makes a get request to the API. If a valid response is received
    the program will continue, otherwise and error message is printed.

    returns the unformated data from the API.
    '''
    f = requests.get("https://eacp.energyaustralia.com.au/codingtest/api/v1/festivals")
    if str(f.status_code) == "200":
        if len(str(f.text)) < 4:
            print("API returned empty string")
            print("Try again later")
            exit(0)
        else:
            return json.loads(f.text)
    elif str(f.status_code) == "429":
        print("API returned error: Too Many Requests")
        print("Try again later")
        exit(0)
    else:
        print("Unknown error occured")
        print("Status: " + str(f.status_code))
        print("Error message: " + str(f.text))
        exit(0)


def binarySearch(itemList, name, nested):
    '''
    This function takes in a list which will either be representing the records,
    bands or festivals. It will then use an efficient binary search to locate either
    where an existing record or band exists in my list or where a new record, band
    or festival should be inserted such that the list remains sorted.

    itemList: is the list that will be searching through, it either holds records, bands or festivals.
    name: is the name of the record, band or festival we are looking for.
    nested: either True or False to indicate whether each item contains its own list.

    returns the index where either the element exists or where a new element should be inserted.
    '''
    name = name.lower()
    start = 0
    stop = len(itemList)
    mid = (start+stop)//2
    # Each loop halves the size of the list we are searching to make sure there are log(N) loops
    while start < stop:
        if nested:
            item = itemList[mid][0].lower()
        else:
            item = itemList[mid].lower()

        if name < item:
            stop = min(mid, stop-1)
            mid = (start+stop)//2
        elif name > item:
            start = max(mid, start+1)
            mid = (start+stop)//2
        else:
            return mid
    return mid

def sortData(data):
    '''
    This function takes in the data in the format described by the Swagger documentation,
    and converts it into a more useful form that is sorted, such that the data is ready to be outputed.

    data: list of data in format described by the Swagger documentation.

    returns a list of records names, each record name contains a list of bands
    and each band contains a list of festivals performed at.
    '''

    records = []
    for festival in data:
        fName = festival.get('name', '')
        for band in festival['bands']:
            rName = band.get('recordLabel', '')
            bName = band.get('name', '')

            if rName != "" and bName != "":
                # Find the position of the band in our new list
                rIndex = binarySearch(records, rName, True)
                if rIndex < len(records) and records[rIndex][0] == rName:
                    bIndex = binarySearch(records[rIndex][1], bName, True)
                    if bIndex < len(records[rIndex][1]) and records[rIndex][1][bIndex][0] == bName:
                        fIndex = binarySearch(records[rIndex][1][bIndex][1], fName, False)
                        records[rIndex][1][bIndex][1].insert(fIndex, fName)
                    else:
                        newBand = [bName, [fName]]
                        records[rIndex][1].insert(bIndex, newBand)
                else:
                    if len(records) == 0:
                        records = [[rName, [[bName, [fName]]]]]
                    else:
                        newRecord = [rName, [[bName, [fName]]]]
                        records.insert(rIndex, newRecord)
    return records

def outputData(data):
    '''
    This function takes in the sorted data and prepares it into an appropiate string.
    I have chosen to just print the string to the terminal but it can easily be adapted to print
    to a file or some other form of output

    data: a list of records names, each record name contains a list of bands
    and each band contains a list of festivals performed at.
    '''
    outputStr = ""
    for record in data:
        outputStr += record[0] + "\n"
        for band in record[1]:
            outputStr += "    " + band[0] + "\n"
            for festival in band[1]:
                if festival != "":
                    outputStr += "        " + festival + "\n"
        outputStr += "\n"

    print(outputStr)

if __name__ == '__main__':
    data = getData()
    data = sortData(data)
    outputData(data)
