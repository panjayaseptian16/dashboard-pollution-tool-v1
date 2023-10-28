import streamlit as st
import random
import sqlite3

# Koneksi ke database
conn = sqlite3.connect('pollution.db')
cursor = conn.cursor()

# Mendefinisikan pertanyaan
pertanyaan = [
    "Apakah polusi udara dapat menyebabkan gangguan pernapasan?",
    "Apakah polusi udara dapat menyebabkan penyakit jantung?",
    "Apakah polusi udara dapat menyebabkan kanker?",
    "Apakah polusi udara dapat menyebabkan penuaan dini?",
    "Apakah polusi udara dapat menyebabkan asma?",
    "Apakah polusi udara dapat menyebabkan iritasi mata?",
    "Apakah polusi udara dapat menyebabkan iritasi kulit?",
    "Apakah polusi udara dapat menyebabkan sakit kepala?",
    "Apakah polusi udara dapat menyebabkan kelelahan?",
]

# Mendefinisikan pilihan jawaban
jawaban = [
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
    ["Ya", "Tidak"],
]

# Mendefinisikan skor
skor = {
    "low": 0,
    "medium": 4,
    "high": 8,
}

# Fungsi untuk mendapatkan pertanyaan random
def get_random_pertanyaan():
    return pertanyaan[random.randint(0, len(pertanyaan) - 1)]

# Fungsi untuk mendapatkan jawaban random
def get_random_jawaban():
    return jawaban[random.randint(0, len(jawaban) - 1)]

# Fungsi untuk menghitung skor
def get_skor(jawaban_user):
    jawaban_benar = []
    for i in range(len(pertanyaan)):
        if jawaban_user[i] == jawaban[i][0]:
            jawaban_benar.append(1)
        else:
            jawaban_benar.append(0)
    return sum(jawaban_benar)

# Fungsi untuk menyimpan data ke database
def simpan_data(nama, umur, domisili, tgl_submit, jawaban_user, skor):
    cursor.execute(
        """
        INSERT INTO knowledge (nama, umur, domisili, tgl_submit, jawaban, skor)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (nama, umur, domisili, tgl_submit, jawaban_user, skor),
    )
    conn.commit()

# Tab pertama
st.title("Knowledge Check")

# Form
nama = st.text_input("Nama")
umur = st.number_input("Umur")
domisili = st.selectbox("Domisili", ("Jakarta Pusat", "Jakarta Timur", "Jakarta Barat", "Jakarta Utara", "Jakarta Selatan", "Bogor", "Depok", "Tangerang", "Bekasi"))

# Menampilkan 10 pertanyaan random
pertanyaan_random = []
for i in range(10):
    pertanyaan_random.append(get_random_pertanyaan())

jawaban_user = []
for i in range(10):
    jawaban_user.append(st.selectbox("Jawaban", ("A", "B", "C", "D")))

# Menghitung skor
skor = get_skor(jawaban_user)

# Hasil
if st.button("Submit"):
    # Menyimpan data ke database
    simpan_data(nama, umur, domisili, datetime.datetime.now(), jawaban_user, skor)

    # Menampilkan hasil
    if skor <= skor["low"]:
        st.write("Pengetahuan Anda rendah")
    elif skor <= skor["medium"]:
        st.write("Pengetahuan Anda sedang")
    else:
        st.write("Pengetahuan Anda tinggi")

    st.write("Anda menjawab {} pertanyaan dengan benar".format(sum(jawaban_user)))
    st.write("Skor Anda adalah {}".format(skor))

# Menutup koneksi ke database
conn.close()