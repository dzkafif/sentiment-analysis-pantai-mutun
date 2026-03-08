# Analisis Sentimen Ulasan Pantai Mutun (Google Maps)

Proyek *End-to-End Machine Learning* untuk mengambil, membersihkan, dan menganalisis sentimen ulasan pengunjung Pantai Mutun di Google Maps menggunakan algoritma Naive Bayes.

## 📌 Tentang Proyek
Proyek ini dibuat untuk melihat opini publik terkait fasilitas, harga, dan kebersihan Pantai Mutun. Alur kerjanya dirancang lengkap (*pipeline*), mulai dari pengambilan data mentah dari internet (*web scraping*) hingga pembuatan model tebakan otomatis (*Machine Learning*).

## Alat & Teknologi
* **Bahasa:** Python
* **Scraping:** Selenium, Chromedriver
* **Pemrosesan Teks:** Sastrawi (Stemming & Stopword), Regex, Pandas
* **Machine Learning:** Scikit-Learn (TF-IDF, Naive Bayes)
* **Visualisasi:** Matplotlib, Seaborn

## Struktur Alur Kerja
Proyek ini dipecah menjadi 4 tahap agar rapi dan mudah dimodifikasi:

1. `01_scraping.py` : Menjalankan *bot* untuk mengambil ulasan dari Google Maps secara otomatis. (Menghasilkan `dataset_ulasan_mutun.csv`).
2. `02_preprocessing.py` : Membersihkan teks dari emoji, angka, tanda baca, mengubah kata gaul (alay) menjadi baku, dan memotong imbuhan kata. (Menghasilkan `data_bersih.csv`).
3. `03_labeling.py` : Memberi label sentimen (positif, negatif, netral) pada tiap ulasan menggunakan kamus kata. (Menghasilkan `review_google_maps_sentiment_analysis.csv`).
4. `04_naive_bayes.py` : Melatih model kecerdasan buatan (Naive Bayes) untuk memprediksi sentimen ulasan baru.

## Fitur Unggulan: Penyelamatan Kata Negasi
Pada tahap pembersihan data, program dimodifikasi agar **tidak menghapus** kata-kata penolakan seperti "tidak", "bukan", dan "jangan". Hal ini bertujuan agar makna kalimat seperti *"tidak konsisten"* tidak berubah menjadi *"konsisten"*. 

## Cara Menjalankan Program

**1. Clone Repositori Ini**
```bash
git clone [https://github.com/username_kamu/nama_repo_kamu.git](https://github.com/username_kamu/nama_repo_kamu.git)
cd nama_repo_kamu