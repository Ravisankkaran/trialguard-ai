"""
Results Retrieval Route
Handles result fetching and filtering
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from services.anomaly_detection import AnomalyDetectionService

logger = logging.getLogger(__name__)
router = APIRouter()
anomaly_service = AnomalyDetectionService()


class ResultsRequest(BaseModel):
    filename: str
    risk_level: str = None  # Normal, Suspicious, Critical, or None for all
    limit: int = 100


@router.get("/results/{filename}")
async def get_results(filename: str, risk_level: str = None, limit: int = 100):
    """
    Retrieve anomaly detection results
    
    - **filename**: Results filename
    - **risk_level**: Filter by risk level (Normal/Suspicious/Critical)
    - **limit**: Maximum results to return
    """
    try:
        results = anomaly_service.get_results(filename, risk_level, limit)
        
        return {
            "status": "success",
            "filename": filename,
            "total_results": len(results),
            "results": results
        }
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Results file not found")
    except Exception as e:
        logger.error(f"Results retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{filename}")
async def get_summary(filename: str):
    """
    Get summary statistics of anomaly detection results
    
    - **filename**: Results filename
    """
    try:
        summary = anomaly_service.get_summary(filename)
        
        return {
            "status": "success",
            "summary": summary
        }
    
    except Exception as e:
        logger.error(f"Summary error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
