import os
import pandas as pd
import timeseries_forecaster as tsf
import model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def futCal(userDate, endDate):
    if userDate > endDate:
        return 1
    return 0

def drive(filename, userDate):
    try:
        # Standardize lowercase filenames
        filename = filename.lower()
        data_path = os.path.join(BASE_DIR, 'data', f'{filename}.xlsx')
        data = pd.read_excel(data_path)

        userDate = pd.to_datetime(userDate)
        lastDate = data['Date'].iloc[-1]
        fut = futCal(userDate, lastDate)

        if fut == 0:
            for col in data.columns[1:]:
                data[col] = data[col].fillna(data[col].mean())

            data['Date'] = pd.to_datetime(data['Date'])

            def existingPrediction(i):
                fd = data.iloc[i, 1:5].tolist()
                result, mae = model.flood_classifier(filename, fd)

                return {
                    'discharge': round(data.iloc[i, 1], 2),
                    'floodRunoff': round(data.iloc[i, 2], 2),
                    'dailyRunoff': round(data.iloc[i, 3], 2),
                    'weeklyRunoff': round(data.iloc[i, 4], 2),
                    'meanAbsoluteError': round(mae, 2),
                    'predicted': 'Normal' if result == 0 else 'High',
                    'actualFlood': 'Normal' if data.iloc[i, -1] == 0 else 'High'
                }

            for i in range(len(data)):
                if data['Date'].iloc[i].date() == userDate.date():
                    return existingPrediction(i)

            return None

        else:
            wtd = 1
            d1 = tsf.discharge_forecast(filename, wtd)
            d2 = tsf.flood_runoff_forecast(filename, wtd)
            d3 = tsf.daily_runoff_forecast(filename, wtd)
            d4 = tsf.weekly_runoff_forecast(filename, wtd)

            import numpy as np
            expanded_weekly = np.repeat(d4['weekly runoff'].values, 7)
            if len(expanded_weekly) < len(d1):
                expanded_weekly = np.pad(expanded_weekly, (0, len(d1) - len(expanded_weekly)), 'edge')
            expanded_weekly = expanded_weekly[:len(d1)]

            data1 = pd.concat([d1, d2['flood runoff'], d3['daily runoff']], axis=1)
            data1['weekly runoff'] = expanded_weekly
            data1['Date'] = pd.to_datetime(data1['Date'])

            def futurePrediction(i):
                fd = data1.iloc[i, 1:].tolist()
                result, mae = model.flood_classifier(filename, fd)

                return {
                    'discharge': round(data1['Discharge'].iloc[i], 2),
                    'floodRunoff': round(data1['flood runoff'].iloc[i], 2),
                    'dailyRunoff': round(data1['daily runoff'].iloc[i], 2),
                    'weeklyRunoff': round(data1['weekly runoff'].iloc[i], 2),
                    'meanAbsoluteError': 'NIL',
                    'predicted': 'Normal' if result == 0 else 'High',
                    'actualFlood': 'NIL'
                }

            for i in range(len(data1)):
                if data1['Date'].iloc[i].date() == userDate.date():
                    return futurePrediction(i)

            return None

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred in drive(): {e}")
        return None
