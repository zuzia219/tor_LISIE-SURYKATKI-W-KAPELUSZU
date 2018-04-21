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
from datetime import date

df_tx = dl.read_transactions()
df_views = dl.read_views()



#output_file("gmap.html")


#ustalamy fokus mapy (np na pierwszy punkt)
map_options = GMapOptions(lat=list(df_tx.loc[:100].latitude)[0], lng=list(df_tx.loc[:100].longitude)[0], map_type="roadmap", zoom=11)

n_points  = 500
categories_path = path.join('DATA','categories.csv')

data = dl.read_transactions()
categories = pd.read_table(categories_path, names = ['id_kategorii', 'id_rodzica', 'nazwa'])

#data_with_categories  = pd.merge(data, categories, left_on='category_id', right_on='id_kategorii') 


source = ColumnDataSource(data={
    'lon'       : data['longitude'].loc[:n_points],
    'lat'       : data['latitude'].loc[:n_points],
    'category'  : data['category_id'].loc[:n_points],
    'ref'       : data['offer_id'].loc[:n_points]
})

#dodamy wskazowki przy naajechaniu myszą
hover = HoverTool(tooltips=[
    ("desc", "@desc"),
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
                   desc=["costam", "jeszcze cos", "co innego", "jakis tekst"],
                   ref=list(df_tx.loc[:new_num].offer_id))
    source.data = new_data
    p.title = str(new_num) + " punktow"
    
slider = Slider(start=1, end=100, value=n_points, step=1, title="numer of doots:")
slider.on_change('value', update_plot)

curdoc().add_root(column(slider, p))

#slider czasu
# Define the callback function: update_plot
def update_plot_2(attr, old, new):
  # set the `yr` name to `slider.value` and `source.data = new_data`
  yr = slider.value
  new_data = {
      #'x'       : data.loc[yr].fertility,
      #'y'       : data.loc[yr].life,
      #'country' : data.loc[yr].Country,
      #'pop'     : (data.loc[yr].population / 20000000) + 2,
      #'region'  : data.loc[yr].region,
  }
  source.data = new_data


# Make a slider object: slider
slider = Slider(start=date(2018, 4, 9), end=date.today(), step=1, value=(date(2018, 4, 9), date.today()), title='Date')

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Make a row layout of widgetbox(slider) and plot and add it to the current document
curdoc().add_root(slider)
#date_range_slider = DateRangeSlider(title="Date Range: ", start=date(2017, 1, 1), end=date.today(), value=(date(2017, 9, 7), date(2017, 10, 15)), step=1)
#curdoc().add_root(column(date_range_slider))


#show(p)
