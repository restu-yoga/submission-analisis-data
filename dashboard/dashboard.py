from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "main_data.csv"

st.set_page_config(
    page_title="Dashboard Kualitas Udara Tiantan",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["datetime"] = pd.to_datetime(data["datetime"])
    data["date"] = pd.to_datetime(data["date"]).dt.date
    return data


def format_number(value: float, suffix: str = "") -> str:
    return f"{value:,.2f}{suffix}"


sns.set_theme(style="whitegrid", palette="Set2")

df = load_data()

st.title("Dashboard Kualitas Udara Stasiun Tiantan")
st.write(
    "Dashboard ini menampilkan ringkasan kualitas udara Stasiun Tiantan, Beijing, "
    "berdasarkan data PRSA periode Maret 2013 hingga Februari 2017."
)

min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar:
    st.header("Filter Data")
    selected_range = st.date_input(
        "Rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if isinstance(selected_range, tuple) and len(selected_range) == 2:
    start_date, end_date = selected_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()

if filtered_df.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

st.subheader("Metrik Ringkas")
metric_cols = st.columns(4)
metric_cols[0].metric("Rata-rata PM2.5", format_number(filtered_df["PM2.5"].mean()))
metric_cols[1].metric("Rata-rata PM10", format_number(filtered_df["PM10"].mean()))
metric_cols[2].metric("Rata-rata Suhu", format_number(filtered_df["TEMP"].mean(), " C"))
metric_cols[3].metric("Jumlah Data", f"{len(filtered_df):,}")

st.subheader("Tren PM2.5 Berdasarkan Waktu")
daily_pm25 = (
    filtered_df.set_index("datetime")
    .resample("D")["PM2.5"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=daily_pm25, x="datetime", y="PM2.5", ax=ax, color="#2563eb")
ax.set_title("Rata-rata Harian PM2.5")
ax.set_xlabel("Tanggal")
ax.set_ylabel("PM2.5")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig)

highest_day = daily_pm25.loc[daily_pm25["PM2.5"].idxmax()]
st.info(
    f"Insight: pada rentang filter ini, rata-rata PM2.5 harian tertinggi terjadi "
    f"pada {highest_day['datetime'].date()} sebesar {highest_day['PM2.5']:.2f}."
)

st.subheader("Perbandingan Rata-rata Polutan Utama")
pollutant_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
pollutant_avg = (
    filtered_df[pollutant_cols]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
pollutant_avg.columns = ["Polutan", "Rata-rata"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=pollutant_avg, x="Polutan", y="Rata-rata", ax=ax, palette="viridis")
ax.set_title("Rata-rata Polutan pada Rentang Tanggal Terpilih")
ax.set_xlabel("Polutan")
ax.set_ylabel("Rata-rata Konsentrasi")
plt.tight_layout()
st.pyplot(fig)

st.info(
    "Insight: CO memiliki skala nilai yang berbeda dari polutan lain, sehingga nilainya "
    "terlihat paling besar pada grafik agregat. Untuk partikulat, PM10 umumnya lebih "
    "tinggi dibanding PM2.5."
)

st.subheader("Rata-rata PM2.5 Berdasarkan Musim")
season_order = ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
season_pm25 = (
    filtered_df.groupby("season", as_index=False)["PM2.5"]
    .mean()
    .set_index("season")
    .reindex(season_order)
    .dropna()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=season_pm25, x="season", y="PM2.5", ax=ax, palette="mako")
ax.set_title("Rata-rata PM2.5 per Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata PM2.5")
plt.tight_layout()
st.pyplot(fig)

highest_season = season_pm25.loc[season_pm25["PM2.5"].idxmax()]
st.info(
    f"Insight: musim dengan rata-rata PM2.5 tertinggi pada rentang filter ini adalah "
    f"{highest_season['season']} dengan nilai {highest_season['PM2.5']:.2f}."
)

st.caption(
    "Sumber data: PRSA Data Tiantan 20130301-20170228. Data telah dibersihkan "
    "melalui interpolasi nilai numerik dan pengisian arah angin yang hilang."
)
