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

from constants import PLOT_QUANTILE



from branca.colormap import linear


def bat_plot():
    batiment = Batiment("Energy")
    list_batiments = batiment.get_batiments_consumption()

    gpd_cons = gpd.GeoDataFrame(list_batiments)

    insee_coms = gpd_cons.insee_com.unique()
    print(insee_coms)

    myscale = (gpd_cons['consumption'].quantile(PLOT_QUANTILE)).tolist()
    print(myscale[-1])


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

        m=folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=15, tiles='stamentoner')

        choro = folium.Choropleth(
            name=f"Energy consumption in {insee_com}",
            geo_data=gpd_consumption[['id','geometry','consumption',"nb_housing"]],
            data=gpd_consumption[gpd_consumption.consumption < myscale[-1]],
            columns=["id", "consumption","nb_housing"],
            key_on="feature.properties.id",
            fill_color='YlGnBu',
            #bins=[0, 5,10,15,20,25,30,50, 100, 1000],
            threshold_scale=myscale,
            legend_name = "Energy consumption in kWh/year/housing",
            nan_fill_color="red",
            font_size= '12px'
        ).add_to(m)

        choro.geojson.add_child(folium.features.GeoJsonTooltip(fields=['id','consumption','nb_housing'],
                                                aliases=['Id','Energy Consumption (kWh/year/housing)','# housing'],
                                                labels=True,
                                                sticky=True,
                                                toLocaleString=True)
)

        folium.LayerControl(autoZIndex=False, collapsed=False).add_to(m)

        m.save(f"./output/index_{insee_com}.html")


if __name__ == '__main__':
    bat_plot()