# 🌾 AI-Based Mandi Price Comparator

> An ML-powered decision-support tool that helps farmers identify the most profitable market to sell their produce — factoring in real mandi prices and transport costs.

![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![ML](https://img.shields.io/badge/ML-scikit--learn%20%7C%20TensorFlow-orange)

---

## 📌 Problem Statement

Farmers in India often lack access to real-time, comparative pricing across agricultural markets (mandis). Without this information, they may sell at a suboptimal market, losing income after factoring in transportation expenses. This tool bridges that gap using ML-based price trend analysis.

---

## 🎯 Features

- 📊 **Multi-Mandi Price Comparison** — Fetches and compares produce prices across multiple APMC mandis
- 🚚 **Transport Cost Adjustment** — Computes net profit/loss after accounting for distance-based transport costs
- 📈 **ML Price Trend Analysis** — Uses historical price data to predict near-term price movements
- ✅ **Market Recommendation** — Recommends the single most profitable mandi for a given crop and location
- 🗺️ **Farmer-Friendly Input** — Simple inputs: crop name, current location, quantity

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| ML Models | scikit-learn, TensorFlow |
| Data Source | Agmarknet / data.gov.in (APMC price datasets) |
| Interface | Streamlit *(planned)* |
| Visualization | Matplotlib, Seaborn |

---

## 🧠 How It Works

```
Farmer Input (crop, location, quantity)
        ↓
Fetch current mandi prices for nearby markets
        ↓
Apply ML model for short-term price trend prediction
        ↓
Calculate net profit = mandi_price × quantity − transport_cost
        ↓
Rank markets and recommend the best option
```

---

## 📁 Project Structure

```
mandi-price-comparator/
│
├── data/                   # Raw and processed mandi price datasets
├── models/                 # Trained ML model files
├── src/
│   ├── data_loader.py      # Fetches and preprocesses price data
│   ├── model.py            # Price trend prediction model
│   ├── transport.py        # Transport cost calculator
│   └── recommender.py      # Final market ranking and recommendation
├── app.py                  # Streamlit UI (planned)
├── requirements.txt
└── README.md
```

---

## 🚧 Current Status

This project is actively under development. Here's what's done and what's next:

- [x] Problem scoping and dataset identification
- [x] Data preprocessing pipeline
- [ ] ML price trend model (in progress)
- [ ] Transport cost module
- [ ] Market ranking engine
- [ ] Streamlit frontend
- [ ] Live demo deployment

---

## 📊 Dataset

Using publicly available agricultural market price data from:
- [Agmarknet](https://agmarknet.gov.in) — Government of India's agricultural marketing portal
- [data.gov.in](https://data.gov.in) — Open government datasets for APMC mandi prices

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/charishmagowda106-oss/mandi-price-comparator.git
cd mandi-price-comparator

# Install dependencies
pip install -r requirements.txt

# Run the app (once available)
streamlit run app.py
```

---

## 💡 Motivation

This project was inspired by real challenges faced by farmers in rural Karnataka who lack decision-making tools to maximize earnings. By combining open government data with ML, the goal is to create a lightweight, accessible tool that can run even on low-bandwidth connections.
