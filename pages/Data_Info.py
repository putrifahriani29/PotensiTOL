import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# Atur layout wide
st.set_page_config(layout="wide", page_title="Informasi Dataset", initial_sidebar_state="auto")

# Fungsi tampilkan tanggal sekarang
def tampilkan_tanggal():
    now = datetime.now()
    tanggal = now.strftime("%A, %d-%m-%Y %H:%M:%S")
    st.markdown(f"""
        <div style='text-align: right; color: #1E3A8A; font-weight: bold; font-size: 0.9rem;'>
            {tanggal}
        </div>
    """, unsafe_allow_html=True)

# Tampilkan toast saat pertama kali halaman dibuka
if "toast_shown" not in st.session_state:
    st.toast("Silakan unggah file CSV atau klik tombol 'Lakukan Analisis Dataset'", icon="ℹ️")
    st.session_state.toast_shown = True

# Tampilkan tanggal dan judul dengan CSS
tampilkan_tanggal()
st.markdown(
    """
    <style>
    .custom-title {
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px #555;
    }
    </style>
    <h1 class="custom-title">Analisis Data Pemanfaatan & Perlindungan Tanah</h1>
    """,
    unsafe_allow_html=True
)

# Upload file
file = st.file_uploader("Unggah file CSV", type=["csv"])

# Tombol untuk memulai analisis
if st.button("📂 Lakukan Analisis Dataset"):
    progress = st.progress(0, text="⏳ Memulai analisis...")

    for i in range(1, 6):
        time.sleep(0.15)
        progress.progress(i * 20, text=f"⏳ Memproses langkah {i}/5...")

    # Baca file dari upload atau default
    if file:
        df = pd.read_csv(file)
        st.success("File berhasil diunggah!")
    else:
        df = pd.read_csv("dataset20052025.csv", sep=";")
        st.info("Menggunakan dataset default")

    # Drop kolom NO jika ada
    if "NO" in df.columns:
        df.drop(columns=["NO"], inplace=True)

    progress.progress(100, text="✅ Analisis selesai!")

    # Tampilkan data awal
    st.subheader("📁 Data Awal")
    st.dataframe(df.head())

    # Informasi struktur
    st.subheader("🧾 Informasi Struktur DataFrame")
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Ringkasan statistik 
    st.subheader("📈 Ringkasan Statistik Data Numerik")
    st.dataframe(df.describe().T)

    # Ringkasan data kategorik dalam tabs
    st.subheader("📋 Ringkasan Data Kategorik")
    kategorik_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if kategorik_cols:
        tabs_kat = st.tabs(kategorik_cols)  # Buat tab untuk tiap kolom kategorik
        for tab, col in zip(tabs_kat, kategorik_cols):
            with tab:
                freq_table = df[col].value_counts(dropna=False).rename_axis(col).reset_index(name='Jumlah')
                st.dataframe(freq_table)
    else:
        st.info("Tidak ada kolom kategorik ditemukan pada data.")

# Univariate Analysis Tabs: Violin, Boxplot, Histogram tanpa KDE
    st.subheader("📊 Univariate Analysis: Distribusi Luas Tanah")
    if "Luas  m2" in df.columns:
        df["Luas  m2"] = pd.to_numeric(df["Luas  m2"], errors="coerce")
        df_luas = df.dropna(subset=["Luas  m2"])

        if not df_luas.empty:
            tabs = st.tabs(["Violin Plot", "Boxplot", "Histogram"])

            # Violin plot
            with tabs[0]:
                violin_fig = px.violin(
                    df_luas,
                    y="Luas  m2",
                    box=True,
                    points="all",
                    color_discrete_sequence=["#1E3A8A"],
                    title="Violin Plot Luas Tanah"
                )
                st.plotly_chart(violin_fig, use_container_width=True)

            # Boxplot
            with tabs[1]:
                box_fig = px.box(
                    df_luas,
                    y="Luas  m2",
                    color_discrete_sequence=["#1E3A8A"],
                    title="Boxplot Luas Tanah"
                )
                st.plotly_chart(box_fig, use_container_width=True)

            # Histogram tanpa KDE
            with tabs[2]:
                hist_fig = go.Figure()
                hist_fig.add_trace(go.Histogram(
                    x=df_luas["Luas  m2"],
                    nbinsx=30,
                    histnorm='density',
                    marker_color='#1E3A8A',
                    opacity=0.7,
                    name='Histogram'
                ))
                hist_fig.update_layout(
                    title="Histogram Luas Tanah",
                    xaxis_title="Luas  m2",
                    yaxis_title="Density"
                )
                st.plotly_chart(hist_fig, use_container_width=True)
        else:
            st.info("Data kolom 'Luas  m2' kosong atau tidak valid.")
    else:
        st.info("Kolom 'Luas  m2' tidak ditemukan pada data.")

    # Visualisasi barplot dan pie/donut chart dengan Plotly
    st.subheader("📋 Visualisasi TARGET")
    col1, col2 = st.columns(2)
    if "POTENSI TOL" in df.columns:
        potensi_tol_data = df["POTENSI TOL"].value_counts().reset_index()
        potensi_tol_data.columns = ["POTENSI TOL", "Count"]

        # Bar chart dengan Plotly
        fig_bar = px.bar(
            potensi_tol_data, 
            x="POTENSI TOL", 
            y="Count", 
            title="BARPLOT POTENSI TOL",
            labels={"POTENSI TOL": "Potensi TOL", "Count": "Jumlah Data"},
            color="POTENSI TOL",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_layout(showlegend=False)
        col1.plotly_chart(fig_bar, use_container_width=True)

        # Pie/donut chart dengan Plotly
        fig_pie = px.pie(
            potensi_tol_data, 
            names="POTENSI TOL", 
            values="Count", 
            title="DISTRIBUSI POTENSI TOL (%)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent')
        col2.plotly_chart(fig_pie, use_container_width=True)
    else:
        col1.info("Kolom 'POTENSI TOL' tidak ditemukan pada data.")
        col2.info("Kolom 'POTENSI TOL' tidak ditemukan pada data.")

    

    st.success("✅ Analisis selesai!")
