# Satu Kota, 31 Cerita

Dashboard Data Storytelling tentang karakteristik 31 kecamatan di Kota Surabaya melalui indikator pendidikan, kesehatan, dan aktivitas ekonomi.

## Fitur
- Delapan bagian cerita sesuai rancangan proyek.
- Navigasi sidebar dengan ikon outline SVG.
- Tipografi Times New Roman dan palet Ink Navy, Parchment Cream, Burgundy, putih, dan hitam.
- Eksplorasi indikator, histogram, boxplot, korelasi Spearman, dan perbandingan wilayah.
- Profil 3 cluster utama dan 9 subcluster eksploratif.
- Persebaran cluster pada lima wilayah.
- Indeks relatif pendidikan, kesehatan, dan ekonomi.
- Foto pendukung yang disimpan lokal di `assets/images`.

## Struktur folder

```text
Surabaya_Data_Story/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── data_bersih_plus_kemiskinan.csv
│   ├── hasil_cluster_per_kecamatan.csv
│   └── kecamatan_prioritas_per_bidang.csv
└── assets/
    └── images/
        ├── surabaya_landmark_suro_boyo.png
        ├── surabaya_skyline_day.png
        ├── surabaya_skyline_sunset.png
        ├── surabaya_skyline_night.png
        ├── permukiman_padat.png
        ├── genangan_permukiman.png
        ├── peta_referensi_surabaya.png
        └── referensi_visual_kota.png
```

## Menjalankan di komputer

1. Ekstrak ZIP.
2. Buka folder `Surabaya_Data_Story` di VS Code.
3. Buat virtual environment (opsional tetapi disarankan).
4. Install dependensi:

```bash
pip install -r requirements.txt
```

5. Jalankan aplikasi:

```bash
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud

1. Buat repository GitHub baru.
2. Unggah seluruh isi folder proyek, termasuk folder `data` dan `assets`.
3. Buka Streamlit Community Cloud dan hubungkan repository.
4. Pilih branch utama dan file `app.py`.
5. Deploy.

Jangan hanya mengunggah `app.py`. Folder `data` dan `assets/images` wajib ikut karena aplikasi membaca CSV dan foto menggunakan path relatif.

## Catatan analisis dan keterbatasan

- Dataset berisi 31 kecamatan dan lima wilayah administratif.
- Dashboard menggunakan hasil cluster yang disertakan dalam `data/hasil_cluster_per_kecamatan.csv`.
- Nomor cluster pada tampilan diurutkan agar sesuai alur narasi: Cluster 1 (16 kecamatan), Cluster 2 (6 kecamatan), Cluster 3 (9 kecamatan). Ini hanya penamaan tampilan; label GMM bersifat nominal.
- Sembilan subcluster ditampilkan sebagai eksplorasi tambahan. Kelompok beranggota satu atau dua kecamatan harus ditafsirkan hati-hati.
- BIC pada kandidat model yang diuji memilih dua komponen. Tiga cluster tetap dipakai sebagai rancangan segmentasi utama, bukan diklaim sebagai optimum BIC.
- Indeks wilayah bersifat deskriptif dan relatif terhadap 31 kecamatan, bukan indeks resmi BPS atau ukuran kesejahteraan penduduk.
- Peta yang disertakan merupakan peta referensi visual. Peta choropleth interaktif yang dapat diklik per kecamatan membutuhkan GeoJSON/shapefile batas administrasi yang tervalidasi. Dashboard ini tidak mengarang koordinat atau batas kecamatan.
- Foto disertakan dari materi yang diberikan dalam percakapan. Pastikan izin penggunaan dan atribusi sumbernya sebelum repository dipublikasikan secara terbuka.
