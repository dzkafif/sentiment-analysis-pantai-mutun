import pandas as pd
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# LOAD DATA
namafile = 'dataset_ulasan_mutun.csv' 
try:
    df = pd.read_csv(namafile)
    print(f"Data berhasil dimuat! Jumlah baris: {len(df)}")
except FileNotFoundError:
    print(f"Error: File '{namafile}' tidak ditemukan. Cek nama file hasil scraping.")
    # Buat dummy data jika file tidak ada (hanya untuk contoh biar kode jalan)
    df = pd.DataFrame({'text': ['Tempatnya bagus bgt!!', 'Makanannya ga enak, mahal.', 'Pelayanan ramah sekali.']})

# Hapus baris yang kolom 'text'-nya kosong (NaN)
df = df.dropna(subset=['text'])

df = df.drop_duplicates(subset=['name', 'text'])
print(f"Jumlah baris setelah hapus duplikat: {len(df)}")

# Kamus Kata Gaul (Slang) -> Baku
kamus_alay = {
    'yg': 'yang', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak',
    'bgt': 'banget', 'dr': 'dari', 'kalo': 'kalau', 'bkn': 'bukan',
    'jd': 'jadi', 'blm': 'belum', 'dgn': 'dengan', 'sdh': 'sudah',
    'aja': 'saja', 'tpt': 'tempat', 'sy': 'saya', 'kak': 'kakak',
    'min': 'admin', 'aq': 'aku', 'krn': 'karena', 'utk': 'untuk'
}

# Setup Sastrawi (Stopword & Stemmer)
factory_stop = StopWordRemoverFactory()
stopwords_indo = factory_stop.get_stop_words()
# Tambahan stopword manual yang sering muncul di review tapi kurang bermakna
stopwords_indo.extend(['sih', 'nya', 'nih', 'tuh', 'dong', 'kan', 'lah', 'pun', 'kok'])

kata_negasi = ['tidak', 'bukan', 'belum', 'jangan']
stopwords_indo = [word for word in stopwords_indo if word not in kata_negasi]

factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()

def cleaning_text(text):
    # 1. Case Folding (Huruf Kecil)
    text = str(text).lower()

    # 2. Hapus URL/Link
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # 3. Hapus Mention (@user) dan Hashtag (#)
    text = re.sub(r'@\w+|#\w+', '', text)

    # 4. Hapus Angka
    text = re.sub(r'\d+', '', text)

    # 5. Hapus Tanda Baca
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 6. Hapus Emoji & Karakter Aneh (Non-ASCII)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # 7. Hapus Spasi Berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def normalize_slang(text):
    words = text.split()
    normalized_words = [kamus_alay[word] if word in kamus_alay else word for word in words]
    return ' '.join(normalized_words)

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords_indo]
    return ' '.join(filtered_words)

# Stemming 
def stemming_text(text):
    return stemmer.stem(text)

print("1. Melakukan Cleaning & Normalisasi...")
df['text_clean'] = df['text'].apply(cleaning_text)
df['text_clean'] = df['text_clean'].apply(normalize_slang)

print("2. Melakukan Stopword Removal...")
df['text_clean'] = df['text_clean'].apply(remove_stopwords)

print("3. Melakukan Stemming (Ini mungkin agak lama)...")
df['text_final'] = df['text_clean'].apply(stemming_text)

# Hapus data yang kosong setelah preprocessing
df = df[df['text_final'] != '']

print("\n✅ PREPROCESSING SELESAI!")
print(df[['text', 'text_final']].head())

# Simpan Hasil
df.to_csv('data_bersih.csv', index=False)
print("File tersimpan sebagai 'data_bersih.csv'")