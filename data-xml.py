# Data Wrangling with MongoDB
# Lesson.2: Data in More Complex Format - XML

#===========================================

# Quiz: Extracting Data
#!/usr/bin/env python
# Your task here is to extract data from xml on authors of an article
# and add it to a list, one item for an author.
# See the provided data structure for the expected format.
# The tags for first name, surname and email should map directly
# to the dictionary keys
import xml.etree.ElementTree as ET

article_file = "exampleResearchArticle.xml"


def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def get_authors(root):
    authors = []
    for author in root.findall('./fm/bibl/aug/au'):
        data = {
                "fnm": None,
                "snm": None,
                "email": None,
                "insr": []
        }

        #data["fnm"] = author[1].text
        #data["snm"] = author[0].text
        #data["email"] = author[3].text

        data['fnm'] = author.find('./fnm').text
        data['snm'] = author.find('./snm').text
        data['email'] = author.find('./email').text
        insr_all = author.findall('./insr')
        for insr in insr_all:
            data['insr'].append(insr.attrib['iid'])

        authors.append(data)

    return authors


def test():
    solution = [{'fnm': 'Omer', 'snm': 'Mei-Dan', 'email': 'omer@extremegate.com'}, {'fnm': 'Mike', 'snm': 'Carmont', 'email': 'mcarmont@hotmail.com'}, {'fnm': 'Lior', 'snm': 'Laver', 'email': 'laver17@gmail.com'}, {'fnm': 'Meir', 'snm': 'Nyska', 'email': 'nyska@internet-zahav.net'}, {'fnm': 'Hagay', 'snm': 'Kammar', 'email': 'kammarh@gmail.com'}, {'fnm': 'Gideon', 'snm': 'Mann', 'email': 'gideon.mann.md@gmail.com'}, {'fnm': 'Barnaby', 'snm': 'Clarck', 'email': 'barns.nz@gmail.com'}, {'fnm': 'Eugene', 'snm': 'Kots', 'email': 'eukots@gmail.com'}]

    root = get_root(article_file)
    data = get_authors(root)

    assert data[0] == solution[0]
    assert data[1]["fnm"] == solution[1]["fnm"]


test()

#===========================
# Quiz: Using Beautiful Soup
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
from bs4 import BeautifulSoup
import requests
import json

html_page = "page_source.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        soup = BeautifulSoup(html, 'html.parser')

        #print soup.find(id="__EVENTVALIDATION" )
        data["eventvalidation"] = soup.find(id="__EVENTVALIDATION" )["value"]
        data["viewstate"] = soup.find(id="__VIEWSTATE" )["value"]

    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_data(html_page)
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")


test()


#===========================
# Problem Set
# Quiz: Carrier List
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Please note that the function 'make_request' is provided for your reference only.
You will not be able to to actually use it from within the Udacity web UI.
All your changes should be in the 'extract_carrier' function.
Also note that the html file is a stripped down version of what is actually on
the website.

Your task in this exercise is to get a list of all airlines. Exclude all of the
combination values like "All U.S. Carriers" from the data that you return.
You should return a list of codes for the carriers.
"""

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        carrier_selection = soup.find(id="CarrierList")
        #print carrier_selection
        carrier_list = carrier_selection.find_all('option')
        #print carrier_list

        for option in carrier_selection.find_all('option')[3:]:
            data.append(option['value'])

    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': airport,
                          'CarrierList': carrier,
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data

if __name__ == "__main__":
    test()

#===========================
# Problem Set
# Quiz: Airport List
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports' function so that it returns a list of airport
codes, excluding any combinations like "All".
"""

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        airport_select = soup.find(id='AirportList')
        airport_options = airport_select.find_all('option')
        for option in airport_options:
            if (len(option['value']) == 3) & (option['value'] != 'All'):
                data.append(option['value'])

        print len(data)
    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

if __name__ == "__main__":
    test()


#===========================
# Problem Set
# Quiz: Processing All
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Let's assume that you combined the code from the previous 2 exercises with code
from the lesson on how to build requests, and downloaded all the data locally.
The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
extract the flight data from that table as a list of dictionaries, each
dictionary containing relevant data from the file and table row. This is an
example of the data structure you should return:

data = [{"courier": "FL",
         "airport": "ATL",
         "year": 2012,
         "month": 12,
         "flights": {"domestic": 100,
                     "international": 100}
        },
         {"courier": "..."}
]

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.

There are couple of helper functions to deal with the data files.
Please do not change them for grading purposes.
All your changes should be in the 'process_file' function.
"""
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    info['flights'] = {}
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html, 'lxml')
        data_table = soup.find('table', class_='dataTDRight')
        data_rows = data_table.find_all('tr')[1:]
        count = 0
        #print len(data_rows)
        for row in data_rows:
            data_columns = row.find_all('td')
            #print (data_columns[2].text.replace(',', '')).isdigit()

            if data_columns[1].text != 'TOTAL':
                info['year'] = int(data_columns[0].text)
                info['month'] = int(data_columns[1].text)
                info['flights']['domestic'] = int(data_columns[2].text.replace(',',''))
                info['flights']['international'] = int(data_columns[3].text.replace(',', ''))
                data.append(info)
            else:
                count += 1

    #print len(data)
    #print count
    return data


def test():
    print "Running a simple test..."
    open_zip(datadir)
    files = process_all(datadir)
    print files

    data = []
    # Test will loop over three data files.
    for f in files:
        data += process_file(f)

    print len(data)
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

    print "... success!"

if __name__ == "__main__":
    test()


#===========================
# Problem Set
# Quiz: Patent Database


#===========================
# Problem Set
# Quiz: Result of Parsing the


#===========================
# Problem Set
# Quiz: Processing Patents
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.

    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    file_object = open(filename)
    patent_str = file_object.read()
    #xml_declaration = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v44-2013-05-16.dtd" [ ]>'
    #print len(xml_declaration)
    start_pos = 0
    end_pos = 0
    n = 0
    while start_pos >= 0:
        next_pos = patent_str.find('<?xml', start_pos + 1)
        new_filename = "{}-{}".format(filename , n)
        f = open(new_filename, 'w')
        f.write(patent_str[start_pos:next_pos])
        f.close
        start_pos = next_pos
        n += 1


    #for patent in patents:



def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()

