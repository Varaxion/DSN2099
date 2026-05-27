import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error
import numpy as np
import warnings

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def flood_classifier(filename, fd, validating=0):
    data_path = os.path.join(BASE_DIR, 'data', f'{filename.lower()}.xlsx')
    data1 = pd.read_excel(data_path)

    for i in range(1, len(data1.columns)):
        data1[data1.columns[i]] = data1[data1.columns[i]].fillna(data1[data1.columns[i]].mean())

    y = data1['Flood']

    for i in range(len(y)):
        if y[i] >= 0.1:
            y[i] = 1

    y = pd.DataFrame(y)
    data1.drop('Flood', axis=1, inplace=True)

    d1 = pd.DataFrame()
    d1["Day"] = data1['Date']
    d1['Months'] = data1['Date']
    d1['Year'] = data1['Date']
    data1['Date'] = pd.to_datetime(data1['Date'])
    d1["Year"] = data1.Date.dt.year
    d1["Months"] = data1.Date.dt.month
    d1["Day"] = data1.Date.dt.day

    data1.drop('Date', inplace=True, axis=1)

    values = data1.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    data1 = pd.DataFrame(scaled, columns=data1.columns)

    data1 = pd.concat([d1, data1], axis=1)

    locate = 0
    for i in range(len(data1["Day"])):
        if data1["Day"][i] == 31 and data1["Months"][i] == 12 and data1["Year"][i] == 2015:
            locate = i
            break

    i = locate + 1

    x_train = data1.iloc[0:i, :]
    y_train = y.iloc[0:i]
    x_test = data1.iloc[i:, :]
    y_test = y.iloc[i:]

    x_train.drop(labels=['Day', 'Months', 'Year'], inplace=True, axis=1)
    x_test.drop(labels=['Day', 'Months', 'Year'], inplace=True, axis=1)

    sm = SMOTE(random_state=2)
    X_train_res, Y_train_res = sm.fit_resample(x_train, y_train)

    x_train, y_train = shuffle(X_train_res, Y_train_res, random_state=0)

    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    clf1 = LinearDiscriminantAnalysis()
    clf1.fit(x_train, y_train)

    y_predict3 = clf1.predict(x_test)
    mae = mean_absolute_error(y_test, y_predict3)

    def predicting(future_data):
        xx = future_data
        xx = np.array(xx).reshape((-1, 4))
        xx = clf1.predict(xx)
        return xx

    xx = predicting(fd)
    return xx, mae
