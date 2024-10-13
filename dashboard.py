# app.py
import streamlit as st
import pandas as pd
import numpy as np
from statistics import mode
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Replace with your service account JSON file path
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'json/glowing-run-353404-cc08efe2b4ba.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet = client.open_by_key("1AlXyNJ3u48BU7zKxz-dnCc7OA10znckKa8apBnIOm-k").sheet1  # Replace with your sheet ID

# CSS to move the sidebar to the right
st.markdown(
    """
    <style>
    .css-18e3th9 {
        flex-direction: row-reverse;
    }
    .css-1d391kg {
        display: none;
    }
    .css-1v3fvcr {
        order: 2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display image above the title
st.image("https://weactive.github.io/weact.png", width=120)

# Set up the app title
st.title("Penilaian Keupayaan Warga Emas Menjalani Aktiviti Harian")

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
            5: "Boleh menaiki tangga dan keluar rumah tanpa bantuan",
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
            1: "Memerlukan pemakanan khusus melalui tiub parenteral (parenteral alimentation)",
            0: "Memerlukan pemakanan khusus melalui alimentasi intravena (intravenous alimentation)"
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
        if st.sidebar.button("Klik Penilaian"):
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
                    4: ("Tiada, tetapi mungkin memerlukan pengawasan di tangga", "#00FF00"),
                    3: ("Perlu Alat bantuan (tongkat, kerusi roda)", "#FFFF00"),
                    2: ("Bantuan untuk pemindahan", "#FFFF00"),
                    1: ("Bantuan untuk pemindahan, sokongan di katil", "#FF0000"),
                    0: ("Bantuan sepenuhnya untuk semua keperluan pergerakan", "#FF0000")
                },
                "toileting": {
                    5: ("Tiada keperluan bantuan", "#00FF00"),
                    4: ("Memerlukan pengawasan sekali-sekala", "#00FF00"),
                    3: ("Memerlukan bantuan untuk menggunakan tandas atau lampin", "#FFFF00"),
                    2: ("Memerlukan bantuan menukar lampin", "#FFFF00"),
                    1: ("Memerlukan bantuan dua orang untuk menukar lampin", "#FF0000"),
                    0: ("Memerlukan penjagaan sepenuh masa", "#FF0000")
                },
                "eating": {
                    5: ("Tiada keperluan bantuan", "#00FF00"),
                    4: ("Tiada keperluan bantuan atau sokongan", "#00FF00"),
                    3: ("Memerlukan bantuan untuk menyuap makanan ke mulut", "#FFFF00"),
                    2: ("Memerlukan makanan lembut dan bantuan untuk makan", "#FFFF00"),
                    1: ("Memerlukan sokongan pemakanan parenteral", "#FF0000"),
                    0: ("Memerlukan sokongan pemakanan sepenuhnya", "#FF0000")
                },
                "mental": {
                    5: ("Tiada keperluan bantuan", "#00FF00"),
                    4: ("Memerlukan pengawasan dan bantuan ingatan", "#00FF00"),
                    3: ("Memerlukan pengawasan dan sokongan tingkah laku", "#FFFF00"),
                    2: ("Memerlukan pengawasan dan sokongan orientasi", "#FFFF00"),
                    1: ("Memerlukan pengawasan dan sokongan tingkah laku menyeluruh", "#FF0000"),
                    0: ("Memerlukan penjagaan sepenuh masa", "#FF0000")
                }
            }

            # Get the results and update display
            assistance_desc, assistance_color = assistance_mapping[predicted_class]
            mobility_desc, mobility_color = details_mapping['mobility'][mobility]
            toileting_desc, toileting_color = details_mapping['toileting'][toileting]
            eating_desc, eating_color = details_mapping['eating'][eating]
            mental_desc, mental_color = details_mapping['mental'][mental]

            # Update inline display with result and color
            overall_result.markdown(f"<span style='color:{assistance_color}'>{assistance_desc}</span>", unsafe_allow_html=True)
            mobility_result.markdown(f"<span style='color:{mobility_color}'>{mobility_desc}</span>", unsafe_allow_html=True)
            toileting_result.markdown(f"<span style='color:{toileting_color}'>{toileting_desc}</span>", unsafe_allow_html=True)
            eating_result.markdown(f"<span style='color:{eating_color}'>{eating_desc}</span>", unsafe_allow_html=True)
            mental_result.markdown(f"<span style='color:{mental_color}'>{mental_desc}</span>", unsafe_allow_html=True)

            # Append data to the Google Sheet
            row_data = [name, age, gender, living_status, location, toileting, mobility, eating, mental, predicted_class]
            sheet.append_row(row_data)
    else:
        st.sidebar.warning("Sila lengkapkan semua medan untuk meneruskan.")
else:
    st.write("Fail tidak dijumpai. Sila periksa laluan fail dan pastikan fail wujud di lokasi yang dinyatakan.")
