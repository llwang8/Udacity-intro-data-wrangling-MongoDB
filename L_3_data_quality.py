# Data Wrangling with MongoDB
# Lesson.3: Data Quality

#===========================================
# Quiz: Correcting Validity

"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):
    data_good = []
    data_bad = []

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        reader.next()
        reader.next()
        reader.next()

        for row in reader:
            if row['URI'].find('http://dbpedia.org') < 0:
                continue

            year = row['productionStartYear'][0:4]

            try:
                year = int(year)
                row['productionStartYear'] = year
                if (year < 1886) or (year > 2014):
                    data_bad.append(row)
                else:
                    data_good.append(row)
            except ValueError:
                if year == 'NULL':
                    data_bad.append(row)

    print len(data_good)
    print len(data_bad)

    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_good:
            writer.writerow(row)

    with open(output_bad, "w") as b:
        writer = csv.DictWriter(b, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_bad:
            writer.writerow(row)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()



#===========================================
# Problem Set Quiz: Auditing Data Quality
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['URI'].find('dbpedia.org') < 0:
                continue
            for field in fields:
                if field not in fieldtypes:
                    fieldtypes[field] = set()

                f_data = row[field]
                f_type = None

                #print row["URI"]

                if (f_data == 'NULL') or (f_data == ''):
                    f_type = type(None)
                elif f_data[0] == '{':
                    f_type = type([])
                else:
                    try:
                        f_data = int(f_data)
                    except ValueError:
                        try:
                            f_data = float(f_data)
                        except ValueError:
                            f_type = type(str())
                        else:
                            f_type = type(1.1)
                    else:
                        f_type = type(int())

                fieldtypes[field].add(f_type)

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()



#===========================================
# Problem Set Quiz: Making a Choice
# choose the more significiant value among 2


#===========================================
# Problem Set Quiz: Fixing the Area
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the
"areaLand" field, you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it
has to return a float representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you
like, but changes to process_file will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'


def fix_area(area):
    if area == 'NULL':
        return None
    elif area[0] == '{':        # if 2 values in a list
        a_list = area[1:-1].split('|')
        area = more_signigiciant(a_list)

    try:
        area = float(area)
    except ValueError:
        print area

    return area

def more_signigiciant(list):
    len0 = len(list[0])
    len1 = len(list[1])
    if len0 > len1:
        return list[0]
    else:
        return list[1]

    return value

def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data

def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0


if __name__ == "__main__":
    test()


#===========================================
# Problem Set Quiz: Other Fields



#===========================================
# Problem Set Quiz: Fixing Name
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

In the previous quiz you recognized that the "name" value can be an array (or
list in Python terms). It would make it easier to process and query the data
later if all values for the name are in a Python list, instead of being
just a string separated with special characters, like now.

Finish the function fix_name(). It will recieve a string as an input, and it
will return a list of all the names. If there is only one name, the list will
have only one item in it; if the name is "NULL", the list should be empty.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import pprint

CITIES = 'cities.csv'


def fix_name(name):
    name_list = []
    if name == 'NULL':
        name_list = []
    elif name[0] == '{':
        name_list += name[1:-1].split('|')
    else:
        name_list.append(name)

    print name_list
    return name_list


def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra metadata
        for i in range(3):
            l = reader.next()
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "name" in line:
                line["name"] = fix_name(line["name"])
            data.append(line)
    return data


def test():
    data = process_file(CITIES)

    print "Printing 20 results:"
    for n in range(20):
        pprint.pprint(data[n]["name"])

    assert data[14]["name"] == ['Negtemiut', 'Nightmute']
    assert data[9]["name"] == ['Pell City Alabama']
    assert data[3]["name"] == ['Kumhari']

if __name__ == "__main__":
    test()


#===========================================
# Problem Set Quiz: Crossfield Auditing
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

If you look at the full city data, you will notice that there are couple of
values that seem to provide the same information in different formats: "point"
seems to be the combination of "wgs84_pos#lat" and "wgs84_pos#long". However,
we do not know if that is the case and should check if they are equivalent.

Finish the function check_loc(). It will recieve 3 strings: first, the combined
value of "point" followed by the separate "wgs84_pos#" values. You have to
extract the lat and long values from the "point" argument and compare them to
the "wgs84_pos# values, returning True or False.

Note that you do not have to fix the values, only determine if they are
consistent. To fix them in this case you would need more information. Feel free
to discuss possible strategies for fixing this on the discussion forum.

The rest of the code is just an example on how this function can be used.
Changes to "process_file" function will not be taken into account for grading.
"""
import csv
import pprint

CITIES = 'cities.csv'


def check_loc(point, lat, longi):
    p_list = point.split(' ')
    if (p_list[0] == lat) & (p_list[1] == longi):
        return True
    else:
        return False

def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra matadata
        for i in range(3):
            l = reader.next()
        # processing file
        for line in reader:
            # calling your function to check the location
            result = check_loc(line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            if not result:
                print "{}: {} != {} {}".format(line["name"], line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            data.append(line)

    return data


def test():
    assert check_loc("33.08 75.28", "33.08", "75.28") == True
    assert check_loc("44.57833333333333 -91.21833333333333", "44.5783", "-91.2183") == False

if __name__ == "__main__":
    test()

#===========================================
# Problem Set Quiz: SQL or MongoDB?
