# TrialGuard AI - Architecture & Technical Specification

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Streamlit Dashboard (Port 8501)               │   │
│  │  - Upload UI                                    │   │
│  │  - Analytics Dashboard                          │   │
│  │  - Risk Heatmaps & Charts                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │ HTTP/JSON
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  /upload  /process  /predict  /results          │   │
│  └─────────────────────────────────────────────────┘   │
│                  (Port 8000)                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Business Logic Layer                      │
│  ┌──────────────────┬──────────────────┬──────────┐    │
│  │  Data Processor  │  Feature Eng.    │  ML Svc  │    │
│  │  - Validation    │  - Patient Feat  │  - IF    │    │
│  │  - Cleaning      │  - Site Features │  - LOF   │    │
│  │  - Normalization │  - Aggregation   │  - AE    │    │
│  └──────────────────┴──────────────────┴──────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Data Storage Layer                        │
│  ┌──────────┬──────────┬──────────┬──────────┐          │
│  │ Raw CSV  │Processed │ Features │ Results  │          │
│  │ Upload   │ Data     │ (engineered)       │          │
│  │          │          │          │          │          │
│  │ data/raw │proc/     │features/ │results/  │          │
│  └──────────┴──────────┴──────────┴──────────┘          │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Ingestion Module (`routes/upload.py`)
**Purpose:** Receive clinical trial datasets

**Features:**
- CSV file upload with validation
- Schema checking against expected format
- File storage in `data/raw/`

**API Endpoint:**
```
POST /api/upload
Content-Type: multipart/form-data
```

### 2. Data Processing Module (`services/data_processor.py`)
**Purpose:** Validate and preprocess raw data

**Operations:**
- Schema validation (check for required columns)
- Missing value handling (mean/median/drop/ffill)
- Data type conversion
- Normalization

**Methods:**
- `validate_schema()` - Check data format
- `process()` - Execute preprocessing pipeline

### 3. Feature Engineering Module (`services/feature_engineering.py`)
**Purpose:** Transform raw data into ML-ready features

**Patient-Level Features:**
- `visit_frequency` - Number of visits per patient
- `ae_rate` - Adverse event rate
- `pd_rate` - Protocol deviation rate
- `query_avg` - Average query count

**Site-Level Features:**
- `total_patients` - Patient count per site
- `site_ae_rate` - Site adverse event rate
- `site_pd_rate` - Site protocol deviation rate
- `query_density` - Query concentration

**Methods:**
- `engineer_features()` - Main feature creation
- `_create_patient_features()` - Patient aggregations
- `_create_site_features()` - Site aggregations

### 4. Anomaly Detection Module (`services/anomaly_detection.py`)
**Purpose:** Apply ML models for anomaly scoring

**Supported Models:**
1. **Isolation Forest** (Primary)
   - Fast, effective on high-dimensional data
   - Config: contamination=0.1
   - Use case: Real-time monitoring

2. **Local Outlier Factor** (Secondary)
   - Density-based approach
   - Config: n_neighbors=20, contamination=0.1
   - Use case: Local pattern detection

3. **Autoencoder** (Advanced)
   - Neural network-based reconstruction error
   - Use case: Complex pattern detection

**Scoring Pipeline:**
1. Feature scaling (StandardScaler)
2. Model inference
3. Score normalization (0-1)
4. Risk categorization

**Risk Categories:**
- Normal: 0.00-0.33 (routine monitoring)
- Suspicious: 0.33-0.66 (review required)
- Critical: 0.66-1.00 (immediate action)

### 5. Frontend Dashboard (`frontend/app.py`)
**Purpose:** Interactive visualizations and controls

**Pages:**
- **Dashboard** - Overview metrics, KPIs, visualizations
- **Data Upload** - File upload and processing
- **Analysis** - Model selection and filtering
- **Settings** - Configuration management

**Visualizations:**
- Risk distribution pie charts
- Anomaly score histograms
- Site heatmaps
- Patient risk rankings
- Time-series trends

## Data Flow

```
1. User uploads CSV file
   │
   └─> /api/upload (FastAPI route)
       │
       └─> DataProcessor.validate_schema()
           └─> Save to data/raw/
               │
               └─> User initiates processing
                   │
                   └─> /api/process
                       │
                       └─> DataProcessor.process()
                           └─> Handle missing values
                               └─> Save to data/processed/
                                   │
                                   └─> User selects model
                                       │
                                       └─> /api/predict
                                           │
                                           └─> FeatureEngineer.engineer_features()
                                               │
                                               └─> AnomalyDetectionService.predict()
                                                   │
                                                   ├─> IsolationForest.predict()
                                                   ├─> LOF.predict()
                                                   └─> Autoencoder.predict()
                                                       │
                                                       └─> Score & classify
                                                           │
                                                           └─> Save results
                                                               │
                                                               └─> Display in dashboard
```

## Technology Stack

### Backend
- **Framework:** FastAPI (async, modern)
- **Server:** Uvicorn (ASGI)
- **Data:** Pandas, NumPy
- **ML:** scikit-learn (Isolation Forest, LOF)
- **Database:** SQLite (MVP) → PostgreSQL (scale)

### Frontend
- **Framework:** Streamlit (rapid development)
- **Visualization:** Plotly (interactive), Matplotlib (static)

### DevOps/Deployment
- **Container:** Docker (optional for Phase 2)
- **Frontend Hosting:** Streamlit Cloud
- **Backend Hosting:** Render/Railway
- **Version Control:** Git/GitHub

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Upload latency | < 5s | ✅ Achievable |
| Processing latency | < 10s | ✅ Achievable |
| Prediction latency | < 2s | ✅ Achievable |
| Dashboard load time | < 3s | ✅ Achievable |
| Model accuracy | > 90% | 🔄 Validation needed |
| False positive rate | < 10% | 🔄 Validation needed |

## Database Schema (MVP - SQLite)

```sql
-- Uploaded Datasets
CREATE TABLE datasets (
    id INTEGER PRIMARY KEY,
    filename TEXT UNIQUE,
    upload_timestamp DATETIME,
    row_count INTEGER,
    column_count INTEGER,
    status TEXT
);

-- Processing Results
CREATE TABLE processing_results (
    id INTEGER PRIMARY KEY,
    dataset_id INTEGER,
    rows_processed INTEGER,
    missing_values JSON,
    timestamp DATETIME,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

-- Anomaly Predictions
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    dataset_id INTEGER,
    patient_id TEXT,
    site_id TEXT,
    anomaly_score FLOAT,
    anomaly_flag INTEGER,
    risk_level TEXT,
    model_type TEXT,
    timestamp DATETIME,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);
```

## Scaling Strategy (Phase 2)

### Database
- SQLite → PostgreSQL
- Connection pooling
- Indexing on common queries

### Processing
- Parallel feature engineering
- Batch processing for large files
- Kafka streaming for real-time

### ML Models
- Model versioning
- A/B testing framework
- Ensemble voting

### Infrastructure
- Load balancer
- Multiple API instances
- Caching layer (Redis)
- CDN for frontend

## Security Considerations

### Current (MVP)
- File type validation (CSV only)
- Size limits
- Error message suppression

### Phase 2
- User authentication (OAuth2/JWT)
- HIPAA compliance
- Data encryption (at rest & in transit)
- Audit logging
- RBAC (Role-based access control)

## Error Handling Strategy

```python
# Graceful degradation
try:
    result = model.predict(X)
except MemoryError:
    # Fall back to simpler model
    result = fallback_model.predict(X)
except Exception as e:
    # Log and return user-friendly error
    return {"error": "Processing failed", "details": safe_message}
```

## Monitoring & Observability

**MVP:**
- Application logs
- Error tracking
- Basic metrics

**Phase 2:**
- Prometheus metrics
- Grafana dashboards
- Distributed tracing
- Custom alerting

## Testing Strategy

**Unit Tests:**
- Test each service independently
- Mock external dependencies

**Integration Tests:**
- Test API endpoints
- Test complete pipeline

**Performance Tests:**
- Latency benchmarks
- Memory profiling

## Version Control & CI/CD

```
main (production)
  ↑
release/v1.0 (staging)
  ↑
develop (development)
  ↑
feature/* (feature branches)
```

## Future Enhancements

1. **SHAP Explainability** - Feature importance visualization
2. **LLM Integration** - Automated anomaly explanations
3. **Real-time Streaming** - Kafka integration
4. **EDC Integration** - Direct data source connectivity
5. **Multi-tenant** - SaaS authentication
6. **Advanced ML** - XGBoost, Neural Networks
7. **Mobile App** - iOS/Android monitoring
