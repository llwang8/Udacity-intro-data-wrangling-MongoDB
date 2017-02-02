# To experiment with this code freely you will have to run this code locally.
# Take a look at the main() function for an example of how to use the code.
# We have provided example json output in the other code editor tabs for you to
# look at, but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    '''
    Modify the function calls and indexing below to answer the questions on
    the next quiz. HINT: Note how the output we get from the site is a
    multi-level JSON document, so try making print statements to step through
    the structure one level at a time or copy the output to a separate output
    file.
    '''
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    pretty_print(results)

    artist_id = results["artists"][1]["id"]
    #print "\nARTIST:"
    #pretty_print(results["artists"][1])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    #releases = artist_data["releases"]
    #print "\nONE RELEASE:"
    #pretty_print(releases[0], indent=2)
    #release_titles = [r["title"] for r in releases]

    #print "\nALL TITLES:"
    #for t in release_titles:
    #    print t

    #disambiguation = results['artists'][0]["disambiguation"] # for "NIRVANA"
    #print "NIRVANA disambiguation:"
    #print disambiguation

    begin_date = results["artists"][0]['life-span']['begin']
    print 'ONE DIRECTION formed on:'
    print begin_date

    #spanish_alias = results['artists'][0]['aliases']
    #print "Beatles spanish alias:"
    #print pretty_print(spanish_alias)

    #begin_area_name = results['artists'][0]['begin-area']['name']
    #print 'Begin-area-name for Queeen:'
    #print begin_area_name

    #count = len(results['artists'])
    #print "Number of bands named First Aid Kit:"
    #print count

if __name__ == '__main__':
    main()



# output
'''
{
    "artists": [
        {
            "aliases": [
                {
                    "begin-date": null,
                    "end-date": null,
                    "locale": null,
                    "name": "Nirvana US",
                    "primary": null,
                    "sort-name": "Nirvana US",
                    "type": null
                }
            ],
            "area": {
                "id": "489ce91b-6658-3307-9877-795b68554c98",
                "name": "United States",
                "sort-name": "United States"
            },
            "begin-area": {
                "id": "a640b45c-c173-49b1-8030-973603e895b5",
                "name": "Aberdeen",
                "sort-name": "Aberdeen"
            },
            "country": "US",
            "disambiguation": "90s US grunge band",
            "id": "5b11f4ce-a62d-471e-81fc-a69a8278c7da",
            "life-span": {
                "begin": "1988-01",
                "end": "1994-04-05",
                "ended": true
            },
            "name": "Nirvana",
            "score": "100",
            "sort-name": "Nirvana",
            "tags": [
                {
                    "count": 1,
                    "name": "punk"
                },
                {
                    "count": 0,
                    "name": "legendary"
                },
                {
                    "count": 0,
                    "name": "90"
                },
                {
                    "count": 1,
                    "name": "seattle"
                },
                {
                    "count": 0,
                    "name": "northwest"
                },
                {
                    "count": 0,
                    "name": "alternative"
                },
                {
                    "count": 0,
                    "name": "rock and indie"
                },
                {
                    "count": 1,
                    "name": "usa"
                },
                {
                    "count": 0,
                    "name": "am\u00e9ricain"
                },
                {
                    "count": 0,
                    "name": "united states"
                },
                {
                    "count": 0,
                    "name": "kurt cobain"
                },
                {
                    "count": 1,
                    "name": "90s"
                },
                {
                    "count": 4,
                    "name": "alternative rock"
                },
                {
                    "count": 0,
                    "name": "band"
                },
                {
                    "count": 14,
                    "name": "grunge"
                },
                {
                    "count": 9,
                    "name": "rock"
                },
                {
                    "count": 1,
                    "name": "acoustic rock"
                },
                {
                    "count": 1,
                    "name": "noise rock"
                },
                {
                    "count": 0,
                    "name": "nirvana"
                },
                {
                    "count": 5,
                    "name": "american"
                }
            ],
            "type": "Group"
        },
        {
            "area": {
                "id": "8a754a16-0027-3a29-b6d7-2b40ea0481ed",
                "name": "United Kingdom",
                "sort-name": "United Kingdom"
            },
            "begin-area": {
                "id": "f03d09b3-39dc-4083-afd6-159e3f0d462f",
                "name": "London",
                "sort-name": "London"
            },
            "country": "GB",
            "disambiguation": "60s band from the UK",
            "id": "9282c8b4-ca0b-4c6b-b7e3-4f7762dfc4d6",
            "life-span": {
                "begin": "1967",
                "ended": null
            },
            "name": "Nirvana",
            "score": "100",
            "sort-name": "Nirvana",
            "tags": [
                {
                    "count": 1,
                    "name": "rock"
                },
                {
                    "count": 1,
                    "name": "pop"
                },
                {
                    "count": 1,
                    "name": "progressive rock"
                },
                {
                    "count": 1,
                    "name": "orchestral"
                },
                {
                    "count": 1,
                    "name": "british"
                },
                {
                    "count": 1,
                    "name": "power pop"
                },
                {
                    "count": 1,
                    "name": "psychedelic rock"
                },
                {
                    "count": 1,
                    "name": "soft rock"
                },
                {
                    "count": 1,
                    "name": "symphonic rock"
                },
                {
                    "count": 1,
                    "name": "english"
                }
            ],
            "type": "Group"
        },
        {
            "area": {
                "id": "6a264f94-6ff1-30b1-9a81-41f7bfabd616",
                "name": "Finland",
                "sort-name": "Finland"
            },
            "country": "FI",
            "disambiguation": "Early 1980's Finnish punk band",
            "id": "85af0709-95db-4fbc-801a-120e9f4766d0",
            "life-span": {
                "ended": null
            },
            "name": "Nirvana",
            "score": "100",
            "sort-name": "Nirvana",
            "tags": [
                {
                    "count": 1,
                    "name": "punk"
                },
                {
                    "count": 1,
                    "name": "finland"
                }
            ],
            "type": "Group"
        },
        {
            "disambiguation": "French band from Martigues, activ during the 70s.",
            "id": "c49d69dc-e008-47cf-b5ff-160fafb1fe1f",
            "life-span": {
                "ended": null
            },
            "name": "Nirvana",
            "score": "100",
            "sort-name": "Nirvana"
        },
        {
            "disambiguation": "founded in 1987 by a Michael Jackson double/imitator",
            "id": "3aa878c0-224b-41e5-abd1-63be359d2bca",
            "life-span": {
                "begin": "1987",
                "ended": null
            },
            "name": "Nirvana",
            "score": "100",
            "sort-name": "Nirvana"
        },
        {
            "id": "b305320e-c158-43f4-b5be-4450e2f99a32",
            "life-span": {
                "ended": null
            },
            "name": "El Nirvana",
            "score": "62",
            "sort-name": "Nirvana, El"
        },
        {
            "aliases": [
                {
                    "begin-date": null,
                    "end-date": null,
                    "locale": null,
                    "name": "Nirvana",
                    "primary": null,
                    "sort-name": "Nirvana",
                    "type": null
                },
                {
                    "begin-date": null,
                    "end-date": null,
                    "locale": null,
                    "name": "Prophet 2002",
                    "primary": null,
                    "sort-name": "Prophet 2002",
                    "type": null
                }
            ],
            "area": {
                "id": "23d10872-f5ae-3f0c-bf55-332788a16ecb",
                "name": "Sweden",
                "sort-name": "Sweden"
            },
            "country": "SE",
            "disambiguation": "Swedish death metal band",
            "id": "f2dfdff9-3862-4be0-bf85-9c833fa3059e",
            "life-span": {
                "begin": "1988",
                "ended": null
            },
            "name": "Nirvana 2002",
            "score": "62",
            "sort-name": "Nirvana 2002",
            "type": "Group"
        },
        {
            "id": "329c04ae-3b73-4ca3-996f-75608ab1befb",
            "life-span": {
                "ended": null
            },
            "name": "Nirvana Singh",
            "score": "62",
            "sort-name": "Singh, Nirvana",
            "type": "Person"
        },
        {
            "area": {
                "id": "489ce91b-6658-3307-9877-795b68554c98",
                "name": "United States",
                "sort-name": "United States"
            },
            "country": "US",
            "id": "c3a64a25-251b-4d03-afba-1471440245b8",
            "life-span": {
                "begin": "2009",
                "ended": null
            },
            "name": "Approaching Nirvana",
            "score": "62",
            "sort-name": "Approaching Nirvana",
            "type": "Group"
        },
        {
            "area": {
                "id": "489ce91b-6658-3307-9877-795b68554c98",
                "name": "United States",
                "sort-name": "United States"
            },
            "country": "US",
            "gender": "female",
            "id": "206419e0-3a7a-49ce-8437-4e757767d02b",
            "life-span": {
                "ended": null
            },
            "name": "Nirvana Savoury",
            "score": "62",
            "sort-name": "Savoury, Nirvana",
            "type": "Person"
        },
        {
            "id": "86f9ae24-ba2a-4d55-9275-0b89b85f6e3a",
            "life-span": {
                "ended": null
            },
            "name": "Weed Nirvana",
            "score": "62",
            "sort-name": "Weed Nirvana"
        },
        {
            "area": {
                "id": "e8ad73e9-9e7f-41c4-a395-6e29260ff1df",
                "name": "Graz",
                "sort-name": "Graz"
            },
            "begin-area": {
                "id": "e8ad73e9-9e7f-41c4-a395-6e29260ff1df",
                "name": "Graz",
                "sort-name": "Graz"
            },
            "disambiguation": "Nirvana-Coverband",
            "id": "46d8dae4-abec-438b-9c62-a3dbb2aaa1b7",
            "life-span": {
                "begin": "2000",
                "ended": null
            },
            "name": "Nirvana Teen Spirit",
            "score": "50",
            "sort-name": "Nirvana Teen Spirit",
            "type": "Group"
        },
        {
            "area": {
                "id": "c621114d-73cc-4832-8afe-f13dc261e5af",
                "name": "Gatineau",
                "sort-name": "Gatineau"
            },
            "begin-area": {
                "id": "c621114d-73cc-4832-8afe-f13dc261e5af",
                "name": "Gatineau",
                "sort-name": "Gatineau"
            },
            "id": "02c4e6bb-7b7a-4686-8c23-df01bfd42b0e",
            "life-span": {
                "begin": "2012-04-05",
                "ended": null
            },
            "name": "Sappy Nirvana Tribute",
            "score": "50",
            "sort-name": "Sappy Nirvana Tribute",
            "type": "Group"
        },
        {
            "id": "bb94730d-22c2-422d-a0a7-fe16a5b3e429",
            "life-span": {
                "ended": null
            },
            "name": "The Attainment of Nirvana",
            "score": "50",
            "sort-name": "Attainment of Nirvana, The"
        },
        {
            "id": "e1388435-f80d-434a-9980-f1c9f5aa9b90",
            "life-span": {
                "ended": null
            },
            "name": "Nirvana Sitar & String Group",
            "score": "43",
            "sort-name": "Nirvana Sitar & String Group"
        }
    ],
    "count": 15,
    "created": "2016-10-18T12:55:39.696Z",
    "offset": 0
}

ARTIST:
{
    "area": {
        "id": "8a754a16-0027-3a29-b6d7-2b40ea0481ed",
        "name": "United Kingdom",
        "sort-name": "United Kingdom"
    },
    "begin-area": {
        "id": "f03d09b3-39dc-4083-afd6-159e3f0d462f",
        "name": "London",
        "sort-name": "London"
    },
    "country": "GB",
    "disambiguation": "60s band from the UK",
    "id": "9282c8b4-ca0b-4c6b-b7e3-4f7762dfc4d6",
    "life-span": {
        "begin": "1967",
        "ended": null
    },
    "name": "Nirvana",
    "score": "100",
    "sort-name": "Nirvana",
    "tags": [
        {
            "count": 1,
            "name": "rock"
        },
        {
            "count": 1,
            "name": "pop"
        },
        {
            "count": 1,
            "name": "progressive rock"
        },
        {
            "count": 1,
            "name": "orchestral"
        },
        {
            "count": 1,
            "name": "british"
        },
        {
            "count": 1,
            "name": "power pop"
        },
        {
            "count": 1,
            "name": "psychedelic rock"
        },
        {
            "count": 1,
            "name": "soft rock"
        },
        {
            "count": 1,
            "name": "symphonic rock"
        },
        {
            "count": 1,
            "name": "english"
        }
    ],
    "type": "Group"
}
requesting http://musicbrainz.org/ws/2/artist/9282c8b4-ca0b-4c6b-b7e3-4f7762dfc4d6?fmt=json&inc=releases

ONE RELEASE:
{
  "barcode": null,
  "country": "GB",
  "date": "1969",
  "disambiguation": "",
  "id": "0b44cb36-550a-491d-bfd9-8751271f9de7",
  "packaging": null,
  "packaging-id": null,
  "quality": "normal",
  "release-events": [
    {
      "area": {
        "disambiguation": "",
        "id": "8a754a16-0027-3a29-b6d7-2b40ea0481ed",
        "iso-3166-1-codes": [
          "GB"
        ],
        "name": "United Kingdom",
        "sort-name": "United Kingdom"
      },
      "date": "1969"
    }
  ],
  "status": "Official",
  "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
  "text-representation": {
    "language": "eng",
    "script": "Latn"
  },
  "title": "To Markos III"
}

ALL TITLES:
To Markos III
Travelling on a Cloud
Songs Of Love And Praise
Songs of Love and Praise
Songs of Love and Praise
Secret Theatre
The Story of Simon Simopath
Me And My Friend
All of Us
The Story of Simon Simopath
To Markos III
Chemistry
Local Anaesthetic
Orange & Blue
Pentecost Hotel
Black Flower
All of Us
'''


