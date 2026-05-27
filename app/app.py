from flask import Flask, render_template, request, flash, redirect, url_for
import os
import flood_pipeline
import rainfall
import flood_alerts

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refresh_flood')
def refresh_flood():
    flood_alerts.water_level_predictor()  # Refresh the flood warning data
    return redirect(url_for('flood_home'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/flood_home')
def flood_home():
    res = flood_alerts.alerting()
    res = ['Flood ALERT for ' + alert for alert in res]
    return render_template('flood_form.html', result=res)


@app.route('/rainfall_home')
def rainfall_home():
    return render_template('rainfall_form.html')


@app.route('/flood_result', methods=['POST', 'GET'])
def flood_result():
    if request.method == 'POST':
        if len(request.form['DATE']) == 0:
            flash("Please enter a date.")
            return redirect(url_for('flood_home'))
        else:
            user_date = request.form['DATE']
            river = request.form['SEL']
            results_dict = flood_pipeline.drive(river, user_date)
            if results_dict is None:
                flash("No data found for the selected river and date. Please try a different combination.")
                return redirect(url_for('flood_home'))
            table = list(results_dict.values())
            return render_template('flood_results.html', result=table)
    else:
        return redirect(url_for('flood_home'))


@app.route('/rainfall_result', methods=['POST', 'GET'])
def rainfall_result():
    if request.method == 'POST':
        if len(request.form['Year']) == 0:
            flash("Please select a year.")
            return redirect(url_for('rainfall_home'))
        else:
            year = request.form['Year']
            region = request.form['SEL']
            mae, score = rainfall.rainfall(year, region)
            if mae == "NIL":
                flash(f"No rainfall data available for {region} in {year}.")
                return redirect(url_for('rainfall_home'))
            return render_template('rainfall_results.html', Mae=mae, Score=score)
    else:
        return redirect(url_for('rainfall_home'))


if __name__ == '__main__':
    app.run(debug=True)
