"""
Feature Engineering Service
Creates features for anomaly detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
FEATURES_DIR = Path(__file__).parent.parent.parent / "data" / "features"
FEATURES_DIR.mkdir(parents=True, exist_ok=True)


class FeatureEngineer:
    """Feature engineering for clinical trial data"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.features_dir = FEATURES_DIR
    
    def engineer_features(self, filename: str) -> Dict:
        """
        Create patient-level and site-level features
        
        Args:
            filename: Processed CSV filename
        
        Returns:
            Feature engineering metadata
        """
        try:
            filepath = self.data_dir / filename
            df = pd.read_csv(filepath)
            
            # Patient-level features
            patient_features = self._create_patient_features(df)
            
            # Site-level features
            site_features = self._create_site_features(df)
            
            # Combine features
            combined_features = self._combine_features(patient_features, site_features, df)
            
            # Save features
            features_path = self.features_dir / f"features_{filename}"
            combined_features.to_csv(features_path, index=False)
            
            logger.info(f"Features engineered: {filename}")
            
            return {
                "total_features": len(combined_features.columns),
                "feature_count": {
                    "patient_level": len(patient_features.columns),
                    "site_level": len(site_features.columns)
                },
                "features_path": str(features_path)
            }
        
        except Exception as e:
            logger.error(f"Feature engineering error: {str(e)}")
            raise
    
    def _create_patient_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create patient-level features"""
        features = df[['patient_id']].drop_duplicates().reset_index(drop=True)
        
        # Visit frequency
        visit_freq = df.groupby('patient_id').size().reset_index(name='visit_frequency')
        features = features.merge(visit_freq, on='patient_id', how='left')
        
        # Adverse event rate
        if 'adverse_event' in df.columns:
            ae_rate = df.groupby('patient_id')['adverse_event'].mean().reset_index(name='ae_rate')
            features = features.merge(ae_rate, on='patient_id', how='left')
        
        # Protocol deviation rate
        if 'protocol_deviation' in df.columns:
            pd_rate = df.groupby('patient_id')['protocol_deviation'].mean().reset_index(name='pd_rate')
            features = features.merge(pd_rate, on='patient_id', how='left')
        
        # Query count average
        if 'query_count' in df.columns:
            query_avg = df.groupby('patient_id')['query_count'].mean().reset_index(name='query_avg')
            features = features.merge(query_avg, on='patient_id', how='left')
        
        return features
    
    def _create_site_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create site-level features"""
        features = df[['site_id']].drop_duplicates().reset_index(drop=True)
        
        # Total patients per site
        patient_count = df.groupby('site_id')['patient_id'].nunique().reset_index(name='total_patients')
        features = features.merge(patient_count, on='site_id', how='left')
        
        # Adverse event rate per site
        if 'adverse_event' in df.columns:
            ae_rate = df.groupby('site_id')['adverse_event'].mean().reset_index(name='site_ae_rate')
            features = features.merge(ae_rate, on='site_id', how='left')
        
        # Protocol deviation rate per site
        if 'protocol_deviation' in df.columns:
            pd_rate = df.groupby('site_id')['protocol_deviation'].mean().reset_index(name='site_pd_rate')
            features = features.merge(pd_rate, on='site_id', how='left')
        
        # Query density per site
        if 'query_count' in df.columns:
            query_density = df.groupby('site_id')['query_count'].sum().reset_index(name='query_density')
            features = features.merge(query_density, on='site_id', how='left')
        
        return features
    
    def _combine_features(self, patient_features: pd.DataFrame, 
                         site_features: pd.DataFrame, 
                         original_df: pd.DataFrame) -> pd.DataFrame:
        """Combine patient and site features"""
        # Merge patient features with site_id from original data
        df_with_site = original_df[['patient_id', 'site_id']].drop_duplicates()
        combined = patient_features.merge(df_with_site, on='patient_id', how='left')
        
        # Merge site features
        combined = combined.merge(site_features, on='site_id', how='left')
        
        return combined
