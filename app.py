import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="DBD Anomaly Dashboard", layout="wide")

st.title("📊 Dashboard Analisis DBD: 50 Kota")
st.write("Deteksi Anomali dengan Machine Learning - Informatika UNAND")

# --- Load Data ---
folder_path = '/content/drive/MyDrive/TB-VDST'
file_path = os.path.join(folder_path, 'dataset_50kota_anomali.csv')

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# --- Sidebar ---
st.sidebar.header("Filter")
kecamatan_list = df['Kecamatan'].unique()
selected_kec = st.sidebar.multiselect("Pilih Kecamatan:", kecamatan_list, default=kecamatan_list[:3])

# Filter data
df_filtered = df[df['Kecamatan'].isin(selected_kec)]

# --- Visualisasi Grafik ---
st.subheader("Tren Kasus & Deteksi Anomali")

# Pisahkan data untuk plotting
df_normal = df_filtered[df_filtered['is_anomali'] == False]
df_anomali = df_filtered[df_filtered['is_anomali'] == True]

fig = px.line(df_filtered, x='Tahun', y='Jumlah_Kasus', color='Kecamatan', 
              markers=True, title="Tren Kasus DBD per Kecamatan")

# Tambahkan titik merah untuk anomali
if not df_anomali.empty:
    fig.add_scatter(
        x=df_anomali['Tahun'], y=df_anomali['Jumlah_Kasus'], 
        mode='markers', marker=dict(color='red', size=12, symbol='x'),
        name='Anomali (Peringatan!)'
    )

st.plotly_chart(fig, use_container_width=True)

# --- Ringkasan Anomali ---
st.subheader("⚠️ Ringkasan Kecamatan Rawan")

anomali_data = df[df['is_anomali'] == True]
if not anomali_data.empty:
    top_anomali = anomali_data['Kecamatan'].value_counts().reset_index()
    top_anomali.columns = ['Kecamatan', 'Jumlah Kejadian Anomali']
    st.table(top_anomali)
else:
    st.success("Data saat ini menunjukkan pola yang normal (tidak ada anomali).")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.write("Project Akhir - Informatika UNAND")