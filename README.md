<div align="center">
  
  # Sahay - Flood & Rainfall Intelligence
  
  *Hydrological forecasting, risk classification, and monthly rainfall analysis for Indian river basins and meteorological subdivisions.*
  
  <br />

  ![Version](https://img.shields.io/badge/version-1.0-blue.svg?style=for-the-badge)
  ![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)
  ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
  ![Tensorflow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
  ![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
  ![ScikitLearn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

<br />

> [!NOTE]  
> **Sahay** (सहाय — *aid* in Sanskrit) was originally developed in 2024, as part of the academic curriculum for the **Project Exhibition - II** course at **VIT Bhopal University**. It has now been completely overhauled into a fully modern, dynamic web application, upgrading its model speed and visual aesthetics to state-of-the-art glassmorphic standards!

---

## 📸 Application Gallery

### The First Impression
Below is the modern, dark-glassmorphic landing interface of Sahay.

<div align="center">
  <img src="screenshots/1-home.png" alt="Sahay Home Landing Hero" width="98%">
</div>

<br/>

### Feature Landing Pages
Below are the parameter input interfaces for both hydrological modules, cleanly separated for user interaction.

<div align="center">
  <img src="screenshots/4-flood-input.png" alt="Flood Prediction Parameter Selection" width="48%">
  <img src="screenshots/8-rain-input.png" alt="Rainfall Subdivision Parameter Selection" width="48%">
</div>

<br/>

### Hydrological Forecasts & CNN Outputs
Below are the Matplotlib dynamically plotted outputs (Discharge trends and CNN bar comparisons).

<div align="center">
  <img src="screenshots/6-flood-output-graph.png" alt="Dynamic Flood Forecast Line Chart" width="48%">
  <img src="screenshots/10-rain-output-graph.png" alt="1D-CNN Rainfall Comparison Bar Chart" width="48%">
</div>

<br/>

<details>
<summary>Click here to expand the full step-by-step UI walkthrough! (All 14 Screenshots)</summary>
<br/>

### 1. Home & Navigation Flow
Visual presentation of the dark-mode landing experience, smooth scrolled transitions, and floating header navigation.

<div align="center">
  <img src="screenshots/1-home.png" alt="Landing Hero" width="31%">
  <img src="screenshots/2-home.png" alt="Core Modules Grid" width="31%">
  <img src="screenshots/3-home.png" alt="Scrolled Features" width="31%">
</div>

<br/>

### 2. Flood Prediction Pipeline Flow
The full prediction lifecycle: from custom date input parameters, through the glowing active loader, to the final dynamic chart results and LDA classification table.

<div align="center">
  <img src="screenshots/4-flood-input.png" alt="Flood Input Form" width="48%">
  <img src="screenshots/5-flood-process.png" alt="Active Loader Spinner" width="48%">
  <br/><br/>
  <img src="screenshots/6-flood-output-graph.png" alt="Dynamic Discharge Trend Chart" width="48%">
  <img src="screenshots/7-flood-output-metrics.png" alt="Classification Table & MAE" width="48%">
</div>

<br/>

### 3. Rainfall Forecasting Module Flow
The full analysis lifecycle: from subdivision select triggers, through the local model loading state, to the dynamically formatted 1D-CNN monthly bar chart comparison and performance metrics.

<div align="center">
  <img src="screenshots/8-rain-input.png" alt="Rainfall Input Form" width="48%">
  <img src="screenshots/9-rain-process.png" alt="Active Loader Spinner" width="48%">
  <br/><br/>
  <img src="screenshots/10-rain-output-graph.png" alt="1D-CNN Predictions Bar Chart" width="48%">
  <img src="screenshots/11-rain-output-metrics.png" alt="Performance Evaluation Scores" width="48%">
</div>

<br/>

### 4. Technical Dossier & Team Showcase (About Page)
High-level overview of our technical approach layers, newly added Core Modules grids, and the hyperlinked Team-204 member grid.

<div align="center">
  <img src="screenshots/12-about.png" alt="Technical Approach Cards" width="31%">
  <img src="screenshots/13-about.png" alt="Core Modules Grid" width="31%">
  <img src="screenshots/14-about.png" alt="Team-204 Credits Grid" width="31%">
</div>

</details>

---

## 🌌 Overview & System Features

**Sahay v1.0** is an end-to-end Hydrological Intelligence web application engineered to predict flood risks and analyze rainfall patterns across India. It bridges the gap between complex deep learning models and direct emergency preparedness.

### Core platform highlights:
* **Flood Prediction Pipeline:** Forecasts hydrological discharge, flood runoff, daily runoff, and weekly runoff up to late 2026 for five major Indian river catchments (Cauvery, Godavari, Krishna, Mahanadi, Son). It applies ARIMA time-series models and classifies the output risk state (Normal / High) utilizing a pre-trained Linear Discriminant Analysis (LDA) classifier.
* **1D-CNN Rainfall Analysis:** Forecasts monthly precipitation (April–December) across all 36 meteorological subdivisions of India using a 1D Convolutional Neural Network trained on over 120 years of IMD climate records (1901–2021).
* **Model Cache Optimization:** Eliminates slow model retraining by dynamically serializing and caching trained CNN models (`.h5` formats) per subdivision. Subsequent regional queries load in milliseconds!
* **Dynamic Chart Generation:** Instantly generates high-readability, color-synchronized charts using Matplotlib (Agg backend). Highlights prediction nodes and trendlines within a glassmorphic color coordinate system.
* **Premium Loader States:** Interactive submit buttons that slide and collapse on submission to yield high-fidelity, glowing circular CSS loading spinners.
* **Legacy Preservation:** The entire historical codebase (`v0`), including the original training Prophet scripts, data workbooks, original screenshots, and academic PDFs, is fully preserved inside `v0Archive/` to document the project's evolution.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, Jinja2, CSS3 | Dark Glassmorphic design system (`sahay.css`) using Google Font *Outfit*. |
| **Backend Engine** | Python, Flask, Werkzeug | Highly responsive Flask micro-framework managing routing, serialization, and plot delivery. |
| **Time-Series Forecast** | Statsmodels (ARIMA) | Dynamic auto-regressive statistical models projecting 3000 days forward. |
| **Deep Learning** | Keras, TensorFlow | 1D-CNN neural network trained on over a century of IMD history. |
| **ML Classification** | Scikit-Learn | Linear Discriminant Analysis (LDA) with SMOTE-balanced training. |
| **Data Orchestration** | Pandas, NumPy | Data cleaning, mean-imputation, and scaling arrays. |
| **Visual Graphics** | Matplotlib | Programmatic rendering of synchronized theme plots (using the Agg backend). |

---

## 📂 Project Architecture

```text
📦 DSN2099
 ┣ 📂 screenshots/         # High-resolution UI screenshots
 ┣ 📂 app/                 # Modern Optimized Application (v1.0)
 ┃ ┣ 📂 data/              # Active river worksheets & IMD rainfall CSV
 ┃ ┃ ┗ 📂 forecast/        # Dynamic ARIMA forecasted river CSV files
 ┃ ┣ 📂 static/            # Design system, SVGs, and generated plots
 ┃ ┃ ┣ 📂 img/             # Brand graphics and dynamic chart target outputs (flood.png, rainfall.png)
 ┃ ┃ ┗ 📜 sahay.css        # Premium Dark Glassmorphic custom CSS files
 ┃ ┣ 📂 templates/         # Jinja2 views (base.html, index.html, about.html, etc.)
 ┃ ┣ 📂 trained/           # Cached 1D-CNN subdivision Keras models (.h5)
 ┃ ┣ 📜 app.py             # Main Flask server entry point & routing endpoints
 ┃ ┣ 📜 flood_pipeline.py  # Flood risk calculator & dynamic plot engine
 ┃ ┣ 📜 model.py           # LDA model training & prediction orchestration
 ┃ ┣ 📜 rainfall.py        # 1D-CNN model architecture, caching, & bar chart plotter
 ┃ ┗ 📜 timeseries_forecaster.py # Underlying ARIMA forecaster algorithms
 ┣ 📂 v0Archive/           # Archived Legacy Codebase & Raw Worksheets
 ┃ ┣ 📂 Archive/           # Original Prophet training scripts & Jupyter confusion notebooks
 ┃ ┣ 📂 data/              # Legacy excel sheets & raw CSVs
 ┃ ┣ 📂 docs/              # Original Project Report, presentation, and VIT syllabus
 ┃ ┣ 📂 legacyUI/          # Screenshots of the original legacy prototype submission
 ┃ ┣ 📂 static/            # Legacy prototype styles, JS scripts, and images
 ┃ ┣ 📂 templates/         # Legacy prototype HTML templates
 ┃ ┣ 📂 trained/           # Legacy trained Prophet pickles (.pkl) & LDA models
 ┃ ┗ 📜 requirements.txt   # Original package dependencies
 ┣ 📜 .env.example         # Sample environment configurations
 ┣ 📜 README.md            # Overhauled project documentation
 ┗ 📜 requirements.txt     # Main environment dependencies list
```

---

## ⚠️ Model Assumptions & Limitations

For academic transparency, Sahay's mathematical and neural pipelines rely on the following bounds:

### 1. ARIMA Forecasting Assumptions
* **Stationarity Constraint:** ARIMA models assume that the underlying hydrological process is stationary (or can be made stationary by differencing). It struggles to adapt to extreme climate-driven anomalies (such as once-in-a-century cloudbursts or severe sudden dam releases) which violate linear historical trend assumptions.
* **Forecast Horizon Decay:** The forecast accuracy degrades progressively as the step size approaches its maximum boundary (3000 days / late 2026), meaning statistical errors compound over long projections.

### 2. LDA Classification Constraints
* **Telemeter Dependency:** The LDA classifier relies on four simultaneous inputs (`Discharge`, `flood runoff`, `daily runoff`, `weekly runoff`). If sensor telemetry fails upstream for even a single metric, classification cannot execute.
* **Class Homoscedasticity:** LDA assumes normally distributed features and equal covariance matrices across risk classes (Normal vs. High). Severe data skewness is balanced using SMOTE, but non-linear features could benefit from Kernel methods.

### 3. 1D-CNN Rainfall Limitations
* **Macro-scale Resolution:** The 1D-CNN operates on IMD's monthly subdivision records. While highly accurate for analyzing seasonal precipitation distributions (April–December) on a sub-continental scale, it **cannot** predict micro-scale localized downpours, hourly convective showers, or urban flash floods.
* **Fixed Timeline Boundary:** The neural network is trained on the historical timeline ending in 2021. Real-world telemetry updates are required for subsequent years.

---

## 🚀 Getting Started

Follow these step-by-step instructions to boot the Sahay intelligence platform on your local machine.

### 1. Set Up Your Environment
Ensure you have Python 3.9+ installed. Open a terminal and navigate to the project directory:
```bash
# Clone the repository and enter the directory
git clone <repository-url>
cd DSN2099

# Create and activate a python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all package dependencies
pip install -r requirements.txt
```

### 2. Initialize Environment Configurations
Generate your local environment config file:
```bash
# Copy the example environment template
cp .env.example .env
```
*Note: Make sure to edit `.env` and set a strong `SECRET_KEY` for session encryption.*

### 3. Run the Server
You can launch the server using either the pure Python entry point or the Flask command-line interface.

**Option A: Launch via pure Python (Recommended)**
```bash
cd app
python app.py
```

**Option B: Launch via Flask CLI**
```bash
cd app
flask --app app run --debug
```

> [!TIP]
> The Flask web server will compile its routing schemas and actively listen on **`http://127.0.0.1:5000`**. Open this address in your web browser to explore Sahay!

---

## ⏭️ Project Continuation

This project was later expanded and continued as a comprehensive **Predictive Disaster Intelligence & Rapid Emergency Response** portal under the **EPICS (DSN3099)** course.

The new iteration introduces major features including a lightning-fast Blood Bank Locator, Emergency Contacts Directory, Interactive Disaster SOPs, and an Incident Reporting Simulator.

🔗 **[View DSN3099 Repository](https://github.com/Varaxion/DSN3099)**

---

## 📜 License

The source code in this project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> [!WARNING]
> **Documentation Exception:** All academic documentation, reports, and presentations located within the `v0Archive/docs/` directory are explicitly excluded from this license and remain the restricted intellectual property of their respective authors and VIT Bhopal University.

---

## 🎓 Academic Origins & Contribution

This repository originated as an academic project for **VIT Bhopal University** by **Team-204** as part of the **Project Exhibition - II** course in 2024. The original conceptual prototype was a collaborative effort by the following team members:

| Name | Registration No. |
| :--- | :---: |
| [**Kavya**](https://github.com/varaxion) | `22BCE10385` |
| [**Simarpreet Singh**](https://github.com/Simarpreet-2607) | `22BCE10914` |
| [**Sneha Mishra**](https://github.com/MISHSNEHA) | `22BCE10932` |
| [**Pooja**](https://github.com/PrajapatPooja) | `22BCE10984` |
| [**Ashish Kumar**](https://github.com/ashish416) | `22BCE11353` |

<br/>

> [!NOTE]
> **v1.0 Overhaul:** While the initial data gathering and legacy model iterations were developed collaboratively by the collective team, the complete system architectural overhaul, 1D-CNN model cache integration, dynamic dark-mode Matplotlib engine, responsive glassmorphic loaders, and the entire premium v1.0 CSS design system were engineered by **Kavya**.

<br/>
<div align="center">
  <em>Sahay • Advancing Hydrological Safety through Intelligence.</em>
  <br /><br />
  <p style="font-size: 13px; color: #8b949e; letter-spacing: 0.5px;">&mdash; Re-engineered by Kavya &mdash;</p>
</div>
