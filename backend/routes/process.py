"""
Data Processing Route
Handles data validation and preprocessing
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from services.data_processor import DataProcessor

logger = logging.getLogger(__name__)
router = APIRouter()
processor = DataProcessor()


class ProcessRequest(BaseModel):
    filename: str
    handle_missing: str = "mean"  # mean, median, drop, ffill


@router.post("/process")
async def process_dataset(request: ProcessRequest):
    """
    Process and validate clinical trial dataset
    
    - **filename**: CSV filename to process
    - **handle_missing**: Strategy for missing values (mean/median/drop/ffill)
    """
    try:
        result = processor.process(request.filename, request.handle_missing)
        
        logger.info(f"Dataset processed: {request.filename}")
        
        return {
            "status": "success",
            "message": "Dataset processed successfully",
            "rows_processed": result.get("rows_processed"),
            "columns": result.get("columns"),
            "missing_values": result.get("missing_values")
        }
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate-schema")
async def validate_schema(filename: str):
    """
    Validate CSV schema against expected format
    
    - **filename**: CSV filename to validate
    """
    try:
        is_valid, issues = processor.validate_schema(filename)
        
        return {
            "status": "success" if is_valid else "invalid",
            "valid": is_valid,
            "issues": issues
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
