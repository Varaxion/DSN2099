import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error

def weekly_runoff_forecast(filename, wtd):
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
    data['weekly runoff'] = raw_data_df["weekly runoff"]
    data = data.set_index(['Date'])

    daily = data.resample('D').sum()
    weekly = data.resample('W').sum()

    values = weekly['weekly runoff'].values.reshape(-1, 1)
    values = values.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    scale = weekly
    scale["weekly runoff"] = scaled

    def making_dataset(i=1):
        if i == 0:
            df1 = scale.iloc[6940:, :]
            df2 = scale.iloc[:6940, :]
            df2.reset_index(inplace=True)
            df2 = df2.rename(columns={'Date': 'ds', 'weekly runoff': 'y'})
            return df1, df2
        else:
            df2 = scale.iloc[:, :]
            df2.reset_index(inplace=True)
            df2 = df2.rename(columns={'Date': 'ds', 'weekly runoff': 'y'})
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
            forecast = arima_model.forecast(steps=25) # Example steps, adjust as needed
            df3 = pd.DataFrame({'ds': pd.date_range(start=df2['ds'].iloc[-1], periods=25, freq='W-SUN'), 'yhat': forecast})
            df4 = df3.iloc[6940:-20, :]
        else:
            forecast = arima_model.forecast(steps=12) # Example steps, adjust as needed
            df3 = pd.DataFrame({'ds': pd.date_range(start=df2['ds'].iloc[-1], periods=12, freq='W-SUN'), 'yhat': forecast})
            df4 = df3
        return df4

    df4 = predicting_data(wtd)
    ypred = df4.iloc[:, 1:]
    ytest = df1.iloc[:, :]

    # Plotting and saving forecasted data
    plt.plot(df2['ds'], df2['y'], label='Actual')
    plt.plot(df4['ds'], df4['yhat'], label='Forecast')
    plt.xlabel('Date')
    plt.ylabel('Weekly Runoff')
    plt.title('Simple Test')
    plt.legend()
    plt.show()

    df4.columns = ['Date', 'weekly runoff']
    values = df4['weekly runoff'].values.reshape(-1, 1)
    values = values.astype('float32')
    val = scaler.inverse_transform(values)
    df4['weekly runoff'] = val
    df4['weekly runoff'] = abs(df4['weekly runoff'])
    df4.to_csv('data/forecast/' + filename + '_weekly_runoff_forecast.csv', index=False)

    if wtd == 0:
        print("mean_absolute_error=", mean_absolute_error(ytest, ypred))

    return df4
