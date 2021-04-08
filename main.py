from database import Batiment
import geopandas as gpd

from branca.colormap import linear

import matplotlib
import matplotlib.pyplot as plt

from constants import LIST_DEPT
from plotv2 import bat_plot
from index import createHTML




if __name__ == '__main__':
    for dept in LIST_DEPT:
            batiment = Batiment("Energy",dept)
            list_batiments = batiment.get_batiments_consumption()
            insee = batiment.get_insee()
            bat_plot(list_batiments,insee,dept)

    createHTML(LIST_DEPT)

    """
    consumption_by_housing_type = {
        'h_new' : 23.5,
        'h_old' : 26.0,
        'c_new' : 13.0,
        'c_old' : 17.0,

    }

    iris_consumption = IrisConsumption(75,2019)
    dict_iris_consumption = iris_consumption.consumption_by_iris()
    """
    """
    dict_dispatch = batiment.housing_by_iris2()
    for iris_code,dispatch in dict_dispatch.items():
        dict_dispatch[iris_code]['ratio'] = ratio_for_iris(dispatch,consumption_by_housing_type,dict_iris_consumption)

    print(dict_dispatch)

    print(batiment.get_batiments_consumption()[0])
    list_batiments = batiment.get_batiments_consumption()
    gpd_consumption = gpd.GeoDataFrame(list_batiments)
    #print(gpd_consumption[['id','geometry','consumption']].head(2))

    colormap = linear.YlGn_09.scale(
        gpd_consumption.consumption.min(), gpd_consumption.consumption.max()
    )
    #print(colormap([gpd_consumption.consumption[0:3]]))
    print(gpd_consumption.consumption.min(), gpd_consumption.consumption.max())
    print(gpd_consumption[gpd_consumption.consumption > 100])

    plt.hist(gpd_consumption.consumption)
    plt.show()
    #bat_dict = dict(zip(gpd_consumption['id'], gpd_consumption['consumption']))
    #print(bat_dict)

    myscale = (gpd_consumption['consumption'].quantile((0,0.1,0.75,0.9,0.98,0.99))).tolist()
    print(myscale)
    """






