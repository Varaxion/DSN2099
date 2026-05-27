import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib
matplotlib.use('Agg')
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _arima_forecast(filename, target_column, freq, steps, train_cutoff=6940):
    """
    Helper function to run the core ARIMA forecasting for a target column.
    """
    data_path = os.path.join(BASE_DIR, 'data', f'{filename}.xlsx')
    raw_data_df = pd.read_excel(data_path, header=0)
    raw_data_df['Date'] = pd.to_datetime(raw_data_df['Date'])

    for col in raw_data_df.columns[1:]:
        raw_data_df[col] = raw_data_df[col].fillna(raw_data_df[col].mean())

    data = pd.DataFrame({'Date': raw_data_df['Date'], target_column: raw_data_df[target_column]})
    data = data.set_index(['Date'])
    
    # Resample based on frequency
    resampled = data.resample(freq).sum()

    values = resampled[target_column].values.reshape(-1, 1).astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    
    scale_df = resampled.copy()
    scale_df[target_column] = scaled
    scale_df.reset_index(inplace=True)
    scale_df = scale_df.rename(columns={'Date': 'ds', target_column: 'y'})

    model = sm.tsa.ARIMA(scale_df['y'], order=(5,1,0))
    arima_model = model.fit()

    forecast = arima_model.forecast(steps=steps)
    forecast_dates = pd.date_range(start=scale_df['ds'].iloc[-1], periods=steps, freq=freq)
    
    df4 = pd.DataFrame({'Date': forecast_dates, target_column: forecast})
    
    val = scaler.inverse_transform(df4[target_column].values.reshape(-1, 1).astype('float32'))
    df4[target_column] = abs(val)

    # Save output
    safe_target = target_column.replace(' ', '_').lower()
    out_path = os.path.join(BASE_DIR, 'data', 'forecast', f'{filename}_{safe_target}_forecast.csv')
    df4.to_csv(out_path, index=False)

    return df4

def discharge_forecast(filename, wtd):
    steps = 30 * 25 if wtd == 0 else 3000
    return _arima_forecast(filename, 'Discharge', 'D', steps)

def flood_runoff_forecast(filename, wtd):
    steps = 30 * 25 if wtd == 0 else 3000
    return _arima_forecast(filename, 'flood runoff', 'D', steps)

def daily_runoff_forecast(filename, wtd):
    steps = 30 * 25 if wtd == 0 else 3000
    return _arima_forecast(filename, 'daily runoff', 'D', steps)

def weekly_runoff_forecast(filename, wtd):
    steps = 25 if wtd == 0 else 450
    return _arima_forecast(filename, 'weekly runoff', 'W-SUN', steps)
