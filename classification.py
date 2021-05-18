from database import Batiment
from constants import DB_NAME, CONSTRUCTION_OLD_DATE
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime,date

from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_log_error
from sklearn import decomposition
from sklearn import svm
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

def update_construction_year(batiment):
    rows = (batiment._get_data_classification())
    bat = pd.DataFrame(rows)
    bat.columns = ['id','type','leger','status','date_cons','logements','etages','mat_mur','mat_toit','source']

    # for training we keep the batiments with a construction year
    bat_train = bat[~bat.date_cons.isna()]
    bat_pred = bat[~bat.date_cons.isna()]
    bat_categorical = pd.get_dummies(bat_train[['leger','status','mat_mur','mat_toit','source']])
    bat_categorical = np.concatenate((bat_train[['logements','etages']].values,bat_categorical.values),axis=1)

    #bat_categorical = pd.get_dummies(bat_train[['mat_mur']])
    #bat_categorical_pred = pd.get_dummies(bat_pred[['mat_mur']])

    bat_train['delta_date'] = bat_train.date_cons.apply(lambda x: 1 if (x - CONSTRUCTION_OLD_DATE).days > 0 else 0)

    X,Y = bat_categorical, bat_train['delta_date'].values
    X_train, X_valide, Y_train, Y_valide = train_test_split(X,Y, test_size = 0.3)


    #X_pred = bat_categorical_pred.values

    #svm_bat = svm.SVC(kernel='linear',verbose = False)
    logic = LogisticRegression(max_iter = 1000)
    boost = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)

    #svm_bat.fit(X,Y)
    #svm_bat.fit(X_train,Y_train)
    logic.fit(X_train,Y_train)
    boost.fit(X_train,Y_train)
    #y_pred = svm_bat.predict(X_pred)
    #y_pred = svm_bat.predict(X_valide)
    y_pred_logic = logic.predict(X_valide)
    y_pred_boost = boost.predict(X_valide)
    print('logistic accuracy', metrics.accuracy_score(Y_valide,y_pred_logic))
    print('XGboost accuracy', metrics.accuracy_score(Y_valide,y_pred_boost))
    return None

if __name__ == '__main__':
    batiment = Batiment(DB_NAME,75)
    y_pred = update_construction_year(batiment)
