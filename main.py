from database import Batiment


from plotv2 import bat_plot
from index import createHTML
from constants import DB_NAME

import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate html files for each insee cod in Paris and aound department")

    parser.add_argument('-d', '--department', action='store',
                        dest='list_dept', type=int, nargs='*',
                        help="Examples: -d 75 92 93 94. "
                        "List of departments to get map for")

    opts = parser.parse_args()

    list_dept = opts.list_dept

    for dept in list_dept:
            batiment = Batiment(DB_NAME,dept)
            list_batiments = batiment.get_batiments_consumption()
            insee = batiment.get_insee()
            bat_plot(list_batiments,insee,dept)

    createHTML(list_dept)








