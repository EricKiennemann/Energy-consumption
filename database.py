import psycopg2
from collections import defaultdict
from datetime import datetime,date
from constants import CONSTRUCTION_OLD_DATE, CONSTRUCTION_OLD_DATE,YEAR_ENERGY_API,DB_HOST, DB_USER, DB_PASSWORD,ENERGY_NEW_INDIVIDUAL,ENERGY_OLD_INDIVIDUAL,ENERGY_NEW_BUILDING,ENERGY_OLD_BUILDING

from open_data import IrisConsumption

import shapely
import shapely.wkt


class Batiment(object):

    def __init__(self, db_name, dept, host = DB_HOST, user = DB_USER, password = DB_PASSWORD):

        self.db_name = db_name
        self.host = host
        self.user = user
        self.dept = dept

        # TODO : password not in clear text
        self.password = password

        self.conn = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.password)


    def get_insee(self):
        cur = self.conn.cursor()
        str_sql = f"""
            select distinct insee_com,nom_com from public."iris_ge_{self.dept}"
            """
        cur.execute(str_sql)
        rows = cur.fetchall()
        return rows

    def _get_data_classification(self):
        # create a cursor
        cur = self.conn.cursor()

        str_sql = f"""
            SELECT id,nature,
            leger,
            etat,
            date_app,
            nb_logts,
            nb_etages,
            mat_murs,
            mat_toits,
            origin_bat
            FROM public.batiment_{self.dept}
            where (usage1 = 'RÃ©sidentiel' or usage2 = 'RÃ©sidentiel') and nb_logts <> 0
        """

        cur.execute(str_sql)
        rows = cur.fetchall()

        cur.close()

        return rows

    def _get_batiments(self):
        # create a cursor
        cur = self.conn.cursor()

        str_sql = f"""
            select iris.code_iris,
		    bat.date_app,
		    bat.nb_logts,
            ST_AsText(ST_Force2D(bat.geom)),
            bat.id,
            iris.insee_com,
            iris.nom_com
            from public."batiment_{self.dept}" as bat
            JOIN public."iris_ge_{self.dept}" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel' or usage1 = 'RÃ©sidentiel' or usage2 = 'RÃ©sidentiel') and nb_logts > 0
            """

        cur.execute(str_sql)
        rows = cur.fetchall()

        list_batiments = [
            {
                'id'        : row[4],
                'iris'      : row[0],
                'insee_com' : row[5],
                'nom_com'   : row[6],
                'date_app'  : row[1],
                'nb_housing'  : row[2],
                'geometry'      : shapely.wkt.loads(row[3]),
            } for row in rows
        ]

        cur.close()

        return list_batiments


    def housing_by_iris2(self):
        self.list_batiments = self._get_batiments()

        old_date = CONSTRUCTION_OLD_DATE
        bat_dispatch = defaultdict(lambda: defaultdict(int))

        for i,bat in enumerate(self.list_batiments):
            if bat['date_app'] is None:
                date_app = old_date
            else:
                date_app = bat['date_app']
            iris = bat['iris']
            if bat['nb_housing'] == 1:
                if date_app > old_date:
                    bat_dispatch[iris]['h_new'] +=1
                    self.list_batiments[i]['type'] = 'h_new'
                else:
                    bat_dispatch[iris]['h_old'] += 1
                    self.list_batiments[i]['type'] = 'h_old'
            elif date_app > old_date:
                    bat_dispatch[iris]['c_new'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_new'
            else:
                    bat_dispatch[iris]['c_old'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_old'
        return bat_dispatch



    def get_batiments_consumption(self):

        consumption_by_housing_type = {
            'h_new' : ENERGY_NEW_INDIVIDUAL,
            'h_old' : ENERGY_OLD_INDIVIDUAL,
            'c_new' : ENERGY_NEW_BUILDING,
            'c_old' : ENERGY_OLD_BUILDING,
        }

        iris_consumption = IrisConsumption(self.dept,YEAR_ENERGY_API)
        dict_iris_consumption = iris_consumption.consumption_by_iris()

        dict_dispatch = self.housing_by_iris2()
        for iris_code,dispatch in dict_dispatch.items():
            dict_dispatch[iris_code]['ratio'] = ratio_for_iris(dispatch,consumption_by_housing_type,dict_iris_consumption[iris_code])


        for i,bat in enumerate(self.list_batiments):
            consumption = round(consumption_by_housing_type[bat['type']] * dict_dispatch[bat['iris']]['ratio'],2)
            self.list_batiments[i]['consumption'] = consumption

        return self.list_batiments

def ratio_for_iris(dispatch,consumption_by_housing_type,iris_consumption):
    total_theo_consumption = 0
    for key,number_housing in dispatch.items():
        total_theo_consumption += number_housing * consumption_by_housing_type[key]
    if total_theo_consumption != 0:
        return iris_consumption / total_theo_consumption
    else:
        return 0

if __name__ == '__main__':

    base = Batiment("Energy",75)
    print(base.get_insee())
