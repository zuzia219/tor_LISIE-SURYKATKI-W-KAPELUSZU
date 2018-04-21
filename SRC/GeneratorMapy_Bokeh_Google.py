# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:37 2018

@author: Andrew
"""
import random
from bokeh.io import output_file, show
from bokeh.models.widgets import DateSlider
from bokeh.models import (Button, Slider,
        ColumnDataSource, GMapOptions, 
        HoverTool, TapTool, OpenURL)
from bokeh.plotting import gmap, curdoc
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

df_transactions = dl.read_transactions()
categories = pd.read_table(categories_path, names = ['id_kategorii', 'id_rodzica', 'nazwa'])

#data_with_categories  = pd.merge(data, categories, left_on='category_id', right_on='id_kategorii') 


source = ColumnDataSource(data={
    'lon'       : df_transactions['longitude'].loc[:1],
    'lat'       : df_transactions['latitude'].loc[:1],
    'category'  : df_transactions['category_id'].loc[:1],
    'ref'       : df_transactions['offer_id'].loc[:1]
})

#dodamy wskazowki przy naajechaniu myszą
hover = HoverTool(tooltips=[
    ("lat", "@lat"),
    ("lon", "@lon"),
    ("category", "@category"),
    ("ref", "@offer_id")
])

#deklarujemy mapę
p = gmap("AIzaSyDfyuSoaKSveZClEteSEg8kPinO1fAdOc8", map_options, title="aaa", tools=[hover, 'pan', 'wheel_zoom', 'tap', 'box_zoom'])

#dodamy url'y dla kliknięć na markery
url = "http://allegro.pl/i@ref.html"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

#dodajemy punkty na mapę
p.circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=0.8, source=source)

#funkcja zmieniajaca ilosc punktow (dla slidera)
def update_plot(attr, old, new):
    new_num = slider.value
    
    new_data=  dict(lat=list(df_tx.loc[:new_num].latitude),
                   lon=list(df_tx.loc[:new_num].longitude),
                   ref=list(df_tx.loc[:new_num].offer_id))
    source.data = new_data
    p.title = str(new_num) + " punktow"
    
slider = Slider(start=1, end=100, value=n_points, step=1, title="numer of doots:")
slider.on_change('value', update_plot)

#slider czasu
def update_plot_time(attr, old, new):
  # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider_time.value
    data_slice = df_transactions[(df_transactions['ttimestamp']<(min_timestamp+yr)) & (df_transactions['ttimestamp']>(min_timestamp-yr)) ].loc[:100]
    print(yr, data_slice)
    new_data = {
       'lon'       : data_slice['longitude'],
       'lat'       : data_slice['latitude'],
       'category'  : data_slice['category_id']
      #'x'       : data.loc[yr].fertility,
      #'y'       : data.loc[yr].life,
      #'country' : data.loc[yr].Country,
      #'pop'     : (data.loc[yr].population / 20000000) + 2,
      #'region'  : data.loc[yr].region,
    }
    source.data = new_data


# Make a slider object: slider
min_timestamp = min(df_tx['ttimestamp'].min(), df_views['ttimestamp'].min())
max_timestamp = max(df_tx['ttimestamp'].max(), df_views['ttimestamp'].max())

slider_time = Slider(start=0, end=max_timestamp-min_timestamp, step=3600, value=0, title='Timestamp', format="{://360}")

# Attach the callback to the 'value' property of slider
slider_time.on_change('value', update_plot_time)

curdoc().add_root(row(widgetbox(slider, slider_time), p))


# Make a row layout of widgetbox(slider) and plot and add it to the current document
#date_range_slider = DateRangeSlider(title="Date Range: ", start=date(2017, 1, 1), end=date.today(), value=(date(2017, 9, 7), date(2017, 10, 15)), step=1)
#curdoc().add_root(column(date_range_slider))


#show(p)
