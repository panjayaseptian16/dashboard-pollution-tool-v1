import streamlit as st
import matplotlib.pyplot as plt
from deta import Deta

tab1,tab2,tab3 = st.tabs(['Personal Pollution Tracker', 'Carbon Footprint', 'Statistics'])
with tab1: 
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
    st.markdown('<p style="text-align: center;" class="title">Personal Pollution Tracker</p>', unsafe_allow_html=True)

    # Tampilan form input
    st.write('<div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
    st.header('Input Data')

    # Form input (isikan sesuai instruksi)
    # Form input
    jumlah_anggota = st.number_input('Jumlah Anggota Keluarga dalam 1 Rumah', min_value=1, help="Masukkan jumlah anggota keluarga dalam 1 rumah")

    membakar_sampah = st.radio('Membakar Sampah (dalam sehari)', ('Ya', 'Tidak'), help="Pilih 'Ya' jika membakar sampah dalam sehari, pilih 'Tidak' jika tidak membakar sampah", index=None)

    gas_lpg = st.radio('Gunakan Gas LPG?', ('Ya', 'Tidak'), help="Pilih 'Ya' jika menggunakan Gas LPG, pilih 'Tidak' jika tidak menggunakan LPG",index=None)
    ukuran_lpg = None
    hari_pemakaian = 0
    if gas_lpg == 'Ya':
        ukuran_lpg = st.selectbox('Ukuran Gas LPG', ('3 KG', '5.5 KG', '12 KG'), help="Pilih ukuran Gas LPG yang digunakan")
        hari_pemakaian = st.number_input('Jumlah Hari Pemakaian', min_value=1, help="Masukkan jumlah hari pemakaian Gas LPG", key='LPG')

    merokok = st.radio('Merokok?', ('Ya', 'Tidak'), help="Pilih 'Ya' jika merokok, pilih 'Tidak' jika tidak merokok",index=None)
    tipe_rokok = None
    batang_rokok = 0
    if merokok == 'Ya':
        tipe_rokok = st.selectbox('Tipe Rokok', ('Rokok Konvensional', 'Rokok Elektrik', 'iQOS'), help="Pilih tipe rokok yang dikonsumsi", key='Tipe Rokok')
        if tipe_rokok == 'Rokok Konvensional':
            batang_rokok = st.number_input('Jumlah Batang Rokok', min_value=1, help="Masukkan jumlah batang rokok yang dikonsumsi")

    penerbangan_domestik = st.number_input('Penerbangan Domestik (dalam tahun ini)', min_value=0, help="Masukkan jumlah penerbangan domestik dalam satu tahun")
    penerbangan_internasional = st.number_input('Penerbangan Internasional (dalam tahun ini)', min_value=0, help="Masukkan jumlah penerbangan internasional dalam satu tahun")

    st.header('Daily Transportation')
    krl = st.number_input('KRL', min_value=0, help="Masukkan jumlah penggunaan KRL dalam sehari")
    transjakarta = st.number_input('Transjakarta', min_value=0, help="Masukkan jumlah penggunaan Transjakarta dalam sehari")
    mrt = st.number_input('MRT', min_value=0, help="Masukkan jumlah penggunaan MRT dalam sehari")
    motor = st.number_input('Total KM Motor per hari', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Motor dalam sehari")
    mobil = st.number_input('Total KM Mobil per hari', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Mobil dalam sehari")
    bahan_bakar_mobil = None
    if mobil >= 1:
        bahan_bakar_mobil = st.radio('Bahan Bakar Mobil', ('Bensin', 'Solar'), help="Pilih jenis bahan bakar mobil",index=None)
    angkot = st.number_input('Total KM Angkot per hari', min_value=0, help="Masukkan total kilometer yang ditempuh oleh Angkot dalam sehari")
    # Tombol Submit
    submitted = st.button('Submit')
    st.write('</div>', unsafe_allow_html=True)

    # Output
    if submitted:
            if not (jumlah_anggota and membakar_sampah and gas_lpg and merokok):
                st.error('Harap mengisi semua isi form sebelum melanjutkan.')
            else:
                st.success('Terima Kasih sudah Submit!')
                st.header('Hasil Pencatatan Pencemaran Pribadi')

                # Hitung total pencemaran berdasarkan input
                if membakar_sampah == 'Ya':
                    total_nox = 2.04 / jumlah_anggota # gram
                    total_co = 28.56 / jumlah_anggota # gram
                    total_sox = 0.34 / jumlah_anggota # gram
                    total_pm10 = 5.44 / jumlah_anggota # gram
                    total_pm25 = 0  # gram
                else:
                    total_nox, total_co, total_sox, total_pm10, total_pm25 = 0, 0, 0, 0, 0

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
                    total_nox += gas_nox
                    total_co += gas_co
                    total_sox += gas_sox
                    total_pm10 += gas_pm10
                # Hitung total pencemaran dari merokok
                if merokok == 'Ya':
                    if tipe_rokok == 'Rokok Konvensional':
                        total_pm10 += batang_rokok * 0.000529  # gram
                        total_pm25 += batang_rokok * 0.0005  # gram
                    elif tipe_rokok == 'iQOS':
                        total_pm10 += 0.0000081  # gram
                        total_pm25 +=  0.0000065 

                # Hitung total pencemaran dari penerbangan
                total_nox += penerbangan_domestik * 51 /365  # gram
                total_sox += penerbangan_domestik * 4.94 /365 # gram
                total_co += penerbangan_domestik * 72.8 /365 # gram
                total_pm10 += penerbangan_domestik * 0.432 /365 # gram
                total_pm25 += penerbangan_domestik * 0.432  /365 # gram

                total_nox += penerbangan_internasional * 2 * 51 /365 # gram
                total_sox += penerbangan_internasional * 2 * 4.94  /365 # gram
                total_co += penerbangan_internasional * 2 *  72.8 /365 # gram
                total_pm10 += penerbangan_internasional * 2 * 0.432 /365 # gram
                total_pm25 += penerbangan_internasional * 2 * 0.432  /365# gram
                total_co2 = 0
                total_hc = 0
                # Hitung total pencemaran dari Daily Transportation
                total_co2_krl = krl * 47.9  # gram
                total_co2_transjakarta = transjakarta * 62.8  # gram
                total_co2_mrt = mrt * 15.4  # gram
                total_co2 = total_co2_krl + total_co2_transjakarta + total_co2_mrt
                # Kalkulasi Total Pencemaran
                motor_co = motor * 14  # gram
                motor_nox = motor * 0.29  # gram
                motor_hc = motor * 5.9  # gram
                motor_pm10 = motor * 0.24  # gram
                motor_sox = motor * 0.008  # gram
                motor_co2 = motor * 115  # gram

                mobil_co = mobil * 40  # gram
                mobil_nox = mobil * 2  # gram
                mobil_hc = mobil * 4  # gram
                mobil_pm10 = mobil * 0.01  # gram
                mobil_sox = mobil * 0.026  # gram
                mobil_co2 = mobil * 273.44  # gram

                if bahan_bakar_mobil == 'Bensin':
                    total_co += mobil_co
                    total_nox += mobil_nox
                    total_hc += mobil_hc
                    total_pm10 += mobil_pm10
                    total_sox += mobil_sox
                    total_co2 += mobil_co2
                elif bahan_bakar_mobil == 'Solar':
                    mobil_solar_co = mobil * 2.8  # gram
                    mobil_solar_nox = mobil * 3.5  # gram
                    mobil_solar_hc = mobil * 0.2  # gram
                    mobil_solar_pm10 = mobil * 0.53  # gram
                    mobil_solar_sox = mobil * 0.44  # gram
                    mobil_solar_co2 = mobil * 272.72  # gram

                    total_co += mobil_solar_co
                    total_nox += mobil_solar_nox
                    total_hc += mobil_solar_hc
                    total_pm10 += mobil_solar_pm10
                    total_sox += mobil_solar_sox
                    total_co2 += mobil_solar_co2

                angkot_co = angkot * 43.1  # gram
                angkot_nox = angkot * 2.1  # gram
                angkot_hc = angkot * 5.01  # gram
                angkot_pm10 = angkot * 0.006  # gram
                angkot_sox = angkot * 0.029  # gram
                angkot_co2 = angkot * 243.2  # gram

                total_co += angkot_co
                total_nox += angkot_nox
                total_hc += angkot_hc
                total_pm10 += angkot_pm10
                total_sox += angkot_sox
                total_co2 += angkot_co2

                total_pencemaran_sehari_gr = round(total_nox + total_co + total_sox + total_pm10 + total_pm25 + total_hc + total_co2, 3)
                total_pencemaran_sebulan_kg = round((total_pencemaran_sehari_gr * 30)/1000,2) 
                total_pencemaran_setahun_ton = round((total_pencemaran_sebulan_kg * 12)/1000000,5)

                deta = Deta(st.secrets["data_key"])

                db = deta.Base("db_test1")
                db.put({
                    "Jumlah Anggota Keluarga": jumlah_anggota,
                    "Membakar Sampah": membakar_sampah,
                    "Gas LPG": gas_lpg,
                    "Ukuran Gas LPG": ukuran_lpg,
                    "Hari Pemakaian Gas LPG": hari_pemakaian,
                    "Merokok": merokok,
                    "Tipe Rokok": tipe_rokok,
                    "Jumlah Batang Rokok": batang_rokok,
                    "Penerbangan Domestik": penerbangan_domestik,
                    "Penerbangan Internasional": penerbangan_internasional,
                    "KRL": krl,
                    "Transjakarta": transjakarta,
                    "MRT": mrt,
                    "Total KM Motor per hari": motor,
                    "Total KM Mobil per hari": mobil,
                    "Bahan Bakar Mobil": bahan_bakar_mobil,
                    "Total KM Angkot per hari": angkot,
                    "Total NOx" : total_nox,
                    "Total CO2" : total_co2,
                    "Total CO" : total_co,
                    "Total SOx" : total_sox,
                    "Total PM10" : total_pm10,
                    "Total PM25" : total_pm25,
                    "Total HC" : total_hc,
                    "Total Pencemaran Harian" : total_pencemaran_sehari_gr,
                    "Total Pencemaran Sebulan" : total_pencemaran_sebulan_kg,
                    "Total Pencemaran Setahun" : total_pencemaran_setahun_ton
                 })

            
                if total_pencemaran_sehari_gr > 0:
                    # Tampilkan hasil pencemaran
                    col1,col2= st.columns(2, gap="small")
                    with col1:
                        st.markdown("""      
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <style>
                                    .card {
                                        width: 300px;
                                        padding: 20px;
                                        border: 1px solid #ddd;
                                        border-radius: 5px;
                                        background-color: #f9f9f9;
                                        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                                        transition: box-shadow 0.3s;
                                        text-align: center;
                                    }

                                    .card:hover {
                                        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
                                    }

                                    .card-title {
                                        font-size: 18px;
                                        margin-bottom: 10px;
                                    }

                                    .card-content {
                                        font-size: 24px;
                                    }
                                </style>
                            </head>
                            <body>
                                <div class="card">
                                    <h3 class="card-title"> Estimasi Total Pencemaran Sehari</h3>
                                    <h1 class="card-content">"""+str(total_pencemaran_sehari_gr)+""" gram</h1>
                                </div>
                            </body>
                            </html>
                            """, unsafe_allow_html=True)
                    with col2:
                        st.markdown("""      
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <style>
                                    .card {
                                        width: 300px;
                                        padding: 20px;
                                        border: 1px solid #ddd;
                                        border-radius: 5px;
                                        background-color: #f9f9f9;
                                        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                                        transition: box-shadow 0.3s;
                                        text-align: center;
                                    }

                                    .card:hover {
                                        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
                                    }

                                    .card-title {
                                        font-size: 18px;
                                        margin-bottom: 10px;
                                    }

                                    .card-content {
                                        font-size: 24px;
                                    }
                                </style>
                            </head>
                            <body>
                                <div class="card">
                                    <h3 class="card-title">Estimasi Total Pencemaran Sebulan</h3>
                                    <h1 class="card-content">"""+str(total_pencemaran_sebulan_kg)+""" kg</h1>
                                </div>
                            </body>
                            </html>
                            """, unsafe_allow_html=True)
                    st.empty()
                    st.markdown('<p style="text-align: center; margin-top:15px;" class="title">Detail Air Pollutant</p>', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(4, 4))
                    labels = ['NOx', 'CO', 'SOx', 'PM10', 'PM2.5', 'HC', 'CO2']
                    sizes = [total_nox, total_co, total_sox, total_pm10, total_pm25, total_hc, total_co2]
                    ax.pie(sizes, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')
                    ax.legend(labels, loc="best")
                    st.pyplot(fig)
                else:
                    st.write("Tidak ada pencemaran yang tercatat.")
