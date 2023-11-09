import streamlit as st
import matplotlib.pyplot as plt

# CSS dan HTML untuk tampilan
st.markdown(
    """
    <style>
    .title {
        font-size: 32px;
        color: #FF5733;
    }

    .result-card {
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tampilan judul
st.markdown('<p class="title">Personal Pollution Tracker</p>', unsafe_allow_html=True)

# Tampilan form input
st.write('<div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
st.header('Input Data')

# Form input
jumlah_anggota = st.number_input('Jumlah Anggota Keluarga dalam 1 Rumah', min_value=1, help="Masukkan jumlah anggota keluarga dalam 1 rumah")

membakar_sampah = st.radio('Membakar Sampah (dalam sehari)', ('Ya', 'Tidak'), help="Pilih 'Ya' jika membakar sampah dalam sehari, pilih 'Tidak' jika tidak")

gas_lpg = st.radio('Gunakan Gas LPG?', ('Ya', 'Tidak'), help="Pilih 'Ya' jika menggunakan Gas LPG, pilih 'Tidak' jika tidak")
if gas_lpg == 'Ya':
    ukuran_lpg = st.selectbox('Ukuran Gas LPG', ('3 KG', '5.5 KG', '12 KG'), help="Pilih ukuran Gas LPG yang digunakan")
    hari_pemakaian = st.number_input('Jumlah Hari Pemakaian', min_value=1, help="Masukkan jumlah hari pemakaian Gas LPG", key='LPG')

merokok = st.radio('Merokok?', ('Ya', 'Tidak'), help="Pilih 'Ya' jika merokok, pilih 'Tidak' jika tidak")
if merokok == 'Ya':
    batang_rokok = st.number_input('Jumlah Batang Rokok', min_value=1, help="Masukkan jumlah batang rokok yang dikonsumsi")
    tipe_rokok = st.selectbox('Tipe Rokok', ('Rokok Konvensional', 'Rokok Elektrik', 'iQOS'), help="Pilih tipe rokok yang dikonsumsi", key='Tipe Rokok')

penerbangan_domestik = st.number_input('Penerbangan Domestik (dalam tahun ini)', min_value=0, help="Masukkan jumlah penerbangan domestik dalam satu tahun")
penerbangan_internasional = st.number_input('Penerbangan Internasional (dalam tahun ini)', min_value=0, help="Masukkan jumlah penerbangan internasional dalam satu tahun")

st.header('Daily Transportation')
krl = st.number_input('KRL (Kali)', min_value=0, help="Masukkan jumlah penggunaan KRL dalam sehari")
transjakarta = st.number_input('Transjakarta (Kali)', min_value=0, help="Masukkan jumlah penggunaan Transjakarta dalam sehari")
mrt = st.number_input('MRT (Kali)', min_value=0, help="Masukkan jumlah penggunaan MRT dalam sehari")
motor_l1 = st.number_input('Total KM Motor L1', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Motor L1 dalam sehari")
motor_l3 = st.number_input('Total KM Motor L3', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Motor L3 dalam sehari")
mobil_city = st.number_input('Total KM Mobil City Car/Hatchback/Sedan', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Mobil City Car/Hatchback/Sedan dalam sehari")
mobil_suv = st.number_input('Total KM Mobil SUV/MPV', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Mobil SUV/MPV dalam sehari")

# Tombol Submit
submitted = st.button('Submit')
st.write('</div>', unsafe_allow_html=True)

# Output
if submitted:
    st.header('Hasil Pencatatan Pencemaran Pribadi')
    st.write('<div class="result-card">', unsafe_allow_html=True)

    # Implementasi logika perhitungan berdasarkan input dari pengguna
    # Hitung total pencemaran dari membakar sampah
    if membakar_sampah == 'Ya':
        total_nox = 2.04  # gram
        total_co = 28.56  # gram
        total_sox = 0.34  # gram
        total_pm10 = 5.44  # gram
    else:
        total_nox, total_co, total_sox, total_pm10 = 0, 0, 0, 0

    # Hitung total pencemaran dari GAS LPG
    if gas_lpg == 'Ya':
        if ukuran_lpg == '3 KG':
            gas_nox = 7.5 / (jumlah_anggota * hari_pemakaian)
            gas_co = 7.5 / (jumlah_anggota * hari_pemakaian)
            gas_sox = 0.075 / (jumlah_anggota * hari_pemakaian)
            gas_pm10 = 0.075 / (jumlah_anggota * hari_pemakaian)
        elif ukuran_lpg == '5.5 KG':
            gas_nox = 13.75 / (jumlah_anggota * hari_pemakaian)
            gas_co = 13.75 / (jumlah_anggota * hari_pemakaian)
            gas_sox = 0.1375 / (jumlah_anggota * hari_pemakaian)
            gas_pm10 = 0.1375 / (jumlah_anggota * hari_pemakaian)
        elif ukuran_lpg == '12 KG':
            gas_nox = 30 / (jumlah_anggota * hari_pemakaian)
            gas_co = 30 / (jumlah_anggota * hari_pemakaian)
            gas_sox = 0.3 / (jumlah_anggota * hari_pemakaian)
            gas_pm10 = 0.3 / (jumlah_anggota * hari_pemakaian)
    else:
        gas_nox, gas_co, gas_sox, gas_pm10 = 0, 0, 0, 0

    # Hitung total pencemaran dari merokok
    if merokok == 'Ya':
        if tipe_rokok == 'Rokok Konvensional':
            total_pm10 += batang_rokok * 0.000529  # gram
            total_pm25 = batang_rokok * 0.0005  # gram
        elif tipe_rokok == 'iQOS':
            total_pm10 = batang_rokok * 0.0000081  # gram
            total_pm25 = batang_rokok * 0.0000065 
    else:
        total_pm10, total_pm25 = 0, 0

    # Hitung total pencemaran dari penerbangan
    total_nox += penerbangan_domestik * 51  # gram
    total_sox += penerbangan_domestik * 4.94  # gram
    total_co += penerbangan_domestik * 0.432  # gram
    total_pm10 += penerbangan_domestik * 0.432  # gram
    total_pm25 += penerbangan_domestik * 0.432  # gram

    total_nox += penerbangan_internasional * 2 * 51  # gram
    total_sox += penerbangan_internasional * 2 * 4.94  # gram
    total_co += penerbangan_internasional * 2 * 0.432  # gram
    total_pm10 += penerbangan_internasional * 2 * 0.432  # gram
    total_pm25 += penerbangan_internasional * 2 * 0.432  # gram

    # Hitung total pencemaran dari Daily Transportation
    total_co2_krl = krl * 4.79  # gram
    total_co2_transjakarta = transjakarta * 62.8  # gram
    total_co2_mrt = mrt * 15.4  # gram

    total_co += total_co2_krl + total_co2_transjakarta + total_co2_mrt  # gram

    total_co += motor_l1 * 1  # gram
    total_nox += motor_l1 * 1.2  # gram

    total_co += motor_l3 * 5.5  # gram
    total_nox += motor_l3 * 0.3  # gram

    if mobil_city or mobil_suv:
     if tipe_mobil and bahan_bakar:
        if tipe_mobil == 'city_car' and bahan_bakar == 'bensin':
            total_co += mobil_city * 2.2  # gram/km
            total_nox += mobil_city * 0.59  # gram/km
        elif tipe_mobil == 'city_car' and bahan_bakar == 'solar':
            total_co += mobil_city * 1  # gram/km
            total_nox += mobil_city * 0.7  # gram/km
            total_pm10 += mobil_city * 0.08  # gram/km
        elif tipe_mobil == 'suv' and bahan_bakar == 'bensin':
            total_co += mobil_suv * 4  # gram/km
            total_nox += mobil_suv * 0.6  # gram/km
        elif tipe_mobil == 'suv' and bahan_bakar == 'solar':
            total_co += mobil_suv * 1.25  # gram/km
            total_nox += mobil_suv * 1  # gram/km
            total_pm10 += mobil_suv * 0.12  # gram/km

    # Tampilkan hasilnya kepada pengguna
    total_pencemaran_sehari = total_nox + total_co + total_sox + total_pm10 + total_pm25
    st.write(f'Total Pencemaran dalam Sehari: {total_pencemaran_sehari} gram')

    # Tampilkan total pencemaran dalam sebulan dan setahun
    total_pencemaran_sebulan = total_pencemaran_sehari * 30
    total_pencemaran_setahun = total_pencemaran_sebulan * 12
    st.write(f'Total Pencemaran dalam Sebulan: {total_pencemaran_sebulan} gram')
    st.write(f'Total Pencemaran dalam Setahun: {total_pencemaran_setahun} gram')

    # Tambahkan pie chart
    if total_pencemaran_sehari > 0:
        fig, ax = plt.subplots()
        labels = ['NOx', 'CO', 'SOx', 'PM10', 'PM2.5']
        sizes = [total_nox, total_co, total_sox, total_pm10, total_pm25]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("Tidak ada pencemaran yang tercatat.")

    st.write('</div>', unsafe_allow_html=True)