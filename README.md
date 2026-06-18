<div align="center">

# 🛡️ PhishGuard

### Neural Network-Powered Phishing URL Detection

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

An AI-powered cybersecurity system that detects phishing URLs in real-time.  
PhishGuard extracts **30 structural features** from any URL and classifies it using a Multi-Layer Perceptron (MLP) Neural Network — delivering instant, high-accuracy security verdicts.

</div>

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time Detection** | Instant URL scanning via an asynchronous REST API with < 100ms latency |
| 🧠 **Neural Network Engine** | Scikit-Learn MLP Classifier with `(32, 16)` architecture achieving **93% accuracy** |
| 🔗 **30-Feature Extraction** | Lexical analysis of IP usage, domain structure, SSL, URL shorteners & more |
| 🗄️ **Data Pipeline** | MongoDB integration for scalable data ingestion with aggregation analytics |
| 🌐 **Web Interface** | Clean, dark-themed UI for interactive URL scanning |

---

## 🏛️ Architecture

```
                   ┌──────────────────────────────────────────────┐
                   │              PhishGuard System               │
                   └──────────────────────────────────────────────┘

 ┌─────────────┐        ┌─────────────────┐        ┌──────────────────┐
 │  Web UI     │  POST  │  FastAPI Server │  ───►  │  Feature         │
 │  (HTML/JS)  │ ─────► │  /predict       │        │  Extractor       │
 └─────────────┘        └────────┬────────┘        │  (30 features)   │
                                 │                 └────────┬─────────┘
                                 │                          │
                                 ▼                          ▼
                         ┌────────────────┐         ┌────────────────┐
                         │  JSON Response │ ◄─────  │  MLP Neural    │
                         │  verdict +     │         │  Network Model │
                         │  confidence    │         │  (.pkl)        │
                         └────────────────┘         └────────────────┘

 ┌──────────────────────────────────────────────────────────────────┐
 │  Training Pipeline:  CSV ──► MongoDB ──► train.py ──► model.pkl  │
 └──────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

<table>
<tr>
<td><b>Category</b></td>
<td><b>Technologies</b></td>
</tr>
<tr>
<td>Backend</td>
<td>FastAPI · Uvicorn · Python 3.13+</td>
</tr>
<tr>
<td>Machine Learning</td>
<td>Scikit-Learn · Pandas · NumPy · Joblib</td>
</tr>
<tr>
<td>Database</td>
<td>MongoDB · PyMongo</td>
</tr>
<tr>
<td>Frontend</td>
<td>HTML5 · CSS3 · Vanilla JavaScript</td>
</tr>
</table>

---

## 📁 Project Structure

```
PhishGuard/
├── api/
│   ├── main.py                 # FastAPI application & /predict endpoint
│   └── feature_extractor.py    # URL feature extraction pipeline (30 features)
├── ml_engine/
│   ├── train.py                # MLP model training & evaluation
│   ├── db_pipeline.py          # CSV → MongoDB data ingestion pipeline
│   └── phishing_nn_model.pkl   # Serialized trained model
├── templates/
│   └── index.html              # Web scanning interface
├── static/
│   ├── style/style.css         # Dark-theme UI styling
│   └── script/script.js        # Frontend API integration
├── data/
│   └── phishingData.csv        # Training dataset
├── .env.example                # Environment config template
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.13+**
- **MongoDB** — [Download & Install](https://www.mongodb.com/try/download/community) (must be running on port `27017`)

### 1️⃣ Clone & Install

```bash
git clone https://github.com/ziadalaa7/PhishGuard.git
cd PhishGuard
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if your MongoDB runs on a custom host/port:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=phishing_Database
```

### 3️⃣ Seed Database & Train Model

```bash
python ml_engine/db_pipeline.py    # Load CSV data into MongoDB
python ml_engine/train.py          # Train the MLP model & save .pkl
```

### 4️⃣ Launch the API

```bash
uvicorn api.main:app --reload
```

The API is now live at `http://localhost:8000` — open `templates/index.html` in your browser to use the web interface.

---

## 📡 API Reference

### `POST /predict`

Analyze a URL for phishing indicators.

**Request:**

```json
{
  "url": "https://www.example.com"
}
```

**Response:**

```json
{
  "verdict": "Legitimate",
  "confidenceScore": 0.97
}
```

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | `string` | `"Legitimate"` or `"Phishing"` |
| `confidenceScore` | `float` | Model confidence (0.0 – 1.0) |

**Example with cURL:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 93% |
| **Precision** | 93% |
| **Recall** | 93% |
| **Prediction Latency** | < 100ms |
| **Model Size** | ~60 KB |

---

## 🔍 Extracted Features (30)

The feature extractor performs lexical and structural analysis on each URL, including:

- **IP Address** detection in domain
- **URL Length** classification (short / medium / long)
- **URL Shortener** service detection (bit.ly, tinyurl, etc.)
- **`@` Symbol** presence
- **Double Slash `//`** redirect detection
- **Hyphen `-`** in domain name
- **Subdomain Depth** (dot count analysis)
- **SSL/HTTPS** validation
- **Non-standard Port** usage
- **HTTPS Token** in domain name

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by Ramez Fawzy Ragheb**

</div>
