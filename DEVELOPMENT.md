# Development Setup Guide

## TrialGuard AI - Development Environment Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### 1. Clone Repository
```bash
cd e:\PROJECT(A)\reena fyn yr
# Repository already initialized
cd trialguard-ai
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your configuration
```

### 5. Run Backend Server
```bash
cd backend
uvicorn main:app --reload

# API will be available at: http://localhost:8000
# API documentation at: http://localhost:8000/docs
```

### 6. Run Frontend (in new terminal)
```bash
cd frontend
streamlit run app.py

# Dashboard will open at: http://localhost:8501
```

## Project Structure Details

### Backend
- `main.py` - FastAPI application entry point
- `routes/` - API endpoints
  - `upload.py` - File upload endpoint
  - `process.py` - Data processing pipeline
  - `predict.py` - Anomaly detection predictions
  - `results.py` - Results retrieval
- `services/` - Business logic
  - `data_processor.py` - Data validation and preprocessing
  - `feature_engineering.py` - Feature creation
  - `anomaly_detection.py` - ML model inference
- `models/` - Data schemas
  - `schemas.py` - Pydantic models for validation
- `utils.py` - Utility functions

### Frontend
- `app.py` - Streamlit dashboard with multiple pages

### Data Directories
- `data/raw/` - Uploaded CSV files
- `data/processed/` - Processed datasets
- `data/features/` - Engineered features
- `data/results/` - Anomaly detection results
- `data/models/` - Saved ML models

## API Endpoints

### Upload Data
```bash
POST /api/upload
Content-Type: multipart/form-data

# Upload a CSV file
```

### Process Data
```bash
POST /api/process
Content-Type: application/json

{
  "filename": "trial_data.csv",
  "handle_missing": "mean"
}
```

### Generate Predictions
```bash
POST /api/predict
Content-Type: application/json

{
  "filename": "processed_trial_data.csv",
  "model_type": "isolation_forest"
}
```

### Get Results
```bash
GET /api/results/{filename}?risk_level=Suspicious&limit=100
```

### Get Summary
```bash
GET /api/summary/{filename}
```

## Testing

### Generate Sample Data
```bash
python -c "from backend.utils import generate_synthetic_trial_data; generate_synthetic_trial_data(output_path='data/raw/sample_trial.csv')"
```

## Debugging

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Check API Health
```bash
curl http://localhost:8000/health
```

## Deployment Notes

### Frontend (Streamlit Cloud)
1. Push code to GitHub
2. Deploy via Streamlit Cloud dashboard
3. Configure secrets for API URL

### Backend (Render/Railway)
1. Create account on Render or Railway
2. Deploy from GitHub
3. Set environment variables
4. Update API base URL in frontend

## Next Steps (Phase 2)

- [ ] Implement SHAP explainability
- [ ] Add Kafka streaming integration
- [ ] Build EDC system integration
- [ ] Implement multi-tenant authentication
- [ ] Add LLM-based anomaly explanations
- [ ] Implement PostgreSQL for scaling
- [ ] Add HIPAA compliance features
- [ ] Build admin dashboard

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Streamlit Docs: https://docs.streamlit.io/
- scikit-learn Docs: https://scikit-learn.org/
- Plotly Docs: https://plotly.com/python/
