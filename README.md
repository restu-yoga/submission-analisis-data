# Proyek Analisis Data Kualitas Udara Stasiun Tiantan

## Deskripsi Proyek

Proyek ini merupakan submission Dicoding kelas Proyek Analisis Data. Dataset yang digunakan adalah Air Quality Dataset, khususnya data kualitas udara Stasiun Tiantan, Beijing, selama periode 2013-2017. Analisis berfokus pada tren PM2.5, perbandingan PM2.5 dan PM10 berdasarkan musim, serta hubungan antara kecepatan angin dan konsentrasi PM2.5.

## Pertanyaan Bisnis

1. Bagaimana tren rata-rata bulanan PM2.5 di Stasiun Tiantan selama periode 2013-2017?
2. Pada musim apa tingkat polusi PM2.5 dan PM10 cenderung paling tinggi di Stasiun Tiantan selama periode 2013-2017?
3. Bagaimana hubungan antara kecepatan angin dan konsentrasi PM2.5 di Stasiun Tiantan selama periode 2013-2017?

## Struktur Folder

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   └── PRSA_Data_Tiantan_20130301-20170228.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Anaconda

Jalankan command berikut dari terminal:

```bash
conda create --name air-quality-analysis python=3.9
conda activate air-quality-analysis
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

Untuk Windows PowerShell, jalankan command berikut dari folder utama `submission`:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Untuk MacOS/Linux, jalankan command berikut dari folder utama `submission`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Menjalankan Notebook

Notebook analisis dapat dijalankan melalui file:

```text
notebook.ipynb
```

Pastikan dataset berada pada path berikut:

```text
data/PRSA_Data_Tiantan_20130301-20170228.csv
```

Buka file `notebook.ipynb` menggunakan Jupyter Notebook atau JupyterLab, lalu jalankan seluruh cell dari awal sampai akhir. Notebook akan menghasilkan data bersih yang digunakan oleh dashboard.

## Run Streamlit App

Pastikan terminal berada di folder utama `submission`, kemudian jalankan command berikut:

```bash
streamlit run dashboard/dashboard.py
```

Command di atas adalah command yang benar karena file `dashboard.py` berada di dalam folder `dashboard`.

Jangan menjalankan command berikut:

```bash
streamlit run dashboard.py
```

Command tersebut tidak sesuai dengan struktur folder project ini.

## Library yang Digunakan

- pandas
- numpy
- matplotlib
- seaborn
- streamlit

## Dataset

Dataset yang digunakan:

```text
PRSA_Data_Tiantan_20130301-20170228.csv
```

Dataset ini berisi data kualitas udara per jam di Stasiun Tiantan. Kolom polutan utama meliputi PM2.5, PM10, SO2, NO2, CO, dan O3. Kolom cuaca meliputi TEMP, PRES, DEWP, RAIN, wd, dan WSPM.

## Catatan

Dashboard membaca data bersih dari:

```text
dashboard/main_data.csv
```

Jika file `dashboard/main_data.csv` belum tersedia, jalankan seluruh cell pada `notebook.ipynb` terlebih dahulu agar data bersih dibuat ulang.
