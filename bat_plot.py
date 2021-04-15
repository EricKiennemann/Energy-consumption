import folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from keplergl import KeplerGl

import geopandas as gpd
import pandas as pd


from database import Batiment
from kepler_config import get_config

from constants import PLOT_QUANTILE,OUTPUT_DIR
import os


def bat_plot_folium(list_batiments,insee,dept):


    gpd_cons = gpd.GeoDataFrame(list_batiments)

    myscale = (gpd_cons['consumption'].quantile(PLOT_QUANTILE)).tolist()
    print(myscale[-1])


    for insee_com,nom_com in insee:
        gpd_consumption = gpd_cons[gpd_cons.insee_com == insee_com]

        gpd_consumption.crs = {'init' :'epsg:4326'}

        centroid=gpd_consumption.geometry.centroid

        m=folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=15, tiles='stamentoner')

        choro = folium.Choropleth(
            name=f"Energy consumption in {nom_com}",
            geo_data=gpd_consumption[['id','geometry','consumption',"nb_housing"]],
            data=gpd_consumption[gpd_consumption.consumption < myscale[-1]],
            columns=["id", "consumption","nb_housing"],
            key_on="feature.properties.id",
            fill_color='YlGnBu',
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

        if not os.path.exists(f'./output/{dept}'):
            os.makedirs(f'./output/{dept}')
        m.save(f"./output/{dept}/{nom_com}.html")


def bat_plot_kepler(list_batiments,list_dept):

    gpd_consumption = gpd.GeoDataFrame(list_batiments)

    gpd_consumption.crs = {'init' :'epsg:4326'}

    gpd_data = gpd_consumption[['id','geometry','consumption',"nb_housing"]]

    map2=KeplerGl()
    map2.add_data(gpd_data,name="Energy_Consumption")
    config = get_config()
    filename = f"EnergyConsumption{'_'.join([str(dept) for dept in list_dept])}.html"
    filepath = os.path.join(OUTPUT_DIR,filename)
    map2.save_to_html(file_name=filepath,config = config)

if __name__ == '__main__':
    dept = 75
    batiment = Batiment("Energy",dept)
    list_batiments = batiment.get_batiments_consumption()
    insee = batiment.get_insee()
    bat_plot(list_batiments,insee,dept)