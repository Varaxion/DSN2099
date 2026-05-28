import os
import pandas as pd
import timeseries_forecaster as tsf
import model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def futCal(userDate, endDate):
    if userDate > endDate:
        return 1
    return 0

def plot_flood_graph(filename, data, selected_idx, is_future=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    # Get window of 15 days before and 15 days after
    start_idx = max(0, selected_idx - 15)
    end_idx = min(len(data) - 1, selected_idx + 15)
    
    window_data = data.iloc[start_idx:end_idx + 1]
    dates = pd.to_datetime(window_data['Date'])
    
    # The discharge column is 'Discharge'
    y_values = window_data['Discharge']
    
    selected_date = pd.to_datetime(data['Date'].iloc[selected_idx])
    selected_val = data['Discharge'].iloc[selected_idx]
    
    fig = plt.figure(figsize=(12, 7))
    fig.suptitle(f"Discharge Trend - {filename.capitalize()}", fontsize=18, color='#f1f5f9', fontweight='bold', y=0.96)
    
    ax = fig.add_subplot(111)
    
    line_color = '#3b82f6' if not is_future else '#a78bfa'
    label_text = 'Historical Discharge' if not is_future else 'Forecasted Discharge'
    
    ax.plot(dates, y_values, color=line_color, linewidth=2.5, label=label_text)
    
    # Highlight the selected date
    ax.axvline(x=selected_date, color='#ef4444', linestyle='--', alpha=0.8, linewidth=1.5, label='Selected Date')
    ax.scatter(selected_date, selected_val, color='#ef4444', s=100, zorder=5, edgecolor='#f1f5f9', linewidth=1.5)
    
    # Add value annotation
    ax.annotate(f"{selected_val:.2f}", 
                xy=(selected_date, selected_val), 
                xytext=(10, 10), 
                textcoords='offset points', 
                color='#ef4444', 
                fontweight='bold',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc="#0d1424", ec="#ef4444", lw=1, alpha=0.8))

    ax.set_ylabel("Discharge (m³/s)", fontsize=14, color='#f1f5f9', fontweight='bold', labelpad=15)
    ax.set_xlabel("Date", fontsize=14, color='#f1f5f9', fontweight='bold', labelpad=15)
    
    leg = ax.legend(fontsize=13, facecolor='#0d1424', edgecolor='none')
    for text in leg.get_texts():
        text.set_color('#f1f5f9')

    ax.set_facecolor('#0d1424')
    fig.patch.set_facecolor('#0a0e1a')
    ax.tick_params(colors='#f1f5f9', labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.15, color='#94a3b8')
    
    # Format x-axis dates nicely
    fig.autofmt_xdate()

    img_path = os.path.join(BASE_DIR, 'static', 'img', 'flood.png')
    
    # Ensure static/img directory exists
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    
    plt.savefig(img_path, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=120)
    plt.close(fig)

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
                    plot_flood_graph(filename, data, i, is_future=False)
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
                    plot_flood_graph(filename, data1, i, is_future=True)
                    return futurePrediction(i)

            return None

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred in drive(): {e}")
        return None
