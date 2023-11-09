import streamlit as st

def main():
    st.title("Personal Pollution Tracker")

    # Form Input
    with st.form("pollution_form"):
        jumlah_anggota_keluarga = st.number_input("Jumlah Anggota Keluarga dalam 1 rumah", min_value=1, step=1)

        st.markdown("<h2 style='color: #008080;'>Membakar Sampah</h2>", unsafe_allow_html=True)
        is_membakar_sampah = st.radio("Membakar sampah:", ('Ya', 'Tidak'))
        membarak_sampah_pollutants = {"NOx": 2.04, "CO": 28.56, "SOx": 0.34, "PM10": 5.44} if is_membakar_sampah == 'Ya' else {"NOx": 0, "CO": 0, "SOx": 0, "PM10": 0}

        st.markdown("<h2 style='color: #008080;'>GAS LPG</h2>", unsafe_allow_html=True)
        is_gas_lpg = st.radio("GAS LPG:", ('Ya', 'Tidak'))
        gas_lpg_pollutants = {"3 KG": {"NOx": 7.5, "CO": 7.5, "SOx": 0.075, "PM10": 0.075},
                              "5.5kg": {"NOx": 13.75, "CO": 13.75, "SOx": 0.1375, "PM10": 0.1375},
                              "12kg": {"NOx": 30, "CO": 30, "SOx": 0.3, "PM10": 0.3}}
        gas_lpg_usage = 0
        if is_gas_lpg == 'Ya':
            ukuran = st.selectbox("Ukuran GAS LPG:", ('3 KG', '5.5kg', '12kg'))
            gas_lpg_usage = st.number_input("Berapa hari pemakaian:", min_value=1, step=1)
            gas_lpg_pollutants = {k: {k2: v2 / jumlah_anggota_keluarga / gas_lpg_usage for k2, v2 in v.items()} for k, v in gas_lpg_pollutants.items()}[ukuran]

        st.markdown("<h2 style='color: #008080;'>Merokok</h2>", unsafe_allow_html=True)
        is_merokok = st.radio("Merokok:", ('Ya', 'Tidak'))
        smoking_pollutants = {"Rokok Konvensional": {"PM10": 0.000529, "PM2.5": 0.0005},
                              "Rokok Elektrik": {"PM10": 0, "PM2.5": 0},
                              "iQOS": {"PM10": 0.0000081, "PM2.5": 0.0000065}}
        smoking_count = 0
        if is_merokok == 'Ya':
            jenis_rokok = st.selectbox("Jenis Rokok:", ('Rokok Konvensional', 'Rokok Elektrik', 'iQOS'))
            if jenis_rokok != 'Rokok Elektrik':
                smoking_count = st.number_input("Berapa batang per hari:", min_value=1, step=1)
                smoking_pollutants = smoking_pollutants[jenis_rokok]
                smoking_pollutants = {k: v * smoking_count for k, v in smoking_pollutants.items()}

        st.markdown("<h2 style='color: #008080;'>Penerbangan Domestik</h2>", unsafe_allow_html=True)
        penerbangan_domestik = st.number_input("Berapa kali penerbangan domestik (dalam tahun ini):", min_value=0, step=1)
        penerbangan_domestik_pollutants = {"NOx": 51, "SOx": 4.94, "CO": 0.432, "PM2.5": 0.432, "PM10": 0.432}
        penerbangan_domestik_pollutants = {k: v * penerbangan_domestik / 365 for k, v in penerbangan_domestik_pollutants.items()}

        st.markdown("<h2 style='color: #008080;'>Penerbangan Internasional</h2>", unsafe_allow_html=True)
        penerbangan_internasional = st.number_input("Berapa kali penerbangan internasional (dalam tahun ini):", min_value=0, step=1)
        penerbangan_internasional_pollutants = {k: v * penerbangan_internasional * 4 / 365 for k, v in penerbangan_domestik_pollutants.items()}

        submit_button = st.form_submit_button(label='Hitung')

    if submit_button:
        total_pollutants = {}
        for pollutants in [membarak_sampah_pollutants, gas_lpg_pollutants, smoking_pollutants, penerbangan_domestik_pollutants, penerbangan_internasional_pollutants]:
            for key, value in pollutants.items():
                total_pollutants[key] = total_pollutants.get(key, 0) + value

        st.markdown("<h2 style='color: #008080;'>Total Pencemaran</h2>", unsafe_allow_html=True)
        total_result_daily = " | ".join([f"{key}: {value}gr/hari" for key, value in total_pollutants.items()])
        total_result_monthly = " | ".join([f"{key}: {value*30}gr/bulan" for key, value in total_pollutants.items()])
        total_result_yearly = " | ".join([f"{key}: {value*365}gr/tahun" for key, value in total_pollutants.items()])
        st.markdown(f"<p style='font-size: 16px;'>Harian: {total_result_daily}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'>Bulanan: {total_result_monthly}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'>Tahunan: {total_result_yearly}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
