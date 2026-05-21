# Sahay - Flood & Rainfall Intelligence

> ML-powered flood prediction and rainfall analysis for Indian river systems and meteorological subdivisions.

---

## Overview

**Sahay** (सहाय — *aid* in Sanskrit) is a Flask web application for hydrological intelligence, built during Project Exhibition 2. It provides:

- **Flood Prediction** — Predict water level classification (Normal / High) for five major Indian rivers using ARIMA time-series forecasting and an LDA classifier trained on historical hydrological data.
- **Rainfall Analysis** — Forecast monthly rainfall patterns for all Indian meteorological subdivisions using a 1D-CNN model trained on the IMD dataset (1901–2021).
- **Live Flood Alerts** — A notice board that flags rivers currently at high flood risk based on 12-month ARIMA forecasts.

---

## Features

- Query flood levels for historical dates (1998–2019) or forecast up to 12 months ahead
- Analyze monthly rainfall for any IMD subdivision from 1901 to 2021
- Live flood alert board with one-click refresh
- Dark glassmorphic UI — responsive, modern, no page reloads
- Chart output: ground truth vs. predicted monthly rainfall visualization

---

## Tech Stack

| Layer       | Technology                                      |
|-------------|--------------------------------------------------|
| Backend     | Python 3, Flask                                  |
| ML Models   | ARIMA (statsmodels), LDA (scikit-learn), 1D-CNN (Keras) |
| Data        | pandas, NumPy, scikit-learn, imbalanced-learn    |
| Frontend    | Jinja2 templates, Vanilla CSS (dark glassmorphic) |
| Font        | Outfit (Google Fonts)                            |

---

## Project Structure

```
DSN2099/
├── Code Base/                  # Main application
│   ├── main.py                 # Flask app and routes
│   ├── driver.py               # Flood prediction orchestrator
│   ├── model.py                # LDA flood classifier
│   ├── alerter.py              # Flood alert generator
│   ├── discharge.py            # ARIMA discharge forecaster
│   ├── flood_runoff.py         # ARIMA flood runoff forecaster
│   ├── daily_runoff.py         # ARIMA daily runoff forecaster
│   ├── weekly_runoff.py        # ARIMA weekly runoff forecaster
│   ├── rainfall.py             # 1D-CNN rainfall predictor
│   ├── requirements.txt        # Python dependencies
│   ├── data/                   # Excel data files and forecast CSVs
│   ├── trained/                # Pre-trained LDA .pkl model files
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── flood_entry.html
│   │   ├── flood_result.html
│   │   ├── rain_entry.html
│   │   ├── rain_result.html
│   │   └── about.html
│   └── static/
│       ├── sahay.css           # Design system (dark glassmorphic)
│       └── img/                # Flood image, rainfall chart output
├── v0Archive/                  # Original exhibition v0 preserved
├── User Interface/             # UI screenshots (v0)
├── Project Report.pdf          # Original project report
├── .env.example                # Environment variable template
└── README.md
```

---

## Local Setup

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   source venv/bin/activate # macOS/Linux
   ```

2. **Install dependencies:**

   ```bash
   pip install -r "Code Base/requirements.txt"
   ```

3. **Set up environment variables:**

   ```bash
   copy .env.example .env     # Windows
   cp .env.example .env       # macOS/Linux
   ```

   Edit `.env` and set a strong `SECRET_KEY`.

4. **Run the application** (from inside `Code Base/`):

   ```bash
   cd "Code Base"
   flask --app main run --debug
   ```

   The app will be available at `http://127.0.0.1:5000`.

---

## Notes

- `.env` is gitignored — never commit your secret key.
- `data/` and `trained/` contain the Excel datasets and pre-trained `.pkl` model files required at runtime.
- The `v0Archive/` folder preserves the original exhibition submission exactly.
- The rainfall chart is saved to `static/img/rainfall.png` on each analysis run.

---

## Team

**Team-204** — Project Exhibition 2, Vellore Institute of Technology

| Member             |
|--------------------|
| @Kavya              |
| @Simarpreet Singh   |
| @Sneha Mishra       |
| @Pooja Prajapat     |
| @Ashish Kumar       |
