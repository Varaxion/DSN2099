import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — prevents blocking the server
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error

# Loading data
def discharge_forecast(filename, wtd):
    # Import raw data
    def import_data():
        raw_data_df = pd.read_excel('data/' + filename + '.xlsx', header=0)
        return raw_data_df

    raw_data_df = import_data()

    raw_data_df['Date'] = pd.to_datetime(raw_data_df['Date'])

    for i in range(1, len(raw_data_df.columns)):
        raw_data_df[raw_data_df.columns[i]] = raw_data_df[raw_data_df.columns[i]].fillna(
            raw_data_df[raw_data_df.columns[i]].mean())

    data = pd.DataFrame()
    data['Date'] = raw_data_df["Date"]
    data['Discharge'] = raw_data_df["Discharge"]
    data = data.set_index(['Date'])

    # Resampling
    daily = data.resample('D').sum()

    # Scaling
    values = daily['Discharge'].values.reshape(-1, 1)
    values = values.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    scale = daily
    scale["Discharge"] = scaled

    # Making dataset for Testing or Training
    def making_dataset(i=1):
        if i == 0:
            df1 = scale.iloc[6940:, :]
            df2 = scale.iloc[:6940, :]
            df2.reset_index(inplace=True)
            df2 = df2.rename(columns={'Date': 'ds', 'Discharge': 'y'})
            return df1, df2
        else:
            df2 = scale.iloc[:, :]
            df2.reset_index(inplace=True)
            df2 = df2.rename(columns={'Date': 'ds', 'Discharge': 'y'})
            return df2, df2

    df1, df2 = making_dataset(wtd)

    # Model (Statsmodels ARIMA)
    # Define the ARIMA model
    model = sm.tsa.ARIMA(df2['y'], order=(5,1,0)) # Example order, adjust as needed

    # Fit the ARIMA model
    arima_model = model.fit()

    # Predicting data
    def predicting_data(i=1):
        if i == 0:
            forecast = arima_model.forecast(steps=30 * 25) # Example steps, adjust as needed
            df3 = pd.DataFrame({'ds': pd.date_range(start=df2['ds'].iloc[-1], periods=30 * 25, freq='D'), 'yhat': forecast})
            df4 = df3.iloc[6940:-20, :]
        else:
            forecast = arima_model.forecast(steps=3000)
            df3 = pd.DataFrame({'ds': pd.date_range(start=df2['ds'].iloc[-1], periods=3000, freq='D'), 'yhat': forecast})
            df4 = df3
        return df4

    df4 = predicting_data(wtd)
    ypred = df4.iloc[:, 1:]
    ytest = df1.iloc[:, :]

    # (Plot display removed — non-interactive backend in use)

    df4.columns = ['Date', 'Discharge']
    values = df4['Discharge'].values.reshape(-1, 1)
    values = values.astype('float32')
    val = scaler.inverse_transform(values)
    df4['Discharge'] = val
    df4['Discharge'] = abs(df4['Discharge'])
    df4.to_csv('data/forecast/' + filename + '_discharge_forecast.csv', index=False)

    if wtd == 0:
        print("mean_absolute_error=", mean_absolute_error(ytest, ypred))

    return df4

# Example usage:
# discharge_forecast("your_filename", 0)  # Replace "your_filename" with the actual filename and 0 for training, 1 for testing
