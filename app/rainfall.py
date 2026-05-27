import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import keras
from sklearn.metrics import mean_absolute_error, explained_variance_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def rainfall(year, region):
    data_path = os.path.join(BASE_DIR, 'data', 'imd_rainfall_2021.csv')
    data = pd.read_csv(data_path)

    if data.isna().sum().sum() > 0:
        data.dropna(inplace=True)

    def plotGraphs(groundTruth, prediction, title):
        N = 9
        ind = np.arange(N)
        width = 0.35

        fig = plt.figure(figsize=(12, 7))
        fig.suptitle(title, fontsize=18, color='#f1f5f9', fontweight='bold', y=0.96)
        ax = fig.add_subplot(111)
        rects1 = ax.bar(ind, groundTruth, width, color='#3b82f6', label='Ground Truth')
        rects2 = ax.bar(ind + width, prediction, width, color='#a78bfa', label='Prediction')

        ax.set_ylabel("Amount of rainfall (mm)", fontsize=14, color='#f1f5f9', fontweight='bold', labelpad=15)
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(('APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'), fontsize=12, color='#f1f5f9')
        
        leg = ax.legend(fontsize=13, facecolor='#0d1424', edgecolor='none')
        for text in leg.get_texts():
            text.set_color('#f1f5f9')

        ax.set_facecolor('#0d1424')
        fig.patch.set_facecolor('#0a0e1a')
        ax.tick_params(colors='#f1f5f9', labelsize=12)
        
        ax.grid(True, linestyle='--', alpha=0.15, color='#94a3b8')

        for rect in rects1:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., h + 3,
                    '%d' % int(h), ha='center', va='bottom', color='#60a5fa', fontsize=11, fontweight='semibold')
        for rect in rects2:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., h + 3,
                    '%d' % int(h), ha='center', va='bottom', color='#c084fc', fontsize=11, fontweight='semibold')

        ax.set_ylim(0, max(max(groundTruth), max(prediction)) * 1.15)

        img_path = os.path.join(BASE_DIR, 'static', 'img', 'rainfall.png')
        plt.savefig(img_path, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=120)
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
        region_slug = region.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('(', '').replace(')', '').replace('__', '_')
        model_dir = os.path.join(BASE_DIR, 'trained')
        model_path = os.path.join(model_dir, f'rainfall_cnn_{region_slug}.h5')

        xTesting, yTesting = dataGeneration(year, region)
        if xTesting is None or len(xTesting) == 0:
            return "NIL", "NIL"

        # Check model cache
        model_loaded = False
        if os.path.exists(model_path):
            try:
                print(f"Loading pre-trained CNN model for {region}...")
                from keras.models import load_model
                model = load_model(model_path)
                model_loaded = True
            except Exception as e:
                print(f"Error loading cached model: {e}. Re-training model...")

        if not model_loaded:
            print(f"Training CNN model from scratch for {region}...")
            from keras.models import Model
            from keras.layers import Dense, Input, Conv1D, Flatten, Dropout

            inputs = Input(shape=(3, 1))
            x = Conv1D(64, 2, padding='same', activation='relu')(inputs)
            x = Conv1D(128, 2, padding='same', activation='relu')(x)
            x = Flatten()(x)
            x = Dense(128, activation='relu')(x)
            x = Dropout(0.2)(x)
            x = Dense(64, activation='relu')(x)
            x = Dense(32, activation='relu')(x)
            x = Dense(1, activation='linear')(x)
            
            model = Model(inputs=[inputs], outputs=[x])
            model.compile(loss='mean_squared_error', optimizer='adamax', metrics=['mae'])

            xTrain, yTrain = dataGeneration2(region)
            model.fit(x=np.expand_dims(xTrain, axis=2), y=yTrain,
                      batch_size=64, epochs=20, verbose=1,
                      validation_split=0.1, shuffle=True)

            try:
                os.makedirs(model_dir, exist_ok=True)
                model.save(model_path)
                print(f"Saved CNN model to {model_path}")
            except Exception as e:
                print(f"Failed to save trained model: {e}")

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

    mae   = format(round(float(mae), 2))
    score = format(round(float(score), 2))
    keras.backend.clear_session()
    return mae, score
