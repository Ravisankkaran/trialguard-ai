"""
Data Upload Route
Handles CSV file uploads and validation
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import logging
import shutil

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload clinical trial dataset (CSV)
    
    - **file**: CSV file with clinical trial data
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        file_path = UPLOAD_DIR / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded successfully: {file.filename}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "message": "Dataset uploaded successfully",
            "path": str(file_path)
        }
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/upload-status")
async def upload_status():
    """Check uploaded datasets"""
    try:
        files = list(UPLOAD_DIR.glob("*.csv"))
        return {
            "status": "success",
            "uploaded_files": [f.name for f in files],
            "count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
