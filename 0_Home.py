import streamlit as st
from PIL import Image
import os
from datetime import datetime
import base64

st.set_page_config(layout="wide", page_title="Home", initial_sidebar_state="auto")

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

# Function to display the header

def display_header():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="
                color: #11009E;
                border-radius: 25%;
                display: inline-block;
                padding: 2%;
                margin: 5% 0;
                border-width: 5px;
                border-style: solid;  /* ini border style */
                border-color: #11009E; /* warna border sama dengan teks */
                font-size: 18px;
            ">
                Program Indeks Pemanfaatan dan Perlindungan Tanah (IP4T)
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    

# Function to display the current date and time
def display_date_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
    day_name = current_datetime.strftime('%A')

    st.markdown(
        f"""
        <div style="text-align: right; color: #6DB9EF; border-radius: 25%; display: inline-block; font-size: medium; text-shadow: 3px red; padding: 2%; margin-left: 65%; font-weight: bold; text-decoration: underline;">
            {day_name}, {formatted_datetime}
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display data information
def display_data_info():
    st.markdown("""
    <div style="color: #0F2167; font-size: 19px; text-align: justify; line-height: 1.6;">
        <strong>IP4T</strong> (Inventarisasi Penguasaan, Pemilikan, Penggunaan, dan Pemanfaatan Tanah) adalah kegiatan pendataan yang dilakukan untuk mengidentifikasi dan mendokumentasikan informasi mengenai tanah, termasuk siapa yang menguasai, memiliki, menggunakan, dan memanfaatkan tanah tersebut.

        <br><br>

        Kegiatan ini bertujuan untuk memberikan kepastian hukum dan informasi yang akurat tentang status tanah. IP4T digunakan sebagai dasar dalam pengambilan kebijakan yang berkaitan dengan <strong>optimalisasi lahan</strong>, <strong>penyelesaian konflik agraria</strong>, serta dukungannya terhadap pelaksanaan <strong>reforma agraria</strong>.

        <br><br>

        Dasar hukum pelaksanaan program IP4T merujuk pada <strong>Undang-Undang Nomor 5 Tahun 1960</strong> tentang <em>Ketentuan Pokok-Pokok Agraria (UUPA)</em>, yang menjadi landasan hukum utama dalam pengaturan agraria di Indonesia. Undang-undang ini lahir sebagai bentuk <strong>reformasi agraria</strong> untuk mengatasi ketimpangan penguasaan tanah, meningkatkan kesejahteraan rakyat, dan menciptakan keadilan agraria yang merata di seluruh wilayah Indonesia.
    </div>

    <br>

    <span style="color: #6DB9EF; font-size: 28px; font-weight: bold; text-decoration: underline;">Pengumpulan Data</span>
    <div style="color: #0F2167; font-size: 19px; text-align: justify; margin-top: 10px;">
        Data yang digunakan dalam penelitian ini diperoleh melalui hasil survei yang dilakukan oleh <strong>Kantor Badan Pertanahan Nasional (BPN) Kabupaten Sukabumi</strong>. Permintaan data dilakukan secara resmi kepada pihak BPN untuk memperoleh informasi terkait penguasaan, pemilikan, penggunaan, dan pemanfaatan tanah (IP4T) di wilayah tersebut.
    </div>
    <br>

    <span style="color: #6DB9EF; font-size: 35px; font-weight: bold; text-decoration: underline;">Data Columns</span>
    <ol>
        Data yang diperlukan pada penelitian ini berupa data IP4T yang terdiri dari atribut Luas, penggunaan tanah, pemanfaatan tanah, pemilikan tanah, penguasaan tanah, dan potensi TOL (Tanah Objek Landreform).
                <br><br>
        <li><code>POTENSI TOL</code>: Potensi keberadaan atau pengaruh TOL (Tanah Objek Landreform) pada area tersebut, yang mencakup:
            <ul>
                <li>Akses Reform</li>
                <li>Potensi TORA</li>
                <li>Sengketa, Konflik dan Perkara</li>
                <li>Legalisasi aset</li>
            </ul>
        </li>
        <li><code>Luas  m2</code>: Luas area tanah yang diamati.</li>
        <li><code>PENGGUNAAN TANAH</code>: Jenis penggunaan tanah pada area tersebut.</li>
        <li><code>PEMANFAATAN TANAH</code>: Cara atau tujuan pemanfaatan tanah di area tersebut.</li>
        <li><code>PEMILIKAN TANAH</code>: Informasi mengenai siapa pemilik tanah tersebut.</li>
        <li><code>PENGUASAAN TANAH</code>: Status penguasaan atas tanah tersebut.</li>
    </ol>
    """, unsafe_allow_html=True)



# Display content for the single page
display_logo()
st.sidebar.markdown('Aplikasi ini merupakan user interface Prediksi Potensi TOL')
display_header()
display_date_time()
display_data_info()

# Info message with a link to the dataset
st.info('Dokumentasi project ini dapat dilihat di GitHub: [PotensiTOL](https://github.com/putrifahriani29/PotensiTOL)')
