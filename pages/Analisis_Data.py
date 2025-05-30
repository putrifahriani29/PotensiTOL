import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
import time
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64

# Atur layout wide
st.set_page_config(layout="wide", page_title="Informasi Dataset", initial_sidebar_state="auto")

# Function to display and center the logo in the sidebar
def display_logo():
    logo_path = 'logo.png'  # Adjust path to your logo file
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_image}" width="150" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.error(f"Logo file '{logo_path}' not found. Please ensure the file is in the correct directory.")
display_logo()
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

def display_title():
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h1 style="
                color: white;
                background-color: #11009E;
                border-radius: 20px;
                padding: 20px;
                display: inline-block;
                font-size: 22px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: bold;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
                margin-bottom: 30px;
            ">
                ANALISIS DATASET PROGAM IP4T DAN MODEL RANDOM FOREST CLASSIFIER
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
display_title()   


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
        df = pd.read_csv("dataset20052025(3).csv", sep=";")
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
                # Hitung frekuensi, dropna=True untuk otomatis drop NaN
                freq = df[col].value_counts(dropna=True) \
                            .rename_axis(col) \
                            .reset_index(name='Jumlah')
                
                # Jika ada string literal 'None' yang ternyata data valid, sesuaikan filter ini
                freq = freq[freq[col].notnull() & (freq[col] != 'None')]

                st.dataframe(freq, use_container_width=True)
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
