import psycopg2
from collections import defaultdict
from datetime import datetime
from constants import DB_OLD_DATE

class Bat_iris(object):

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

    def _get_bat_iris(self):
        # create a cursor
        cur = self.conn.cursor()

	    # execute a statement
        cur.execute(
            """
            select iris.code_iris,
		    bat.date_creat,
		    bat.nb_logts,
		    bat.geom2d2
            from public."BATIMENT" as bat
            JOIN public."IRIS_GE" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel') and nb_logts > 0
            """
        )

        rows = cur.fetchall()

        cur.close()

        return rows

    def _dispatch_by_bat(self):
        old_date = datetime.strptime(DB_OLD_DATE,'%d/%m/%y')
        bat_dispatch = defaultdict(dict())
        rows = self._get_bat_iris()
        for row in rows:
            if row[2] == 1:
                if datetime.strptime(row[1], '%y-%m/%d %H:%M:%S') > old_date:
                    bat_dispatch[row[0]]['h_new'] +=1
                else:
                    bat_dispatch[row[0]]['h_old'] += 1
            elif datetime.strptime(row[1], '%y-%m/%d %H:%M:%S') > old_date:
                    bat_dispatch[row[0]]['c_new'] += row[2]
            else:
                    bat_dispatch[row[0]]['c_old'] += row[2]
        return bat_dispatch

if __name__ == '__main__':
    base = Bat_iris("Energy")
    print(base._dispatch_by_bat())
