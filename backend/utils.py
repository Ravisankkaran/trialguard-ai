"""
Utility functions for TrialGuard AI
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def generate_synthetic_trial_data(
    n_patients: int = 500,
    n_sites: int = 10,
    n_visits: int = 5,
    output_path: str = None
) -> pd.DataFrame:
    """
    Generate synthetic clinical trial dataset for testing
    
    Args:
        n_patients: Number of patients
        n_sites: Number of sites
        n_visits: Average visits per patient
        output_path: Optional path to save CSV
    
    Returns:
        Synthetic trial DataFrame
    """
    np.random.seed(42)
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for patient_id in range(1, n_patients + 1):
        site_id = np.random.randint(1, n_sites + 1)
        n_patient_visits = np.random.poisson(n_visits) + 1
        
        for visit_num in range(n_patient_visits):
            visit_date = start_date + timedelta(days=np.random.randint(0, 365))
            
            # Normal data
            adverse_event = np.random.binomial(1, 0.1)
            protocol_deviation = np.random.binomial(1, 0.05)
            lab_values = np.random.normal(100, 15)
            query_count = np.random.poisson(2)
            
            # Inject some anomalies
            if np.random.random() < 0.05:  # 5% anomalies
                adverse_event = 1
                protocol_deviation = 1
                lab_values = np.random.choice([50, 200])  # Outlier values
                query_count = np.random.randint(10, 20)
            
            data.append({
                'patient_id': f'P{patient_id:05d}',
                'site_id': f'Site {site_id}',
                'visit_date': visit_date.strftime('%Y-%m-%d'),
                'visit_number': visit_num + 1,
                'adverse_event': adverse_event,
                'protocol_deviation': protocol_deviation,
                'lab_values': lab_values,
                'query_count': query_count,
                'data_entry_delay_days': np.random.randint(0, 7)
            })
    
    df = pd.DataFrame(data)
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Synthetic data saved to {output_path}")
    
    return df


def create_feature_summary(df: pd.DataFrame) -> dict:
    """Create summary statistics for features"""
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_stats': df.describe().to_dict()
    }


def validate_required_columns(df: pd.DataFrame, required_columns: list) -> tuple:
    """Validate required columns exist"""
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing
