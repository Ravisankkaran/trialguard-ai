# TrialGuard AI - Data Dictionary

## Dataset Columns

### Patient Identifiers
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| patient_id | String | Unique patient identifier | P00001 |
| site_id | String | Clinical research site ID | Site 3 |

### Visit Information
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| visit_date | Date | Visit date (YYYY-MM-DD) | 2024-03-15 |
| visit_number | Integer | Sequential visit number | 1, 2, 3... |

### Clinical Outcomes
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| adverse_event | Binary/Count | Adverse event flag or count | 0 or 1 |
| protocol_deviation | Binary/Count | Protocol deviation flag | 0 or 1 |
| lab_values | Float | Laboratory test results | 95.5 |

### Data Quality
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| query_count | Integer | Number of data clarification queries | 0-50 |
| data_entry_delay_days | Integer | Days between visit and entry | 0-30 |

## Engineered Features

### Patient-Level Features
| Feature | Calculation | Use Case |
|---------|-----------|----------|
| visit_frequency | Count of visits per patient | Patient compliance |
| ae_rate | Mean adverse events | Safety profile |
| pd_rate | Mean protocol deviations | Compliance |
| query_avg | Mean query count | Data quality |

### Site-Level Features
| Feature | Calculation | Use Case |
|---------|-----------|----------|
| total_patients | Count of unique patients | Site capacity |
| site_ae_rate | Mean adverse events per site | Site safety performance |
| site_pd_rate | Mean protocol deviations | Site compliance |
| query_density | Total queries per site | Site data quality issues |

## Anomaly Score Interpretation

### Score Ranges
- **0.00 - 0.33**: Normal - No anomaly detected
- **0.33 - 0.66**: Suspicious - Potential anomaly
- **0.66 - 1.00**: Critical - High confidence anomaly

### Risk Categories
| Risk Level | Score Range | Action |
|-----------|------------|--------|
| Normal | 0.00-0.33 | Routine monitoring |
| Suspicious | 0.33-0.66 | Review & investigate |
| Critical | 0.66-1.00 | Immediate escalation |

## Expected Data Quality

### Missing Values
- Expected: < 5% missing per column
- Handling: mean/median imputation for numeric, drop for categorical

### Outliers
- Detection: Isolation Forest (primary model)
- Validation: Manual review recommended for critical cases

## Data Validation Rules

1. **patient_id**: Must be non-empty, unique within site
2. **site_id**: Must match predefined site list
3. **visit_date**: Must be within trial period
4. **adverse_event**: Binary (0/1) or count ≥ 0
5. **protocol_deviation**: Binary (0/1) or count ≥ 0
6. **lab_values**: Numeric, within expected range (typically 50-200)
7. **query_count**: Non-negative integer

## Data Volume Expectations

### MVP Scale
- **Patients**: 500-5,000
- **Sites**: 5-20
- **Visits**: 5-15 per patient
- **Records**: 5,000-75,000 rows

### Scaling (Phase 2)
- **Patients**: 10,000-100,000+
- **Records**: 100,000-1,000,000+ rows
- Storage: Move to PostgreSQL
- Processing: Batch + stream hybrid
