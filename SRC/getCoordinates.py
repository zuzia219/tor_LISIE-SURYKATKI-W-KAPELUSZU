# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:21:36 2018

@author: Andrew
"""

import urllib
import simplejson

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
apiKey = "AIzaSyC7duHJJJIHh0pQ1FHzxQn-xIZN_34Ut9g"

# funkcja dla otrzymania wspolrzednych miejsca
def get_coordinates(query, apiKey):
    query = query.encode('utf-8')
    params = {
        'address': query
    }
    url = googleGeocodeUrl + urllib.parse.urlencode(params) + "&key=" + apiKey
    json_response = urllib.request.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print (query, latitude, longitude)
    else:
        latitude, longitude = None, None
        return 0
    return latitude, longitude

# fucnkcja wczytania pliku z nazwami miast do listy
def getKeys(plik):
    miasta_list = []
    
    with open(plik) as f:
        miasta_list = f.readlines()
    
    miasta_list = [line.strip() for line in miasta_list]
    miasta_list = [line.replace("\n", "") for line in miasta_list]
    
    return miasta_list
    
# fucnkcja wygenerowania csv z miastami i ich wspolrzednymi
def genPlikWithCoords(miasta_list, plik):
    with open(plik, "w") as f:
        for miasto in miasta_list:
            while (True):
                coord = get_coordinates(miasto, apiKey)
                if (coord):
                    print (miasto + " " + str(coord))
                    break

            f.write(miasto + "," + str(coord[0]) + "," + str(coord[1]) + "\n")



## dla wygenerowania pliku:      
genPlikWithCoords(getKeys('miasta_nazwy.txt'), "miasta_wsp.txt")