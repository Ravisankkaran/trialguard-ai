"""
Data Processing Service
Handles data validation and preprocessing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Expected columns in clinical trial dataset
EXPECTED_COLUMNS = [
    'patient_id', 'site_id', 'visit_date', 'adverse_event',
    'protocol_deviation', 'lab_values', 'query_count'
]

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


class DataProcessor:
    """Data validation and preprocessing"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.processed_dir = PROCESSED_DIR
    
    def validate_schema(self, filename: str) -> Tuple[bool, list]:
        """Validate CSV schema"""
        try:
            filepath = self.data_dir / filename
            df = pd.read_csv(filepath, nrows=5)
            
            issues = []
            for col in EXPECTED_COLUMNS:
                if col not in df.columns:
                    issues.append(f"Missing column: {col}")
            
            return len(issues) == 0, issues
        
        except Exception as e:
            logger.error(f"Schema validation error: {str(e)}")
            return False, [str(e)]
    
    def process(self, filename: str, handle_missing: str = "mean") -> Dict:
        """
        Process and preprocess dataset
        
        Args:
            filename: CSV filename
            handle_missing: Strategy for missing values
        
        Returns:
            Processing result metadata
        """
        try:
            filepath = self.data_dir / filename
            df = pd.read_csv(filepath)
            
            # Store original shape
            original_shape = df.shape
            
            # Handle missing values
            missing_before = df.isnull().sum().to_dict()
            
            if handle_missing == "drop":
                df = df.dropna()
            elif handle_missing == "ffill":
                df = df.fillna(method='ffill')
            elif handle_missing == "median":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            else:  # mean (default)
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            
            # Save processed data
            processed_path = self.processed_dir / f"processed_{filename}"
            df.to_csv(processed_path, index=False)
            
            logger.info(f"Dataset processed: {filename}")
            
            return {
                "rows_processed": len(df),
                "columns": list(df.columns),
                "missing_values": missing_before,
                "original_rows": original_shape[0],
                "original_columns": original_shape[1],
                "processed_path": str(processed_path)
            }
        
        except Exception as e:
            logger.error(f"Data processing error: {str(e)}")
            raise
