from database import Batiment


from bat_plot import bat_plot_folium,bat_plot_kepler
from index import createHTML
from constants import DB_NAME

import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate html files for each insee cod in Paris and aound department")

    parser.add_argument('-d', '--department', action='store',
                        dest='list_dept', type=int, nargs='*',
                        help="Examples: -d 75 92 93 94. "
                        "List of departments to get map for")

    parser.add_argument('-v', '--visu', action='store',
                        dest='visu', type=str, default='kepler',
                        help="-v kepler (default) or -v folium "
                        "visualisation done with kepler.gl (default) all data on a single html"
                        " or with folium with one html by insee code")

    opts = parser.parse_args()

    list_dept = opts.list_dept

    if opts.visu == 'folium':
        for dept in list_dept:
                batiment = Batiment(DB_NAME,dept)
                list_batiments = batiment.get_batiments_consumption()
                insee = batiment.get_insee()
                bat_plot_folium(list_batiments,insee,dept)

        createHTML(list_dept)
    elif opts.visu=='kepler':

        list_batiments = list()
        for dept in list_dept:
                batiment = Batiment(DB_NAME,dept)
                list_batiments.extend(batiment.get_batiments_consumption())

        bat_plot_kepler(list_batiments,list_dept)







