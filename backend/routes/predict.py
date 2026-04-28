"""
Anomaly Prediction Route
Handles ML model inference
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from services.anomaly_detection import AnomalyDetectionService

logger = logging.getLogger(__name__)
router = APIRouter()
anomaly_service = AnomalyDetectionService()


class PredictionRequest(BaseModel):
    filename: str
    model_type: str = "isolation_forest"  # isolation_forest, lof, autoencoder


class ManualPredictionRequest(BaseModel):
    patient_id: str
    visit_frequency: int
    ae_rate: float
    pd_rate: float
    query_avg: float
    site_id: str
    total_patients: int
    site_ae_rate: float
    site_pd_rate: float
    query_density: int
    model_type: str = "isolation_forest"


@router.post("/predict")
async def generate_predictions(request: PredictionRequest):
    """
    Generate anomaly scores and flags
    
    - **filename**: Processed CSV filename
    - **model_type**: ML model to use (isolation_forest/lof/autoencoder)
    """
    try:
        predictions = anomaly_service.predict(request.filename, request.model_type)
        
        logger.info(f"Predictions generated for {request.filename} using {request.model_type}")
        
        return {
            "status": "success",
            "message": "Predictions generated successfully",
            "model_used": request.model_type,
            "total_records": predictions.get("total_records"),
            "anomalies_detected": predictions.get("anomalies_detected"),
            "results_path": predictions.get("results_path")
        }
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict-manual")
async def manual_prediction(request: ManualPredictionRequest):
    """
    Generate anomaly prediction for single patient/site data
    
    - **patient_id**: Unique patient identifier
    - **visit_frequency**: Number of visits
    - **ae_rate**: Adverse event rate (0.0-1.0)
    - **pd_rate**: Protocol deviation rate (0.0-1.0)
    - **query_avg**: Average query count
    - **site_id**: Site identifier
    - **total_patients**: Total patients at site
    - **site_ae_rate**: Site adverse event rate
    - **site_pd_rate**: Site protocol deviation rate
    - **query_density**: Total queries at site
    - **model_type**: ML model to use
    """
    try:
        # Create single-row dataframe from input
        data = {
            "patient_id": [request.patient_id],
            "visit_frequency": [request.visit_frequency],
            "ae_rate": [request.ae_rate],
            "pd_rate": [request.pd_rate],
            "query_avg": [request.query_avg],
            "site_id": [request.site_id],
            "total_patients": [request.total_patients],
            "site_ae_rate": [request.site_ae_rate],
            "site_pd_rate": [request.site_pd_rate],
            "query_density": [request.query_density]
        }

        prediction = anomaly_service.predict_manual(data, request.model_type)

        logger.info(f"Manual prediction generated for patient {request.patient_id} using {request.model_type}")

        return {
            "status": "success",
            "message": "Manual prediction generated successfully",
            "model_used": request.model_type,
            "patient_id": request.patient_id,
            "site_id": request.site_id,
            "anomaly_score": prediction.get("anomaly_score"),
            "anomaly_flag": prediction.get("anomaly_flag"),
            "risk_level": prediction.get("risk_level")
        }

    except Exception as e:
        logger.error(f"Manual prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/available-models")
def get_available_models():
    """
    Get list of available ML models
    """
    return {
        "models": ["isolation_forest", "lof", "autoencoder"],
        "descriptions": {
            "isolation_forest": "Isolation Forest - Good for high-dimensional data",
            "lof": "Local Outlier Factor - Good for local anomalies",
            "autoencoder": "Autoencoder - Neural network based anomaly detection"
        }
    }


@router.get("/available-models")
async def available_models():
    """Get list of available anomaly detection models"""
    return {
        "models": [
            {
                "name": "isolation_forest",
                "description": "Primary model - Fast and effective",
                "status": "available"
            },
            {
                "name": "lof",
                "description": "Secondary model - Density-based",
                "status": "available"
            },
            {
                "name": "autoencoder",
                "description": "Advanced model - Neural network-based",
                "status": "available"
            }
        ]
    }
