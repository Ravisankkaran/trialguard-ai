"""
TrialGuard AI - Quick Start Script
Generate sample data and test the pipeline
"""

import sys
from pathlib import Path
import pandas as pd

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from utils import generate_synthetic_trial_data
from services.data_processor import DataProcessor
from services.feature_engineering import FeatureEngineer
from services.anomaly_detection import AnomalyDetectionService


def main():
    """Run complete pipeline with sample data"""
    
    print("🧪 TrialGuard AI - Quick Start\n")
    
    # Step 1: Generate sample data
    print("Step 1: Generating synthetic trial data...")
    data_path = Path("data/raw/sample_trial.csv")
    df = generate_synthetic_trial_data(
        n_patients=500,
        n_sites=10,
        n_visits=5,
        output_path=str(data_path)
    )
    print(f"✅ Generated {len(df)} records with {len(df.columns)} features\n")
    print(df.head())
    
    # Step 2: Process data
    print("\nStep 2: Processing data...")
    processor = DataProcessor()
    
    # Validate schema
    is_valid, issues = processor.validate_schema(data_path.name)
    if is_valid:
        print(f"✅ Schema validation passed")
    else:
        print(f"⚠️ Schema issues: {issues}")
    
    # Process data
    result = processor.process(data_path.name, handle_missing="mean")
    print(f"✅ Processed {result['rows_processed']} records")
    print(f"   Columns: {result['columns']}\n")
    
    # Step 3: Feature Engineering
    print("Step 3: Engineering features...")
    engineer = FeatureEngineer()
    processed_filename = f"processed_{data_path.name}"
    features_result = engineer.engineer_features(processed_filename)
    print(f"✅ Created {features_result['total_features']} features")
    print(f"   Patient-level: {features_result['feature_count']['patient_level']}")
    print(f"   Site-level: {features_result['feature_count']['site_level']}\n")
    
    # Step 4: Anomaly Detection
    print("Step 4: Running anomaly detection models...")
    anomaly_service = AnomalyDetectionService()
    
    models = ["isolation_forest", "lof", "autoencoder"]
    
    for model in models:
        print(f"\n  Running {model.replace('_', ' ').title()}...")
        features_filename = f"features_processed_{data_path.name}"
        result = anomaly_service.predict(features_filename, model_type=model)
        
        print(f"  ✅ {result['total_records']} records analyzed")
        print(f"     Anomalies detected: {result['anomalies_detected']} ({result['anomaly_percentage']:.2f}%)")
    
    # Step 5: Summary
    print("\n" + "="*50)
    print("✅ Pipeline Execution Complete!")
    print("="*50)
    print(f"\nData Files Created:")
    print(f"  Raw:      data/raw/{data_path.name}")
    print(f"  Processed: data/processed/processed_{data_path.name}")
    print(f"  Features:  data/features/features_processed_{data_path.name}")
    print(f"  Results:   data/results/results_*.csv")
    
    print("\n📊 Next Steps:")
    print("  1. Start backend: cd backend && uvicorn main:app --reload")
    print("  2. Start frontend: cd frontend && streamlit run app.py")
    print("  3. Upload data and monitor anomalies in the dashboard")
    
    print("\n📖 Documentation:")
    print("  - README.md - Project overview")
    print("  - DEVELOPMENT.md - Setup guide")
    print("  - DATA_DICTIONARY.md - Data reference")


if __name__ == "__main__":
    main()
