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

    # check for errors
    if str(f.status_code) == "200":
        if len(str(f.text)) < 4:
            print("API returned empty string")
            print("Try again later")
            exit(0)
    elif str(f.status_code) == "429":
        print("API returned error: Too Many Requests")
        print("Try again later")
        exit(0)
    else:
        print("Unknown error occured")
        print("Status: " + str(f.status_code))
        print("Error message: " + str(f.text))
        exit(0)

    # if everything is successful then return the data
    # format the data from a json string to a python list
    return json.loads(f.text)

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
        # check to see if we are looking through items that are themselves lists
        if nested:
            item = itemList[mid][0].lower()
        else:
            item = itemList[mid].lower()

        # if the item we are looking for is smaller than the mid point then reduce
        # the end range of our search, if the item is larger than the mid point then
        # increase the start point of our search
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
                # Find the position of this items record in our records list
                rIndex = binarySearch(records, rName, True)
                if rIndex < len(records) and records[rIndex][0] == rName:
                    # Find the position of this items band in this records band list
                    bIndex = binarySearch(records[rIndex][1], bName, True)
                    if bIndex < len(records[rIndex][1]) and records[rIndex][1][bIndex][0] == bName:
                        # Find where the festival should be inserted into in this bands festival list
                        fIndex = binarySearch(records[rIndex][1][bIndex][1], fName, False)
                        records[rIndex][1][bIndex][1].insert(fIndex, fName)
                    else:
                        # We have a new band so we insert into the records band list
                        newBand = [bName, [fName]]
                        records[rIndex][1].insert(bIndex, newBand)
                else:
                    if len(records) == 0:
                        # This is our first record
                        records = [[rName, [[bName, [fName]]]]]
                    else:
                        # This is a new record and so we insert it into our records list
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
