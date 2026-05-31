from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "main_data.csv"
SEASON_ORDER = ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
PM25_CATEGORY_ORDER = [
    "Baik",
    "Sedang",
    "Tidak Sehat Ringan",
    "Tidak Sehat",
    "Sangat Tidak Sehat",
]


st.set_page_config(
    page_title="Dashboard Kualitas Udara Tiantan",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["datetime"] = pd.to_datetime(data["datetime"])

    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"])
    else:
        data["date"] = data["datetime"].dt.normalize()

    return data


def format_decimal(value: float, suffix: str = "") -> str:
    return f"{value:,.2f}{suffix}"


sns.set_theme(style="whitegrid", palette="Set2")
df = load_data()

st.title("Dashboard Kualitas Udara Stasiun Tiantan")
st.write(
    "Dashboard ini menganalisis data kualitas udara Stasiun Tiantan, Beijing, "
    "selama periode 2013-2017. Visualisasi disusun untuk menjawab tiga "
    "pertanyaan bisnis utama terkait tren PM2.5, pola musiman PM2.5 dan PM10, "
    "serta hubungan kecepatan angin dengan PM2.5."
)

min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

with st.sidebar:
    st.header("Filter Tanggal")
    selected_dates = st.date_input(
        "Pilih rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
filtered_df = df[
    (df["datetime"] >= start_datetime) & (df["datetime"] <= end_datetime)
].copy()

if filtered_df.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

st.subheader("Metrik Ringkas")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM2.5", format_decimal(filtered_df["PM2.5"].mean()))
col2.metric("Rata-rata PM10", format_decimal(filtered_df["PM10"].mean()))
col3.metric("Rata-rata WSPM", format_decimal(filtered_df["WSPM"].mean(), " m/s"))
col4.metric("Jumlah Data", f"{len(filtered_df):,}")

st.subheader("Pertanyaan Bisnis 1")
st.markdown(
    "**Bagaimana tren rata-rata bulanan PM2.5 di Stasiun Tiantan selama periode 2013-2017?**"
)

monthly_pm25 = (
    filtered_df.set_index("datetime")
    .resample("MS")["PM2.5"]
    .mean()
    .dropna()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly_pm25, x="datetime", y="PM2.5", marker="o", ax=ax, color="#2563eb")
ax.set_title("Tren Rata-rata Bulanan PM2.5 di Stasiun Tiantan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata PM2.5")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig)

highest_month = monthly_pm25.loc[monthly_pm25["PM2.5"].idxmax()]
lowest_month = monthly_pm25.loc[monthly_pm25["PM2.5"].idxmin()]
st.info(
    f"Insight: rata-rata bulanan PM2.5 tertinggi pada rentang filter ini terjadi "
    f"pada {highest_month['datetime'].strftime('%Y-%m')} sebesar {highest_month['PM2.5']:.2f}. "
    f"Nilai terendah terjadi pada {lowest_month['datetime'].strftime('%Y-%m')} sebesar "
    f"{lowest_month['PM2.5']:.2f}."
)

st.subheader("Pertanyaan Bisnis 2")
st.markdown(
    "**Pada musim apa tingkat polusi PM2.5 dan PM10 cenderung paling tinggi di Stasiun Tiantan selama periode 2013-2017?**"
)

season_summary = (
    filtered_df.groupby("season")[["PM2.5", "PM10"]]
    .mean()
    .reindex(SEASON_ORDER)
    .dropna()
)
season_pm = season_summary.reset_index().melt(
    id_vars="season",
    var_name="Polutan",
    value_name="Rata-rata Konsentrasi",
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=season_pm,
    x="season",
    y="Rata-rata Konsentrasi",
    hue="Polutan",
    order=SEASON_ORDER,
    ax=ax,
    palette=["#2563eb", "#f97316"],
)
ax.set_title("Rata-rata PM2.5 dan PM10 Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Konsentrasi")
ax.legend(title="Polutan")
plt.tight_layout()
st.pyplot(fig)

highest_pm25_season = season_summary["PM2.5"].idxmax()
highest_pm10_season = season_summary["PM10"].idxmax()
st.info(
    f"Insight: rata-rata PM2.5 tertinggi terjadi pada {highest_pm25_season} "
    f"sebesar {season_summary.loc[highest_pm25_season, 'PM2.5']:.2f}. "
    f"Rata-rata PM10 tertinggi terjadi pada {highest_pm10_season} "
    f"sebesar {season_summary.loc[highest_pm10_season, 'PM10']:.2f}."
)

st.subheader("Pertanyaan Bisnis 3")
st.markdown(
    "**Bagaimana hubungan antara kecepatan angin dan konsentrasi PM2.5 di Stasiun Tiantan selama periode 2013-2017?**"
)

correlation = filtered_df["WSPM"].corr(filtered_df["PM2.5"])
st.metric("Korelasi WSPM dengan PM2.5", format_decimal(correlation))

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=filtered_df,
    x="WSPM",
    y="PM2.5",
    alpha=0.25,
    s=18,
    edgecolor=None,
    ax=ax,
    color="#0f766e",
)
ax.set_title("Hubungan Kecepatan Angin dengan PM2.5")
ax.set_xlabel("Kecepatan Angin/WSPM")
ax.set_ylabel("PM2.5")
plt.tight_layout()
st.pyplot(fig)

if correlation < 0:
    wind_insight = (
        "korelasi bernilai negatif, sehingga kecepatan angin yang lebih tinggi "
        "cenderung diikuti oleh penurunan PM2.5."
    )
else:
    wind_insight = (
        "korelasi tidak bernilai negatif pada rentang filter ini, sehingga hubungan "
        "antara kecepatan angin dan PM2.5 perlu dibaca lebih hati-hati."
    )

st.info(f"Insight: nilai korelasi WSPM dengan PM2.5 adalah {correlation:.3f}; {wind_insight}")

st.subheader("Analisis Tambahan: Kategori Tingkat Polusi PM2.5")
category_count = (
    filtered_df["pm25_category"]
    .value_counts()
    .reindex(PM25_CATEGORY_ORDER)
    .fillna(0)
    .reset_index()
)
category_count.columns = ["Kategori PM2.5", "Jumlah Data"]

fig, ax = plt.subplots(figsize=(11, 5))
sns.barplot(
    data=category_count,
    x="Kategori PM2.5",
    y="Jumlah Data",
    hue="Kategori PM2.5",
    order=PM25_CATEGORY_ORDER,
    ax=ax,
    palette="rocket",
    legend=False,
)
ax.set_title("Jumlah Data Berdasarkan Kategori PM2.5")
ax.set_xlabel("Kategori PM2.5")
ax.set_ylabel("Jumlah Data Per Jam")
plt.xticks(rotation=20)
plt.tight_layout()
st.pyplot(fig)

dominant_category = category_count.loc[category_count["Jumlah Data"].idxmax()]
st.info(
    f"Insight: kategori PM2.5 yang paling sering muncul pada rentang filter ini adalah "
    f"{dominant_category['Kategori PM2.5']} sebanyak {int(dominant_category['Jumlah Data']):,} data."
)

st.caption(
    "Dashboard membaca data dari dashboard/main_data.csv. Data bersih dibuat dari "
    "PRSA_Data_Tiantan_20130301-20170228.csv dengan penanganan missing value dan "
    "penambahan kolom musim serta kategori PM2.5."
)
