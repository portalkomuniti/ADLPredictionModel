# app.py
import streamlit as st
import pandas as pd
import numpy as np
from statistics import mode
import os
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Replace with your service account JSON file path
creds = Credentials.from_service_account_file(
    'json/client_secret_806467693509-0l8h7t8c7edm3cf2qnjd2dm77m0on9l3.apps.googleusercontent.com.json', scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet = client.open_by_key("1AlXyNJ3u48BU7zKxz-dnCc7OA10znckKa8apBnIOm-k").sheet1  # Replace with your sheet ID

# Display image above the title
st.image("https://weactive.github.io/weact.png", width=120)

# Set up the app title
st.title("Penilaian Keupayaan Warga Emas Dalam Aktiviti Harian")

# Define file paths
data_file_path = r"ADLdataclass.csv"

# Check if the data file exists at the specified path
if os.path.exists(data_file_path):
    # Load the data
    data = pd.read_csv(data_file_path)

    # Sidebar inputs for personal details
    name = st.sidebar.text_input("Nama", value="").upper()
    age = st.sidebar.number_input("Umur", min_value=0, max_value=120, step=1)
    gender = st.sidebar.selectbox("Jantina", options=["Sila Pilih", "Lelaki", "Perempuan"])
    living_status = st.sidebar.selectbox("Status Penjagaan", 
                                         options=["Sila Pilih", "Tinggal bersendirian", "Tinggal bersama keluarga", 
                                                  "Tinggal di Pusat Jagaan Awam", "Tinggal di Pusat Jagaan Swasta"])
    location = st.sidebar.selectbox("Negeri", 
                                    options=["Sila Pilih", "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", 
                                             "Pahang", "Perak", "Perlis", "Pulau Pinang", "Selangor", "Terengganu", 
                                             "Sabah", "Sarawak", "WP Putrajaya", "WP Kuala Lumpur", "WP Labuan"])

    # Dropdowns for assessments
    st.sidebar.write("### Status Keupayaan")
    toileting = st.sidebar.selectbox(
        "Keupayaan Menggunakan Tandas",
        options=["Pilih Status Anda", 5, 4, 3, 2, 1, 0],
        format_func=lambda x: {
            "Pilih Status Anda": "Sila Pilih",
            5: "Menggunakan tandas secara bebas sekurang-kurangnya 2 minggu",
            4: "Menggunakan tandas secara bebas dengan kadangkala gagal",
            3: "Memerlukan bantuan menggunakan tandas, kadangkala menggunakan lampin",
            2: "Sentiasa memerlukan lampin, bekerjasama dalam menukar",
            1: "Kesukaran dalam menukar lampin, memerlukan 2 orang",
            0: "Menggunakan beg air kencing"
        }[x]
    )
    mobility = st.sidebar.selectbox(
        "Keupayaan Pergerakan",
        options=["Pilih Status Anda", 5, 4, 3, 2, 1, 0],
        format_func=lambda x: {
            "Pilih Status Anda": "Sila Pilih",
            5: "Boleh naik tangga dan keluar rumah tanpa bantuan",
            4: "Boleh berjalan sendiri di lantai rata, tetapi tidak boleh naik tangga",
            3: "Boleh bergerak dengan alat bantuan (tongkat, kerusi roda, dll.)",
            2: "Memerlukan bantuan untuk pemindahan tetapi boleh duduk sendiri",
            1: "Tidak boleh berpindah sendiri tetapi boleh bergolek di atas katil",
            0: "Tidak boleh mengubah kedudukan badan di atas katil"
        }[x]
    )
    eating = st.sidebar.selectbox(
        "Keupayaan Untuk Makan",
        options=["Pilih Status Anda", 5, 4, 3, 2, 1, 0],
        format_func=lambda x: {
            "Pilih Status Anda": "Sila Pilih",
            5: "Boleh makan secara bebas tanpa bantuan",
            4: "Boleh makan secara bebas tetapi mungkin mengotorkan meja",
            3: "Memerlukan bantuan untuk makan, tiada masalah menelan",
            2: "Kesukaran menelan, memerlukan makanan lembut",
            1: "Memerlukan pemakanan khusus melalui tiub intravena (parenteral alimentation)",
            0: "Memerlukan pemakanan alimentasi intravena (intravenous alimentation)"
        }[x]
    )
    mental = st.sidebar.selectbox(
        "Status Keupayaan Mental",
        options=["Pilih Status Anda", 5, 4, 3, 2, 1, 0],
        format_func=lambda x: {
            "Pilih Status Anda": "Sila Pilih",
            5: "Tiada gangguan kognitif",
            4: "Kehilangan ingatan, tiada tingkah laku bermasalah",
            3: "Tingkah laku bermasalah, tiada gangguan orientasi",
            2: "Gangguan orientasi yang teruk, tiada tingkah laku bermasalah",
            1: "Gangguan orientasi dan tingkah laku bermasalah yang teruk",
            0: "Tiada aktiviti mental atau respon"
        }[x]
    )

    # Display labels with placeholders for results in single lines
    col1, col2 = st.columns([1, 12])
    col1.markdown("**Nama:**")
    name_display = col2.write(name if name else "")

    col1, col2 = st.columns([1, 1.91])
    col1.markdown("**Penilaian Keseluruhan:**")
    overall_result = col2.empty()

    col1, col2 = st.columns([1, 1.91])
    col1.markdown("**Keupayaan Pergerakan:**")
    mobility_result = col2.empty()

    col1, col2 = st.columns([1, 1.91])
    col1.markdown("**Keupayaan Menggunakan Tandas:**")
    toileting_result = col2.empty()

    col1, col2 = st.columns([1, 1.91])
    col1.markdown("**Keupayaan Untuk Makan:**")
    eating_result = col2.empty()

    col1, col2 = st.columns([1, 1.91])
    col1.markdown("**Keupayaan Mental:**")
    mental_result = col2.empty()

    # Ensure valid selections have been made for personal details and assessments
    if all(value != "Pilih Status Anda" for value in [toileting, mobility, eating, mental]) and gender != "Pilih" and living_status != "Pilih":
        # Prediction button
        if st.sidebar.button("Nilaikan Tahap Limitasi"):
            # Determine the predicted class as the mode of input scores
            input_data = [toileting, mobility, eating, mental]
            predicted_class = mode(input_data)

            # Assistance level descriptions with traffic light colors
            assistance_mapping = {
                5: ("Tiada keperluan bantuan", "#00FF00"),  # Green
                4: ("Perlu Pengawasan oleh ahli keluarga", "#FFFF00"),  # Yellow
                3: ("Perlu Bantuan oleh ahli keluarga", "#FFFF00"),  # Yellow
                2: ("Perlu Sokongan penuh oleh keluarga", "#FFFF00"),  # Yellow
                1: ("Perlu Sokongan pakar", "#FF0000"),  # Red
                0: ("Perlu Penjagaan sepenuhnya", "#FF0000")  # Red
            }

            # Detailed assistance descriptions with traffic light colors
            details_mapping = {
                "mobility": {
                    5: ("Tiada keperluan bantuan", "#00FF00"),
                     # Additional mappings...
                },
                # Additional mappings for toileting, eating, and mental
            }

            # Get the results and update display
            assistance_desc, assistance_color = assistance_mapping[predicted_class]
            mobility_desc, mobility_color = details_mapping['mobility'][mobility]
            # Update inline display with result and color
            overall_result.markdown(f"<span style='color:{assistance_color}'>{assistance_desc}</span>", unsafe_allow_html=True)
            # Additional display updates...

            # Append data to the Google Sheet
            row_data = [name, age, gender, living_status, location, toileting, mobility, eating, mental, predicted_class]
            sheet.append_row(row_data)
    else:
        st.sidebar.warning("Sila isi semua medan untuk meneruskan.")
else:
    st.write("Fail tidak dijumpai. Sila periksa laluan fail dan pastikan fail wujud di lokasi yang dinyatakan.")
