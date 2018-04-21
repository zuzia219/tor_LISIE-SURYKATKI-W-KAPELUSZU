# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:37 2018

@author: Andrew
"""
import random
from bokeh.io import output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import (Button, Slider,
        ColumnDataSource, GMapOptions, 
        HoverTool, TapTool, OpenURL)
from bokeh.plotting import gmap, curdoc,figure
from bokeh.layouts import column, row, widgetbox
import pandas as pd
import data_load as dl
from os import path
from datetime import date, datetime

df_tx = dl.read_transactions()
df_views = dl.read_views()



#ustalamy fokus mapy (np na pierwszy punkt)
map_options = GMapOptions(lat=list(df_tx.loc[:1].latitude)[0], lng=list(df_tx.loc[:1].longitude)[0], map_type="roadmap", zoom=11)

n_points  = 500
categories_path = path.join('DATA','categories.csv')

categories = pd.read_table(categories_path, names = ['id_kategorii', 'id_rodzica', 'nazwa'])

#data_with_categories  = pd.merge(data, categories, left_on='category_id', right_on='id_kategorii') 


source_transactions = ColumnDataSource(data={
    'lon'       : df_tx['longitude'].loc[:1],
    'lat'       : df_tx['latitude'].loc[:1],
    'category'  : df_tx['category_id'].loc[:1],
    'ref'       : df_tx['offer_id'].loc[:1]
})

source_views = ColumnDataSource(data={
    'lon'       : df_views['longitude'].loc[:1],
    'lat'       : df_views['latitude'].loc[:1],
    'category'  : df_views['category_id'].loc[:1],
    'ref'       : df_views['offer_id'].loc[:1]
})

#dodamy wskazowki przy naajechaniu myszą
hover_tx = HoverTool(names = ["tx"], 
        tooltips=[
    ("tx", ""),
    ("lat", "@lat"),
    ("lon", "@lon"),
    ("category", "@category"),
    ("ref", "@offer_id")
])

#dodamy wskazowki przy naajechaniu myszą
hover_views = HoverTool(names = ["views"], 
        tooltips=[
    ("views", ""),
    ("lat", "@lat"),
    ("lon", "@lon"),
    ("category", "@category"),
    ("ref", "@offer_id")
])

#deklarujemy mapę
p1 = gmap("AIzaSyDfyuSoaKSveZClEteSEg8kPinO1fAdOc8", map_options, title="Views and transactions", tools=[hover_tx, hover_views, 'pan', 'wheel_zoom', 'tap', 'box_zoom'])

#dodamy url'y dla kliknięć na markery
url = "http://allegro.pl/i@ref.html"
taptool = p1.select(type=TapTool)
taptool.callback = OpenURL(url=url)

#dodajemy punkty transakcji na mapę
tx_circles = p1.circle(x="lon", y="lat", name="tx", size=10, fill_color="blue", fill_alpha=0.8, source=source_transactions)
#tx_circles.select(dict(type=HoverTool)).tooltips = {"lat": "@lat","lon": "@lon"}

#dodajemy punkty wyswietlen na mapę
views_squares = p1.square(x="lon", y="lat", name="views", size=10, fill_color="orange", fill_alpha=0.8, source=source_views)
#views_squares.select(dict(type=HoverTool)).tooltips = { "category": "@category"}

#slider czasu
def update_plot_time(attr, old, new):
  # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider_time.value
    #x_range
    #y_range

    data_slice = df_tx[(df_tx['ttimestamp']<(min_timestamp+yr)) & (df_tx['ttimestamp']>(min_timestamp-yr)) ].loc[:100]
    new_data_transactions = {
       'lon'       : data_slice['longitude'],
       'lat'       : data_slice['latitude'],
       'category'  : data_slice['category_id']
    }
    source_transactions.data = new_data_transactions

    data_slice = df_views[(df_views['ttimestamp']<(min_timestamp+yr)) & (df_views['ttimestamp']>(min_timestamp-yr)) ].loc[:100]
    new_data_views = {
       'lon'       : data_slice['longitude'],
       'lat'       : data_slice['latitude'],
       'category'  : data_slice['category_id']
    }
    source_views.data = new_data_views

# Make a slider object: slider
min_timestamp = min(df_tx['ttimestamp'].min(), df_views['ttimestamp'].min())
max_timestamp = max(df_tx['ttimestamp'].max(), df_views['ttimestamp'].max())

slider_time = Slider(start=0, end=max_timestamp-min_timestamp, step=3600, value=0, title='Timestamp', format="{://360}")

# Attach the callback to the 'value' property of slider
slider_time.on_change('value', update_plot_time)

tab1 = Panel(child=p1, title="Map")

p2 = figure(plot_width = 300, plot_height=300)

tab2 = Panel(child=p2, title="Events count")

tabs = Tabs(tabs=[tab1,tab2])

curdoc().add_root(row(widgetbox(slider_time), tabs))

