import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — prevents plt.show() blocking
import matplotlib.pyplot as plt
import keras
from sklearn.metrics import mean_absolute_error, explained_variance_score


def rainfall(year, region):
    data = pd.read_csv(r'data\Sub_Division_IMD_2021.csv')

    if data.isna().sum().sum() > 0:
        data.dropna(inplace=True)

    def plotGraphs(groundTruth, prediction, title):
        N = 9
        ind = np.arange(N)
        width = 0.27

        fig = plt.figure(figsize=(18, 10))
        fig.suptitle(title, fontsize=12)
        ax = fig.add_subplot(111)
        rects1 = ax.bar(ind, groundTruth, width, color='#3b82f6')
        rects2 = ax.bar(ind + width, prediction, width, color='#8b5cf6')

        ax.set_ylabel("Amount of rainfall")
        ax.set_xticks(ind + width)
        ax.set_xticklabels(('APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'))
        ax.legend((rects1[0], rects2[0]), ('Ground truth', 'Prediction'))
        ax.set_facecolor('#0d1424')
        fig.patch.set_facecolor('#0a0e1a')
        ax.tick_params(colors='#94a3b8')
        ax.yaxis.label.set_color('#94a3b8')

        for rect in rects1:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h,
                    '%d' % int(h), ha='center', va='bottom', color='#94a3b8')
        for rect in rects2:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h,
                    '%d' % int(h), ha='center', va='bottom', color='#94a3b8')

        plt.savefig('static/img/rainfall.png', facecolor=fig.get_facecolor())
        plt.close(fig)

    def dataGeneration(year, region):
        temp = data[['SUBDIVISION', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
                     'AUG', 'SEP', 'OCT', 'NOV', 'DEC']].loc[data['YEAR'] == year]
        dataYear = np.asarray(temp[['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
                                    'AUG', 'SEP', 'OCT', 'NOV', 'DEC']].loc[temp['SUBDIVISION'] == region])
        xYear = None
        yYear = None
        for i in range(dataYear.shape[1] - 3):
            if xYear is None:
                xYear = dataYear[:, i:i + 3]
                yYear = dataYear[:, i + 3]
            else:
                xYear = np.concatenate((xYear, dataYear[:, i:i + 3]), axis=0)
                yYear = np.concatenate((yYear, dataYear[:, i + 3]), axis=0)
        return xYear, yYear

    def dataGeneration2(region):
        regionData = np.asarray(data[['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
                                      'AUG', 'SEP', 'OCT', 'NOV', 'DEC']].loc[data['SUBDIVISION'] == region])
        X = None
        y = None
        for i in range(regionData.shape[1] - 3):
            if X is None:
                X = regionData[:, i:i + 3]
                y = regionData[:, i + 3]
            else:
                X = np.concatenate((X, regionData[:, i:i + 3]), axis=0)
                y = np.concatenate((y, regionData[:, i + 3]), axis=0)
        return X, y

    def prediction2(year, region):
        from keras.models import Model
        from keras.layers import Dense, Input, Conv1D, Flatten

        # 1D-CNN model
        inputs = Input(shape=(3, 1))
        x = Conv1D(64, 2, padding='same', activation='elu')(inputs)
        x = Conv1D(128, 2, padding='same', activation='elu')(x)
        x = Flatten()(x)
        x = Dense(128, activation='elu')(x)
        x = Dense(64, activation='elu')(x)
        x = Dense(32, activation='elu')(x)
        x = Dense(1, activation='linear')(x)
        model = Model(inputs=[inputs], outputs=[x])
        model.compile(loss='mean_squared_error', optimizer='adamax', metrics=['mae'])

        xTesting, yTesting = dataGeneration(year, region)
        if xTesting is None or len(xTesting) == 0:
            return "NIL", "NIL"

        xTrain, yTrain = dataGeneration2(region)
        model.fit(x=np.expand_dims(xTrain, axis=2), y=yTrain,
                  batch_size=64, epochs=20, verbose=1,
                  validation_split=0.1, shuffle=True)

        yPred = model.predict(np.expand_dims(xTesting, axis=2))
        mae   = mean_absolute_error(yTesting, yPred)
        score = explained_variance_score(yTesting, yPred)

        yYearPred = [yPred[i][0] for i in range(9)]
        yPredArr  = np.array(yYearPred)
        plotGraphs(yTesting, yPredArr, f'Year: {year}  Region: {region}')
        return mae, score

    mae, score = prediction2(int(year), region)

    if mae == "NIL":
        return "NIL", "NIL"

    # Format metrics gracefully
    mae   = format(round(float(mae), 2))
    score = format(round(float(score), 2))
    keras.backend.clear_session()
    return mae, score
