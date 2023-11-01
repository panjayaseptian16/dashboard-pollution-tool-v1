import streamlit as st
import datetime

# Membuat koneksi dengan database
conn = conn = st.experimental_connection('pollution_db', type='sql', autocommit=True)
c = conn.session

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
name = st.text_input('Nama:')
age = st.number_input('Umur:',  min_value=17, max_value=50, step=1)
location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'))

with st.form("knowledge_check_form"):
    st.write("Jawablah pertanyaan berikut (pilih salah satu opsi jawaban)")
    user_answers = []
    for i in range(10):
        user_answers.append(st.radio(questions[i], options[i]))

    submitted = st.form_submit_button(label='Submit')

    if submitted and all(user_answers):
        submit_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        points = calculate_points(user_answers)

        # Masukkan data ke dalam database
        c.execute('''
            INSERT INTO knowledge (name, age, location, submit_date, answers, points, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) 
            VALUES (:name, :age, :location, :submit_date, :answers, :points, :q1, :q2, :q3, :q4, :q5, :q6, :q7, :q8, :q9, :q10)
        ''', {
            'name': name,
            'age': age,
            'location': location,
            'submit_date': submit_date,
            'answers': ','.join(user_answers),
            'points': points,
            'q1': user_answers[0],
            'q2': user_answers[1],
            'q3': user_answers[2],
            'q4': user_answers[3],
            'q5': user_answers[4],
            'q6': user_answers[5],
            'q7': user_answers[6],
            'q8': user_answers[7],
            'q9': user_answers[8],
            'q10': user_answers[9]
        })

        c.commit()

        # Menampilkan hasil
        st.write('Terima kasih telah mengisi Knowledge Check!')
        st.write('Tanggal Submit:', submit_date)
        st.write('Total Poin:', points)

conn.reset()