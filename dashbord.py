import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Smart RT AI Dashboard", layout="wide")

st.title("🤖 Smart RT AI Dashboard")
LOG_FILE = "logs/detection_log.csv"

# cek apakah file ada
if os.path.exists(LOG_FILE):

    df = pd.read_csv(LOG_FILE)

    st.subheader("📋 Detection Log")x
    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Event Statistik")
        st.bar_chart(df["event"].value_counts())

    with col2:
        st.subheader("📈 Confidence")
        st.line_chart(df["confidence"])

else:
    st.warning("Belum ada data deteksi")

st.write("Dashboard akan update setiap refresh")