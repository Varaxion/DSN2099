import os
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.utils import shuffle
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def alerting():
    path = os.path.join(BASE_DIR, 'data', 'forecast', 'forecasted_level_of_rivers.csv')
    if not os.path.exists(path):
        return []
    data1 = pd.read_csv(path)
    res = []
    for i in range(data1.shape[1]):
        for j in range(data1.shape[0]):
            if data1.iloc[j, i] == 1:
                res.append(data1.columns[i].capitalize())
                break
    return res

def water_level_predictor():
    filenames = ['cauvery', 'godavari', 'krishna', 'mahanadi', 'son']

    def flood_classifier(filename, data):
        data_path = os.path.join(BASE_DIR, 'data', f'{filename}.xlsx')
        data1 = pd.read_excel(data_path)

        for i in range(1, len(data1.columns)):
            data1[data1.columns[i]] = data1[data1.columns[i]].fillna(data1[data1.columns[i]].mean())

        y = data1['Flood']
        for i in range(len(y)):
            if y[i] >= 0.1:
                y[i] = 1
        y = pd.DataFrame(y)

        data1.drop('Flood', axis=1, inplace=True)
        data1.drop('Date', inplace=True, axis=1)

        sm = SMOTE(random_state=2)
        X_train_res, Y_train_res = sm.fit_resample(data1, y)
        x_train, y_train = shuffle(X_train_res, Y_train_res, random_state=0)

        clf1 = LinearDiscriminantAnalysis()
        clf1.fit(x_train, y_train)
        y_predict = clf1.predict(data)
        return y_predict

    def data_creator(filename):
        d1 = pd.read_csv(os.path.join(BASE_DIR, 'data', 'forecast', f'{filename}_discharge_forecast.csv'))
        d2 = pd.read_csv(os.path.join(BASE_DIR, 'data', 'forecast', f'{filename}_flood_runoff_forecast.csv'))
        d3 = pd.read_csv(os.path.join(BASE_DIR, 'data', 'forecast', f'{filename}_daily_runoff_forecast.csv'))
        d4 = pd.read_csv(os.path.join(BASE_DIR, 'data', 'forecast', f'{filename}_weekly_runoff_forecast.csv'))

        import numpy as np
        expanded_weekly = np.repeat(d4['weekly runoff'].values, 7)
        if len(expanded_weekly) < len(d1):
            expanded_weekly = np.pad(expanded_weekly, (0, len(d1) - len(expanded_weekly)), 'edge')
        expanded_weekly = expanded_weekly[:len(d1)]

        data = d1.copy()
        data['flood runoff'] = d2['flood runoff']
        data['daily runoff'] = d3['daily runoff']
        data['weekly runoff'] = expanded_weekly

        for i in range(1, len(data.columns)):
            data[data.columns[i]] = data[data.columns[i]].fillna(data[data.columns[i]].mean())
        data.drop('Date', inplace=True, axis=1)
        return data

    y_pred = pd.DataFrame()
    for filename in filenames:
        data = data_creator(filename)
        y = flood_classifier(filename, data)
        y_pred[filename] = y

    out_path = os.path.join(BASE_DIR, 'data', 'forecast', 'forecasted_level_of_rivers.csv')
    y_pred.to_csv(out_path, index=False)
