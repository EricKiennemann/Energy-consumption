import psycopg2
from collections import defaultdict
from datetime import datetime,date
from constants import DB_OLD_DATE

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
		    bat.geom2d2
            from public."BATIMENT" as bat
            JOIN public."IRIS_GE" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel') and nb_logts > 0
            and iris.iris = '6115'
            """
        )
        rows = cur.fetchall()

        list_batiments = [
            {
                'iris'      : row[0],
                'date_app'  : row[1],
                'nb_housing'  : row[2],
                'geom'      : row[3],
            } for row in rows
        ]

        cur.close()

        return list_batiments

    def _get_bat_iris(self):
        # create a cursor
        cur = self.conn.cursor()


	    # execute a statement
        cur.execute(
            """
            select iris.code_iris,
		    bat.date_app,
		    bat.nb_logts,
		    bat.geom2d2
            from public."BATIMENT" as bat
            JOIN public."IRIS_GE" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel') and nb_logts > 0
            and iris.iris = '6115'
            """
        )

        rows = cur.fetchall()

        cur.close()

        return rows

    def housing_by_iris2(self):
        old_date = date.fromisoformat(DB_OLD_DATE)
        bat_dispatch = defaultdict(lambda: defaultdict(int))
        #rows = self._get_bat_iris()
        for i,bat in enumerate(self.list_batiments):
            iris = bat['iris']
            if bat['nb_housing'] == 1:
                #if datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
                if bat['date_app'] > old_date:
                    bat_dispatch[iris]['h_new'] +=1
                    self.list_batiments[i]['type'] = 'h_new'
                else:
                    bat_dispatch[iris]['h_old'] += 1
                    self.list_batiments[i]['type'] = 'h_old'
            #elif datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
            elif bat['date_app'] > old_date:
                    bat_dispatch[iris]['c_new'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_new'
            else:
                    bat_dispatch[iris]['c_old'] += bat['nb_housing']
                    self.list_batiments[i]['type'] = 'c_old'
        return bat_dispatch

    def housing_by_iris(self):
        old_date = date.fromisoformat(DB_OLD_DATE)
        bat_dispatch = defaultdict(lambda: defaultdict(int))
        rows = self._get_bat_iris()
        for row in rows:
            if row[2] == 1:
                #if datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
                if row[1] > old_date:
                    bat_dispatch[row[0]]['h_new'] +=1
                else:
                    bat_dispatch[row[0]]['h_old'] += 1
            #elif datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > old_date:
            elif row[1] > old_date:
                    bat_dispatch[row[0]]['c_new'] += row[2]
            else:
                    bat_dispatch[row[0]]['c_old'] += row[2]
        return bat_dispatch

    def get_batiments_consumption(self,consumption_by_housing_type,dict_dispatch):

        for i,bat in enumerate(self.list_batiments):
            consumption = bat['nb_housing'] * consumption_by_housing_type[bat['type']] * dict_dispatch[bat['iris']]['ratio']
            self.list_batiments[i]['consumption'] = consumption

        return self.list_batiments



if __name__ == '__main__':
    base = Batiment("Energy")
    print(base.housing_by_iris2)
