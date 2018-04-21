# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:37 2018

@author: Andrew
"""
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import (Button, Slider,
        ColumnDataSource, GMapOptions,
        HoverTool, TapTool, OpenURL)
from bokeh.plotting import gmap, curdoc,figure
from bokeh.layouts import row, widgetbox
import pandas as pd
import data_load as dl
from os import path

df_tx = dl.read_transactions()
df_views = dl.read_views()

print(type(df_tx), type(df_views))
#ustalamy fokus mapy (np na pierwszy punkt)
map_options = GMapOptions(lat=53.0, lng=18.6, map_type="roadmap", zoom=8)

categories_path = path.join('DATA','categories.csv')

categories = pd.read_table(categories_path, names = ['category_id', 'id_rodzica', 'nazwa'])

print(categories.info())


print(categories.columns)
#data_with_categories  = df_tx.merge( categories, left_on='category_id', right_on='id_kategorii') 
#data_with_categories  = df_tx.merge( categories) 
#print(data_with_categories.head())

source_transactions = ColumnDataSource(data={
    'category'  : df_tx['category_id'].loc[:1],
    'lat'       : df_tx['latitude'].loc[:1],
    'lon'       : df_tx['longitude'].loc[:1],
    'quantity'  : df_tx['item_quantity'].loc[:1],
    'imgs':[
        'https://image.flaticon.com/icons/svg/31/31624.svg',
    ]
})

source_views = ColumnDataSource(data={
    'category'  : df_views['category_id'].loc[:1],
    'lat'       : df_views['latitude'].loc[:1],
    'lon'       : df_views['longitude'].loc[:1],
    'imgs':[
        'https://image.flaticon.com/icons/svg/31/31624.svg',
    ]
})
#dodamy wskazowki przy naajechaniu myszą
hover_tx = HoverTool(tooltips="""
    <div>
        <div>
            <img
                src="@imgs" height="20" alt="@imgs" width="20"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 14px; font-weight: bold;">lat: @lat</span><br>
            <span style="font-size: 14px; font-weight: bold;">lon: @lon</span><br>
            <span style="font-size: 14px; font-weight: bold;">pcs: @quantity</span><br>
            <span style="font-size: 14px; font-weight: bold;">category: @category</span><br>
        </div>
    </div>
    """
)

#dodamy wskazowki przy naajechaniu myszą
hover_views = HoverTool(tooltips="""
    <div>
        <div>
            <img
                src="@imgs" height="20" alt="@imgs" width="20"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 14px; font-weight: bold;">lat: @lat</span><br>
            <span style="font-size: 14px; font-weight: bold;">lon: @lon</span><br>
            <span style="font-size: 14px; font-weight: bold;">category: @category</span><br>
        </div>
    </div>
    """
)

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
    imgs_transaction = ['https://image.flaticon.com/icons/svg/31/31624.svg' for _ in range(len(data_slice))]
    new_data_transactions = {
       'category'  : data_slice['category_id'],
       'quantity'  : data_slice['item_quantity'],
        'lat'       : data_slice['latitude'],
        'lon'       : data_slice['longitude'],
       'imgs'      : imgs_transaction
    }
    source_transactions.data = new_data_transactions

    data_slice = df_views[(df_views['ttimestamp']<(min_timestamp+yr)) & (df_views['ttimestamp']>(min_timestamp-yr)) ].loc[:100]
    imgs_views = ['http://simpleicon.com/wp-content/uploads/basket.svg' for _ in range(len(data_slice))]
    new_data_views = {
       'category'  : data_slice['category_id'],
        'lat'       : data_slice['latitude'],
        'lon'       : data_slice['longitude'],
       'imgs'      : imgs_views
    }
    source_views.data = new_data_views

# Make a slider object: slider
min_timestamp = min(df_tx['ttimestamp'].min(), df_views['ttimestamp'].min())
max_timestamp = max(df_tx['ttimestamp'].max(), df_views['ttimestamp'].max())

slider_time = Slider(start=0, end=max_timestamp-min_timestamp, step=3600, value=0, title='Timestamp', format="{://360}")

# Attach the callback to the 'value' property of slider
slider_time.on_change('value', update_plot_time)

tab1 = Panel(child=p1, title="Map")

p2 = figure(plot_width = 500, plot_height=500)

bin_number = (lambda x: 96*(x-min_timestamp)//(max_timestamp - min_timestamp))
df_tx['bin'] = df_tx['ttimestamp'].apply(bin_number) 
df_tx_binned =  df_tx.groupby('bin').count()
p2.line(df_tx_binned.index, df_tx_binned['ttimestamp'], legend = "transactions", color="blue")

df_views['bin'] = df_views['ttimestamp'].apply(bin_number) 
df_views_binned = df_views.groupby('bin').count()/100
p2.line(df_views_binned.index, df_views_binned['ttimestamp'], legend = "views / 100", color="orange")

p2.xaxis.axis_label = 'time [h]'

tab2 = Panel(child=p2, title="Events count")

tabs = Tabs(tabs=[tab1,tab2])

curdoc().add_root(row(widgetbox(slider_time), tabs))

