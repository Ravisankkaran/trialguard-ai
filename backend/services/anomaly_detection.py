"""
Anomaly Detection Service
ML models for anomaly detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "features"
RESULTS_DIR = Path(__file__).parent.parent.parent / "data" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR = Path(__file__).parent.parent.parent / "data" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class AnomalyDetectionService:
    """Anomaly detection using multiple ML models"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.results_dir = RESULTS_DIR
        self.models_dir = MODELS_DIR
        self.scaler = StandardScaler()
    
    def predict(self, filename: str, model_type: str = "isolation_forest") -> Dict:
        """
        Generate anomaly scores and predictions
        
        Args:
            filename: Features CSV filename (or processed data filename)
            model_type: Model to use (isolation_forest/lof/autoencoder)
        
        Returns:
            Prediction metadata
        """
        try:
            # Load features
            filepath = self.data_dir / filename
            if not filepath.exists():
                # Try from processed dir - if found, we need to engineer features first
                from services.data_processor import PROCESSED_DIR
                processed_filepath = PROCESSED_DIR / filename
                if processed_filepath.exists():
                    # Automatically engineer features from processed data
                    from services.feature_engineering import FeatureEngineer
                    feature_engineer = FeatureEngineer()
                    features_result = feature_engineer.engineer_features(filename)
                    
                    # Now load the engineered features
                    features_filename = f"features_{filename}"
                    filepath = self.data_dir / features_filename
                else:
                    raise FileNotFoundError(f"Neither features nor processed data found for {filename}")
            
            df = pd.read_csv(filepath)
            
            # Select numeric features (exclude patient_id and site_id if present)
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Remove non-feature columns
            exclude_cols = ['patient_id', 'site_id']
            feature_cols = [col for col in numeric_cols if col not in exclude_cols]
            
            if not feature_cols:
                raise ValueError("No numeric feature columns found in the data")
            
            X = df[feature_cols].fillna(0)
            
            # Normalize features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train/predict based on model type
            if model_type == "isolation_forest":
                scores, flags = self._isolation_forest(X_scaled)
            elif model_type == "lof":
                scores, flags = self._lof(X_scaled)
            elif model_type == "autoencoder":
                scores, flags = self._autoencoder_simple(X_scaled)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Create results dataframe
            results_df = df.copy()
            results_df['anomaly_score'] = scores
            results_df['anomaly_flag'] = flags
            results_df['risk_level'] = self._calculate_risk_level(scores)
            
            # Save results
            results_path = self.results_dir / f"results_{model_type}_{filename}"
            results_df.to_csv(results_path, index=False)
            
            # Count anomalies
            anomaly_count = (flags == 1).sum()
            
            logger.info(f"Predictions generated: {filename} using {model_type}")
            
            return {
                "total_records": len(results_df),
                "anomalies_detected": int(anomaly_count),
                "anomaly_percentage": float((anomaly_count / len(results_df)) * 100),
                "results_path": str(results_path),
                "model_used": model_type
            }
        
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def _isolation_forest(self, X: np.ndarray) -> tuple:
        """Isolation Forest anomaly detection"""
        model = IsolationForest(contamination=0.1, random_state=42)
        flags = model.fit_predict(X)
        scores = -model.score_samples(X)  # Convert to anomaly scores
        
        # Normalize scores to 0-1
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
        
        # Convert flags (-1 -> 1, 1 -> 0)
        flags = np.where(flags == -1, 1, 0)
        
        return scores, flags
    
    def _lof(self, X: np.ndarray) -> tuple:
        """Local Outlier Factor anomaly detection"""
        model = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        flags = model.fit_predict(X)
        scores = -model.negative_outlier_factor_
        
        # Normalize scores
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
        
        # Convert flags
        flags = np.where(flags == -1, 1, 0)
        
        return scores, flags
    
    def _autoencoder_simple(self, X: np.ndarray) -> tuple:
        """
        Simple autoencoder using reconstruction error
        (PyTorch implementation optional for Phase 2)
        """
        # Simplified version: use mean squared error as anomaly score
        mean = np.mean(X, axis=0)
        reconstruction_error = np.mean((X - mean) ** 2, axis=1)
        
        # Normalize
        scores = (reconstruction_error - reconstruction_error.min()) / \
                (reconstruction_error.max() - reconstruction_error.min() + 1e-8)
        
        # Set threshold at 90th percentile
        threshold = np.percentile(scores, 90)
        flags = (scores > threshold).astype(int)
        
        return scores, flags
    
    def _calculate_risk_level(self, scores: np.ndarray) -> List[str]:
        """Convert anomaly scores to risk levels"""
        risk_levels = []
        for score in scores:
            if score < 0.33:
                risk_levels.append("Normal")
            elif score < 0.66:
                risk_levels.append("Suspicious")
            else:
                risk_levels.append("Critical")
        return risk_levels
    
    def get_results(self, filename: str, risk_level: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve results with optional filtering"""
        try:
            # Find results file
            results_files = list(self.results_dir.glob(f"*{filename}"))
            if not results_files:
                raise FileNotFoundError(f"No results found for {filename}")
            
            results_path = results_files[0]
            df = pd.read_csv(results_path)
            
            # Filter by risk level
            if risk_level:
                df = df[df['risk_level'] == risk_level]
            
            # Sort by anomaly score (descending)
            df = df.sort_values('anomaly_score', ascending=False)
            
            # Apply limit
            df = df.head(limit)
            
            return df.to_dict('records')
        
        except Exception as e:
            logger.error(f"Results retrieval error: {str(e)}")
            raise
    
    def get_summary(self, filename: str) -> Dict:
        """Get summary statistics"""
        try:
            results_files = list(self.results_dir.glob(f"*{filename}"))
            if not results_files:
                raise FileNotFoundError(f"No results found for {filename}")
            
            results_path = results_files[0]
            df = pd.read_csv(results_path)
            
            risk_counts = df['risk_level'].value_counts().to_dict()
            
            return {
                "total_records": len(df),
                "anomalies_detected": (df['anomaly_flag'] == 1).sum(),
                "risk_distribution": risk_counts,
                "average_anomaly_score": float(df['anomaly_score'].mean()),
                "max_anomaly_score": float(df['anomaly_score'].max()),
                "min_anomaly_score": float(df['anomaly_score'].min())
            }
        
        except Exception as e:
            logger.error(f"Summary error: {str(e)}")
            raise
    
    def predict_manual(self, data: Dict, model_type: str = "isolation_forest") -> Dict:
        """
        Generate prediction for single patient/site data
        
        Args:
            data: Dictionary with feature values
            model_type: Model to use (isolation_forest/lof/autoencoder)
        
        Returns:
            Single prediction result
        """
        try:
            # Create dataframe from input data
            df = pd.DataFrame(data)
            
            # Select numeric features (exclude patient_id and site_id)
            numeric_cols = [col for col in df.columns if col not in ['patient_id', 'site_id']]
            X = df[numeric_cols].fillna(0)
            
            # Normalize features
            X_scaled = self.scaler.fit_transform(X)
            
            # Generate prediction based on model type
            if model_type == "isolation_forest":
                scores, flags = self._isolation_forest(X_scaled)
            elif model_type == "lof":
                scores, flags = self._lof(X_scaled)
            elif model_type == "autoencoder":
                scores, flags = self._autoencoder_simple(X_scaled)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Get single prediction
            anomaly_score = float(scores[0])
            anomaly_flag = int(flags[0])
            risk_level = self._calculate_risk_level([anomaly_score])[0]
            
            return {
                "anomaly_score": anomaly_score,
                "anomaly_flag": anomaly_flag,
                "risk_level": risk_level
            }
        
        except Exception as e:
            logger.error(f"Manual prediction error: {str(e)}")
            raise
