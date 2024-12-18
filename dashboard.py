import streamlit as st
import pandas as pd
import numpy as np
from statistics import mode
import os
from datetime import datetime

# Display image above the title
st.image("https://weactive.github.io/weact.png", width=120)

# Set up the app title
st.title("Penilaian Keupayaan Warga Emas Dalam Aktiviti Harian")

# Define file paths
data_file_path = r"ADLdataclass.csv"
predictions_file_path = r"user_predictions.xlsx"

# Initialize reset flag in session state
if 'reset' not in st.session_state:
    st.session_state['reset'] = False

# Check if reset flag is set, and reset inputs if needed
if st.session_state['reset']:
    st.session_state['name'] = ""
    st.session_state['age'] = 0
    st.session_state['gender'] = "Sila Pilih"
    st.session_state['living_status'] = "Sila Pilih"
    st.session_state['location'] = "Sila Pilih"
    st.session_state['toileting'] = "Pilih Status Anda"
    st.session_state['mobility'] = "Pilih Status Anda"
    st.session_state['eating'] = "Pilih Status Anda"
    st.session_state['mental'] = "Pilih Status Anda"
    st.session_state['reset'] = False  # Clear the flag

# Sidebar inputs for personal details using session state
name = st.sidebar.text_input("Nama", value=st.session_state.get('name', ""), key="name").upper()
age = st.sidebar.number_input("Umur", min_value=0, max_value=120, step=1, value=st.session_state.get('age', 0), key="age")
gender = st.sidebar.selectbox("Jantina", options=["Sila Pilih", "Lelaki", "Perempuan"], index=["Sila Pilih", "Lelaki", "Perempuan"].index(st.session_state.get('gender', "Sila Pilih")), key="gender")
living_status = st.sidebar.selectbox("Status Penjagaan", options=["Sila Pilih", "Tinggal bersendirian", "Tinggal bersama keluarga", "Tinggal di Pusat Jagaan Awam", "Tinggal di Pusat Jagaan Swasta"], index=["Sila Pilih", "Tinggal bersendirian", "Tinggal bersama keluarga", "Tinggal di Pusat Jagaan Awam", "Tinggal di Pusat Jagaan Swasta"].index(st.session_state.get('living_status', "Sila Pilih")), key="living_status")
location = st.sidebar.selectbox("Negeri", options=["Sila Pilih", "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Selangor", "Terengganu", "Sabah", "Sarawak", "WP Putrajaya", "WP Kuala Lumpur", "WP Labuan"], index=["Sila Pilih", "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Selangor", "Terengganu", "Sabah", "Sarawak", "WP Putrajaya", "WP Kuala Lumpur", "WP Labuan"].index(st.session_state.get('location', "Sila Pilih")), key="location")

# Dropdowns for assessments with session state
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
    }[x], index=["Pilih Status Anda", 5, 4, 3, 2, 1, 0].index(st.session_state.get('toileting', "Pilih Status Anda")), key="toileting"
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
    }[x], index=["Pilih Status Anda", 5, 4, 3, 2, 1, 0].index(st.session_state.get('mobility', "Pilih Status Anda")), key="mobility"
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
    }[x], index=["Pilih Status Anda", 5, 4, 3, 2, 1, 0].index(st.session_state.get('eating', "Pilih Status Anda")), key="eating"
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
    }[x], index=["Pilih Status Anda", 5, 4, 3, 2, 1, 0].index(st.session_state.get('mental', "Pilih Status Anda")), key="mental"
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
mandatory_fields_filled = all([
    name,
    age != 0,
    gender != "Sila Pilih",
    living_status != "Sila Pilih",
    location != "Sila Pilih",
    toileting != "Pilih Status Anda",
    mobility != "Pilih Status Anda",
    eating != "Pilih Status Anda",
    mental != "Pilih Status Anda"
])

# Show warning if not all mandatory fields are filled
if not mandatory_fields_filled:
    st.sidebar.warning("Sila lengkapkan semua medan untuk meneruskan.")

# Prediction button
if mandatory_fields_filled and st.sidebar.button("Sila Klik Untuk Penilaian"):
    # Get the current date for the record
    current_date = datetime.now().strftime("%Y-%m-%d")

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
            1: ("Memerlukan Bantuan dua orang untuk menukar lampin", "#FF0000"),
            0: ("Memerlukan penjagaan sepenuh masa", "#FF0000")
        },
        "eating": {
            5: ("Tiada keperluan bantuan", "#00FF00"),
            4: ("Tiada keperluan bantuan atau sokongan", "#00FF00"),
            3: ("Memerlukan bantuan untuk menyuap makanan ke mulut", "#FFFF00"),
            2: ("Memerlukan makanan lembut dan bantuan untuk makan", "#FFFF00"),
            1: ("Sokongan pemakanan parenteral", "#FF0000"),
            0: ("Sokongan pemakanan sepenuhnya", "#FF0000")
        },
        "mental": {
            5: ("Tiada keperluan bantuan", "#00FF00"),
            4: ("Pengawasan, bantuan ingatan", "#00FF00"),
            3: ("Sokongan tingkah laku, pengawasan", "#FFFF00"),
            2: ("Sokongan orientasi, pengawasan", "#FFFF00"),
            1: ("Pengawasan dan sokongan tingkah laku menyeluruh", "#FF0000"),
            0: ("Penjagaan sepenuh masa", "#FF0000")
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

    # Save the results to the Excel file
    results = {
        "Date": current_date,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Living Status": living_status,
        "Location": location,
        "Toileting": toileting,
        "Mobility": mobility,
        "Eating": eating,
        "Mental": mental,
        "Predicted Class": predicted_class
    }

    results_df = pd.DataFrame([results])

    if os.path.exists(predictions_file_path):
        # Append the data to an existing Excel file
        with pd.ExcelWriter(predictions_file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            results_df.to_excel(writer, sheet_name='Predictions', index=False, header=False, startrow=writer.sheets['Predictions'].max_row)
    else:
        # Create a new Excel file and save the data
        with pd.ExcelWriter(predictions_file_path, engine='openpyxl') as writer:
            results_df.to_excel(writer, sheet_name='Predictions', index=False)

    st.success("Keputusan Penilaian")

    # Set reset flag to clear inputs on the next run
    st.session_state['reset'] = True
