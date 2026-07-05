# 📊 Intelligent Anomaly Monitoring System
### *Machine Learning Based System Monitoring & Explainable AI Dashboard*

[![System Health: Healthy](https://img.shields.io/badge/System%20Health-Healthy-brightgreen)](#) 
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)

**Live Demo:** [Check out the Live Dashboard](https://explainable-ai-anomaly-detection-for-small-businesses-dkyywvwa.streamlit.app/) 

---

# 🚀 Project Overview

## Problem Statement

Modern systems such as industrial machines, sensors, and business processes generate continuous time-series data. Monitoring these signals manually becomes difficult as data volume grows, while traditional threshold-based methods often fail to capture more complex patterns.

**Core Question:**

How can unusual system behavior be detected automatically while providing simple, easy-to-understand insights?

---
![Dashboard Overview](Images/Dashboard_Overview.png)
---

## Objective

This project aims to:

* Detect anomalies using an LSTM model supported by statistical analysis.
* Classify anomalies using rule-based logic.
* Visualize system performance through an interactive Streamlit dashboard.
* Demonstrate how machine learning and statistics can support monitoring applications.

---

# 🏗️ System Architecture

```
Synthetic Data Generation
          ↓
Feature Engineering
          ↓
LSTM Model
          ↓
Statistical Analysis
          ↓
Processed Dataset
          ↓
Streamlit Dashboard
```

---

# 🔬 Data & Machine Learning Pipeline

## 1. Synthetic Data Generation

A synthetic industrial signal was generated to simulate machine behavior using:

* Daily cyclic patterns
* Random noise
* Controlled anomaly injection

Injected anomaly types include:

* Spike
* Drop
* Drift
* Level Shift
* Volatility

This provides a controlled environment for testing anomaly detection methods.

---

## 2. Feature Engineering

The raw signal was transformed into analytical features before model prediction.

| Feature         | Purpose                       |
| --------------- | ----------------------------- |
| rolling_mean_30 | Trend detection               |
| rolling_std_30  | Volatility measurement        |
| value_diff      | Sudden change detection       |
| pct_change      | Relative variation            |
| z_score         | Statistical anomaly detection |

---

## 3. LSTM-Based Detection

The LSTM model learns normal sequential behavior and predicts whether a signal deviates from expected patterns.

The model output is then combined with statistical analysis to improve anomaly detection.

---

## 4. Rule-Based Classification

Instead of only identifying whether an anomaly exists, detected events are categorized into meaningful types:

| Type        | Description           |
| ----------- | --------------------- |
| Spike       | Sudden increase       |
| Drop        | Sudden decrease       |
| Drift       | Gradual change        |
| Level Shift | Structural change     |
| Volatility  | Increased instability |

---

# 📊 Dashboard Overview

The Streamlit dashboard provides a complete view of system behavior through multiple visual components.

### KPI Summary

Displays:

* Latest observations
* Weekly anomalies
* Weekly anomaly rate
* Overall anomaly rate
* System health indicator

---

### Signal Monitoring

Visualizes:

* Raw signal
* Rolling average
* Detected anomalies

This helps identify when and where abnormal behavior occurs.

---

### Z-Score Analysis

Shows statistical deviation from the mean along with upper and lower thresholds, providing a mathematical basis for anomaly detection.

---

### Anomaly Analysis

Includes:

* Anomaly type distribution
* Severity distribution
* Daily and weekly anomaly trends

These visuals help summarize overall system behavior.

---

### Feature Correlation

A correlation heatmap highlights relationships between engineered features such as:

* Value
* Percentage Change
* Z-Score
* Value Difference

---

### Insight Panel

The dashboard summarizes:

* Latest detected anomaly
* Most severe anomaly
* Possible cause
* Example recommendations

---

# ⭐ Key Highlights

* Combined LSTM predictions with statistical analysis for anomaly detection.
* Applied feature engineering techniques to improve model inputs.
* Built an interactive Streamlit dashboard for monitoring and visualization.
* Used rule-based logic to classify detected anomalies into meaningful categories.

---

# 📈 Project Limitations

* Uses synthetic data instead of real industrial signals.
* Processes batch data rather than live streaming data.
* Model retraining is not automated.
* Currently supports monitoring of a single signal.

---

# 🚀 Future Improvements

* Real-time data streaming using Kafka or MQTT.
* Automated model retraining.
* Email or SMS alert integration.
* Support for monitoring multiple sensors simultaneously.

---

# ✅ Conclusion

This project demonstrates an end-to-end workflow for anomaly detection by combining machine learning, statistical analysis, feature engineering, and interactive visualization. It highlights how time-series data can be monitored effectively while presenting results in a simple and interpretable dashboard.

---

