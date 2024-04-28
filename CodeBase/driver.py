import discharge as dp
import flood_runoff as frp
import daily_runoff as drp
import weekly_runoff as wrp
import model 
import pandas as pd

def fut_cal(user_date, end_date):
    """
    Determine if the given date is in the future compared to the end date.

    Args:
    - user_date (datetime): The date to be checked.
    - end_date (datetime): The end date for comparison.

    Returns:
    - int: 1 if user_date is in the future, 0 otherwise.
    """
    if user_date > end_date:
        return 1  # Future Data
    else:
        return 0  # Existing Data

def drive(filename, user_date):
    """
    Perform flood prediction based on the given filename and user_date.

    Args:
    - filename (str): The filename (without extension) of the data file.
    - user_date (str): The user-provided date in string format ('YYYY-MM-DD').

    Returns:
    - dict: A dictionary containing flood prediction results.
    """
    try:
        data = pd.read_excel(f'data/{filename}.xlsx')

        user_date = pd.to_datetime(user_date)
        last_date = data['Date'].iloc[-1]
        fut = fut_cal(user_date, last_date)

        if fut == 0:
            # Existing data prediction
            for col in data.columns[1:]:
                data[col] = data[col].fillna(data[col].mean())

            data['Date'] = pd.to_datetime(data['Date'])

            def existing_prediction(i):
                fd = data.iloc[i, 1:].tolist()  # Extract all columns except 'Date'

                result, mae = model.flood_classifier(filename, fd)

                discharge = round(data.iloc[i, 1], 2)
                floodrunoff = round(data.iloc[i, 2], 2)
                dailyrunoff = round(data.iloc[i, 3], 2)
                weeklyrunoff = round(data.iloc[i, 4], 2)
                mae = round(mae, 2)

                predicted = 'Normal' if result == 0 else 'High'
                actual = 'Normal' if data.iloc[i, -1] == 0 else 'High'

                return {
                    "discharge": discharge,
                    "floodrunoff": floodrunoff,
                    "dailyrunoff": dailyrunoff,
                    "weeklyrunoff": weeklyrunoff,
                    "meanabsoluteerrorr": mae,
                    "predicted": predicted,
                    "actualflood": actual
                }

            for i in range(len(data)):
                if data['Date'].iloc[i].date() == user_date.date():
                    return existing_prediction(i)

            print("Choose a valid date")
            return None
            
        else:
            # Future data prediction
            wtd = 1
            d1 = dp.discharge_forecast(filename, wtd)
            d2 = frp.flood_runoff_forecast(filename, wtd)
            d3 = drp.daily_runoff_forecast(filename, wtd)
            d4 = wrp.weekly_runoff_forecast(filename, wtd)
            
            data1 = pd.concat([d1, d2['flood runoff'], d3['daily runoff'], d4['weekly runoff']], axis=1)
            data1.index = pd.to_datetime(data1.index)

            def future_prediction(i):
                fd = data1.iloc[i].tolist()

                result, mae = model.flood_classifier(filename, fd)

                discharge = round(data1.iloc[i, 0], 2)
                floodrunoff = round(data1.iloc[i, 1], 2)
                dailyrunoff = round(data1.iloc[i, 2], 2)
                weeklyrunoff = round(data1.iloc[i, 3], 2)
                mae = round(mae, 2)

                predicted = 'Normal' if result == 0 else 'High'

                return {
                    "discharge": discharge,
                    "floodrunoff": floodrunoff,
                    "dailyrunoff": dailyrunoff,
                    "weeklyrunoff": weeklyrunoff,
                    "meanabsoluteerrorr": 'NIL',
                    "predicted": predicted,
                    "actualflood": 'NIL'
                }

            for i in range(len(data1)):
                if data1.index[i].date() == user_date.date():
                    return future_prediction(i)

            print("Choose a valid future date")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Test the function
results = drive("example", "2024-04-25")
print(results)
