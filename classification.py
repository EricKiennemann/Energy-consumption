from database import Batiment
from constants import DB_NAME
import pandas as pd

if __name__ == '__main__':

    list_dept=[75]
    list_batiments = list()
    for dept in list_dept:
            batiment = Batiment(DB_NAME,dept)
            rows = (batiment._get_data_classification())
            df_batiment = pd.DataFrame(rows)
            df_batiment.columns = [['id','type','leger','status','date_cons','logements','etages','mat_mur','mat_toit','source']]
            print(df_batiment.head())

            df_batiment.summary()


