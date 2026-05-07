# 📊 Intelligent Anomaly Monitoring System
### *Machine Learning Based System Monitoring & Explainable AI Dashboard*

[![System Health: Healthy](https://img.shields.io/badge/System%20Health-Healthy-brightgreen)](#) 
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LSTM](https://img.shields.io/badge/ML%20Model-LSTM-orange.svg)](#)

**Live Demo:** [Check out the Live Dashboard](https://explainable-ai-anomaly-detection-for-small-businesses-dkyywvwa.streamlit.app/) 

---

## 🚀 Project Overview
In modern industrial and business environments, manual monitoring of time-series data is impossible at scale. This project provides an **End-to-End Intelligent Monitoring System** that doesn't just detect anomalies—it explains them.

By combining **Deep Learning (LSTM)** with **Statistical Rule Engines**, this system converts raw sensor data into actionable business intelligence, helping small to medium enterprises (SMEs) reduce downtime and prevent system failures.

### Key Features
* **Real-time Detection:** Hybrid approach using LSTM Neural Networks and Z-Score statistics.
* **Explainable AI (XAI):** Automatically classifies anomalies as "Spikes," "Drops," or "Drifts."
* **Proactive Insights:** Suggests solutions based on the type and severity of the detected event.
* **Executive Dashboard:** High-level KPIs for quick decision-making.

---

## 🛠️ System Architecture
The system follows a modular pipeline designed for scalability:
1.  **Data Generation:** Synthetic simulation of industrial machine signals (sinusoidal patterns + noise).
2.  **Feature Engineering:** Calculation of Rolling Means, Volatility, and Z-Scores.
3.  **ML Engine:** LSTM model trained to predict normal behavior and flag deviations.
4.  **Logic Layer:** Rule-based classification of anomaly types and severity levels.
5.  **Frontend:** An interactive Streamlit dashboard for data visualization.

---

## 📈 Dashboard Walkthrough

### 1. High-Level System Health
The dashboard opens with a **KPI Layer** providing an instant snapshot of system performance, including weekly observation counts and anomaly rates.

### 2. Signal Intelligence
The **Signal Monitoring Timeline** compares raw values against the rolling mean to visualize trends, while the **Z-Score Detection** chart provides mathematical proof for every alert triggered.

### 3. Root Cause Analysis
We categorize anomalies by type and severity to help engineers prioritize their response.
* **Anomaly Type Distribution:** Breakdown of Spikes vs. Drops.
* **Severity Distribution:** Categorization into Medium, High, and Critical based on statistical deviation.

---

## 🔬 Technical Deep Dive

### Statistical Foundation
The system utilizes the **Z-Score** to quantify how far a data point deviates from the mean:
$$Z = \frac{x - \mu}{\sigma}$$
* $Z < 2$: Normal Behavior
* $Z > 3$: Strong Anomaly (Action Required)

### Feature Correlation
To enable root-cause analysis, the system includes a **Correlation Heatmap**. This helps users understand which features (like sudden value changes vs. long-term trends) are driving the anomalies.

---

## 💡 Potential Causes & Solutions
The **Insight Panel** provides human-readable explanations. Instead of a "True/False" flag, the system explains:
> **Latest Anomaly:** Spike detected at 12:39:00.
> **Potential Cause:** A recent deviation in the monitored signal exceeded the threshold.
> **Suggested Solution:** Check power supply stability or sensor calibration.