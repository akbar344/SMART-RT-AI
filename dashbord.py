import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# CSS background
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
color: white;
}

[data-testid="stSidebar"] {
background-color: #111;
}

</style>
""", unsafe_allow_html=True)

# Konfigurasi halaman
st.set_page_config(
    page_title="Smart RT AI",
    page_icon="🤖",
    layout="wide"
)

# ======================
# HEADER
# ======================

st.title("🤖 Smart RT AI")
st.caption("Smart Neighborhood Monitoring System")

st.divider()

# ======================
# SIDEBAR
# ======================

menu = st.sidebar.selectbox(
    "Menu Dashboard",
    [
        "🏠 Dashboard",
        "👨‍👩‍👧 Data Warga",
        "📊 Statistik",
        "📷 Monitoring",
        "ℹ️ Tentang"
    ]
)

st.sidebar.success("System Status : Online")

# ======================
# DATA CONTOH
# ======================

data = {
    "Nama": ["Budi","Siti","Andi","Rina","Dodi","Agus"],
    "RT": [1,1,2,2,3,3],
    "Status": ["Aman","Aman","Peringatan","Aman","Aman","Peringatan"]
}

df = pd.DataFrame(data)

# ======================
# DASHBOARD
# ======================

if menu == "🏠 Dashboard":

    st.subheader("Ringkasan Sistem")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Warga", len(df))
    col2.metric("Status Aman", (df["Status"]=="Aman").sum())
    col3.metric("Peringatan", (df["Status"]=="Peringatan").sum())
    col4.metric("RT Aktif", df["RT"].nunique())

    st.divider()

    st.subheader("Statistik Status Warga")

    status_chart = df["Status"].value_counts()
    st.bar_chart(status_chart)

# ======================
# DATA WARGA
# ======================

elif menu == "👨‍👩‍👧 Data Warga":

    st.subheader("Database Warga")

    st.dataframe(df,use_container_width=True)

# ======================
# STATISTIK
# ======================

elif menu == "📊 Statistik":

    st.subheader("Statistik per RT")

    rt_chart = df.groupby("RT").count()["Nama"]
    st.bar_chart(rt_chart)

# ======================
# MONITORING
# ======================

if menu == "Monitoring":

    import streamlit as st

st.title("Monitoring Video")

video_file = st.file_uploader("test,mp4")

if video_file:
    st.video(video_file)

# ======================
# TENTANG
# ======================

elif menu == "ℹ️ Tentang":

    st.subheader("Tentang Smart RT AI")

    st.write("""
    Smart RT AI adalah sistem monitoring lingkungan berbasis AI
    untuk meningkatkan keamanan dan pengelolaan data warga.
    
    Fitur:
    - Dashboard monitoring
    - Statistik warga
    - Monitoring CCTV
    - Sistem berbasis web
    """)