import psycopg2
from collections import defaultdict
from datetime import datetime,date
from constants import DB_OLD_DATE
from open_data import IrisConsumption

import shapely
import shapely.wkt


class Batiment(object):

    def __init__(self, db_name, host = "localhost", user = "postgres", password = "postgres"):

        self.db_name = db_name
        self.host = host
        self.user = user

        # TODO : password not in clear text
        self.password = password

        self.conn = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.password)

        self.list_batiments = self._get_batiments()

    def _get_batiments(self):
        # create a cursor
        cur = self.conn.cursor()

        cur.execute(
            """
            select iris.code_iris,
		    bat.date_app,
		    bat.nb_logts,
		    ST_AsText(bat.geom2d2),
            bat.id,
            iris.insee_com
            from public."BATIMENT" as bat
            JOIN public."IRIS_GE" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel') and nb_logts > 0
            --and iris.insee_com = '75117'
            """
        )
        rows = cur.fetchall()

        list_batiments = [
            {
                'id'        : row[4],
                'iris'      : row[0],
                'insee_com' : row[5],
                'date_app'  : row[1],
                'nb_housing'  : row[2],
                'geometry'      : shapely.wkt.loads(row[3]),
            } for row in rows
        ]

        cur.close()

        return list_batiments


    def housing_by_iris2(self):
        old_date = date.fromisoformat(DB_OLD_DATE)
        bat_dispatch = defaultdict(lambda: defaultdict(int))
        #rows = self._get_bat_iris()
        for i,bat in enumerate(self.list_batiments):
            if bat['date_app'] is None:
                date_app = old_date
            else:
                date_app = bat['date_app']
            iris = bat['iris']
            if bat['nb_housing'] == 1:
                #if datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
                if date_app > old_date:
                    bat_dispatch[iris]['h_new'] +=1
                    self.list_batiments[i]['type'] = 'h_new'
                else:
                    bat_dispatch[iris]['h_old'] += 1
                    self.list_batiments[i]['type'] = 'h_old'
            #elif datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
            elif date_app > old_date:
                    bat_dispatch[iris]['c_new'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_new'
            else:
                    bat_dispatch[iris]['c_old'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_old'
        return bat_dispatch



    def get_batiments_consumption(self):

        consumption_by_housing_type = {
            'h_new' : 23.5,
            'h_old' : 26.0,
            'c_new' : 13.0,
            'c_old' : 17.0,
        }

        iris_consumption = IrisConsumption(75,2019)
        dict_iris_consumption = iris_consumption.consumption_by_iris()
        print("c iris : ",dict_iris_consumption['751124812'])

        #batiment = Batiment("Energy")
        dict_dispatch = self.housing_by_iris2()
        for iris_code,dispatch in dict_dispatch.items():
            dict_dispatch[iris_code]['ratio'] = ratio_for_iris(dispatch,consumption_by_housing_type,dict_iris_consumption[iris_code])

        #print(dict_dispatch)
        #print(batiment.get_batiments_consumption(consumption_by_housing_type,dict_dispatch)[0])
        #list_batiments = batiment.get_batiments_consumption(consumption_by_housing_type,dict_dispatch)

        for i,bat in enumerate(self.list_batiments):
            #consumption = bat['nb_housing'] * consumption_by_housing_type[bat['type']] * dict_dispatch[bat['iris']]['ratio']
            consumption = round(consumption_by_housing_type[bat['type']] * dict_dispatch[bat['iris']]['ratio'],2)
            self.list_batiments[i]['consumption'] = consumption

        return self.list_batiments

def ratio_for_iris(dispatch,consumption_by_housing_type,iris_consumption):
    total_theo_consumption = 0
    for key,number_housing in dispatch.items():
        total_theo_consumption += number_housing * consumption_by_housing_type[key]
    #print(total_theo_consumption,iris_consumption)
    if total_theo_consumption != 0:
        return iris_consumption / total_theo_consumption
    else:
        return 0

if __name__ == '__main__':
    base = Batiment("Energy")
    print(base.housing_by_iris2)
