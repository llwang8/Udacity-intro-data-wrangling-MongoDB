# Data Wrangling with MongoDB
# Lesson.1: Data Extraction Fundation

#===========================================

# Quiz: Parsing CSV Files

# Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
# split each line on "," and then for each line, create a dictionary
# where the key is the header title of the field, and the value is the value of that field in the row.
# The function parse_file should return a list of dictionaries,
# each data line in the file being a single list entry.
# Field names and values should not contain extra whitespace, like spaces or newline characters.
# You can use the Python string method strip() to remove the extra whitespace.
# You have to parse only the first 10 data lines in this exercise,
# so the returned list should have 10 entries!
import os

DATADIR = ""
DATAFILE = "beatles-diskography.csv"


def parse_file(datafile):
    data = []
    n = 0
    with open(datafile, "r") as f:
        header = f.readline().split(',')
        for line in f:
            entry = {}
            if (n < 10):
                field = line.split(',')
                for i, value in enumerate(field):
                    entry[header[i].strip()] = value.strip()

                n += 1
                data.append(entry)

    print data[0]
    print data[9]
    return data


def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

test()

#==================================
# Quiz: Reading Excel Files
#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    maxval = None
    minval = None
    maxtime = None
    mintime = None
    total = 0

    ### example on how you can get the data
    data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    cval = sheet.col_values(1, start_rowx=1, end_rowx=None)

    maxval = max(cval)
    minval = min(cval)

    maxpos = cval.index(maxval) + 1
    minpos = cval.index(minval) + 1

    maxtime = sheet.cell_value(maxpos, 0)
    mintime = sheet.cell_value(minpos, 0)

    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:",
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):",
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):",
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):",
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)


    data = {
            'maxtime': xlrd.xldate_as_tuple(maxtime, 0),
            'maxvalue': maxval,
            'mintime': xlrd.xldate_as_tuple(mintime, 0),
            'minvalue': minval,
            'avgcoast': sum(cval) / float(len(cval))
    }

    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()


#==================================
# Problem Set Quiz: Using CSV Module
#!/usr/bin/env python
"""
Your task is to process the supplied file and use the csv module to extract data from it.
The data comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. You should extract the name of the station from it.

The data should be returned as a list of lists (not dictionaries).
You can use the csv modules "reader" method to get data in such format.
Another useful method is next() - to get the next line from the iterator.
You should only change the parse_file function.
"""
import csv
import os

DATADIR = ""
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'rb') as f:
        name = f.readline().strip().split(',')[1]
        #name = "MOUNTAIN VIEW MOFFETT FLD NAS"
        header = f.next()
        #print header

        print name
        print name == "MOUNTAIN VIEW MOFFETT FLD NAS"
        print "MOUNTAIN VIEW MOFFETT FLD NAS" == "MOUNTAIN VIEW MOFFETT FLD NAS"

        for line in f:
            data.append(line.strip().split(','))
        print data[97]
        print len(data)
    # Do not change the line below
    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()



#==================================
# Problem Set Quiz: Exel To CSV
# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile
import re

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    # print sheet.col_values(1, start_rowx=1, end_rowx=3)
    station_col = None
    station_name = None
    max_load = None
    max_pos = None
    max_hour_end = None
    headers = [str(cell.value) for cell in sheet.row(0)]

    data = [['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']]
    for i in range(1, 9):
        entry = []
        station_col = sheet.col_values(i, start_rowx=1, end_rowx=None)
        station_name = headers[i]
        #print station_name
        max_load = max(station_col)
        max_pos = station_col.index(max_load) + 1
        max_hour_end = sheet.cell_value(max_pos, 0)
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(max_hour_end, 0)

        entry.append(station_name)
        entry.append(year)
        entry.append(month)
        entry.append(day)
        entry.append(hour)
        entry.append(max_load)
        data.append(entry)

    print data
    print len(data)
    return data

def save_file(data, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        for line in data:
            writer.writerow(line)

def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            print line
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()




#==================================
# Problem Set Quiz: Wrangling JSON
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This exercise shows some important concepts that you should be aware about:
- using codecs module to write unicode files
- using authentication with web APIs
- using offset when accessing web APIs

To run this code locally you have to register at the NYTimes developer site
and get your own API key. You will be able to complete this exercise in our UI
without doing so, as we have provided a sample result.

Your task is to process the saved file that represents the most popular
articles (by view count) from the last day, and return the following data:
- list of dictionaries, where the dictionary key is "section" and value is "title"
- list of URLs for all media entries with "format": "Standard Thumbnail"

All your changes should be in the article_overview function.
The rest of functions are provided for your convenience, if you want to access
the API by yourself.
"""
import json
import codecs
import requests

URL_MAIN = "http://api.nytimes.com/svc/"
URL_POPULAR = URL_MAIN + "mostpopular/v2/"
API_KEY = { "popular": "",
            "article": ""}


def get_from_file(kind, period):
    filename = "popular-{0}-{1}.json".format(kind, period)
    with open(filename, "r") as f:
        return json.loads(f.read())


def article_overview(kind, period):
    data = get_from_file(kind, period)
    titles = []
    urls =[]
    i, j, k = 0, 0, 0

    #print data[0]['title']
    for article in data:
        title = article['title']
        section = article['section']
        titles.append({section: title})
        for media in article['media']:
            for mdata in media['media-metadata']:
                    if mdata['format'] == 'Standard Thumbnail':
                        urls.append(mdata['url'])

    return (titles, urls)


def query_site(url, target, offset):
    # This will set up the query with the API key and offset
    # Web services often use offset paramter to return data in small chunks
    # NYTimes returns 20 articles per request, if you want the next 20
    # You have to provide the offset parameter
    if API_KEY["popular"] == "" or API_KEY["article"] == "":
        print "You need to register for NYTimes Developer account to run this program."
        print "See Intructor notes for information"
        return False
    params = {"api-key": API_KEY[target], "offset": offset}
    r = requests.get(url, params = params)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def get_popular(url, kind, days, section="all-sections", offset=0):
    # This function will construct the query according to the requirements of the site
    # and return the data, or print an error message if called incorrectly
    if days not in [1,7,30]:
        print "Time period can be 1,7, 30 days only"
        return False
    if kind not in ["viewed", "shared", "emailed"]:
        print "kind can be only one of viewed/shared/emailed"
        return False

    url += "most{0}/{1}/{2}.json".format(kind, section, days)
    data = query_site(url, "popular", offset)

    return data


def save_file(kind, period):
    # This will process all results, by calling the API repeatedly with supplied offset value,
    # combine the data and then write all results in a file.
    data = get_popular(URL_POPULAR, "viewed", 1)
    num_results = data["num_results"]
    full_data = []
    with codecs.open("popular-{0}-{1}.json".format(kind, period), encoding='utf-8', mode='w') as v:
        for offset in range(0, num_results, 20):
            data = get_popular(URL_POPULAR, kind, period, offset=offset)
            full_data += data["results"]

        v.write(json.dumps(full_data, indent=2))


def test():
    titles, urls = article_overview("viewed", 1)
    assert len(titles) == 20
    assert len(urls) == 30
    assert titles[2] == {'Opinion': 'Professors, We Need You!'}
    assert urls[20] == 'http://graphics8.nytimes.com/images/2014/02/17/sports/ICEDANCE/ICEDANCE-thumbStandard.jpg'


if __name__ == "__main__":
    test()


#==================================




#==================================





#==================================




#==================================