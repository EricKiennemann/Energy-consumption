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

import geopandas as gpd
import pandas as pd

from database import Batiment

app = Flask(__name__)


@app.route('/')
def index():
    batiment = Batiment("Energy")
    list_batiments = batiment.get_batiments_consumption()
    #pd_consumption = pd.DataFrame(list_batiments)
    gpd_consumption = gpd.GeoDataFrame(list_batiments)
    gpd_consumption.crs = {'init' :'epsg:4326'}
    #print(gpd_consumption)

    start_coords = (48.8534 , 2.3488)
    m = folium.Map(location=start_coords, zoom_start=14)

    folium.GeoJson(
        gpd_consumption['geometry'],
    ).add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)