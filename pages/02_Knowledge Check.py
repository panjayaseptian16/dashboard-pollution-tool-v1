import streamlit as st
from deta import Deta
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(
    page_title="Dashboard and Realtime Monitoring",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# List of questions, options, and correct answers
questions = [
    "Polutan udara utama di Jakarta adalah...",
    "Dampak polusi udara di Jakarta terhadap kesehatan manusia adalah...",
    "Apa langkah konkret yang dapat diambil warga untuk mengurangi polusi udara dalam ruangan di lingkungan rumah?",
    "Selain regulasi kendaraan, langkah apa yang diambil pemerintah untuk mengurangi polusi udara di Jakarta?",
    "Dampak polusi udara di Jakarta terhadap ekonomi adalah...",
    "Apa jenis vegetasi yang paling efektif dalam menyerap polutan udara di perkotaan Jakarta?",
    "Apa langkah-langkah yang bisa diambil pemerintah untuk mempromosikan pola transportasi berkelanjutan di Jakarta?",
    "Bagaimana peningkatan jumlah industri tekstil di sekitar Jakarta berkontribusi terhadap polusi air di daerah sekitarnya?",
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
    ['a. Peningkatan kualitas air', 'b. Peningkatan kesejahteraan masyarakat', 'c. Peningkatan konsumsi energi', 'd. Peningkatan produksi limbah cair'],
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
                   'd. Peningkatan produksi limbah cair', 
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
        age = st.number_input('Umur:',  min_value=17, max_value=50, step=1, help='Umur minimal 17 tahun dan maksimal 50 tahun', value=None, placeholder="Masukkan umur Anda")
        location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'), help='Pilih domisili Anda', index=None)

        with st.form("knowledge_check_form", clear_on_submit=True):
            st.write("Jawablah pertanyaan berikut (pilih salah satu opsi jawaban)")
            user_answers = []
            for i in range(10):
                if i < len(questions):
                    user_answers.append(st.radio(questions[i], options[i], index=None))

            submitted = st.form_submit_button(label='Submit')

        if submitted and all(user_answers):
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
        else: 
                st.error('Kamu belum mengisi semua form', icon="🚨")
with tab2: 
    st.subheader("Statistics of Pollution Knowledge Quiz")
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("db_test")
    db_content = db.fetch().items
    st.write(db_content)
    df = pd.DataFrame(db_content)
    submit_counts = df.shape[0]
    avg_age = df["age"].mean()
    avg_points = df["points"].mean()

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

    st.write("Number of Submissions:", submit_counts)
    st.write("Average Age:", avg_age)
    st.write("Average Points:", avg_points)

    st.text("Line Chart: Submission Frequency over Time")
    df["submit_date"] = pd.to_datetime(df["submit_date"])
    df["submit_date"] = df["submit_date"].dt.date
    submission_counts_per_date = df["submit_date"].value_counts().sort_index()
    st.line_chart(submission_counts_per_date)

    st.subheader("Bar Chart: Age Distribution")
    fig, ax = plt.subplots()
    ax.bar(df["name"], df["age"])
    st.pyplot(fig)

    for i, (question, counts) in enumerate(zip(questions, [q1_counts, q2_counts, q3_counts, q4_counts, q5_counts, q6_counts, q7_counts, q8_counts, q9_counts, q10_counts])):
        st.subheader(f"Bar Chart: Answers for {question}")
        fig, ax = plt.subplots()
        colors = ['skyblue' if answer.lower() == correct_answers[i].lower() else 'lightcoral' for answer in counts.index]
        counts.plot(kind="bar", color=colors, ax=ax)
        st.pyplot(fig)