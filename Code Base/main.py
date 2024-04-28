from flask import Flask, render_template, request, redirect, url_for, flash
import driver
import rainfall
import alerter

app = Flask(__name__)

app.secret_key = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refresh_flood')
def refresh_flood():
    alerter.water_level_predictor()  # To refresh the flood warning data
    return redirect(url_for('flood_home'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/flood_home')
def flood_home():
    res = alerter.alerting()
    res = ['Flood ALERT for ' + alert for alert in res]
    return render_template('flood_entry.html', result=res)


@app.route('/rainfall_home')
def rainfall_home():
    return render_template('rain_entry.html')


@app.route('/flood_result', methods=['POST', 'GET'])
def flood_result():
    if request.method == 'POST':
        if len(request.form['DATE']) == 0:
            flash("Please Enter Data!!")
            return redirect(url_for('flood_home'))
        else:
            user_date = request.form['DATE']
            river = request.form['SEL']
            results_dict = driver.drive(river, user_date)
            table = list(results_dict.values())
            return render_template('flood_result.html', result=table)
    else:
        return redirect(url_for('flood_home'))


@app.route('/rainfall_result', methods=['POST', 'GET'])
def rainfall_result():
    if request.method == 'POST':
        if len(request.form['Year']) == 0:
            flash("Please Enter Data!!")
            return redirect(url_for('rainfall_home'))
        else:
            year = request.form['Year']
            region = request.form['SEL']
            mae, score = rainfall.rainfall(year, region)
            return render_template('rain_result.html', Mae=mae, Score=score)
    else:
        return redirect(url_for('rainfall_home'))


if __name__ == '__main__':
    app.run(debug=True)
