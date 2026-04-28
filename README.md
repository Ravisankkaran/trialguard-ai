# TrialGuard AI 🧪

**Intelligent Clinical Trial Monitoring Platform**

TrialGuard AI is a machine learning-powered SaaS platform for real-time clinical trial monitoring, designed to reduce data cleaning delays and improve trial efficiency.

## 🎯 Vision

Detect anomalies early in ongoing clinical trials through:
- Real-time anomaly detection using ML
- Continuous monitoring of accumulating trial data
- Risk scoring for sites, patients, and variables
- Interactive dashboards with explainability

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Backend
```bash
cd backend
uvicorn main:app --reload
```

### 3. Run Frontend
```bash
cd frontend
streamlit run app.py
```

## 📂 Project Structure
```
trialguard-ai/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/                 # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── upload.py          # File upload endpoint
│   │   ├── process.py         # Data processing endpoint
│   │   ├── predict.py         # Anomaly prediction endpoint
│   │   └── results.py         # Results retrieval endpoint
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── data_processor.py  # Data validation & preprocessing
│   │   ├── feature_engineering.py  # Feature creation
│   │   └── anomaly_detection.py    # ML model inference
│   └── models/                # Data models & schemas
│       ├── __init__.py
│       └── schemas.py         # Pydantic models
├── frontend/
│   └── app.py                 # Streamlit dashboard
├── data/                      # Dataset storage
│   └── raw/                   # Raw CSV files
├── notebooks/                 # Jupyter notebooks
├── requirements.txt           # Python dependencies
└── README.md
```

## 🧠 Core Modules

### 4.1 Data Ingestion
- CSV upload with schema validation
- Simulated streaming (batch refresh)
- Kaggle dataset integration via kagglehub

### 4.2 Feature Engineering
**Patient-Level Features:**
- Visit frequency
- Average visit gap
- Event rate

**Site-Level Features:**
- Total patients
- Adverse event rate
- Protocol deviation rate
- Query density

### 4.3 Anomaly Detection Models
- **Isolation Forest** (primary)
- **Local Outlier Factor** (secondary)
- **Autoencoder** (advanced)

Output: Anomaly score + risk category (Normal/Suspicious/Critical)

### 4.4 Dashboard
- Site anomaly heatmap
- Patient risk ranking
- Time-series anomaly trends
- Drill-down analytics

## 📊 Key Features

✅ **MVP Scope:**
- CSV upload with validation
- Feature engineering pipeline
- Multi-model anomaly detection
- Interactive Streamlit dashboard
- Plotly visualizations

⏳ **Phase 2:**
- Real-time Kafka streaming
- EDC system integration
- Multi-tenant SaaS authentication

## 📈 Success Metrics

| Metric | Target |
|--------|--------|
| Detection latency | ↓ 40% |
| Data cleaning time | ↓ 30% |
| False positive rate | < 10% |
| User engagement | High |

## 🛠️ Technology Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **ML:** scikit-learn (Isolation Forest, LOF), PyTorch (Autoencoder)
- **Data:** Pandas, NumPy
- **Database:** SQLite (MVP) → PostgreSQL (scalable)
- **Visualization:** Plotly, Matplotlib
- **Deployment:** Streamlit Cloud (Frontend), Render/Railway (Backend)

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload clinical dataset (CSV) |
| `/process` | POST | Run data pipeline |
| `/predict` | POST | Generate anomaly scores |
| `/results` | GET | Fetch detection results |

## 🔐 Non-Functional Requirements

- **Scalability:** Modular microservices architecture
- **Performance:** < 2s prediction latency
- **Reliability:** Error handling for bad data
- **Security:** File validation & safe storage

## 🚀 Future Enhancements

- SHAP explainability layer
- LLM-based anomaly explanations
- Multi-user SaaS (auth system)
- Real-time streaming pipeline

## 📦 Dataset

Uses Phase III Clinical Trial Dataset from Kaggle (via kagglehub)

**Expected Columns:**
- `patient_id`: Unique patient identifier
- `site_id`: Clinical site
- `visit_date`: Visit timestamp
- `adverse_event`: Binary/count
- `protocol_deviation`: Binary/count
- `lab_values`: Numerical
- `query_count`: Data queries

## 👤 Target Users

- Clinical Data Managers
- Biostatisticians
- Clinical Research Associates (CRAs)
- Pharmaceutical companies

---

**Build with ❤️ for clinical research**
