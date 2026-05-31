# Proyek Analisis Data Kualitas Udara Stasiun Tiantan

Proyek ini menganalisis kualitas udara di Stasiun Tiantan, Beijing, menggunakan dataset PRSA Data Tiantan periode 1 Maret 2013 hingga 28 Februari 2017. Analisis berfokus pada tren PM2.5, perbandingan PM2.5 dan PM10 berdasarkan musim, serta hubungan polutan dengan variabel cuaca.

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

## Cara Menjalankan Notebook

1. Buka folder `submission`.
2. Jalankan Jupyter Notebook atau JupyterLab.
3. Buka file `notebook.ipynb`.
4. Jalankan semua cell dari awal sampai akhir.

Notebook akan membaca dataset dari folder `data` dan menyimpan data bersih ke `dashboard/main_data.csv`.

## Cara Menjalankan Dashboard

1. Pastikan semua library pada `requirements.txt` sudah terpasang.
2. Masuk ke folder `submission`.
3. Jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan membaca data bersih dari `dashboard/main_data.csv` dan menampilkan filter tanggal, metrik ringkas, serta visualisasi kualitas udara.

## Library yang Digunakan

- pandas
- numpy
- matplotlib
- seaborn
- streamlit
