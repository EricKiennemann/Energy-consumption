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

    gpd_cons = gpd.GeoDataFrame(list_batiments)

    insee_coms = gpd_cons.insee_com.unique()
    print(insee_coms)

    for insee_com in insee_coms:
        gpd_consumption = gpd_cons[gpd_cons.insee_com == insee_com]

        bat_dict = dict(zip(gpd_consumption['id'], gpd_consumption['consumption']))

        colormap = linear.YlGn_09.scale(
            gpd_consumption.consumption.min(), gpd_consumption.consumption.max()
        )

        map_colors = lambda x: {
        'fillColor': colormap(bat_dict[x['properties']['id']]),
        'color': 'black',
        'weight': 0.25,
        'fillOpacity': 0.5,
        }

        #print(colormap)

        gpd_consumption.crs = {'init' :'epsg:4326'}
        #print(gpd_consumption)

        #start_coords = (48.8534 , 2.3488)
        centroid=gpd_consumption.geometry.centroid

        m=folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=14, tiles='stamentoner')
        colormap.caption = "Energy Consumption"

        """
        folium.GeoJson(
            gpd_consumption[['id','geometry','consumption']],
            zoom_on_click=True,
            name="energy Consumption",
            style_function= map_colors
            tooltip=folium.features.Tooltip(fields=['id','consumption'],
                                                aliases=['bat','Energy Consumption'],
                                                labels=True,
                                                sticky=True,
                                                toLocaleString=True)
        ).add_to(m)
        """

        folium.Choropleth(
            geo_data=gpd_consumption[['id','geometry','consumption']],
            data=gpd_consumption,
            columns=["id", "consumption"],
            key_on="feature.properties.id",
            fill_color="YlGn",
            bins=[0, 5,10,15,20,25,30,50, 100, 1000],

        ).add_to(m)

        #colormap.add_to(m)

        m.save(f"./output/index_{insee_com}.html")


if __name__ == '__main__':
    bat_plot()