Sentiment Analysis of Google Maps Reviews for Pantai Mutun

Proyek End-to-End Machine Learning untuk mengumpulkan, membersihkan, dan menganalisis sentimen ulasan pengunjung Pantai Mutun dari Google Maps menggunakan algoritma Naive Bayes.

📌 Project Overview

Proyek ini bertujuan untuk menganalisis opini publik terkait pengalaman pengunjung di Pantai Mutun, seperti fasilitas, kebersihan, dan harga tiket. Data diambil langsung dari ulasan Google Maps menggunakan teknik web scraping, kemudian diproses menggunakan metode Natural Language Processing (NLP) untuk menentukan sentimen setiap ulasan.

Pipeline proyek ini mencakup:
- Pengambilan data ulasan dari internet
- Pembersihan dan normalisasi teks
- Pemberian label sentimen
- Pelatihan model Machine Learning
- Evaluasi model dan visualisasi hasil

📊 Dataset
Sumber Data: Google Maps Reviews
Lokasi: Pantai Mutun, Lampung
Jumlah Data: ±100 ulasan pengunjung
Distribusi sentimen ulasan:
- Positif : 41
- Negatif : 23
- Netral : 41
Dataset dikumpulkan secara otomatis menggunakan Selenium Web Scraping.

🛠 Tools & Technologies
- Programming Language
- Python
- Web Scraping
- Selenium
- Chromedriver
- Data Processing
- Pandas
- Regex
- Sastrawi (Indonesian stemming & stopword removal)
- Machine Learning
- Scikit-learn
- TF-IDF Vectorization
- Multinomial Naive Bayes
- Visualization
- Matplotlib
- Seaborn

🔄 Project Workflow
Proyek ini dibagi menjadi beberapa tahap agar pipeline mudah dipahami dan direplikasi.
1. Data Scraping
Mengambil ulasan pengguna dari Google Maps menggunakan Selenium.
File: 01_scraping.py
Output: dataset_ulasan_mutun.csv
2. Text Preprocessing
Membersihkan teks ulasan dengan beberapa tahap:
- Lowercasing
- Menghapus emoji
- Menghapus angka dan tanda baca
- Normalisasi kata tidak baku
- Stopword removal
- Stemming menggunakan Sastrawi
File: 02_preprocessing.py
Output: data_bersih.csv
3. Sentiment Labeling
Memberikan label sentimen pada setiap ulasan menggunakan pendekatan lexicon-based sentiment analysis.
File: 03_labeling.py
Output: review_google_maps_sentiment_analysis.csv
4. Machine Learning Model
Melatih model Naive Bayes menggunakan fitur TF-IDF untuk memprediksi sentimen ulasan.
File:04_naive_bayes.py
Output:
- Model prediksi sentimen
- Evaluasi model

⭐ Special Feature: Negation Handling
Pada tahap preprocessing, program dimodifikasi agar tidak menghapus kata negasi seperti:
- tidak
- bukan
- jangan
Hal ini penting untuk menjaga makna kalimat.
Contoh:
"tidak bagus" → tetap mempertahankan kata "tidak"
Tanpa teknik ini, kalimat bisa berubah makna menjadi: "bagus"
yang dapat menyebabkan kesalahan klasifikasi sentimen.

📈 Data Visualization
- Beberapa visualisasi digunakan untuk memahami pola sentimen pada ulasan.
- Sentiment Distribution
- Grafik distribusi jumlah ulasan berdasarkan sentimen.
- Confusion Matrix
- Digunakan untuk mengevaluasi performa model klasifikasi.
- Visualisasi dibuat menggunakan Matplotlib dan Seaborn.

🚀 How to Run the Project
1. Clone Repository
git clone https://github.com/dzkafif/sentiment-analysis-pantai-mutun.git 
cd sentiment-analysis-pantai-mutun
2. Install Dependencies
pip install -r requirements.txt
3. Run the Pipeline

Jalankan setiap tahap secara berurutan:
python 01_scraping.py
python 02_preprocessing.py
python 03_labeling.py
python 04_naive_bayes.py

Author:
Muhammad Dzakwan Afif
Information Systems Student

GitHub:
https://github.com/dzkafif