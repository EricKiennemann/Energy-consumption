""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask

import folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup

import geopandas as gpd
import pandas as pd

from database import Batiment



from branca.colormap import linear


def bat_plot():
    batiment = Batiment("Energy")
    list_batiments = batiment.get_batiments_consumption()
    gpd_consumption = gpd.GeoDataFrame(list_batiments)

    bat_dict = dict(zip(gpd_consumption['id'], gpd_consumption['consumption']))

    colormap = linear.YlGn_09.scale(
        gpd_consumption.consumption.min(), gpd_consumption.consumption.max()
    )

    map_colors = lambda x: {
    'fillColor': colormap(bat_dict[x['properties']['id']]),
    'color': 'black',
    'weight': 0.25,
    'fillOpacity': 0.5
}
    #print(colormap)

    gpd_consumption.crs = {'init' :'epsg:4326'}
    #print(gpd_consumption)

    start_coords = (48.8534 , 2.3488)
    m = folium.Map(location=start_coords, tiles = 'Stamen Toner',zoom_start=14)

    folium.GeoJson(
        gpd_consumption[['id','geometry','consumption']],
        zoom_on_click=True,
        name="energy Consumption",
        style_function= map_colors
    ).add_to(m)

    m.save("index.html")


if __name__ == '__main__':
    bat_plot()