import streamlit as st
import sqlite3
import datetime
import time

# Membuat koneksi dengan database
conn = sqlite3.connect('pollution.db')
c = conn.cursor()

# Daftar pertanyaan dan jawaban
questions = [
    "Apa penyebab utama dari polusi udara?",
    "Apa yang dimaksud dengan 'smog'?",
    # Tambahkan pertanyaan lain di sini
]

# Daftar opsi jawaban
options = ['a', 'b', 'c', 'd']

# Fungsi untuk menghitung poin
def calculate_points(answers):
    point = 0
    for ans in answers:
        if ans == 'a':
            point += 1
    return point

# Tampilkan form untuk pengguna
st.title('Knowledge Check on Pollution')
name = st.text_input('Nama:')
age = st.number_input('Umur:',  min_value=0, max_value=150, step=1)
location = st.selectbox('Domisili:', ('Jakarta Pusat', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Selatan', 'Bogor', 'Depok', 'Tangerang', 'Bekasi'))

start_check = st.button('Mulai Knowledge Check')
if start_check:
    start_time = time.time()
    if time.time() - start_time <= 300:  # Batas waktu 5 menit
        with st.form("knowledge_check_form"):
            st.write("Jawablah pertanyaan berikut (pilih salah satu opsi jawaban)")
            user_answers = []
            for i in range(10):
                if i < len(questions):
                    user_answers.append(st.radio(questions[i], options))

            st.form_submit_button(label='Submit')

        if user_answers:
            submit_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            points = calculate_points(user_answers)

            # Memasukkan data ke database
            c.execute('''
                INSERT INTO knowledge (name, age, location, submit_date, answers, points) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, age, location, submit_date, ','.join(user_answers), points))

            conn.commit()

            # Menampilkan hasil
            st.write('Terima kasih telah mengisi Knowledge Check!')
            st.write('Nama:', name)
            st.write('Umur:', age)
            st.write('Domisili:', location)
            st.write('Tanggal Submit:', submit_date)
            st.write('Jawaban:', ','.join(user_answers))
            st.write('Poin:', points)
    else:
        st.write("Waktu telah habis. Silakan submit jawaban Anda.")

conn.close()
