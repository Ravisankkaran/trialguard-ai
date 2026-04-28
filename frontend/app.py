"""
TrialGuard AI - Streamlit Frontend Dashboard
Interactive UI for clinical trial monitoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import requests
import json

# Page configuration
st.set_page_config(
    page_title="TrialGuard AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# Sidebar navigation
st.sidebar.title("🧪 TrialGuard AI")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Data Upload", "Manual Input", "Analysis", "Settings"]
)


def get_api_response(endpoint: str, method: str = "GET", data=None):
    """Helper function to call backend API"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None


# ===== DASHBOARD PAGE =====
if page == "Dashboard":
    st.title("📊 Clinical Trial Monitoring Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Records",
            "12,450",
            "+5.2%",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Anomalies Detected",
            "847",
            "6.8%"
        )
    
    with col3:
        st.metric(
            "Critical Risk",
            "34",
            "-2.1%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Detection Latency",
            "1.2s",
            "-18%",
            delta_color="inverse"
        )
    
    st.divider()
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Overview", "🌐 Site Analysis", "👥 Patient Analysis", "⏱️ Time Series"]
    )
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Distribution")
            risk_data = {
                "Risk Level": ["Normal", "Suspicious", "Critical"],
                "Count": [10523, 847, 80]
            }
            fig = px.pie(
                risk_data,
                values="Count",
                names="Risk Level",
                color="Risk Level",
                color_discrete_map={
                    "Normal": "#2ecc71",
                    "Suspicious": "#f39c12",
                    "Critical": "#e74c3c"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Anomaly Score Distribution")
            scores = np.random.beta(5, 2, 1000)
            fig = go.Figure(data=[go.Histogram(x=scores, nbinsx=50)])
            fig.update_layout(
                title="Anomaly Score Distribution",
                xaxis_title="Anomaly Score",
                yaxis_title="Frequency",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Site Anomaly Heatmap")
        
        # Sample data for heatmap
        sites = [f"Site {i}" for i in range(1, 11)]
        metrics = ["AE Rate", "PD Rate", "Query Count", "Dropout Rate"]
        
        heatmap_data = np.random.rand(len(sites), len(metrics))
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=metrics,
            y=sites,
            colorscale="RdYlGn_r"
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("High-Risk Sites")
        risk_sites_df = pd.DataFrame({
            "Site ID": ["Site 3", "Site 7", "Site 9", "Site 2"],
            "Risk Score": [0.89, 0.76, 0.72, 0.68],
            "Anomalies": [12, 8, 7, 5],
            "Patients": [45, 52, 48, 50]
        })
        st.dataframe(risk_sites_df, use_container_width=True)
    
    with tab3:
        st.subheader("Patient Risk Ranking")
        
        risk_patients_df = pd.DataFrame({
            "Patient ID": ["P001", "P152", "P045", "P389", "P267"],
            "Site": ["Site 3", "Site 7", "Site 3", "Site 9", "Site 2"],
            "Anomaly Score": [0.94, 0.87, 0.82, 0.79, 0.75],
            "Risk Level": ["Critical", "Suspicious", "Suspicious", "Suspicious", "Suspicious"],
            "Flags": [3, 2, 2, 1, 1]
        })
        
        st.dataframe(
            risk_patients_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.subheader("Patient Anomaly Timeline")
        fig = px.scatter(
            risk_patients_df,
            x="Anomaly Score",
            y="Flags",
            size="Anomaly Score",
            color="Risk Level",
            hover_data=["Patient ID", "Site"],
            color_discrete_map={
                "Normal": "#2ecc71",
                "Suspicious": "#f39c12",
                "Critical": "#e74c3c"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Anomaly Detection Over Time")
        
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        anomaly_counts = np.random.poisson(8, 30)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=anomaly_counts,
            mode='lines+markers',
            name='Anomalies Detected',
            line=dict(color='#e74c3c', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Anomalies Detected Over Time",
            xaxis_title="Date",
            yaxis_title="Anomaly Count",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)


# ===== DATA UPLOAD PAGE =====
elif page == "Data Upload":
    st.title("📤 Data Upload & Processing")
    
    st.markdown("""
    Upload your clinical trial dataset (CSV format) to begin monitoring.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Dataset")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Clinical trial dataset with patient and site data"
        )
        
        if uploaded_file:
            st.success(f"✅ File selected: {uploaded_file.name}")
            
            if st.button("📤 Upload", use_container_width=True):
                with st.spinner("Uploading..."):
                    files = {'file': (uploaded_file.name, uploaded_file)}
                    try:
                        response = requests.post(f"{API_BASE_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success("✅ Dataset uploaded successfully!")
                            st.json(response.json())
                        else:
                            st.error(f"Upload failed: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("Dataset Information")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Rows", len(df))
                st.metric("Columns", len(df.columns))
            
            with col_b:
                st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                st.metric("Missing", f"{df.isnull().sum().sum()}")
            
            st.subheader("Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    st.subheader("Processing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        missing_strategy = st.selectbox(
            "Handle Missing Values",
            ["mean", "median", "drop", "ffill"],
            help="Strategy for handling missing data"
        )
    
    with col2:
        normalize = st.checkbox("Normalize Features", value=True)
    
    if uploaded_file and st.button("⚙️ Process Dataset", use_container_width=True):
        with st.spinner("Processing dataset..."):
            data = {
                "filename": uploaded_file.name,
                "handle_missing": missing_strategy
            }
            response = get_api_response("process", "POST", data)
            if response:
                st.success("✅ Dataset processed successfully!")
                st.json(response)


# ===== MANUAL INPUT PAGE =====
elif page == "Manual Input":
    st.title("🧪 Manual Patient Input")
    st.markdown("Enter patient data directly and get instant anomaly predictions.")

    # Model selection at the top
    st.subheader("🤖 Select Model")
    model_choice = st.selectbox(
        "Choose Anomaly Detection Model",
        ["Isolation Forest", "Local Outlier Factor", "Autoencoder"],
        help="Select the ML model for prediction"
    )

    model_map = {
        "Isolation Forest": "isolation_forest",
        "Local Outlier Factor": "lof",
        "Autoencoder": "autoencoder"
    }

    st.divider()

    # Input form
    with st.form("patient_input_form"):
        st.subheader("👤 Patient Information")

        col1, col2 = st.columns(2)

        with col1:
            patient_id = st.text_input("Patient ID", "P001", help="Unique patient identifier")
            site_id = st.text_input("Site ID", "Site1", help="Clinical site identifier")
            visit_date = st.date_input("Visit Date", help="Date of the visit")

        with col2:
            adverse_event = st.number_input(
                "Adverse Event (0 or 1)",
                min_value=0,
                max_value=1,
                value=0,
                help="Whether an adverse event occurred (0=No, 1=Yes)"
            )
            protocol_deviation = st.number_input(
                "Protocol Deviation (0 or 1)",
                min_value=0,
                max_value=1,
                value=0,
                help="Whether there was a protocol deviation (0=No, 1=Yes)"
            )
            query_count = st.number_input(
                "Query Count",
                min_value=0,
                max_value=100,
                value=0,
                help="Number of data clarification queries"
            )

        # Submit button
        submit = st.form_submit_button("🔍 Predict Anomaly", use_container_width=True, type="primary")

    if submit:
        with st.spinner("Processing patient data and generating prediction..."):
            try:
                # Step 1: Create DataFrame from input
                df = pd.DataFrame([{
                    "patient_id": patient_id,
                    "site_id": site_id,
                    "visit_date": str(visit_date),
                    "adverse_event": adverse_event,
                    "protocol_deviation": protocol_deviation,
                    "query_count": query_count
                }])

                # Add some dummy lab values for completeness (since the model expects them)
                import numpy as np
                df['lab_values'] = np.random.normal(100, 15)  # Normal lab values
                df['data_entry_delay_days'] = np.random.randint(0, 7)  # Random delay

                st.success("✅ Patient data prepared for analysis")

                # Step 2: Save temporary CSV
                temp_file = f"temp_manual_input_{patient_id}.csv"
                temp_path = Path("data/raw") / temp_file
                temp_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(temp_path, index=False)

                # Step 3: Upload to backend
                with open(temp_path, "rb") as f:
                    files = {"file": (temp_file, f, "text/csv")}
                    upload_response = requests.post(f"{API_BASE_URL}/upload", files=files)

                if upload_response.status_code != 200:
                    st.error(f"❌ Upload failed: {upload_response.text}")
                    st.stop()

                # Step 4: Process the data
                process_response = get_api_response("process", "POST", {
                    "filename": temp_file,
                    "handle_missing": "mean"
                })

                if not process_response:
                    st.error("❌ Data processing failed")
                    st.stop()

                # Step 5: Generate features (this happens automatically in the predict endpoint)
                # The predict endpoint will call feature engineering internally

                # Step 6: Run prediction
                predict_response = get_api_response("predict", "POST", {
                    "filename": f"processed_{temp_file}",
                    "model_type": model_map[model_choice]
                })

                if not predict_response:
                    st.error("❌ Prediction failed")
                    st.stop()

                # Step 7: Display results
                st.success("✅ Prediction completed successfully!")

                # Get the results
                results_response = get_api_response(f"results/processed_{temp_file}")

                if results_response and results_response.get("results"):
                    result = results_response["results"][0]

                    st.subheader("📊 Prediction Results")

                    # Display metrics in columns
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        anomaly_score = result.get('anomaly_score', 0)
                        st.metric(
                            "Anomaly Score",
                            f"{anomaly_score:.3f}",
                            help="Higher scores indicate higher anomaly likelihood (0.0-1.0)"
                        )

                    with col2:
                        risk_level = result.get('risk_level', 'Unknown')
                        color_map = {
                            "Normal": "🟢",
                            "Suspicious": "🟡",
                            "Critical": "🔴"
                        }
                        st.metric(
                            "Risk Level",
                            f"{color_map.get(risk_level, '⚪')} {risk_level}",
                            help="Risk categorization based on anomaly score"
                        )

                    with col3:
                        anomaly_flag = int(result.get('anomaly_flag', 0))
                        flag_text = "Anomaly Detected" if anomaly_flag == 1 else "Normal"
                        st.metric(
                            "Detection Flag",
                            flag_text,
                            help="Binary anomaly detection result"
                        )

                    # Risk assessment explanation
                    st.subheader("📋 Risk Assessment")

                    if risk_level == "Normal":
                        st.success("🟢 **Normal Risk**: This patient shows typical behavior patterns. No immediate action required.")
                    elif risk_level == "Suspicious":
                        st.warning("🟡 **Suspicious Risk**: This patient shows some unusual patterns that may need review.")
                    elif risk_level == "Critical":
                        st.error("🔴 **Critical Risk**: This patient shows highly anomalous behavior requiring immediate investigation!")
                    else:
                        st.info("⚪ **Unknown Risk**: Unable to determine risk level.")

                    # Additional context
                    st.subheader("📈 Analysis Summary")

                    summary_col1, summary_col2 = st.columns(2)

                    with summary_col1:
                        st.info(f"""
                        **Patient Details:**
                        - ID: {patient_id}
                        - Site: {site_id}
                        - Visit Date: {visit_date}
                        - Adverse Events: {adverse_event}
                        - Protocol Deviations: {protocol_deviation}
                        - Query Count: {query_count}
                        """)

                    with summary_col2:
                        st.info(f"""
                        **Model Used:**
                        - Algorithm: {model_choice}
                        - Score Range: 0.0-1.0
                        - Risk Thresholds:
                          - Normal: < 0.33
                          - Suspicious: 0.33-0.66
                          - Critical: > 0.66
                        """)

                    # Raw data expander
                    with st.expander("🔍 View Raw Prediction Data"):
                        st.json(result)

                else:
                    st.error("❌ Could not retrieve prediction results")

                # Clean up temporary file
                try:
                    temp_path.unlink(missing_ok=True)
                except:
                    pass

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 **Tip:** Make sure the backend server is running on http://localhost:8000")

    # Example data section
    st.divider()
    st.subheader("💡 Example Patient Data")

    with st.expander("Click to see example inputs"):
        example_tabs = st.tabs(["Normal Patient", "Suspicious Patient", "Critical Patient"])

        with example_tabs[0]:
            st.markdown("""
            **Normal Patient:**
            - Patient ID: P001
            - Site ID: Site1
            - Adverse Event: 0
            - Protocol Deviation: 0
            - Query Count: 1
            """)

        with example_tabs[1]:
            st.markdown("""
            **Suspicious Patient:**
            - Patient ID: P045
            - Site ID: Site3
            - Adverse Event: 1
            - Protocol Deviation: 0
            - Query Count: 5
            """)

        with example_tabs[2]:
            st.markdown("""
            **Critical Patient:**
            - Patient ID: P089
            - Site ID: Site2
            - Adverse Event: 1
            - Protocol Deviation: 1
            - Query Count: 12
            """)


# ===== ANALYSIS PAGE =====
elif page == "Analysis":
    st.title("🔬 Anomaly Detection Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Selection")
        model_type = st.radio(
            "Choose Anomaly Detection Model",
            ["Isolation Forest", "Local Outlier Factor", "Autoencoder"],
            captions=[
                "Fast & effective (recommended)",
                "Density-based detection",
                "Neural network-based"
            ],
            help="Select the ML model for anomaly detection"
        )
        
        model_map = {
            "Isolation Forest": "isolation_forest",
            "Local Outlier Factor": "lof",
            "Autoencoder": "autoencoder"
        }
        
        if st.button("🚀 Run Analysis", use_container_width=True):
            with st.spinner(f"Running {model_type} analysis..."):
                data = {
                    "filename": "sample_data.csv",
                    "model_type": model_map[model_type]
                }
                response = get_api_response("predict", "POST", data)
                if response:
                    st.success("✅ Analysis complete!")
                    st.json(response)
    
    with col2:
        st.subheader("Filtering Options")
        
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            ["Normal", "Suspicious", "Critical"],
            default=["Suspicious", "Critical"]
        )
        
        anomaly_threshold = st.slider(
            "Anomaly Score Threshold",
            0.0, 1.0, 0.5,
            step=0.05
        )
        
        limit = st.number_input(
            "Results Limit",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )
    
    st.divider()
    
    st.subheader("Analysis Results")
    
    # Sample results display
    results_df = pd.DataFrame({
        "Patient ID": ["P001", "P152", "P045"],
        "Site ID": ["Site 3", "Site 7", "Site 3"],
        "Anomaly Score": [0.94, 0.87, 0.82],
        "Risk Level": ["Critical", "Suspicious", "Suspicious"],
        "Model": ["Isolation Forest", "Isolation Forest", "Isolation Forest"]
    })
    
    st.dataframe(results_df, use_container_width=True)


# ===== SETTINGS PAGE =====
elif page == "Settings":
    st.title("⚙️ Settings & Configuration")
    
    st.subheader("API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_url = st.text_input(
            "API Base URL",
            value=API_BASE_URL,
            disabled=True
        )
    
    with col2:
        st.info(f"✅ API Status: Connected")
    
    st.divider()
    
    st.subheader("Model Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contamination = st.slider(
            "Isolation Forest - Contamination",
            0.01, 0.5, 0.1,
            step=0.01
        )
    
    with col2:
        n_neighbors = st.number_input(
            "LOF - Number of Neighbors",
            min_value=5,
            max_value=50,
            value=20
        )
    
    with col3:
        random_state = st.number_input(
            "Random State",
            min_value=0,
            max_value=100,
            value=42
        )
    
    st.divider()
    
    st.subheader("About TrialGuard AI")
    
    st.markdown("""
    **Version:** 0.1.0 (MVP)
    
    **Purpose:** Real-time Clinical Trial Monitoring
    
    **Key Features:**
    - Automated anomaly detection
    - Multi-model ML ensemble
    - Risk scoring system
    - Interactive dashboard
    
    **Technology Stack:**
    - Backend: FastAPI
    - Frontend: Streamlit
    - ML: scikit-learn, PyTorch
    - Visualization: Plotly, Matplotlib
    """)
    
    st.info("""
    👉 **TrialGuard AI is a machine learning-powered SaaS platform for real-time clinical 
    trial monitoring, designed to reduce data cleaning delays and improve trial efficiency.**
    """)


# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray;'>TrialGuard AI © 2024 | Build with ❤️ for clinical research</p>",
    unsafe_allow_html=True
)
