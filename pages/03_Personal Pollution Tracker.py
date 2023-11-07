import streamlit as st

# Fungsi untuk menghitung total polusi
def hitung_total_polusi(data_kegiatan):
    total_polusi = 0
    for kegiatan, nilai in data_kegiatan.items():
        if kegiatan == "Naik Kendaraan":
            total_polusi += 0.5 * nilai["Jarak (km)"] * nilai["Waktu (jam)"]
        elif kegiatan == "Merokok":
            total_polusi += 0.2 * nilai
        # Tambahkan pernyataan kondisional untuk setiap kegiatan lain yang ingin Anda tambahkan

    return total_polusi

# Judul aplikasi
st.title('Personal Pollution Tracker')

# Membuat input untuk data pengguna
with st.form(key='input_form'):
    st.header('Masukkan Data Anda')

    data_kegiatan = {}
    jumlah_kegiatan = st.number_input('Masukkan jumlah kegiatan yang ingin Anda masukkan', min_value=1, step=1)

    for i in range(jumlah_kegiatan):
        nama_kegiatan = st.text_input(f'Masukkan nama kegiatan ke-{i+1}')
        if nama_kegiatan not in data_kegiatan:
            if nama_kegiatan == "Naik Kendaraan":
                jarak = st.number_input('Jarak yang ditempuh (km)', min_value=0, step=1)
                waktu = st.number_input('Waktu perjalanan (jam)', min_value=0, step=1)
                data_kegiatan[nama_kegiatan] = {"Jarak (km)": jarak, "Waktu (jam)": waktu}
            elif nama_kegiatan == "Merokok":
                jumlah = st.number_input('Berapa banyak batang rokok', min_value=0, step=1)
                data_kegiatan[nama_kegiatan] = jumlah
            # Tambahkan pernyataan kondisional untuk setiap kegiatan lain yang ingin Anda tambahkan

    submitted = st.form_submit_button('Hitung Polusi')

# Menampilkan hasil perhitungan
if submitted:
    total_polusi = hitung_total_polusi(data_kegiatan)
    st.header('Hasil Perhitungan Polusi Anda')
    st.write(f'Total polusi yang dihasilkan dalam sehari: {total_polusi} satuan')
