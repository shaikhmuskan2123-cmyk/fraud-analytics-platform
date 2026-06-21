import os
import streamlit as st
import pandas as pd
import plotly.express as px

from services.predictor import predict_transaction

from database.db import (
    create_tables,
    save_transaction,
    get_all_transactions,
    get_total_transactions,
    get_total_frauds,
    get_average_risk,
    get_latest_transaction
)

from services.report_generator import (
    generate_transaction_report
)

# -------------------------
# Initialize Database
# -------------------------

create_tables()

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Fraud Analytics Platform",
    page_icon="🛡️",
    layout="wide"
)



# -------------------------
# Title
# -------------------------

st.title("🛡️ Fraud Analytics Platform")

st.markdown("---")

# -------------------------
# Sidebar Inputs
# -------------------------

st.sidebar.header("Transaction Details")

amount = float(
    st.sidebar.text_input(
        "Amount",
        "1000"
    )
)

time = int(
    st.sidebar.text_input(
        "Hour of Transaction (0-23)",
        "12"
    )
)

transactions_today = int(
    st.sidebar.text_input(
        "Transactions Today",
        "1"
    )
)

is_foreign = st.sidebar.selectbox(
    "Foreign Transaction",
    ["No", "Yes"]
)

is_foreign = 1 if is_foreign == "Yes" else 0

is_high_risk_country = st.sidebar.selectbox(
    "High Risk Country",
    ["No", "Yes"]
)

is_high_risk_country = 1 if is_high_risk_country == "Yes" else 0

predict_button = st.sidebar.button(
    "Predict Fraud"
)

# -------------------------
# Prediction
# -------------------------

if predict_button:

    result = predict_transaction(
        amount,
        time,
        transactions_today,
        is_foreign,
        is_high_risk_country
    )

    save_transaction(
        amount,
        time,
        transactions_today,
        is_foreign,
        is_high_risk_country,
        result["prediction"],
        result["risk_score"],
        result["risk_level"]
    )

    st.subheader("Prediction Result")

    if result["prediction"] == 1:

        st.error(
            f"⚠ Fraud Detected ({result['risk_level']})"
        )

    else:

        st.success(
            f"✅ Normal Transaction ({result['risk_level']})"
        )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Risk Score",
        f"{result['risk_score']}%"
    )

    col2.metric(
        "Risk Level",
        result["risk_level"]
    )

    col3.metric(
        "Prediction",
        result["prediction"]
    )

    st.info(
        result["recommendation"]
    )

# -------------------------
# Dashboard Metrics
# -------------------------

st.markdown("---")

st.subheader("Analytics Dashboard")

total_transactions = get_total_transactions()
total_frauds = get_total_frauds()
average_risk = get_average_risk()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "Fraud Cases",
    total_frauds
)

col3.metric(
    "Average Risk",
    f"{average_risk}%"
)

# -------------------------
# Transaction History
# -------------------------

records = get_all_transactions()

columns = [
    "ID",
    "Amount",
    "Time",
    "Transactions Today",
    "Foreign",
    "High Risk Country",
    "Prediction",
    "Risk Score",
    "Risk Level",
    "Created At"
]

if len(records) > 0:

    df = pd.DataFrame(
        records,
        columns=columns
    )

    st.markdown("---")

    st.subheader("Transaction History")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------------
    # Fraud Distribution
    # ---------------------

    st.markdown("---")

    st.subheader("Fraud Distribution")

    fraud_counts = (
        df["Prediction"]
        .value_counts()
        .reset_index()
    )

    fraud_counts.columns = [
        "Prediction",
        "Count"
    ]

    fig = px.pie(
        fraud_counts,
        names="Prediction",
        values="Count",
        title="Fraud vs Normal Transactions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------
    # Risk Distribution
    # ---------------------

    st.markdown("---")

    st.subheader("Risk Score Distribution")

    fig2 = px.histogram(
        df,
        x="Risk Score",
        nbins=10,
        title="Risk Score Histogram"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -------------------------
# Generate PDF Report
# -------------------------

st.markdown("---")

st.subheader("Generate Latest PDF Report")

if st.button("Generate Report"):

    latest = get_latest_transaction()

    if latest:

        report_file = generate_transaction_report(
            transaction_id=latest[0],
            amount=latest[1],
            time=latest[2],
            transactions_today=latest[3],
            is_foreign=latest[4],
            is_high_risk_country=latest[5],
            prediction=latest[6],
            risk_score=latest[7],
            risk_level=latest[8],
            recommendation="Generated from dashboard"
        )

        with open(report_file, "rb") as pdf_file:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name=os.path.basename(report_file),
                mime="application/pdf"
            )

    else:

        st.warning("No transactions available.")


    

# -------------------------
# Footer
# -------------------------

st.markdown("---")

st.caption(
    "Fraud Analytics Platform | Python + ML + Flask + SQLite + Streamlit"
)