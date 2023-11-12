import streamlit as st
from deta import Deta
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns

st.set_page_config(
    page_title="Dashboard and Realtime Monitoring",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    )


# List of questions, options, and correct answers
questions = [
    "Polutan udara utama di Jakarta adalah...",
    "Dampak polusi udara di Jakarta terhadap kesehatan manusia adalah...",
    "Apa langkah konkret yang dapat diambil warga untuk mengurangi polusi udara dalam ruangan di lingkungan rumah?",
    "Selain regulasi kendaraan, langkah apa yang diambil pemerintah untuk mengurangi polusi udara di Jakarta?",
    "Dampak polusi udara di Jakarta terhadap ekonomi adalah...",
    "Apa jenis vegetasi yang paling efektif dalam menyerap polutan udara di perkotaan Jakarta?",
    "Apa langkah-langkah yang bisa diambil pemerintah untuk mempromosikan pola transportasi berkelanjutan di Jakarta?",
    "Bagaimana konsep ekonomi sirkular berperan dalam mengurangi dampak polusi udara terhadap kesehatan masyarakat?",
    "Program pemerintah apa yang bertujuan untuk mengurangi polusi udara di Jakarta?",
    "Salah satu cara untuk mengurangi polusi udara di Jakarta adalah dengan mengurangi penggunaan kendaraan pribadi. Aktivitas apa yang bisa dilakukan untuk mengurangi penggunaan kendaraan pribadi, tetapi membutuhkan dukungan dari masyarakat?"
]

options = [
    ['a. Nitrogen dioksida (NO2)', 'b. Sulfur dioksida (SO2)', 'c. Partikel halus (PM2.5)', 'd. Metana (CH4)'],
    ['a. Iritasi mata dan hidung', 'b. Penyakit jantung dan paru-paru', 'c. Kanker', 'd. Semua jawaban benar'],
    ['a. Menggunakan pembersih udara HEPA', 'b. Meningkatkan penggunaan parfum', 'c. Menambah jumlah hewan peliharaan', 'd. Menutup ventilasi'],
    ['a. Penghijauan trotoar', 'b. Penggunaan lebih banyak plastik ramah lingkungan', 'c. Peningkatan pembakaran sampah', 'd. Perluasan jalan raya'],
    ['a. Menurunkan produktivitas kerja', 'b. Meningkatkan biaya kesehatan', 'c. Menurunkan daya saing', 'd. Semua jawaban benar'],
    ['a. Rumput', 'b. Pohon berdaun lebar', 'c. Semak belukar', 'd. Alga'],
    ['a. Meningkatkan harga bahan bakar', 'b. Membangun lebih banyak jalan tol', 'c. Meningkatkan tarif parkir', 'd. Memberikan insentif bagi pengguna transportasi umum'],
    ['a. Dengan meningkatkan akses terhadap pelayanan kesehatan', 'b. Dengan menekan produksi limbah berbahaya', 'c. Dengan mengurangi harga obat-obatan', 'd. Dengan meningkatkan ketersediaan kendaraan pribadi'],
    ['a. Program Langit Biru', 'b. Program Jakarta Hijau', 'c. Program Kendaraan Bermotor Listrik', 'd. Program Pengendalian Sampah'],
    ['a. Menggunakan kendaraan umum', 'b. Berjalan kaki', 'c. Bersepeda', 'd. Melakukan carpooling']
]

correct_answers = ['c. Partikel halus (PM2.5)', 
                   'd. Semua jawaban benar', 
                   'a. Menggunakan pembersih udara HEPA', 
                   'a. Penghijauan trotoar', 
                   'd. Semua jawaban benar', 
                   'b. Pohon berdaun lebar', 
                   'd. Memberikan insentif bagi pengguna transportasi umum', 
                   'b. Dengan menekan produksi limbah berbahaya', 
                   'a. Program Langit Biru', 
                   'd. Melakukan carpooling']

# Function to calculate points
def calculate_points(answers):
    point = 0
    for i in range(len(answers)):
        if answers[i].lower() == correct_answers[i].lower():
            point += 1
    return point

# Tampilkan form untuk pengguna
st.title('Knowledge Check on Pollution')

tab1, tab2= st.tabs(["Knowledge Quiz", "Statistics"])

with tab1:
        name = st.text_input('Nama:', placeholder='Masukkan nama Anda', help='Nama tidak boleh kosong')
        sex = st.selectbox('Jenis Kelamin:',('Laki-Laki', 'Perempuan'), index=None, help='Pilih jenis kelamin anda')
        age = st.number_input('Umur:',  min_value=17, max_value=50, step=1, help='Umur minimal 17 tahun dan maksimal 50 tahun', value=None, placeholder="Masukkan umur Anda")
        location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'), help='Pilih domisili Anda', index=None)

        with st.form("knowledge_check_form", clear_on_submit=True):
            st.write("Jawablah pertanyaan berikut (pilih salah satu opsi jawaban)")
            user_answers = []
            for i in range(10):
                if i < len(questions):
                    user_answers.append(st.radio(questions[i], options[i], index=None))

            submitted = st.form_submit_button(label='Submit')

        if submitted and all(user_answers) and name and age and location and sex:
            submit_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            points = calculate_points(user_answers) 

            # Connect to Deta Base with your Project Key
            deta = Deta(st.secrets["data_key"])

            # If the user clicked the submit button,
            # write the data from the form to the database.
            db = deta.Base("db_test")

            if submitted and all(user_answers):
                db.put({
                    "name": name,
                    "sex" : sex,
                    "age": age,
                    "location": location,
                    "submit_date": submit_date,
                    "points": points,
                    "q1": user_answers[0],
                    "q2": user_answers[1],
                    "q3": user_answers[2],
                    "q4": user_answers[3],
                    "q5": user_answers[4],
                    "q6": user_answers[5],
                    "q7": user_answers[6],
                    "q8": user_answers[7],
                    "q9": user_answers[8],
                    "q10": user_answers[9]
                })
                st.success('Terima kasih telah mengisi Knowledge Check!')
                st.write('Tanggal Submit:', submit_date)
                st.write('Total Poin:', points)
                st.markdown(
                            """
                            <style>
                                .container {
                                    width: 80%;
                                    margin: 0 auto;
                                    overflow: hidden;
                                }
                                .text-animation {
                                    text-align: center;
                                    color: #008080;
                                    font-size: 24px;
                                    font-weight: bold;
                                    white-space: nowrap;
                                    overflow: hidden;
                                    border-right: 0.15em solid;
                                    animation: typing 6s steps(35, end) infinite, color-change 8s infinite;
                                }

                                @keyframes typing {
                                    from { width: 0 }
                                    to { width: 100% }
                                }

                                @keyframes color-change {
                                    0% { color: #FF1493; }
                                    25% { color: #1E90FF; }
                                    50% { color: #32CD32; }
                                    75% { color: #FFA500; }
                                    100% { color: #FF1493; }
                                }
                            </style>
                            """,
                            unsafe_allow_html=True)
                st.markdown(
                            """
                            <div class="container">
                            <p class="text-animation">Upgrade pengetahuanmu dengan menonton video ini!</p>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                col19,col20,col21 = st.columns(3,gap="large")
                with col19:
                    st.markdown(
                            """
                            <style>
                                .card {
                                    width: 350px;
                                    background-color: #f8f9fa;
                                    padding: 20px;
                                    border-radius: 10px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                    text-align: center;
                                    transition: transform 0.3s;
                                }
                                .card:hover {
                                    transform: scale(1.05);
                                }
                                .button {
                                    display: inline-block;
                                    background-color: #3498db;
                                    color: #fff;
                                    border: none;
                                    padding: 10px 16px;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    transition: background-color 0.3s;
                                }
                                .button:hover {
                                    background-color: #2980b9;
                                }
                                .thumbnail {
                                    width: 300px;
                                    height: 250px;
                                    border-radius: 10px;
                                    object-fit: cover;
                                    margin-bottom: 15px;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                    video_id = "pbrpdUiSYMY"  # Ganti dengan ID video YouTube yang diinginkan
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"  # URL thumbnail dari video YouTube

                    st.markdown(
                            f"""
                            <div class="card">
                                <h3 style='font-size:20px'>Air pollution - How does it impact our health?</h3>
                                <img src="{thumbnail_url}" alt="Thumbnail" class="thumbnail">
                                <p>Klik tombol di bawah untuk menonton video:</p>
                                <a href="https://www.youtube.com/watch?v={video_id}" target="_blank"><button class="button">Tonton Video</button></a>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                with col20:
                    st.markdown(
                            """
                            <style>
                                .card {
                                    width: 350px;
                                    background-color: #f8f9fa;
                                    padding: 20px;
                                    border-radius: 10px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                    text-align: center;
                                    transition: transform 0.3s;
                                }
                                .card:hover {
                                    transform: scale(1.05);
                                }
                                .button {
                                    display: inline-block;
                                    background-color: #3498db;
                                    color: #fff;
                                    border: none;
                                    padding: 10px 16px;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    transition: background-color 0.3s;
                                }
                                .button:hover {
                                    background-color: #2980b9;
                                }
                                .thumbnail {
                                    width: 300px;
                                    height: 250px;
                                    border-radius: 10px;
                                    object-fit: cover;
                                    margin-bottom: 15px;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                    video_id1 = "fephtrPt6wk"  # Ganti dengan ID video YouTube yang diinginkan
                    thumbnail_url1 = f"https://img.youtube.com/vi/{video_id1}/0.jpg"  # URL thumbnail dari video YouTube

                    st.markdown(
                            f"""
                            <div class="card">
                                <h3 style='font-size:20px'>Air Pollution | What Causes Air Pollution? | The Dr Binocs Show | </h3>
                                <img src="{thumbnail_url1}" alt="Thumbnail" class="thumbnail">
                                <p>Klik tombol di bawah untuk menonton video:</p>
                                <a href="https://www.youtube.com/watch?v={video_id1}" target="_blank"><button class="button">Tonton Video</button></a>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                with col21:
                    st.markdown(
                            """
                            <style>
                                .card {
                                    width: 350px;
                                    background-color: #f8f9fa;
                                    padding: 20px;
                                    border-radius: 10px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                    text-align: center;
                                    transition: transform 0.3s;
                                }
                                .card:hover {
                                    transform: scale(1.05);
                                }
                                .button {
                                    display: inline-block;
                                    background-color: #3498db;
                                    color: #fff;
                                    border: none;
                                    padding: 10px 16px;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    transition: background-color 0.3s;
                                }
                                .button:hover {
                                    background-color: #2980b9;
                                }
                                .thumbnail {
                                    width: 300px;
                                    height: 250px;
                                    border-radius: 10px;
                                    object-fit: cover;
                                    margin-bottom: 15px;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                    video_id2 = "0gjnhBfvnZs"  # Ganti dengan ID video YouTube yang diinginkan
                    thumbnail_url2 = f"https://img.youtube.com/vi/{video_id2}/0.jpg"  # URL thumbnail dari video YouTube

                    st.markdown(
                            f"""
                            <div class="card">
                                <h3 style='font-size:20px'> Six ways to reduce air pollution </h3>
                                <img src="{thumbnail_url2}" alt="Thumbnail" class="thumbnail">
                                <p>Klik tombol di bawah untuk menonton video:</p>
                                <a href="https://www.youtube.com/watch?v={video_id2}" target="_blank"><button class="button">Tonton Video</button></a>
                            </div>
                            """,
                            unsafe_allow_html=True)
                st.empty()
                st.empty()
                st.markdown(
                            """
                            <style>
                                .container {
                                    width: 50%;
                                    margin: 0 auto;
                                    overflow: hidden;
                                }
                                .text-animation {
                                    text-align: center;
                                    color: #008080;
                                    font-size: 24px;
                                    font-weight: bold;
                                    white-space: nowrap;
                                    overflow: hidden;
                                    border-right: 0.15em solid;
                                    animation: typing 6s steps(25, end) infinite, color-change 8s infinite;
                                }

                                @keyframes typing {
                                    from { width: 0 }
                                    to { width: 100% }
                                }

                                @keyframes color-change {
                                    0% { color: #FF1493; }
                                    25% { color: #1E90FF; }
                                    50% { color: #32CD32; }
                                    75% { color: #FFA500; }
                                    100% { color: #FF1493; }
                                }
                            </style>
                            """,
                            unsafe_allow_html=True)
                st.markdown(
                            """
                            <div class="container">
                            <p class="text-animation">Naik level dengan membaca artikel ini!</p>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                col16,col17,col18 = st.columns(3, gap="small")
                with col16:
                    st.markdown(
                        """
                        <style>
                            .card {
                                width: 300px;
                                border: 2px solid #e6e6e6;
                                border-radius: 10px;
                                overflow: hidden;
                                margin: 20px;
                                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                                transition: 0.3s;
                                font-family: 'Arial';
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                background-color: #f9f9f9;
                                text-align: center;
                            }

                            .card:hover {
                                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
                                transform: scale(1.05);
                            }

                            .card-content {
                                padding: 20px;
                            }

                            .card-content h3 {
                                color: #333;
                                font-size: 1.5em;
                                margin: 0;
                            }

                            .card-link {
                                text-decoration: none;
                                color: #333;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    url = 'https://news.detik.com/berita/d-6073382/pemprov-dki-siapkan-program-langit-biru-untuk-perbaiki-kualitas-udara'
                    title = 'Pemprov DKI Siapkan Program Langit Biru'

                    st.markdown(
                        f"""
                        <div class="card">
                            <a class="card-link" href="{url}" target="_blank">
                                <div class="card-content">
                                    <h3>{title}</h3>
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col17:
                    st.markdown(
                        """
                        <style>
                            .card {
                                width: 300px;
                                border: 2px solid #e6e6e6;
                                border-radius: 10px;
                                overflow: hidden;
                                margin: 20px;
                                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                                transition: 0.3s;
                                font-family: 'Arial';
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                background-color: #f9f9f9;
                                text-align: center;
                            }

                            .card:hover {
                                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
                                transform: scale(1.05);
                            }

                            .card-content {
                                padding: 20px;
                            }

                            .card-content h3 {
                                color: #333;
                                font-size: 1.5em;
                                margin: 0;
                            }

                            .card-link {
                                text-decoration: none;
                                color: #333;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    url = 'https://www.siloamhospitals.com/informasi-siloam/artikel/bahaya-polusi-udara'
                    title = '8 Bahaya Polusi Udara'

                    st.markdown(
                        f"""
                        <div class="card">
                            <a class="card-link" href="{url}" target="_blank">
                                <div class="card-content">
                                    <h3>{title}</h3>
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col18:
                    st.markdown(
                        """
                        <style>
                            .card {
                                width: 300px;
                                border: 2px solid #e6e6e6;
                                border-radius: 10px;
                                overflow: hidden;
                                margin: 20px;
                                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                                transition: 0.3s;
                                font-family: 'Arial';
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                background-color: #f9f9f9;
                                text-align: center;
                            }

                            .card:hover {
                                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
                                transform: scale(1.05);
                            }

                            .card-content {
                                padding: 20px;
                            }

                            .card-content h3 {
                                color: #333;
                                font-size: 1.5em;
                                margin: 0;
                            }

                            .card-link {
                                text-decoration: none;
                                color: #333;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    url = 'https://solarimpulse.com/air-pollution-solutions'
                    title = 'Air Pollution Solutions'

                    st.markdown(
                        f"""
                        <div class="card">
                            <a class="card-link" href="{url}" target="_blank">
                                <div class="card-content">
                                    <h3>{title}</h3>
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                col22,col23,col24 = st.columns(3, gap="small")
                with col23:
                    st.markdown(
                        """
                        <style>
                            .card {
                                width: 300px;
                                border: 2px solid #e6e6e6;
                                border-radius: 10px;
                                overflow: hidden;
                                margin: 20px;
                                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                                transition: 0.3s;
                                font-family: 'Arial';
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                background-color: #f9f9f9;
                                text-align: center;
                            }

                            .card:hover {
                                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
                                transform: scale(1.05);
                            }

                            .card-content {
                                padding: 20px;
                            }

                            .card-content h3 {
                                color: #333;
                                font-size: 1.5em;
                                margin: 0;
                            }

                            .card-link {
                                text-decoration: none;
                                color: #333;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    url = 'https://www.pca.state.mn.us/news-and-stories/what-you-can-do-about-air-pollution'
                    title = 'What you can do about air pollution ?'

                    st.markdown(
                        f"""
                        <div class="card">
                            <a class="card-link" href="{url}" target="_blank">
                                <div class="card-content">
                                    <h3>{title}</h3>
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


        else: 
                st.error('Kamu belum mengisi semua form', icon="🚨")


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
        db = deta.Base("db_test")
        db_content = db.fetch().items

        df = pd.DataFrame(db_content)
        submit_counts = df.shape[0]
        avg_age = df["age"].mean() 
        avg_age = math.ceil(avg_age)
        avg_points = df["points"].mean()
        avg_points = math.ceil(avg_points)

        q1_counts = df["q1"].value_counts()
        q2_counts = df["q2"].value_counts()
        q3_counts = df["q3"].value_counts()
        q4_counts = df["q4"].value_counts()
        q5_counts = df["q5"].value_counts()
        q6_counts = df["q6"].value_counts()
        q7_counts = df["q7"].value_counts()
        q8_counts = df["q8"].value_counts()
        q9_counts = df["q9"].value_counts()
        q10_counts = df["q10"].value_counts()

        with st.container():
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown(f"<h3 style='text-align: center;'>Total Submissions</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{submit_counts}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>Average Age</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{avg_age} Years Old</h2>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<h3 style='text-align: center;'>Average Points</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center;color:red; font-weight:bold;'>{avg_points} Points</h2>", unsafe_allow_html=True)
        
            col4,col5 = st.columns(2)
            with col4:
                st.markdown(f"<h3 style='text-align: center;'>Submissions Frequency over Time</h3>", unsafe_allow_html=True)
                st.empty()
                df["submit_date"] = pd.to_datetime(df["submit_date"])
                df["submit_date"] = df["submit_date"].dt.date
                submission_counts_per_date = df["submit_date"].value_counts().sort_index()
                st.line_chart(submission_counts_per_date, height=408)
            with col5:
                st.markdown(f"<h3 style='text-align: center;'>Age Distribution</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.hist(df["age"])
                st.pyplot(fig)
            col25,col26 = st.columns(2)
            with col25 : 
                fig, ax = plt.subplots()
                domisili_counts = df['location'].value_counts()
                sns.barplot(x=domisili_counts.index, y=domisili_counts.values, palette='viridis', ax=ax)
                ax.set_title("Distribution of Data by Location")
                ax.set_xlabel("Location")
                ax.set_ylabel("Count")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
                st.pyplot(fig)
            with col26:
                sex_counts = df['sex'].value_counts()
                # Buat pie chart
                fig, ax = plt.subplots(figsize=(4,4))
                ax.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
                ax.set_title('Distribution of Sex')
                # Tampilkan di Streamlit
                st.pyplot(fig)
            col27,col28,col29 = st.columns([1,2,1])
            with col28:
                points = df['points']  # Ganti dengan kolom yang sesuai
                # Kategorisasi nilai points
                low_count = sum(1 for point in points if point in range(0, 4))
                medium_count = sum(1 for point in points if point in range(4, 8))
                high_count = sum(1 for point in points if point in range(8, 11))
                # Membuat pie chart
                fig, ax = plt.subplots(figsize=(5,5))
                ax.pie([low_count, medium_count, high_count], labels=['Low Knowledge', 'Medium Knowledge', 'High Knowledge'], colors=['#ff9999','#66b3ff','#99ff99'], autopct='%1.1f%%')
                ax.set_title("Knowledge Level Distribution")
                # Menampilkan pie chart di Streamlit
                st.pyplot(fig)
            col6,col7 = st.columns(2)
            with col6:
                correct_answer = correct_answers[0]
                st.subheader("Bar Chart: Answers for Question 1")
                fig, ax = plt.subplots()
                colors = ['red' if ans != correct_answer else 'green' for ans in q1_counts.index]
                q1_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            with col7: 
                st.subheader("Bar Chart: Answers for Question 2")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[1]
                colors = ['red' if ans != correct_answer else 'green' for ans in q2_counts.index]
                q2_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            col8,col9 = st.columns(2)
            with col8:
                st.subheader("Bar Chart: Answers for Question 3")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[2]
                colors = ['red' if ans != correct_answer else 'green' for ans in q3_counts.index]
                q3_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            with col9:
                st.subheader("Bar Chart: Answers for Question 4")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[3]
                colors = ['red' if ans != correct_answer else 'green' for ans in q4_counts.index]
                q4_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            col10,col11 = st.columns(2)
            with col10:
                st.subheader("Bar Chart: Answers for Question 5")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[4]
                colors = ['red' if ans != correct_answer else 'green' for ans in q5_counts.index]
                q5_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            with col11:
                st.subheader("Bar Chart: Answers for Question 6")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[5]
                colors = ['red' if ans != correct_answer else 'green' for ans in q6_counts.index]
                q6_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            col12,col13 = st.columns(2)
            with col12:
                st.subheader("Bar Chart: Answers for Question 7")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[6]
                colors = ['red' if ans != correct_answer else 'green' for ans in q7_counts.index]
                q7_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            with col13:
                st.subheader("Bar Chart: Answers for Question 8")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[7]
                colors = ['red' if ans != correct_answer else 'green' for ans in q8_counts.index]
                q8_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            col14,col15 = st.columns(2)
            with col14:
                st.subheader("Bar Chart: Answers for Question 9")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[8]
                colors = ['red' if ans != correct_answer else 'green' for ans in q9_counts.index]
                q9_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)
            with col15:
                st.subheader("Bar Chart: Answers for Question 10")
                fig, ax = plt.subplots()
                correct_answer = correct_answers[9]
                colors = ['red' if ans != correct_answer else 'green' for ans in q10_counts.index]
                q10_counts.plot(kind="barh", color=colors, ax=ax)
                st.pyplot(fig)