import discharge as dp
import flood_runoff as frp
import daily_runoff as drp
import weekly_runoff as wrp
import model
import pandas as pd


def futCal(userDate, endDate):
    """
    Determine if the given date is in the future compared to the end date.

    Args:
        userDate (datetime): The date to be checked.
        endDate  (datetime): The end date for comparison.

    Returns:
        int: 1 if userDate is in the future, 0 otherwise.
    """
    if userDate > endDate:
        return 1  # Future data
    else:
        return 0  # Existing data


def drive(filename, userDate):
    """
    Perform flood prediction based on the given filename and userDate.

    Args:
        filename (str): The filename (without extension) of the data file.
        userDate (str): The user-provided date in string format ('YYYY-MM-DD').

    Returns:
        dict: A dictionary containing flood prediction results, or None on failure.
    """
    try:
        data = pd.read_excel(f'data/{filename}.xlsx')

        userDate = pd.to_datetime(userDate)
        lastDate = data['Date'].iloc[-1]
        fut = futCal(userDate, lastDate)

        if fut == 0:
            # Existing data prediction
            for col in data.columns[1:]:
                data[col] = data[col].fillna(data[col].mean())

            data['Date'] = pd.to_datetime(data['Date'])

            def existingPrediction(i):
                fd = data.iloc[i, 1:5].tolist()  # Exclude 'Date' and 'Flood'

                result, mae = model.flood_classifier(filename, fd)

                discharge    = round(data.iloc[i, 1], 2)
                floodRunoff  = round(data.iloc[i, 2], 2)
                dailyRunoff  = round(data.iloc[i, 3], 2)
                weeklyRunoff = round(data.iloc[i, 4], 2)
                mae          = round(mae, 2)

                predicted = 'Normal' if result == 0 else 'High'
                actual    = 'Normal' if data.iloc[i, -1] == 0 else 'High'

                return {
                    'discharge':          discharge,
                    'floodRunoff':        floodRunoff,
                    'dailyRunoff':        dailyRunoff,
                    'weeklyRunoff':       weeklyRunoff,
                    'meanAbsoluteError':  mae,
                    'predicted':          predicted,
                    'actualFlood':        actual
                }

            for i in range(len(data)):
                if data['Date'].iloc[i].date() == userDate.date():
                    return existingPrediction(i)

            return None

        else:
            # Future data prediction
            wtd = 1
            d1 = dp.discharge_forecast(filename, wtd)
            d2 = frp.flood_runoff_forecast(filename, wtd)
            d3 = drp.daily_runoff_forecast(filename, wtd)
            d4 = wrp.weekly_runoff_forecast(filename, wtd)

            import numpy as np
            expanded_weekly = np.repeat(d4['weekly runoff'].values, 7)
            if len(expanded_weekly) < len(d1):
                expanded_weekly = np.pad(expanded_weekly, (0, len(d1) - len(expanded_weekly)), 'edge')
            expanded_weekly = expanded_weekly[:len(d1)]

            data1 = pd.concat([d1, d2['flood runoff'], d3['daily runoff']], axis=1)
            data1['weekly runoff'] = expanded_weekly
            data1['Date'] = pd.to_datetime(data1['Date'])

            def futurePrediction(i):
                fd = data1.iloc[i, 1:].tolist() # Skip the 'Date' column

                result, mae = model.flood_classifier(filename, fd)

                discharge    = round(data1['Discharge'].iloc[i], 2)
                floodRunoff  = round(data1['flood runoff'].iloc[i], 2)
                dailyRunoff  = round(data1['daily runoff'].iloc[i], 2)
                weeklyRunoff = round(data1['weekly runoff'].iloc[i], 2)

                predicted = 'Normal' if result == 0 else 'High'

                return {
                    'discharge':         discharge,
                    'floodRunoff':       floodRunoff,
                    'dailyRunoff':       dailyRunoff,
                    'weeklyRunoff':      weeklyRunoff,
                    'meanAbsoluteError': 'NIL',
                    'predicted':         predicted,
                    'actualFlood':       'NIL'
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
