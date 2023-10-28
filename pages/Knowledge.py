import streamlit as st
import sqlite3
import datetime
import time

# Create a connection to the database
conn = sqlite3.connect('pollution.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        location TEXT,
        submit_date TEXT,
        answers TEXT,
        points INTEGER
    )
''')

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

# Display form for the user
st.title('Knowledge Check on Pollution')

# Function to validate input
def validate_input(name, age, location):
    if name.strip() == '':
        st.error('Nama tidak boleh kosong.')
        return False

    if age < 17 or age > 45:
        st.error('Umur harus antara 17 dan 45 tahun.')
        return False

    if location.strip() == '':
        st.error('Domisili tidak boleh kosong.')
        return False

    return True

# Variables for user information
name = st.text_input('Nama:')
age = st.number_input('Umur:',  min_value=17, max_value=45, step=1)
location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'))

# Display start button
start_check = st.button('Mulai Knowledge Check')
submitted = False  # Initialize the submitted variable

if start_check:
    start_time = time.time()
    user_answers = []
    form_submitted = False

    # Display questions and options within the form
    with st.form("knowledge_check_form"):
        st.write("Jawablah pertanyaan berikut (pilih salah satu opsi jawaban)")
        for i in range(len(questions)):
            user_answer = st.radio(questions[i], options[i])
            user_answers.append(user_answer)

        # Validate input within the form
        if st.form_submit_button(label='Selesai'):
            form_submitted = True

    # Handle the form submission
    if form_submitted:
        if time.time() - start_time <= 300:  # 5-minute time limit
            if validate_input(name, age, location):
                submit_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                points = calculate_points(user_answers)

                # Insert data into the database
                c.execute('''
                    INSERT INTO knowledge (name, age, location, submit_date, answers, points) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, age, location, submit_date, ','.join(user_answers), points))

                conn.commit()

                # Display results
                st.write('Terima kasih telah mengisi Knowledge Check!')
                st.write('Nama:', name)
                st.write('Umur:', age)
                st.write('Domisili:', location)
                st.write('Tanggal Submit:', submit_date)
                st.write('Jawaban:', ','.join(user_answers))
                st.write('Poin:', points)
                st.stop()
        else:
            st.write("Waktu telah habis. Silakan submit jawaban Anda.")

# Close the database connection
conn.close()
