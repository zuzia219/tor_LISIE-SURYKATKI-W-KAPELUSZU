# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:37 2018

@author: Andrew
"""
import random
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, TapTool, OpenURL
from bokeh.plotting import gmap

output_file("gmap.html")

#ustalamy fokus mapy
map_options = GMapOptions(lat=53.2900, lng=18.7000, map_type="roadmap", zoom=11)

#dane dla generacji losowych punktow
number  = 100
minLat = 50   #53
maxLat = 60   #56
minLon = 15   #18
maxLon = 20   #20

# generujemy punkty (losowe na razie)
source = ColumnDataSource(
    data=dict(lat=[ random.uniform(minLat, maxLat) for x in range (0, number) for y in range(0, number)],
              lon=[  random.uniform(minLon, maxLon) for x in range (0, number) for y in range(0, number)],
              desc=["costam", "jeszcze cos", "co innego", "jakis tekst"],
              ref=[random.randint(0,100) for x in range(0, 2) for y in range(0, number)])
)
    
#dodamy wskazowki przy naajechaniu myszą
hover = HoverTool(tooltips=[
    ("desc", "@desc"),
])

#deklarujemy mapę
p = gmap("AIzaSyDfyuSoaKSveZClEteSEg8kPinO1fAdOc8", map_options, title="aaa", tools=[hover, 'pan', 'wheel_zoom', 'tap', 'box_zoom'])

#dodamy url'y dla kliknięć na markery
url = "https://id-@ref-.allegrosandbox.pl/"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)  

#dodajemy punkty na mapę
p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

#show(p)