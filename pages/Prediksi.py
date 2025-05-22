import streamlit as st
import pickle
import pandas as pd
import time

# --------------------- Konfigurasi Halaman ---------------------
# Atur layout wide
st.set_page_config(layout="wide", page_title="Prediksi Potensi TOL", initial_sidebar_state="auto")

st.markdown("""
    <div style='
        text-align: center;
        color: #004AAD;
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    '>
        <div style="font-size: 2.2rem; font-weight: bold;">
            PREDIKSI POTENSI TOL
        </div>
        <div style="font-size: 1.3rem; font-weight: bold;">
            (Tanah Objek Landreform)
        </div>
    </div>
""", unsafe_allow_html=True)


# --------------------- Styling Tombol ---------------------
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007BFF;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.75em 1.5em;
        transition: background-color 0.3s ease;
        font-size: 18px;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #FFD600;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------- Fungsi Styling Output ---------------------
def generate_style(param_name, value, bg_color="#FFF5C2", text_color="blue"):
    return f'''
    <div style="
        background-color: {bg_color};
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
        color: {text_color};
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        font-size: 110%;
    ">
        {param_name}<br>
        <span style="font-size: 150%; color: #6DB9EF;">{value}</span>
    </div>
    '''

# --------------------- Load Model ---------------------
@st.cache_resource
def load_model():
    with open("model_rf_potensiTOL.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# --------------------- Form Input Pengguna ---------------------
st.markdown("### 🧾 Masukkan Karakteristik Lahan")

penguasaan = st.selectbox("PENGUASAAN TANAH", 
    ["Penggarap", "Pemilik", "Fasos Fasum", "Aset Desa", "Pemerintah"])

kepemilikan = st.selectbox("KEPEMILIKAN TANAH", 
    ["Terdaftar", "Belum Terdaftar", "Terdaftar (HGU Baru)", 
     "Tidak Terdaftar", "Terdaftar (tumpang tindih)"])

penggunaan = st.selectbox("PENGGUNAAN TANAH", 
    ["Tegalan", "Rumah Tinggal", "Kebun Campuran", "Mushola", "Masjid", 
     "PAUD", "Madrasah", "Pangkalan Ojek", "Kebun", "Lainnya"])

pemanfaatan = st.selectbox("PEMANFAATAN TANAH", 
    ["Tanaman semusim", "Tempat tinggal", "Produksi pertanian", 
     "Sarana Ibadah", "Sarana Pendidikan", "Olahraga", "Usaha", "Tanaman tahunan"])

luas = st.number_input("Luas Lahan (m²)", min_value=1, max_value=500000, value=10000, step=1)

# --------------------- Tombol Submit di Tengah ---------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button("TAMPILKAN PREDIKSI ")

# --------------------- Proses Prediksi ---------------------
if submit:
    st.toast("Memproses data...", icon="⏳")
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)
    progress.empty()

    input_df = pd.DataFrame([{
        "PENGUASAAN TANAH": penguasaan,
        "PEMILIKAN TANAH": kepemilikan,
        "PENGGUNAAN TANAH": penggunaan,
        "PEMANFAATAN TANAH": pemanfaatan,
        "Luas  m2": luas   # perhatikan spasi ini
    }])

    try:
        prediksi = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat prediksi: {e}")
        st.stop()

    # --------------------- Tampilkan Hasil Input ---------------------
    st.markdown("## Hasil Input Parameter")
    col1, col2 = st.columns(2)
    col1.markdown(generate_style("Penguasaan Tanah", penguasaan), unsafe_allow_html=True)
    col2.markdown(generate_style("Kepemilikan Tanah", kepemilikan), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(generate_style("Penggunaan Tanah", penggunaan), unsafe_allow_html=True)
    col2.markdown(generate_style("Pemanfaatan Tanah", pemanfaatan), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(generate_style("Luas Lahan (m²)", luas), unsafe_allow_html=True)
    col2.empty()

    # --------------------- Hasil Prediksi ---------------------
    st.markdown(f"""
    <div style="
        margin-top: 30px;
        padding: 15px;
        background-color: #C2D5FF;
        border-radius: 20px;
        border: 4px double blue;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #B80000;
        box-shadow: 0 0 15px #C2D5FF;
    ">
        Hasil Prediksi: <span style="text-transform: uppercase;">{prediksi}</span>
    </div>
    """, unsafe_allow_html=True)

    st.snow()
