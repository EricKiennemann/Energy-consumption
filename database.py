import psycopg2

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

    def get_bat_iris(self):
        # create a cursor
        cur = self.conn.cursor()

	    # execute a statement
        cur.execute(
            """
            select iris.code_iris,
		    bat.usage1,
		    bat.usage2,
		    date_creat,
		    nb_logts,
		    bat.geom2d2
            from public."BATIMENT" as bat
            JOIN public."IRIS_GE" AS iris
            ON ST_Contains(iris.geom, bat.geom)
            where (usage1 = 'Résidentiel' or usage2 = 'Résidentiel')
            """
        )

        rows = cur.fetchall()

        cur.close()

        return rows

if __name__ == '__main__':
    base = Bat_iris("Energy")
    print(base.get_bat_iris())
