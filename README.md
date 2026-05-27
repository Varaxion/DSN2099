# 🌊 Sahay - Flood & Rainfall Intelligence

> **Hydrological intelligence, forecasting, and automated alerting for Indian river systems.**

**Sahay** (सहाय — *aid* in Sanskrit) is a modern, end-to-end Machine Learning web application built to predict flood risks and analyze rainfall patterns across India. It leverages time-series forecasting and deep learning to deliver critical insights through a beautiful, glassmorphic UI.

Developed for **Project Exhibition 2** at Vellore Institute of Technology.

---

## ✨ Features

- **🌊 Flood Prediction Pipeline**
  - Analyzes historical hydrological data (1998–2019) across five major Indian rivers (Cauvery, Godavari, Krishna, Mahanadi, Narmada).
  - Uses **ARIMA** (AutoRegressive Integrated Moving Average) to forecast future discharge, flood runoff, daily runoff, and weekly runoff up to 3000 days ahead.
  - Classifies the flood risk (Normal / High) using a dynamically trained **Linear Discriminant Analysis (LDA)** model.
- **🌧️ Rainfall Analysis & Forecasting**
  - Forecasts monthly rainfall patterns across all Indian meteorological subdivisions.
  - Utilizes a **1D-CNN (Convolutional Neural Network)** trained on over a century of IMD data (1901–2021).
  - Generates instant, dynamic visualization charts comparing ground truth against predicted rainfall.
- **🚨 Live Alert Board**
  - A real-time notice board flagging rivers currently at high flood risk, automatically scanning 12-month ARIMA forecasts with a single click.
- **💎 Premium UI/UX**
  - Features a completely bespoke dark glassmorphic design system (`sahay.css`).
  - Fully responsive layout with smooth micro-animations, gradient buttons, and zero page-reloads for core interactions.

---

## 🛠️ Tech Stack

| Component | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, Jinja2, Vanilla CSS (Glassmorphism), Google Fonts (Outfit) |
| **Backend** | Python 3, Flask, Werkzeug |
| **Machine Learning** | scikit-learn (LDA), Keras/TensorFlow (1D-CNN), statsmodels (ARIMA) |
| **Data Processing** | Pandas, NumPy, imbalanced-learn (SMOTE) |
| **Visualization** | Matplotlib (Agg backend) |

---

## 🚀 Local Installation

1. **Clone and enter the directory:**
   ```bash
   git clone <repository-url>
   cd DSN2099
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   *Make sure to edit `.env` and set a strong `SECRET_KEY`.*

5. **Run the server:**
   ```bash
   cd app
   flask --app main run --debug
   ```
   Navigate to `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure

```text
DSN2099/
├── app/                    # Core Application Logic
│   ├── main.py             # Flask app & routing
│   ├── driver.py           # Flood ML orchestrator (ARIMA + LDA)
│   ├── rainfall.py         # 1D-CNN rainfall predictor
│   ├── data/               # Excel datasets & forecast CSVs
│   ├── trained/            # Pre-trained ML models
│   ├── static/sahay.css    # Glassmorphic design system
│   └── templates/          # Jinja2 views (base.html, index.html, etc.)
├── Screenshots/            # App previews
├── v0Archive/              # Preserved original exhibition submission (Legacy)
│   ├── legacyUI/           # Original UI screenshots
│   └── docs/               # Original project reports
└── README.md               # Project documentation
```

---

## 🤝 Team & Contributions

**Team-204** — Project Exhibition 2, Vellore Institute of Technology

| Member |
| :--- |
| @Kavya |
| @Simarpreet Singh |
| @Sneha Mishra |
| @Pooja Prajapat |
| @Ashish Kumar |

**V1.0 Overhaul:** While the initial conceptual prototype and data collection were developed collectively by Team-204, the complete architectural redesign, robust ML pipeline fixes, and the premium modern Glassmorphic V1.0 frontend were entirely engineered by Kavya (@varaxion).
