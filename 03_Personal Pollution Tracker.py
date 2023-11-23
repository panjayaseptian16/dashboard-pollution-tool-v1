import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from deta import Deta
import math
from datetime import datetime

st.set_page_config(
    page_title="Personal Pollution Tracker",
    page_icon="🔖",
    layout="wide",
    initial_sidebar_state="auto"
    )

tab1,tab2,tab3 = st.tabs(['Personal Pollution Tracker', 'Statistics',"Source Data"])
with tab3: 
    with st.container():
        st.markdown("""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <style>
                            table {
                                width: 80%;
                                border-collapse: collapse;
                                margin-top: 20px;
                            }

                            th, td {
                                border: 1px solid #dddddd;
                                text-align: center;
                                padding: 12px;
                                transition: background-color 0.3s ease, color 0.3s ease;
                            }

                            th {
                                background-color: #f2f2f2;
                            }

                            a {
                                color: #183D3D;
                                text-decoration: none;
                                font-weight: bold;
                                font-size: 14px;
                                transition: color 0.3s ease;
                            }

                            a:hover {
                                text-decoration: underline;
                                color: #ff4500;
                            }

                            tr:hover {
                                background-color: #f5f5f5;
                            }
                        </style>
                    </head>
                    <body>
                        <table>
                            <tr>
                                <th style='color:#183D3D;'>Estimate Emission Factor Source-Data</th>
                            </tr>
                            <tr>
                                <td><a href="https://indonesia.go.id/kategori/indonesia-dalam-angka/2533/membenahi-tata-kelola-sampah-nasional">Average daily waste per individual</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://ppkl.menlhk.go.id/website/filebox/609/190710181542PEDOMAN%20TEKNIS%20PENYUSUNAN%20INVENTARISASI%20EMISI.pdf">LPG & Aviation</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://js.bsn.go.id/index.php/standardisasi/article/view/792/pdf">Train Emission</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://ppis.bsn.go.id/downloads/2021/Life%20Cycle%20Assessment%20Penggunaan%20Bahan%20Bakar,%20Refrigeran%20dan%20Energi%20Listrik%20pada%20Transjakarta.pdf">Transjakarta</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://jakartamrt.co.id/id/info-terkini/24-juta-lebih-orang-gunakan-mrt-jakarta-pada-desember-2022">MRT - Average daily ridership in December 2022</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://jakartamrt.co.id/sites/default/files/2023-07/Sustainability%20Report%20MRT%20Jakarta%202022.pdf">MRT - CO2 Tons in December 2022</a></td>
                            </tr>
                            <tr>
                                <td><a href="http://komara.weebly.com/uploads/6/5/3/7/6537907/g_permen_lh_12_2010_pelaksanaan_pengendalian_pencemaran_udara_di_daerah.pdf">Motorcycles & Cars</a></td>
                            </tr>
                            <tr>
                                <td><a href="https://www.tandfonline.com/doi/epdf/10.1080/02786826.2017.1300231?needAccess=true">Cigarettes</a></td>
                            </tr>
                        </table>
                    </body>
                    </html>""",unsafe_allow_html=True)
with tab1: 
    # CSS dan HTML untuk tampilan
    col4,col5,col6 = st.columns([1,3,1])
    with col5:
        st.markdown(
            """
            <style>
            .title {
                font-size: 32px;
                color: #FFFD8C;
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
        name = st.text_input('Nama:', placeholder='Masukkan nama Anda', help='Nama tidak boleh kosong')
        sex = st.selectbox('Jenis Kelamin:',('Laki-Laki', 'Perempuan'), index=None, help='Pilih jenis kelamin anda')
        age = st.number_input('Umur:',  min_value=17, max_value=50, step=1, help='Umur minimal 17 tahun dan maksimal 50 tahun', value=None, placeholder="Masukkan umur Anda")
        location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'), help='Pilih domisili Anda', index=None)
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
                if not (jumlah_anggota and membakar_sampah and gas_lpg and merokok and name and age and sex and location):
                    st.error('Harap mengisi semua isi form sebelum melanjutkan.')
                else:
                    st.success('Terima Kasih sudah Submit!')
                    st.header('Hasil Pencatatan Pencemaran Pribadi')
                    submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                    total_pencemaran_setahun_ton = round((total_pencemaran_sebulan_kg * 12)/1000000,2)

                    deta = Deta(st.secrets["data_key"])

                    db = deta.Base("db_test1")
                    db.put({
                        "Name": name,
                        "Submission Date": submission_date,
                        "Jenis Kelamin" : sex,
                        "Usia" : age,
                        "Domisili" : location,
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
                        with st.container():
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
                                                background-color: #183D3D;
                                                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                                                transition: box-shadow 0.3s;
                                                text-align: center;
                                                color: 183D3D;
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
                                                background-color: #183D3D;
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
                            fig, ax = plt.subplots(figsize=(2, 2))
                            labels = ['NOx', 'CO', 'SOx', 'PM10', 'PM2.5', 'HC', 'CO2']
                            sizes = [total_nox, total_co, total_sox, total_pm10, total_pm25, total_hc, total_co2]

                            # Mengurutkan data berdasarkan ukuran
                            sorted_sizes, sorted_labels = zip(*sorted(zip(sizes, labels), reverse=True))
                            # Hanya mempertahankan 3 label tertinggi
                            show_labels = 3
                            visible_labels = sorted_labels[:show_labels]
                            visible_sizes = sorted_sizes[:show_labels]

                            ax.pie(visible_sizes, autopct='%1.1f%%', startangle=90)
                            ax.axis('equal')
                            legend = ax.legend(visible_labels, loc="best", bbox_to_anchor=(1, 0.5), fontsize="xx-small")
                            st.pyplot(fig)

                    else:
                        st.write("Tidak ada pencemaran yang tercatat.")

expected_password = st.secrets["tab2_password"]
tab2_access_granted = False

with tab2:
    password = st.text_input("Enter Password (Developer Only)", type="password")
    if password == expected_password:
        st.success("Correct Password! You can access Tab 2.")
        tab2_access_granted = True
    else:
        st.warning("Incorrect Password! Please try again.")
        tab2_access_granted = False

if tab2_access_granted:
    tab2 = st.tabs(["Statistics"])
    if tab2[0]:

        deta = Deta(st.secrets["data_key"])
        db = deta.Base("db_test1")
        db_content = db.fetch().items

        df = pd.DataFrame(db_content)
        submit_counts = df.shape[0]
        avg_age = df["Usia"].mean()
        avg_age = math.ceil(avg_age)
        avg_pollution = df["Total Pencemaran Harian"].mean()
        avg_pollution = math.ceil(avg_pollution)
        with st.container():
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown(f"<h3 style='text-align: center;'>Total Submissions</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{submit_counts}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>Average Age</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{avg_age} Years Old</h2>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<h3 style='text-align: center;'>Average Daily Emissions</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{avg_pollution} gr</h2>", unsafe_allow_html=True)
            col7,col8,col12 = st.columns(3)
            # Visualization 4: Pie chart for Jenis Kelamin
            with col7:
                sex_counts = df['Jenis Kelamin'].value_counts()
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.pie(sex_counts, labels=['Men','Women'], autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
                ax.set_title("Gender Distribution")
                st.pyplot(fig,use_container_width=True)
            # Visualization 5: Bar plot for Domisili
            with col12:
                fig, ax = plt.subplots()
                domisili_counts = df['Domisili'].value_counts()
                sns.barplot(x=domisili_counts.index, y=domisili_counts.values, palette='viridis', ax=ax)
                ax.set_title("Distribution of Data by Location")
                ax.set_xlabel("Location")
                ax.set_ylabel("Count")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
                st.pyplot(fig,use_container_width=True)
            st.markdown(f"<h3 style='text-align: center;'>Household</h3>", unsafe_allow_html=True)

            col4, col5, col6 = st.columns(3)
            with col4:
                membakar_sampah_counts = df['Membakar Sampah'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(membakar_sampah_counts, labels=['Yes','No'], autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
                ax.set_title("Waste Burning Distribution")
                st.pyplot(fig,use_container_width=True)
            # Visualization 2: Count plot for Ukuran Gas LPG
            with col5:
                sns.set_theme(style="darkgrid")
                fig, ax = plt.subplots()
                sns.countplot(x='Ukuran Gas LPG', data=df, palette='viridis', ax=ax)
                ax.set_title("Distribution of LPG Gas Size")
                ax.set_xlabel("LPG Gas Size")
                ax.set_ylabel("Count")
                st.pyplot(fig,use_container_width=True)
            # Visualization 3: Bar plot for Jumlah Anggota Keluarga
            with col6:
                fig, ax = plt.subplots()
                # Use seaborn's histplot with automatic bin selection
                sns.histplot(df['Jumlah Anggota Keluarga'], kde=False, color='skyblue', ax=ax)
                ax.set_title("Distribution of Number of Household Members")
                ax.set_xlabel("Number of Household Members")
                ax.set_ylabel("Count")
                st.pyplot(fig,use_container_width=True)

            st.markdown(f"<h3 style='text-align: center;'>Smoking Activity</h3>", unsafe_allow_html=True)
            col16,col17,col18 = st.columns(3)
            with col16 :
                # Histogram untuk jumlah batang rokok
                fig, ax = plt.subplots()
                sns.histplot(df["Jumlah Batang Rokok"], bins=10, kde=False, color="skyblue", ax=ax)
                plt.title('Distribution of Cigarette Consumption')
                plt.xlabel('Number of Cigarettes')
                plt.ylabel('Frequency')
                st.pyplot(fig,use_container_width=True)
            with col17 :   
                # Pie chart untuk tipe rokok
                fig, ax = plt.subplots()
                df['Tipe Rokok'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, colors=['lightcoral', 'lightgreen'])
                plt.title('Distribution of Cigarette Types')
                st.pyplot(fig,use_container_width=True)
            with col18 :
                # Bar chart untuk Merokok atau Tidak
                df['Merokok'] = df['Merokok'].map({'Ya': 'Yes', 'Tidak': 'No'})
                fig, ax = plt.subplots()
                sns.countplot(x="Merokok", data=df, palette="pastel", ax=ax)
                plt.title('Smoking Status')
                plt.xlabel('Smoking')
                plt.ylabel('Count')
                st.pyplot(fig,use_container_width=True)
            st.markdown(f"<h3 style='text-align: center;'>Transportation</h3>", unsafe_allow_html=True)
            col9,col10,col11 = st.columns(3)
            with col9: 
                transportation_data = df[["Total KM Motor per hari", "Total KM Mobil per hari", "Total KM Angkot per hari"]]
                total_km_motor = transportation_data["Total KM Motor per hari"].sum()
                total_km_mobil = transportation_data["Total KM Mobil per hari"].sum()
                total_km_angkot = transportation_data["Total KM Angkot per hari"].sum()
                values = [total_km_motor, total_km_mobil, total_km_angkot]
                fig, ax = plt.subplots()
                ax.pie(values, labels=['Daily Motorcycle Mileage (km)', 'Daily Car Mileage (km)', 'Daily Angkot Mileage (km)'], autopct='%1.1f%%', startangle=90,
                    colors=['skyblue', 'lightcoral', 'lightgreen'])
                ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
                plt.title('Transportation Habits')
                plt.xlabel('Mode of Transportation')
                plt.ylabel('Percentage')
                st.pyplot(fig,use_container_width=True)
            with col10: 
                # Menghitung total penerbangan domestik dan internasional
                total_domestic_flights = df['Penerbangan Domestik'].sum()
                total_international_flights = df['Penerbangan Internasional'].sum()

                # Membuat DataFrame baru untuk digunakan pada seaborn
                df_bar = pd.DataFrame({
                    'Flight Type': ['Domestic', 'International'],
                    'Total Flights': [total_domestic_flights, total_international_flights]
                })
                # Membuat bar plot horizontal menggunakan seaborn
                fig, ax = plt.subplots()
                sns.barplot(x='Total Flights', y='Flight Type', data=df_bar, palette=['skyblue', 'lightcoral'], orient='horizontal')
                ax.set_xlabel('Number of Flights')
                ax.set_ylabel('Flight Type')
                ax.set_title('Domestic Flights vs International Flights')
                # Hapus st.pyplot() jika menjalankan di lingkungan lokal
                st.pyplot(fig)

            with col11:
                transport_counts = df[['KRL', 'Transjakarta', 'MRT']].sum()
                fig, ax = plt.subplots()
                transport_counts.plot(kind='bar', color=['#ffcc99', '#66b3ff', '#99ff99'], ax=ax)
                ax.set_title("Total Public Transportation Usage")
                ax.set_xlabel("Public Transportation Mode")
                ax.set_ylabel("Total Usage")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
                st.pyplot(fig,use_container_width=True)
            st.markdown(f"<h3 style='text-align: center;'>Pollution Estimation</h3>", unsafe_allow_html=True)
            col13,col14,col15 = st.columns(3)
            with col13 : 
                pollution_labels = ["Total NOx", "Total CO2", "Total CO", "Total SOx", "Total PM10", "Total PM25", "Total HC"]
                pollution_data = [df[label].iloc[0] for label in pollution_labels]
                # Plotting
                fig, ax = plt.subplots()
                sns.barplot(x=pollution_labels, y=pollution_data, palette="coolwarm", ax=ax)
                ax.set_title('Total Pollutant Emissions')
                ax.set_ylabel('Total Emissions (grams)')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                # Display the plot in Streamlit
                st.pyplot(fig,use_container_width=True)
            with col15:
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.lineplot(x='Submission Date', y='Total Pencemaran Harian', data=df, marker='o', color='purple')
                plt.title('Daily Pollution Over Time')
                plt.xlabel('Submission Date')
                plt.ylabel('Total Emissions (grams)')
                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

                # Display the plot in Streamlit
                st.pyplot(fig,use_container_width=True)





