# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:37 2018

@author: Andrew
"""
import random
from bokeh.io import output_file, show
from bokeh.models import Button, Slider
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, TapTool, OpenURL
from bokeh.plotting import gmap, curdoc
from bokeh.layouts import column
import pandas as pd
import data_load as dl
from os import path
#output_file("gmap.html")


#ustalamy fokus mapy
map_options = GMapOptions(lat=53.2900, lng=18.7000, map_type="roadmap", zoom=11)

n_points  = 100
categories_path = path.join('DATA','categories.csv')

data = dl.read_transactions()
categories = pd.read_table(categories_path, names = ['id_kategorii', 'id_rodzica', 'nazwa'])

#data_with_categories  = pd.merge(data, categories, left_on='category_id', right_on='id_kategorii') 


source = ColumnDataSource(data={
    'lon'       : data['longitude'].loc[:n_points],
    'lat'       : data['latitude'].loc[:n_points],
    'category' : data['category_id'].loc[:n_points],
})
#dodamy wskazowki przy naajechaniu myszą
hover = HoverTool(tooltips=[
    ("desc", "@desc"),
    ("lat", "@lat"),
    ("lon", "@lon"),
    ("category", "@category")
])

#deklarujemy mapę
p = gmap("AIzaSyDfyuSoaKSveZClEteSEg8kPinO1fAdOc8", map_options, title="aaa", tools=[hover, 'pan', 'wheel_zoom', 'tap', 'box_zoom'])

#dodamy url'y dla kliknięć na markery
url = "http://allegro.pl/i@.html"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)  

#dodajemy punkty na mapę
p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

#funkcja zmieniajaca ilosc punktow (dla slidera)
def update_plot(attr, old, new):
    new_num = slider.value
    
    new_data=dict(lat=[random.uniform(minLat, maxLat) for x in range (0, new_num) for y in range(0, n_points)],
                  lon=[random.uniform(minLon, maxLon) for x in range (0, new_num) for y in range(0, n_points)],
                  desc=["costam", "jeszcze cos", "co innego", "jakis tekst"],
                  ref=[random.randint(0,100) for x in range(0, 2) for y in range(0, new_num)])
    source.data = new_data
    p.title = str(new_num) + " punktow"
    
slider = Slider(start=1, end=100, value=n_points, step=1, title="numer of doots:")
slider.on_change('value', update_plot)

curdoc().add_root(column(slider, p))

#show(p)
