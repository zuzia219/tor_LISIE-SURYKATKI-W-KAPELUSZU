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

df_tx = dl.read_transactions()
df_views = dl.read_views()

#output_file("gmap.html")


#ustalamy fokus mapy (np na pierwszy punkt)
map_options = GMapOptions(lat=list(df_tx.loc[:100].latitude)[0], lng=list(df_tx.loc[:100].longitude)[0], map_type="roadmap", zoom=11)

#dane dla generacji losowych punktow
number  = 100
minLat = 50   #53
maxLat = 60   #56
minLon = 15   #18
maxLon = 20   #20

# generujemy punkty (losowe na razie)

#df_tx.iloc[1]['offer_id']
zakres = slice(0, 100)


source = ColumnDataSource(
         data=dict(lat=list(df_tx.loc[:100].latitude),
                   lon=list(df_tx.loc[:100].longitude),
                   desc=["costam", "jeszcze cos", "co innego", "jakis tekst"],
                   ref=list(df_tx.loc[:100].offer_id))
)
    
#dodamy wskazowki przy naajechaniu myszą
hover = HoverTool(tooltips=[
    ("desc", "@desc"),
])

#deklarujemy mapę
p = gmap("AIzaSyDfyuSoaKSveZClEteSEg8kPinO1fAdOc8", map_options, title="aaa", tools=[hover, 'pan', 'wheel_zoom', 'tap', 'box_zoom'])

#dodamy url'y dla kliknięć na markery
url = "http://allegro.pl/i@ref.html"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)  

#dodajemy punkty na mapę
p.circle(x="lon", y="lat", size=12, fill_color="blue", fill_alpha=0.8, source=source)

#funkcja zmieniajaca ilosc punktow (dla slidera)
def update_plot(attr, old, new):
    new_num = slider.value
    
    new_data=  dict(lat=list(df_tx.loc[:100].latitude),
                   lon=list(df_tx.loc[:100].longitude),
                   desc=["costam", "jeszcze cos", "co innego", "jakis tekst"],
                   ref=list(df_tx.loc[:100].offer_id))
    source.data = new_data
    p.title = str(new_num) + " punktow"
    
slider = Slider(start=1, end=100, value=number, step=1, title="numer of doots:")
slider.on_change('value', update_plot)

curdoc().add_root(column(slider, p))

#show(p)
